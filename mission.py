import sympy as sy
import numpy as np
import matplotlib.pyplot as plt

class Mission(object):
    def __init__(self, mission):
        n_phases, initial_state, time_step, break_alt, masses, chutes, max_time, max_ke = mission
        assert n_phases == len(break_alt) == len(masses)
        self.__as = 0
        self.__vs = 1
        self.n = n_phases
        self.dt = time_step
        self.time_lim = max_time
        self.ke_lim = max_ke
        self.phase = break_alt
        self.equ = []
        self.state = initial_state
        self.mass = masses
        for i in range(n_phases):
            self.equ.append(self.make_equ(masses[i], chutes[i].S, chutes[i].cd))

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
        try:
            over_time = min(np.where(self.time > self.time_lim)[0])
            print("*** Altitude where max time is exceeded: {0:.2f} ft ***".format(self.path[over_time, self.__as]))
        except ValueError:
            pass
        print("Velocity of final descent: {0:.2f} ft/s".format(abs(self.yf[1])))
        if 'masses' in kwargs:
            i = 0
            for m in kwargs["masses"]:
                i += 1
                ke = self.kinetic_energy(self.yf[1], m)
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
        return

    @staticmethod
    def make_equ(mass, area, c_d):
        r_y, v_y = sy.symbols("r_y, v_y")
        g = 32.17405
        rho = 0.0023769
        d_r_y = v_y

        d_v_drag = (c_d * 0.5 * rho * area * v_y ** 2) / mass
        d_v_y = d_v_drag - g

        var = [r_y, v_y]
        equs = sy.Matrix([d_r_y, d_v_y])
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

    def plot_path(self, label=""):
        x = self.time
        y = self.path[:, 0]
        plt.scatter(self.time_lim, 0, label="Time limit")
        plt.scatter(self.tf, 0, c="BLACK", marker="x")
        plt.plot(x, y, label=label)
        plt.title("Altitude Plot")
        plt.xlabel("Time (sec)")
        plt.ylabel("Altitude (ft)")

    def plot_vel(self, label=""):
        x = self.time
        y = -self.path[:, 1]
        plt.scatter(self.tf, self.ke2vel(self.ke_lim, self.mass[-1]), label="Velocity limit")
        plt.scatter(self.tf, -self.yf[1], c="BLACK", marker="x")
        plt.plot(x, y, label=label)
        plt.title("Velocity Plot")
        plt.xlabel("Time (sec)")
        plt.ylabel("Velocity (ft/s)")

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
