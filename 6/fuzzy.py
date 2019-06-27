import numpy as np
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# Sparse universe makes calculations faster, without sacrifice accuracy.
# Only the critical points are included here; making it higher resolution is
# unnecessary.
universe = np.linspace(-2, 2, 5)

# Create the three fuzzy variables - two inputs, one output
INPUT_driver_age = ctrl.Antecedent(universe, 'driver-age')
INPUT_car_age = ctrl.Antecedent(universe, 'car-age')
#INPUT_weather = ctrl.Antecedent(universe, 'weather')
OUTPUT_accident_probability = ctrl.Consequent(universe, 'acccident-probability')

# Here we use the convenience `automf` to populate the fuzzy variables with
# terms. The optional kwarg `names=` lets us specify the names of our Terms.
ages = ['young', 'middle-aged', 'old']
#weather = ['stormy', 'foggy', 'rainy', 'cloudy', 'sunny']
accident_probabilities = ['low', 'medium', 'high']
INPUT_driver_age.automf(names=ages)
INPUT_car_age.automf(names=ages)
#INPUT_weather.automf(names=weather)
OUTPUT_accident_probability.automf(names=accident_probabilities)

rule0 = ctrl.Rule(antecedent=((INPUT_driver_age['young'] | INPUT_driver_age['old']) |
                              #(INPUT_weather['stormy'] | INPUT_weather['foggy']) |
                              (INPUT_car_age['old']) ),
                  consequent=OUTPUT_accident_probability['high'], label='rule high')

rule1 = ctrl.Rule(antecedent=( (INPUT_car_age['middle-aged']) ),#|
                               #(INPUT_weather['rainy']) ),
                  consequent=OUTPUT_accident_probability['medium'], label='rule medium')

rule2 = ctrl.Rule(antecedent=( (INPUT_driver_age['middle-aged']) |
                               (INPUT_car_age['young']) #|
                               #(INPUT_weather['cloudy'] | INPUT_weather['sunny']) 
                               ),
                  consequent=OUTPUT_accident_probability['low'], label='rule low')

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2])

# Later we intend to run this system with a 21*21 set of inputs, so we allow
# that many plus one unique runs before results are flushed.
# Subsequent runs would return in 1/8 the time!
sim = ctrl.ControlSystemSimulation(system, flush_after_run=21 * 21 + 1)

# We can simulate at higher resolution with full accuracy
upsampled = np.linspace(-2, 2, 21)
a,b = np.meshgrid(upsampled, upsampled)#, upsampled)
z = np.zeros_like(a)

# Loop through the system 21*21 times to collect the control surface
for i in range(21):
    for j in range(21):
        sim.input['driver-age'] = a[i, j]
        sim.input['car-age'] = b[i, j]
        #sim.input['weather'] = c[i, j]
        sim.compute()
        z[i, j] = sim.output['acccident-probability']

# dicts for converting values to ints:
map_age = {'young': 0, 'middle-aged': 1, 'old': 2}
map_weather = {'stormy': 0, 'foggy': 1, 'rainy': 2, 'cloudy': 3, 'sunny': 4}
map_probs = {'low': 0, 'medium': 1, 'high': 2}

# Visualize these universes and membership functions

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(a, b, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)


cset = ax.contourf(a, b, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5, label='accident probability')
cset = ax.contourf(a, b, z, zdir='a', offset=3, cmap='viridis', alpha=0.5, label='drivers age')
cset = ax.contourf(a, b, z, zdir='b', offset=3, cmap='viridis', alpha=0.5, label='cars age')

ax.view_init(30, 200)
plt.show()