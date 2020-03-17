"""
Author: Alex Stubbles

Description: The Mission class takes initial conditions and all mission parameters then generates a numerical descent
simulation.

Details: The numerical simulation uses a Runge-Kutta 4 integrator for the numerical simulation until one of the breaking
conditions have been met. The breaking conditions can only be set using the state vector in the simulation. The
simulation will save the entire run as a ndarray and has plotting capabilities to visualize the velocity and position
over time. The simulation is currently a 1D simulation that does not take crosswind into account. ***Creating a 2D
Simulation in the same framework would be very useful for testing non-uniform crosswinds***
"""
import sympy as sy
import numpy as np
import matplotlib.pyplot as plt


class Results(object):
    def __init__(self):
        self.path = []
        self.time = []
        self.ke = []
        self.pos = []
        self.vel = []
        self.pos_final = []
        self.vel_final = []
        self.time_final = []


class Mission(object):
    def __init__(self, mission):
        """
        This class is given mission parameters and initial conditions of the simulation to set up the equations of
        motion. The equations of motion are then evaluated using numerical integration until breaking conditions
        are achieved. The method run_mission() is called after initialization of the Mission class.
        :param mission: list of initial parameters that is returned by running the function in XXX_setup.py.
        """
        self.__as = 0
        self.__vs = 1
        self.__equ = []
        self.__state = mission.initial_state
        self.__n = mission.n
        self.__split = None
        self.title = mission.title
        self.dt = mission.dt
        self.time_lim = mission.max_time
        self.ke_lim = mission.max_ke
        self.phase = mission.bc
        self.mass = mission.masses
        for i in range(self.__n):
            self.__equ.append(self.make_equ(mission.masses[i], mission.chutes[i].S, mission.chutes[i].cd))
        self.results = Results()

    def run_mission(self, split=None):
        """
        Evaluates all phases of the mission iteratively. The mission will run until the breaking conditions have been
        met which is defined as part of the classes initialization. The integration can be cut into multiple phases with
        the final state vector is the initial state vector for the next phase.
        :return:
        """
        if split is None:
            mass = self.mass
        else:
            assert isinstance(split, list), "This must be a list of ndarrays"
            for element in split:
                assert isinstance(element, np.ndarray), "This must be a list of ndarrays"
            assert len(split) == self.__n, "List must have the same length as the number of phases"
            mass = split
            self.__split = split
        y = self.__state
        time = np.array([0])
        state = y
        state = state.reshape((1, len(y)))
        for i in range(self.__n):
            y, t = self.sim(y, self.dt[i], self.__equ[i], i)
            self.results.path.append(y)
            self.results.pos.append(y[:, self.__as])
            self.results.vel.append(y[:, self.__vs])
            self.results.pos_final.append(y[-1, self.__as])
            self.results.vel_final.append(y[-1, self.__vs])
            self.results.time.append(t)
            self.results.time_final.append(t[-1])
            self.results.ke.append(self.kinetic_energy(self.results.path[i][-1, self.__vs], mass[i]))
            time = np.append(time, t + time[-1])
            state = np.append(state, y, axis=0)
            y = y[-1, :]
        self.results.path.insert(0, state)
        self.results.time.insert(0, time)
        self.results.time_final.insert(0, time[-1])
        self.results.pos.insert(0, self.results.path[0][:, self.__as])
        self.results.vel.insert(0, self.results.path[0][:, self.__vs])
        return state, time

    def sim(self, y_i, dt, func, phase):
        """
        Evaluates the equations of motion using numerical integration. The integration method chosen is the
        Runge-Kutta 4 integrator.
        :param y_i: initial state vector
        :param dt: time step for that phase
        :param func: The equations of motion
        :param phase: The current phase that is being run
        :return:
            results: ndarray of all state vectors for the entire descent.
            time: ndarray of the time which each state vector correlates with.
        """
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

    @staticmethod
    def make_equ(mass, area, c_d):
        """
        Using symbolics to derive the equations of motion for each falling section with a given mass, area, and
        coefficient of drag
        :param mass: list of masses for each phase of descent
        :param area: list of reference area for each phase
        :param c_d: list of drag coefficients for each phase
        :return: function that will input a ndarray state vector and return the time derivative
        """
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

    def bcon(self, y, bc):
        """
        This evaluates whether the breaking conditions have been met.
        :param y: The current state vector
        :param bc: The breaking condition being evaluated
        :return: bool
        """
        s = self.__as
        return y[s] > bc

    def plot_path(self, label=""):
        """
        Plots the altitude over time of descent
        :param label: Label of the object descending
        :return: None
        """
        x = self.results.time[0]
        y = self.results.path[0][:, 0]
        plt.scatter(self.time_lim, 0, label="Time limit")
        plt.scatter(self.results.time[0][-1], 0, c="BLACK", marker="x")
        plt.plot(x, y, label=label)
        plt.title("Altitude Plot")
        plt.xlabel("Time (sec)")
        plt.ylabel("Altitude (ft)")

    @staticmethod
    def rk4(yn, f, h):
        """
        Runge-Kutta 4 integrator which integrates over the constant time step h
        :param yn: the current state vector
        :param f: The function for the state vector that takes the current state vector as the input
        :param h: Time step to integrate over
        :return: The change in state vector over the time step h
        """
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
        """
        Calculate the kinetic energy given velocity and mass
        :param v: velocity
        :param m: mass
        :return: kinetic energy
        """
        return 0.5 * m * v ** 2

    @staticmethod
    def ke2vel(ke, m):
        """
        Given kinetic energy and mass the velocity is calculated
        :param ke: Kinetic energy
        :param m: mass
        :return: velocity
        """
        return np.sqrt(ke*2.0/m)

    def display(self, table, append=False, **kwargs):
        if "dec" in kwargs:
            dec = kwargs["dec"]
        else:
            dec = 2
        if table == "drift":
            wind_speeds = [0, 5, 10, 15, 20]
            descent_time = self.results.time_final[0]
            drift_distance = [round(1.466667*wind*descent_time, dec) for wind in wind_speeds]
            row_format = "{:>10}" * (len(wind_speeds) + 1)
            if not append:
                print("Drift Due to Wind (ft)")
                print(row_format.format("", *wind_speeds))
            print(row_format.format(self.title, *drift_distance))
        elif table == "velocity":
            vel = [round(abs(v), dec) for v in self.results.vel_final]
            fz = "Phase "
            phases = [fz+str(i+1) for i in range(self.__n)]
            row_format = "{:>10}" * (len(phases) + 1)
            if not append:
                print("Max Descent Velocity (ft/s)")
                print(row_format.format("", *phases))
            print(row_format.format(self.title, *vel))
        elif table == "time":
            time = [t for t in self.results.time_final]
            fz = "Phase "
            phases = [fz+str(i+1) for i in range(self.__n)]
            phases.insert(0, "Total")
            row_format = "{:>10}" * (len(phases) + 1)
            if not append:
                print("Time for Descent (s)")
                print(row_format.format("", *phases))
            print(row_format.format(self.title, *time))
        elif table == "ke":
            if isinstance(self.results.ke[0], np.ndarray):
                splits = len(self.results.ke[0])
                ke = []
                for s in range(splits):
                    row = []
                    for phase in self.results.ke:
                        row.append(round(phase[s], dec))
                    ke.append(row)
            if self.__split is not None:
                if "sections" in kwargs:
                    mass_names = kwargs["sections"]
                else:
                    mass_names = ["Mass"+str(i+1) for i in range(len(self.__split))]
            else:
                mass_names = self.title
            fz = "Phase "
            phases = [fz+str(i+1) for i in range(self.__n)]
            row_format = "{:>10}" * (len(phases) + 1)
            if not append:
                print("Kinetic Energy (ft lbs)")
                print(row_format.format("", *phases))
            for i, row in enumerate(ke):
                print(row_format.format(mass_names[i], *row))
        else:
            assert False, "Invalid display table\nYou entered \"{0}\"\nOptions: drift, velocity, time, ke".format(table)
