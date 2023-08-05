from spiffy.orbit import *

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
