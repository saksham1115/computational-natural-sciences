from particles import particle
import  math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class MC_simulator():
    """
    Units
    sigma - metres
    epsilon - joules
    position_of_particles - metres
    velocities - m/s
    time-step = femtoseconds
    mass = kg
    """
    def __init__(self, num_of_particles, sigma, epsilon, length_of_box=1e-8, initial_velocity=1.57*1e2, pbc=False):
        self.sigma = sigma
        self.epsilon = epsilon
        self.particles = []
        self.box_length = length_of_box
        self.pbc = pbc
        for i in range(num_of_particles):
            self.particles.append(particle(length_of_box=length_of_box,velocity=initial_velocity, mass=6.69*1e-26))
        self.num_of_particles = num_of_particles

    def show_info(self):
        for i in self.particles:
            print i

    def lj_potential(self):
        potential = 0.0
        for i in range(self.num_of_particles - 1):
            for j in range(i + 1, self.num_of_particles):
                dx = (self.particles[i].posx - self.particles[j].posx)
                dy = (self.particles[i].posy - self.particles[j].posy)
                dz = (self.particles[i].posz - self.particles[j].posz)

                if self.pbc:
                    dx = dx - self.box_length*(math.floor(dx/self.box_length))
                    dy = dy - self.box_length*(math.floor(dy/self.box_length))
                    dz = dz - self.box_length*(math.floor(dz/self.box_length))
                    if abs(dx) > 0.5*self.box_length:
                        dx -= self.box_length*(dx/abs(dx))
                    if abs(dy) > 0.5*self.box_length:
                        dy -= self.box_length*(dy/abs(dy))
                    if abs(dz) > 0.5*self.box_length:
                        dz -= self.box_length*(dz/abs(dz))
                r = dx**2 + dy**2 + dz**2

                attractive_term = ((self.sigma**2)/float(r))**3
                repulsive_term = attractive_term**2
                potential += repulsive_term - attractive_term

        potential = 4.0 * self.epsilon * potential
        return potential

    def kinetic_energy(self):
        kinetic = 0.0
        for i in range(self.num_of_particles):
            kinetic += ((self.particles[i].velx**2 + self.particles[i].vely**2 + self.particles[i].velz**2)*self.particles[i].mass)/2.0

        return kinetic


    def sample_energies(self):
        return self.kinetic_energy() ,self.lj_potential()


    def calc_forces(self):
        for i in range(self.num_of_particles - 1):
            for j in range(i + 1, self.num_of_particles):
                dx = (self.particles[i].posx - self.particles[j].posx)
                dy = (self.particles[i].posy - self.particles[j].posy)
                dz = (self.particles[i].posz - self.particles[j].posz)
                if self.pbc:
                    dx = dx - self.box_length*(math.floor(dx/self.box_length))
                    dy = dy - self.box_length*(math.floor(dy/self.box_length))
                    dz = dz - self.box_length*(math.floor(dz/self.box_length))
                    if abs(dx) > 0.5*self.box_length:
                        dx -= self.box_length*(dx/abs(dx))
                    if abs(dy) > 0.5*self.box_length:
                        dy -= self.box_length*(dy/abs(dy))
                    if abs(dz) > 0.5*self.box_length:
                        dz -= self.box_length*(dz/abs(dz))

                r = dx**2 + dy**2 + dz**2

                attractive_term = ((self.sigma**2)/float(r))**3
                repulsive_term = attractive_term**2
                force = (48.0*self.epsilon*(repulsive_term - 0.5*attractive_term))/(float(r))

                #calculating forces for each dimension
                self.particles[i].forcex += force*dx
                self.particles[j].forcex += force*dx*-1.0

                self.particles[i].forcey += force*dy
                self.particles[j].forcey += force*dy*-1.0

                self.particles[i].forcez += force*dz
                self.particles[j].forcez += force*dz*-1.0

    def clear_forces(self):
        for i in range(self.num_of_particles):
            self.particles[i].forcex = 0.0
            self.particles[i].forcey = 0.0
            self.particles[i].forcez = 0.0


    def init_integrator(self, timestep, type="leapfrog"):
        if type=="leapfrog":
            for i in range(self.num_of_particles):
                self.intgr = integrator.leapfrog_integrator(self.particles[i],timestep)


    def integrate_equations_of_motion_pos(self, timestep):
       for i in range(self.num_of_particles):
            self.intgr.integrate_positions(self.particles[i],timestep,self.pbc, self.box_length)

    def integrate_equations_of_motion_vel(self, timestep):
       for i in range(self.num_of_particles):
            self.intgr.integrate_velocities(self.particles[i],timestep)

    def simulate(self, timestep, total_time_steps, verbose=False):
        step = 0
        kinetic = []
        potential = []
        total = []
        self.calc_forces()
        self.init_integrator(timestep,"leapfrog")	
        while step < total_time_steps:
            if verbose==True:
                print "Time Simulated: " + str(step) + " femtoseconds, ",
            self.integrate_equations_of_motion_pos(timestep)
            self.calc_forces()
            self.integrate_equations_of_motion_vel(timestep)
            step += 1.0
            KE, PE = self.sample_energies()
            if verbose==True:
                print "Kinetic: " + str(KE) + ", Potential: " + str(PE)
            kinetic.append(KE)
            potential.append(PE)
            total.append(KE+PE)
            self.clear_forces()
        return kinetic, potential, total

    def show_particles(self):
        fig = plt.figure()
        ax = Axes3D(plt.gcf())
        ax.scatter(np.array([i.posx for i in self.particles]), np.array([i.posy for i in self.particles]), np.array([i.posz for i in self.particles]))
        plt.show()

def main():
    simulation_length = 200
    timestep = 1e-12
    sim = simulator(256, 3.4*1e-10, 1.65*1e-21, pbc=True)
    #plot initial positions of particles
    sim.show_particles()

    ke, pe, te = sim.simulate(timestep, simulation_length, verbose=True)

    #plotting energies at each time-step
    x_ticks = np.arange(simulation_length)
    plt.plot(x_ticks, np.array(ke), label="Kinetic Energy")
    plt.plot(x_ticks, np.array(pe), label="Potential Energy")
    plt.plot(x_ticks, np.array(te), label="Total Energy")
    plt.legend(loc=2)
    plt.show()
    #sim.show_info()
    #plot position of particles at end of simulation
    sim.show_particles()
    return


#boiler-plate argument
if __name__ == '__main__':
    main()

