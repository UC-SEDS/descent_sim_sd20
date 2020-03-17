from simulator.setup import MissionSetup
from tools import toslugs
import numpy as np


name = "Rocket"
drogue = '24'
main = 'certXXL'

# Constraints
max_ke = 75.0  # ft lbs
max_time = 90.0  # sec

initial_state = np.array([4000.0, 0.0])
phases = 2
# set up mission parameters
dt = [0.01, 0.01]  # time step for each phase
mid_section = toslugs(17.81, 'lb')
aft_section = toslugs(14.67 + 4.06, 'lb')
rocket = mid_section + aft_section  # total rocket mass
mass = [rocket, rocket]  # mass for each phase
bc = [600.0, 0.0]  # altitude breaking conditions
chutes = [drogue, main]  # parachute used for each phase

rocket_setup = MissionSetup(name, phases, chutes, mass, bc, dt, initial_state)

name = "Payload"
pay = 'certL'
fall = 'freefall'
# Rocket mission
initial_state = np.array([4000.0, 0.0])
phases = 2
# set up mission parameters
m_drone = toslugs(1.57, 'lb')
m_nose = toslugs(2.4, 'lb')  # mass of nose cone (slug)
m_can = toslugs(9.34, 'lb')  # mass of payload section (slug)
m_pay = m_can + m_nose
m_pay_empty = m_can + m_nose
dt = [0.01, 0.01]
mass = [m_pay, m_pay]
bc = [600.0, 0.0]
chutes = [fall, pay]

payload_setup = MissionSetup(name, phases, chutes, mass, bc, dt, initial_state)