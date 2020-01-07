"""
Author: Alex Stubbles

Description: The Mission class takes initial conditions and all mission parameters then generates a numerical descent
simulation.

Details: The numerical simulation uses a Runge-Kutta 4 integrator for the numerical simulation until one of the breaking
conditions have been met. The breaking conditions can only be set using the state vector in the simulation. The
simulation will save the entire run as a ndarray and has plotting capabilities to visualize the velocity and position
over time. The simulation is currently a 1D simulation that does not take crosswind into account. ***Creating a 2D
Simulation in the same framework would be very useful for varying testing non-uniform crosswinds***
"""
import sympy as sy
import numpy as np
import matplotlib.pyplot as plt

class Mission(object):
    def __init__(self, mission):
        n_phases, initial_state, time_step, break_alt, masses, chutes, wind_speed, max_time, max_ke = mission
        assert n_phases == len(break_alt) == len(masses)
        self.__as = 1  # the element in the state vector that holds the altitude
        self.__vs = 3  # the element in the state vector that holds the y velocity
        self.n = n_phases
        self.dt = time_step
        self.time_lim = max_time
        self.ke_lim = max_ke
        self.phase = break_alt
        self.equ = []
        self.state = initial_state
        self.mass = masses
        self.v_o = wind_speed
        for i in range(n_phases):
            self.equ.append(self.make_equ(masses[i], chutes[i].S, chutes[i].cd, self.v_o))

        self.path = None
        self.time = None
        self.ke = None
        self.tf = None
        self.yf = None

    def run_mission(self):
        y = self.state
        time = np.array([0])
        state = y
        state = state.reshape((1, len(y)))
        for i in range(self.n):
            y, t = self.sim(y, self.dt[i], self.equ[i], i)
            time = np.append(time, t + time[-1])
            state = np.append(state, y, axis=0)
            y = y[-1, :]
        self.path = state
        self.time = time
        self.tf = time[-1]
        self.yf = self.path[-1, :]
        self.ke = self.kinetic_energy(self.path[-1, self.__vs], self.mass[-1])
        return state, time

    def results(self, name="", **kwargs):
        print("-------------------- {0:s} --------------------".format(str(name)))
        print("Time of descent: {0:.2f}".format(self.tf))
        print()
        try:
            over_time = min(np.where(self.time > self.time_lim)[0])
            print("*** Altitude where max time is exceeded: {0:.2f} ft ***".format(self.path[over_time, self.__as]))
        except ValueError:
            pass
        print("Velocity of final descent: {0:.2f} ft/s".format(abs(self.yf[self.__vs])))
        print()
        if 'masses' in kwargs:
            i = 0
            for m in kwargs["masses"]:
                i += 1
                ke = self.kinetic_energy(self.yf[self.__vs], m)
                print("Kinetic Energy section {0} on touchdown: {1:.2f} ft lbs".format(i, ke))
                if ke > self.ke_lim:
                    print("*** Kinetic energy section {0} Exceeded by: {1:.2f} ft lbs ***".format(i, ke - self.ke_lim))
        else:
            print("Kinetic Energy on touchdown: {0:.2f} ft lbs".format(self.ke))
            if self.ke > self.ke_lim:
                print("*********************************************")
                print("Kinetic energy Exceeded by: {0:.2f} ft lbs".format(self.ke - self.ke_lim))
                print("*********************************************")
        print()
        print("Drift distance with {0:.2f} fps wind: {1:.2f} ft".format(self.v_o, self.yf[0]))
        print()
        return

# TODO: test wind turbine wind gradient function

    @staticmethod
    def make_equ(mass, area, c_d, v_o):
        x, y, u, v = sy.symbols("x, y, u, v", real=True)
        wind = v_o * sy.log(y/0.3) / sy.log(10/0.3)
        g = 32.17405
        rho = 0.0023769
        theta = sy.atan2(v, u + wind)
        vel_abs = sy.sqrt((u + wind) ** 2 + v ** 2)
        drag = (c_d * 0.5 * rho * area * vel_abs ** 2) / mass

        d_x = -u
        d_y = v
        d_u = -drag * sy.cos(theta)
        d_v = -drag * sy.sin(theta) - g

        var = [x, y, u, v]
        equs = sy.Matrix([d_x, d_y, d_u, d_v])
        l_equ = sy.lambdify([var], equs)
        return l_equ

    def sim(self, y_i, dt, func, phase):
        y = y_i
        results = []
        it = 0
        while self.bcon(y, self.phase[phase]):
            it += 1
            y = self.rk4(y, func, dt)
            results.append(y)
        results = np.asarray(results)
        time = np.arange(it) * dt
        return results, time

    def bcon(self, y, bc):
        s = self.__as
        return y[s] > bc

    def plot_tvalt(self, label=""):
        x = self.time
        y = self.path[:, self.__as]
        plt.scatter(self.time_lim, 0, label="Time limit")
        plt.scatter(self.tf, 0, c="BLACK", marker="x")
        plt.plot(x, y, label=label)
        plt.title("Altitude vs Time Plot")
        plt.xlabel("Time (sec)")
        plt.ylabel("Altitude (ft)")

    def plot_path(self, label=""):
        x = self.path[:, 0]
        y = self.path[:, self.__as]
        plt.plot(x, y, label=label)
        plt.title("Path Plot")
        plt.xlabel("Drift (ft)")
        plt.ylabel("Altitude (ft)")

    def plot_vel_fall(self, label=""):
        x = self.time
        y = -self.path[:, self.__vs]
        plt.scatter(self.tf, self.ke2vel(self.ke_lim, self.mass[-1]), label="Velocity limit")
        plt.scatter(self.tf, -self.yf[self.__vs], c="BLACK", marker="x")
        plt.plot(x, y, label=label)
        plt.title("Fall Velocity Plot")
        plt.xlabel("Time (sec)")
        plt.ylabel("Velocity (ft/s)")

    def plot_vel_drft(self, label=""):
        x = -self.path[:, 2]
        y = self.path[:, self.__as]
        plt.plot(x, y, label=label)
        plt.title("Drift Velocity Plot")
        plt.xlabel("Velocity (ft/s)")
        plt.ylabel("Altitude (ft)")

    @staticmethod
    def rk4(yn, f, h):
        shp = yn.shape
        yn = yn.flatten()
        k1 = (f(yn) * h).flatten()
        y = yn + 0.5 * k1
        k2 = (f(y) * h).flatten()
        y = yn + 0.5 * k2
        k3 = (f(y) * h).flatten()
        y = yn + k3
        k4 = (f(y) * h).flatten()
        return (yn + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0).reshape(shp)

    @staticmethod
    def kinetic_energy(v, m):
        return 0.5 * m * v ** 2

    @staticmethod
    def ke2vel(ke, m):
        return np.sqrt(ke*2.0/m)
