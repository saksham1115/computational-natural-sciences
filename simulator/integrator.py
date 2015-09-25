import math
class leapfrog_integrator():
    def __init__(self, particle, dt):
        particle.velx = particle.velx + particle.forcex*dt*(1.0/(2.0*particle.mass)) #euler for initialization

    def integrate_positions(self, particle, dt, pbc, box_length):
        particle.posx = particle.posx + particle.velx*dt
        particle.posy = particle.posy + particle.vely*dt
        particle.posz = particle.posz + particle.velz*dt
        

    #correcting the positions of atoms going outside the box
        if pbc:
            if particle.posx > box_length or particle.posx < 0.0:
                particle.posx -= box_length*(math.floor(particle.posx/box_length))

            if particle.posy > box_length or particle.posy < 0.0:
                particle.posy -= box_length*(math.floor(particle.posy/box_length))

            if particle.posz > box_length or particle.posz < 0.0:
                particle.posz -= box_length*(math.floor(particle.posz/box_length))

    def integrate_velocities(self, particle, dt):  
        particle.velx = particle.velx + particle.forcex*dt*(1.0/particle.mass)
        particle.vely = particle.vely + particle.forcey*dt*(1.0/particle.mass)
        particle.velz = particle.velz + particle.forcez*dt*(1.0/particle.mass)
