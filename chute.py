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
        self.cd = c_drag
        self.S = surf_area

    def effective_area(self, v, m, rho, g, update=False):
        """Calculate effective area of a parachute"""
        S = (m * g) / (0.5 * self.cd * rho * v ** 2)
        if update:
            self.S = S
        return S

    def circular_area(self, d, update=False):
        """Calculate area of a circle"""
        S = np.pi * (d / 2.0) ** 2
        if update:
            self.S = S
        return S
