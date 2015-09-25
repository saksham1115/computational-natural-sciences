import numpy as np

class particle():
    #randomly assigning positions and velocities
    def __init__(self, length_of_box, velocity, mass):
        self.posx = np.random.uniform(low=0.0, high=length_of_box)
        self.posy = np.random.uniform(low=0.0, high=length_of_box)
        self.posz = np.random.uniform(low=0.0, high=length_of_box)

        self.velx = np.random.uniform(-velocity,velocity)
        self.vely = np.random.uniform(-velocity,velocity)
        self.velz = np.random.uniform(-velocity,velocity)

        self.forcex = 0.0
        self.forcey = 0.0
        self.forcez = 0.0
        self.mass = mass

    def __str__(self):
        return "Position: " + str(self.posx) + ", " + str(self.posy) + ", " + str(self.posz) + "\nVelocity: " + str(self.velx) + ", " + str(self.vely) + ", " + str(self.velz)




