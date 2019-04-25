import numpy as np
from numpy import *
import matplotlib.pyplot as plt 

data = genfromtxt('scores.csv', delimiter=',')

#Extract the data needed to perform a regression
x = array(data[:,0])
y = array(data[:,1])

#Plot the data for a first impression
plt.figure(1)
plt.scatter(x,y)
plt.xlabel('Hours of study')
plt.ylabel('Test scores')
plt.show()



def estimate_coef(x, y): 
	# number of observations/points 
	n = np.size(x) 

	# HERE: Get the mean of x and y vector (hint: use built-in functions)
	mean_x, mean_y = np.mean(x), np.mean(y)

	# calculating cross-deviation and deviation about x 
	SS_xy = np.sum(y*x) - n*mean_y*mean_x 
	SS_xx = np.sum(x*x) - n*mean_x*mean_x 

	# HERE: Calculate the regression coefficients 
	beta_1 = SS_xy / SS_xx
	beta_0 = mean_y - beta_1*mean_x
	
	return(beta_0, beta_1) 

def plot_regression_line(x, y, b): # b = estimated coefficient 
	# HERE: plot the actual points as scatter plot 
	plt.scatter(x, y, color = "m", 
               marker = "o", s = 30)

	# HERE: compute the predicted response vector 
	y_pred = b[0] + b[1]*x 

	# plotting the regression line 
	plt.plot(x, y_pred, color = "k") 

	# putting labels 
	plt.xlabel('x') 
	plt.ylabel('y') 

	# function to show plot 
	plt.show() 

# DATASET INPUT
def main(): 	
	# estimating coefficients 
	b = estimate_coef(x, y) 
	print('The estimated coefficients are ' + repr(b[0]) + ' and ' + repr(b[1]))

	# plotting regression line 
	plt.figure(2)
	plot_regression_line(x, y, b) 
	
if __name__ == "__main__": 
	main() 
