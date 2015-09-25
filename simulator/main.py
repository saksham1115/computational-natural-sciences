import md_simulator
import numpy as np
import matplotlib.pyplot as plt

def MD_main():
    simulation_length = 200
    timestep = 1e-12
    sim = md_simulator.MD_simulator(256, 3.4*1e-10, 1.65*1e-21, length_of_box=1e-7, pbc=True)
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

def MC_main():



def main():
    MD_main()


#boiler-plate argument
if __name__ == '__main__':
    main()
