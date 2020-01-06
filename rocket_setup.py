from mission_chutes import drogue_chutes, main_chutes
import numpy as np
from tools import toslugs, tofeet

def rocket_setup():
    # import parachutes
    drogue = drogue_chutes['36']
    main = main_chutes['certXL']

    # Constraints
    max_ke = 75.0  # ft lbs
    max_time = 90.0  # sec

    initial_state = np.array([4000.0, 0.0])
    phases = 2
    # set up mission parameters
    dt = [0.01, 0.01]  # time step for each phase
    mass = [toslugs(31.8, 'lb'), toslugs(31.8 - 4.0, 'lb')]  # mass for each phase
    bc = [500.0, 0.0]  # altitude breaking conditions
    chutes = [drogue, main]  # parachute used for each phase
    return [phases, initial_state, dt, bc, mass, chutes, max_time, max_ke]
