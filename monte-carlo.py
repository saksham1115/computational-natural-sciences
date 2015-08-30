from random import uniform
import matplotlib.pyplot as plt


def main():
	X = []
	Y = []
	T = 1000
	N = 100000
	a = 2.0
	b = 3.0
	for i in xrange(T):
		Y.append(N)
		n = 0 
		for j in xrange(N):
			x,y = uniform(0.0,a),uniform(0.0,b)
			if (x/a)*(x/a) + (y/b)*(y/b) - 1.0 <= 0.0:
				n += 1
		area = 4.0*(a*b*n)/N
		error = (22.0/7.0)*a*b - area
		print str(i) + " : " + str(area) + " : " + str(error)
		X.append(error)
		N += 1000
	plt.plot(Y,X,"r")
	plt.show()

if __name__ == '__main__':
	main()