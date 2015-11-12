from sympy import *
from sympy.abc import x

def evaluate(a):
	return a.evalf()

def main():
	N = int(raw_input("Enter the number of Carbon atoms present : "))
	n = int(raw_input("Enter the number of bonds present in the atom: "))
	d = [[0 for l in xrange(N)] for l in xrange(N)]
	for i in xrange(0,n):
		string  = raw_input("Enter the atom number b/w which bond is formed: ( Eg. 1 2 ) ")
		string = string.split()
		a = int(string[0])
		b = int(string[1])
		if a == b :
			n = n + 1
			print "Can't be the same"
			continue
		d[ a - 1 ][ b - 1 ] = 1
		d[ b - 1 ][ a - 1 ] = 1
	for i in xrange(N):
		d[i][i] = x
	temp = d
	d = Matrix(d)
#	print d
	d = d.diagonalize()
#	print d[1]
	d = list(d[1])
	d = filter(lambda a: a!=0,d)
#	print d
	eq = poly(1,x)
	for term in d :
		eq *= poly(term)
#	print eq
	values = solve(eq)
	values.sort()
	values.reverse()
	coefficients = []
#	print values
	for value in values:
		print "value for x is : " + str(value)
		y = value
		coeff = []
		func = []
		f = -1
		for i in range(N):
			coeff.append(Symbol('c' + str(i+1)))
			f += Symbol('c' + str(i+1))**2
#		print coeff
		func.append(f)
		for i in range(N):
			f = 0
			for j in range(N):
				if temp[i][j] is x:
					f += y*coeff[j]
				else:
					f += temp[i][j]*coeff[j]
			func.append(f)
#		print func
		answer = solvers.solve(func,coeff)
		answer = answer[len(answer)-1]
		coefficients.append(answer)
		print answer
	charge_density = [0 for l in range(N)]
	for i in range(N):
		for j in range(N/2):
			charge_density[i] += 2*(coefficients[j][i]**2)
	charge_density = map(evaluate,charge_density)
	print "------------------"
	print charge_density
	print "------------------"



if __name__ == '__main__':
	main()