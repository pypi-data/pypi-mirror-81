from mayavi.mlab import *
import numpy as np


class Plotter:
    """Class to gather plotting functionalities.
    Interfaces with mayavi functions"""
    def __init__(self):
        pass

    @staticmethod
    def plot_trajectory(trajectory, **kwargs):
        """Plots curve from trajectory (3d x time numpy array).
        Returns plot3d object"""
        plot = plot3d(trajectory[0, :], trajectory[1, :], trajectory[2, :],
                      **kwargs)
        return plot

    @staticmethod
    def plot_separation(pos1, pos2, **kwargs):
        """Plots straight line between 2 points"""
        # todo: better way of dealing with np.arrays needed by mayavi
        plot = plot3d([np.double(pos1[0]), np.double(pos2[0])],
                      [np.double(pos1[1]), np.double(pos2[1])],
                      [np.double(pos1[2]), np.double(pos2[2])],
                      **kwargs)
        return plot

    @staticmethod
    def plot_vector(pos, direction, **kwargs):
        """Plots arrow at pos, pointing w/ direction"""

        # todo: guarantee normalized dir? and/or produce dir from 2 positions
        plot = quiver3d([np.double(pos[0])],
                        [np.double(pos[1])],
                        [np.double(pos[2])],
                        [np.double(direction[0])],
                        [np.double(direction[1])],
                        [np.double(direction[2])],
                        **kwargs)
        return plot

    @staticmethod
    def plot_point(pos, **kwargs):
        """PLots ball to represent body"""

        # todo: special visualization cases for Sun and planets?
        plot = points3d(np.double(pos[0]),
                        np.double(pos[1]),
                        np.double(pos[2]),
                        **kwargs)
        return plot
