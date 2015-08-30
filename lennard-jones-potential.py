from random import uniform
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

global N,pos,vel,epsilon,sigma,mass,time,delta


def calculate_vel(value):
	x = value[0]
	y = value[1]
	z = value[2]
	return sqrt( x*x + y*y + z*z )

def calculate_squarevel(value):
	x = value[0]
	y = value[1]
	z = value[2]
	return x*x + y*y + z*z

def calculate_position(first,second):
	x1,y1,z1 = first[0],first[1],first[2]
	x2,y2,z2 = second[0],second[1],second[2]
	return sqrt( pow( x2 - x1 , 2 ) + pow( y2 - y1 , 2) + pow( z2 - z1 , 2) )

def calculate_force(first,second):
	temp = -1 * 24 * epsilon * ( 2 * pow( sigma , 12 ) / pow( calculate_position( first , second ) , 13 ) - pow( sigma , 6 ) / pow( calculate_position( first , second ) , 7))
	temp_x = ( second[0] - first[0] )/calculate_position(first,second)
	temp_y = ( second[1] - first[1] )/calculate_position(first,second)
	temp_z = ( second[2] - first[2] )/calculate_position(first,second)
	return ( temp * temp_x , temp * temp_y , temp * temp_z )

if __name__ == "__main__":
	time = []
	t = 0
	delta = 0.001
	epsilon = 1
	sigma = 1
	mass = 1
	N = 100
	pos = []
	count = 2001	
	i = 0
	V = []
	K = []
	T = []

	# Initializations Start
	for x in xrange(N):
		temp = [uniform(0,10),uniform(0,10),uniform(0,10)]
		pos.append(temp)
	
	vel = []
	
	for x in xrange(N):
		temp = [uniform(-10,10),uniform(-10,10),uniform(-10,10)]
		vel.append(temp)
	# Initialization End


	while i < count:
		t += delta
		time.append(t)
		i += 1	
		kinetic = []
		
		for x in xrange(N):
			temp = 0.5 * mass * calculate_squarevel(vel[x])
			kinetic.append(temp)
		total_kinetic = sum(kinetic)

		potential = []
		total_potential = []
		for x in range(N):
			array = []
			for y in range(N):
				if x == y:
					array.append(0)
					continue
				temp = 4 * epsilon * ( pow( sigma / calculate_position( pos[x] , pos[y] ) , 12 ) - pow( sigma / calculate_position( pos[x] , pos[y] ) , 6 ) )
				array.append(temp)
			potential.append(array)
		for x in range(N):
			temp = 0
			for y in range(N):
				temp = sum(potential[y])
			total_potential.append(temp)
		total_potential = sum(total_potential)


		force = []
		for x in range(N):
			array = []
			for y in range(N):
				if x == y:
					val = (0,0,0)
					array.append(val)
					continue
				temp = calculate_force( pos[x] , pos[y] )
				array.append(temp)
			force.append(array)

		for x in range(N):
			force_x,force_y,force_z = 0,0,0
			for temp in force[x]:
				force_x += temp[0]
				force_y += temp[1]
				force_z += temp[2]
			acc_x,acc_y,acc_z = force_x / mass,force_y / mass,force_z / mass
			pos[x][0] += vel[x][0]*delta + 0.5 * acc_x * delta * delta
			pos[x][1] += vel[x][1]*delta + 0.5 * acc_y * delta * delta
			pos[x][2] += vel[x][2]*delta + 0.5 * acc_z * delta * delta
			vel[x][0] = vel[x][0] + acc_x * delta
			vel[x][1] = vel[x][1] + acc_y * delta
			vel[x][2] = vel[x][2] + acc_z * delta
		if i == 1:
			continue
		print i-1," : ",total_potential + total_kinetic, " , ",total_potential, " , ",total_kinetic
		K.append(total_kinetic)
		V.append(total_potential)
		T.append(total_kinetic + total_potential)
	time.pop()
	plt.plot(time,T,"r")
	plt.plot(time,V,"g")
	plt.plot(time,K,"b")
	plt.show()