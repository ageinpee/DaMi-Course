''' Solution to Part III - Python functions. Comment out the parts you do not wish to execute or copy 
a specific function into a new py-file'''
 
#Sum of squares, where you can simply use the square function you were given
def sum_of_squares(x, y):
	return square(x) + square(y)
print sum_of_squares(3, 5) # Try out yourself

#Increment by 1
x = 0
y = 0
def incr(x):
	y = x + 1
	return y
print incr(5) # Try out yourself

# Increment by any n; quite straightforward, right?

x = 0
y = 0
def incr_by_n(x, n):
	y = x + n
	return y
print incr_by_n(4,2) # Try out yourself


#Factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
n=int(input("The number you want to compute the factorial of: ")) # User input
print "Result:", factorial(4) # Try out yourself

#Display numbers between 1 and 10 using 'for' ...
for a in range(1, 11):
	print a
	
#... and 'while'
a=1
while a<=10:
	print a
	a+=1

#Test if a number is between 1 and 10 (can be of any range though)
def number_in_range(n):
    if n in range(1,10):
        print( " %s is in the range"%str(n))
    else :
        print "The number is outside the given range."
test_range(8) # Try out yourself

'''Multiple if-conditionals
Note, that no keyword 'end' is needed! Instead, program blocks are controlled via indentation.
For beginners, indentation errors are most likely to occur, so playing around and extending smaller
code snippets to bigger program code can better help understanding the underlying
Python interpretation process'''

def chain_conditions(x,y):
	if x < y:
		print x, "is less than", y
	elif x > y:
		print x, "is greater than", y
	else:
		print x, "and", y, "are equal" 
chain_conditions(50, 10) # Try out yourself

#Prime number
def test_prime(n):
    if (n==1):
        return False
    elif (n==2):
        return True;
    else:
        for x in range(2,n):
            if(n % x==0):
                return False
        return True             
print(test_prime(7)) # Try out yourself
