# -*- coding:utf-8 -*-
# Disclaimer: this file is for teaching purpose only! You are not allowed to publish,
# distribute, share, or use the code except for the demonstration and
# execution in the Data Mining practical course summer semester 2019.

# *** Self-Organising Map ***

import numpy, scipy
import Gnuplot
import sys
import time
import random

# set parameters
dim_a, dim_b = 10, 15                         	# Define the map; e.g. 10,10 is a 10 by 10 grid
sigma = numpy.max([float(dim_a),float(dim_b)])  # initial map interaction range
repetitions = 3									# number of repetitions over all data 
#   reep in mind: we have no (1) repetitions for "continous" data
mu = 0.03                                 		# learning step size

# add the path to SOM-Data to load data
data_path = "SOM-Data/"
datafile = "triangle.dat"
#datafile = "box.dat"
#datafile = "sphere.dat"
data = numpy.loadtxt(data_path+datafile,delimiter=' ')
dim_in = numpy.shape(data)[1]
num_data = numpy.shape(data)[0]

# initialise architecture
size_map = dim_a * dim_b
W = numpy.zeros((size_map, dim_in))
map_net = numpy.zeros(size_map)
map_act = numpy.zeros(size_map)

# feedback for terminal/gui (defines the speed of this simulation)
feedback_iter = 500							# number of repetitions between feedback
feedback_time = 0.01							# pause in sec every feedback_iter repetitions

# trigger the visual feedback in Gnuplot
g1 = Gnuplot.Gnuplot()
print "SOM start", datafile

# initialize weights
for j in range(dim_in):
    for k in range(size_map):
        W[k,j] += numpy.random.uniform(numpy.min(data[:,j]),numpy.max(data[:,j]))

# for small data sets, repeat all-over again
for batch in range(repetitions):
    # iterate (one data point per iteration)
    for iteration in range(num_data):

        # current data point
        x = data[iteration]

        # neurons' inner activation
        for k in range(size_map):
            map_net[k] = numpy.dot(W[k]-x,W[k]-x)

        # find winner
        winner = scipy.argmin(map_net)

        # activation with map interaction function
        for k in range(size_map):
            dist = numpy.sqrt((k/dim_b-winner/dim_b)**2 + (k%dim_b-winner%dim_b)**2)
            map_act[k] = numpy.exp(-0.5 * dist**2 / sigma**2)

        # learning step
        for k in range(size_map):
            W[k] += mu * map_act[k] * (x-W[k])

        # reduce map interaction range
        sigma *= 0.999
		
		# occasionally give some feedback
        if iteration % feedback_iter == 0:
            print "iteration=", iteration, "sigma=", sigma, "winner=", winner, "x=", x
            time.sleep(feedback_time)

            # THE FOLLOWING CODE IS JUST USED TO PROPERLY DISPLAY THE SOM
	    # IT IS NOT PART OF THE CORE SOM ALGORITHM AND CAN THUS BE IGNORED 
            # Draws the SOM for display with Gnuplot
            # (write weights as 2D- or 3D-point coordinates)
            f = open(data_path+"out.dat", 'wb')
            for i in range(dim_a):
                for k in range(dim_b):
                    for j in range(dim_in):
                        val_ch = str(W[i*dim_b+k,j]) + " "
                        f.write(val_ch)
                    f.write("\n")
                f.write("\n")
            f.close()
            
            f = open(data_path+"out.gnu", 'wb')
            for i in range(dim_a):
                for k in range(dim_b-1):
                    val_string = "set arrow from "
                    for j in range(dim_in):
                        val_string += str(W[i*dim_b+k,j])
                        if j < dim_in - 1:
                            val_string += ", "
                    val_string += " to "
                    for j in range(dim_in):
                        val_string += str(W[i*dim_b+k+1,j])
                        if j < dim_in - 1:
                            val_string += ", "
                    val_string += " nohead\n"
                    f.write(val_string)
            
            for k in range(dim_b):
                for i in range(dim_a-1):
                    val_string = "set arrow from "
                    for j in range(dim_in):
                        val_string += str(W[i*dim_b+k,j])
                        if j < dim_in - 1:
                            val_string += ", "
                    val_string += " to "
                    for j in range(dim_in):
                        val_string += str(W[(i+1)*dim_b+k,j])
                        if j < dim_in - 1:
                            val_string += ", "
                    val_string += " nohead\n"
                    f.write(val_string)
            
            val_string = "set arrow from "
            
            f.write("replot\n")

            f.close()
            
            g1.reset()
            g1('unset key')
            
            #for 2d plots:
            g1('plot "'+data_path+datafile+'" with dots')
            g1('replot "'+data_path+'out.dat" with points')
            g1.load(data_path+"out.gnu")
            
            #for 3d plots:            
            #g2('splot "'+datafile+'" with dots')
            # ------------            

print "SOM finished", datafile

raw_input("Press Enter to close") # use this of you want to run the script from command line
