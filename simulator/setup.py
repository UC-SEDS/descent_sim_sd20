from setup_files.mission_chutes import parachutes
import numpy as np


class MissionSetup(object):
    def __init__(self, name, n_phases, chutes, masses, break_alt, time_step, state, ke_limit=75, time_limit=90):
        assert isinstance(name, str), "\"name\" must be a string"
        assert isinstance(chutes, list), "\"chutes\" must be a list of parachute names"
        assert isinstance(masses, list), "\"masses\" must be a list of masses per phase"
        assert len(chutes) == n_phases, "\"chutes\" must have the same number of parachutes as the number of phases"
        assert len(masses) == n_phases, "\"masses\" must have the same number of masses as the number of phases"
        assert len(time_step) == n_phases, "\"time_step\" must have the same number of masses as the number of phases"
        assert isinstance(state, np.ndarray), "\"state\" must be instantiate as an ndarray"
        assert len(state.flatten()) == 2, "\"state\" must be a (2, ) ndarray"
        assert isinstance(ke_limit, (float, int)), "\"ke_limit\" must be a float or int"
        assert isinstance(time_limit, (float, int)), "\"time_limit\" must be a float or int"
        self.title = name
        self.max_ke = ke_limit
        self.max_time = time_limit
        self.chutes = []
        self.n = n_phases
        for chute in chutes:
            try:
                self.chutes.append(parachutes[chute])
            except IndexError:
                pass
        self.initial_state = state.flatten()
        self.masses = masses
        self.bc = break_alt
        self.dt = time_step
