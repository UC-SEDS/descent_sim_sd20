from mission_chutes import payload_chutes
import numpy as np
from tools import toslugs, tofeet

def payload_setup():
    # Constraints
    max_ke = 75.0  # ft lbs
    max_time = 90.0  # sec

    # import parachute data
    pay = payload_chutes['main']
    fall = payload_chutes['freefall']

    # Rocket mission
    initial_state = np.array([4000.0, 0.0])
    phases = 3
    # set up mission parameters
    m_drone = toslugs(1.57, 'lb')
    m_nose = toslugs(1.875, 'lb')  # mass of nose cone (slug)
    m_can = toslugs(7.67 - 1.875, 'lb')  # mass of payload section (slug)
    m_pay = m_can + m_nose + m_drone
    m_pay_empty = m_can + m_nose
    dt = [0.01, 0.01, 0.01]  # time step for each phase
    mass = [m_pay, m_pay, m_pay_empty]  # mass for each phase
    bc = [600.0, 400, 0.0]  # altitude breaking conditions
    chutes = [fall, pay, pay]  # parachute used for each phase
    return [phases, initial_state, dt, bc, mass, chutes, max_time, max_ke]
