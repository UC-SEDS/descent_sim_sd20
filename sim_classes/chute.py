"""
Author: Alex Stubbles

Description: The Parachute class defines contains the drag and geometry of the parachute. The parachute class is called
by the Mission class and used for numerical descent calculations. The Parachute class is setup in mission_chutes.py for
each parachute considered for the mission. The parachute class can also be used for objects in freefall give that the
CD and surface area are known.
"""
import numpy as np


class Parachute(object):
    def __init__(self, c_drag, surf_area):
        """
        This class sets up parameters for drag on the descending object
        :param c_drag: Total coefficient of drag on the falling object
        :param surf_area: The reference area for the object which is surface area of the parachute
        """
        self.cd = c_drag
        self.S = surf_area

    def effective_area(self, v, m, rho, g, update=True):
        """
        Calculate effective area of a parachute
        :param v: velocity of parachute
        :param m: mass attached to parachute
        :param rho: air density during descent
        :param g: gravitational acceleration at location
        :param update: default True, flag to save over surface area (S)
        :return: effective surface area backed out from test fall
        """
        S = (m * g) / (0.5 * self.cd * rho * v ** 2)
        if update:
            self.S = S
        return S

    def circular_area(self, d, update=True):
        """
        Calculate area of a circle
        :param d: diameter of parachute
        :param update: default True, flag to save over surface area (S)
        :return:
        """
        S = np.pi * (d / 2.0) ** 2
        if update:
            self.S = S
        return S
