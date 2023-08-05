import numpy as np
from mayavi import mlab
from sympy.physics.mechanics import *
from numpy import cos, sin, linspace
from spiffy.plotter import Plotter


class Orbit:
    '''Base orbit class that is used to build circular and eliptical orbits
    frame: sympy.ReferenceFrame object
    center: point/trajectory of the attractor #todo rename?
    color: (R,G,B) tuple to be used when plotting trajectory and body'''

    def __init__(self, frame, center, color = (0, 0, 0)):
        self.frame = frame
        self.center = center
        self.color = color

    def get_position(self, epoch) -> Vector:
        pass

    def get_trajectory(self, epoch: np.array, center = None, frame = None):
        '''Returns a 2D or 3D numpy array of results from get_position()
        over time'''
        if type(self) == CircularOrbit3D:
            pos = np.zeros_like([epoch, epoch, epoch], dtype = float)
        elif type(self) == CircularOrbit2D:
            pos = np.zeros_like([epoch, epoch], dtype = float)

        if frame is None:
            # todo: better explanation of how sympy frames work here,
            # some way to add the possib. of plotting around earth
            frame = self.frame

        for idx, ti in enumerate(epoch):
            # calls get_position() for each time, subtract center position
            if center is None:
                vec = self.get_position(ti).to_matrix(frame)
            else:
                vec = (self.get_position(ti) -
                       center.get_position(ti)).to_matrix(frame)
            pos[:, idx] = vec[:]
        return pos


class CircularOrbit2D(Orbit):
    '''2D circular orbit, built as toy model of 3D orbit. DEPRECATED'''

    def __int__(self, frame, center, radius = 0.0,
                omega = 0.0, phase = 0.0):
        super().__init__(frame, center)
        self.radius = phase
        self.omega = phase
        self.phase = phase

    def get_position(self, epoch, frame = None):
        # given an epoch, returns a vector for position
        if frame is None:
            frame = self.frame

        r = self.radius
        om = self.omega
        ph = self.phase
        center = self.center
        x = r * cos(om * epoch + ph) * frame.x
        y = r * sin(om * epoch + ph) * frame.y

        if center is None:
            return x + y
        elif type(center) is CircularOrbit2D:
            return x + y + center.get_position(epoch)

    def plot_orbit(self, center = None):
        # plots orbit using matplotlib
        # todo pass other frame
        # todo calculate period before choosing t
        t = linspace(0, 6.28, 10000)
        pos_x = np.zeros_like(t, dtype = float)
        pos_y = np.zeros_like(t, dtype = float)

        for idx, ti in enumerate(t):
            if center is None:
                vec = self.get_position(ti).to_matrix(self.frame)
            else:
                vec = (self.get_position(ti) - center.get_position(ti)).to_matrix(self.frame)
            pos_x[idx] = vec[0]
            pos_y[idx] = vec[1]

        return pos_x[:], pos_y[:]


class CircularOrbit3D(Orbit):
    '''Model of a ideal 3D orbit'''

    def __init__(self, parentFrame, center = None,
                 radius: float = 0, omega: float = 0, inclination: float = 0,
                 phase: float = 0, ascNode: float = 0, color = (0, 0, 0)):
        super().__init__(parentFrame, center, color)
        self.frame = parentFrame.orientnew(
                'frame', 'Space', (inclination, 0, ascNode), 123)
        # todo: orient new frame with 'Space'
        # todo: fix frame naming scheme
        self.radius = radius
        self.omega = omega  # todo: rename parm
        self.phase = phase  # todo: rename parm
        self.ascNode = ascNode  # todo: rename parm

    def get_position(self, epoch, frame = None):
        '''given an epoch, returns a sympy vector for position'''
        # todo pass other frame argument
        r = self.radius
        om = self.omega
        ph = self.phase
        if frame is None:
            frame = self.frame

        x = r * cos(om * epoch + ph) * frame.x
        y = r * sin(om * epoch + ph) * frame.y
        z = 0 * frame.z
        if self.center is None:
            return x + y + z
        elif type(self.center) is CircularOrbit3D:
            return x + y + z + self.center.get_position(epoch).express(frame)

    def get_position_matrix(self, epoch, frame):
        """Returns matrix instead of Vector to be used w/ Plotter"""
        return self.get_position(epoch).to_matrix(frame)

    def get_direction(self, other, epoch, frame):
        print(other.get_position(epoch, frame))
        print(self)
        print(other)
        print(self.get_position(epoch, frame))
        direction = other.get_position(epoch, frame) - self.get_position(epoch, frame)
        return direction.simplify().normalize()

    def get_direction_matrix(self, other, epoch, frame):
        return self.get_direction(other, epoch, frame).to_matrix(frame)

    def plot_orbit2D(self, center = None):
        # DEPRECATED
        t = linspace(0, 5, 3000)
        pos_x = []
        pos_y = []

        for idx, ti in enumerate(t):
            if center is None:
                vec = self.get_position(ti).to_matrix(self.frame)
            else:
                vec = (self.get_position(ti)).to_matrix(self.frame)
            pos_x.append(vec[0])
            pos_y.append(vec[1])

        return pos_x[:], pos_y[:]


if __name__ == '__main__':
    # testing the orbit and plotter classes
    N = ReferenceFrame('N')
    t = linspace(0.1, 0.5, 500)  # numpy array

    # creates 3 orbits. Two objects orbiting a main body
    earth_orbit = CircularOrbit3D(N, None, 1, 1, 0, color = (1, 1, 1))
    sat1_orbit = CircularOrbit3D(N, center = earth_orbit, radius = 0.1,
                                 omega = 120, inclination = 85*(np.pi/180),
                                 ascNode = 0, color = (0, 1, 0))
    sat2_orbit = CircularOrbit3D(N, center = earth_orbit, radius = 0.1,
                                 omega = 120, inclination = 85*(np.pi/180),
                                 ascNode = 120*(np.pi/180), color = (0, 0, 1))
    sat3_orbit = CircularOrbit3D(N, center = earth_orbit, radius = 0.1,
                                 omega = 120, inclination = 85*(np.pi/180),
                                 ascNode = 240*(np.pi/180), color = (1, 0, 0))

    orbits = [earth_orbit, sat1_orbit, sat2_orbit, sat3_orbit]
    for obt in orbits:
        Plotter.plot_trajectory(obt.get_trajectory(t, frame = N),
                                tube_radius = None, color = obt.color)
        Plotter.plot_point(obt.get_position_matrix(0.1, N),
                           scale_factor = 0.01, color = obt.color)
    avg_pos = (sat1_orbit.get_position_matrix(0.1, N) +
               sat2_orbit.get_position_matrix(0.1, N) +
               sat3_orbit.get_position_matrix(0.1, N))/3
    plane_vec = sat1_orbit.get_direction_matrix(sat2_orbit, 0.1, N)
    mlab.show()  # calls mayavi show
