import numpy as np


class parachute(object):
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
