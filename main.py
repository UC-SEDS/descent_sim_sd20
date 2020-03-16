from tools import toslugs
from sim_classes.mission import Mission
from setup.payload_setup import payload_setup
from setup.rocket_setup import rocket_setup
import matplotlib.pyplot as plt
import numpy as np

# call mission setups
rocket_mission = rocket_setup()
pay_mission = payload_setup()


# setup the missions class for each independent section
rocket = Mission(rocket_mission)
payload = Mission(pay_mission)

# run simulation
mid_section = toslugs(17.81, 'lb')
aft_section = toslugs(14.67 + 4.06, 'lb')
split = [np.array([mid_section, aft_section]),
         np.array([mid_section, aft_section])]
rocket.run_mission(split=split)
full_pay_section = toslugs(9.34, 'lb')
nose_section = toslugs(2.4, 'lb')
split = [np.array([full_pay_section, nose_section]),
         np.array([full_pay_section, nose_section])]
payload.run_mission(split=split)

# Plotting results
plt.figure(1)
rocket.plot_path("Rocket Path")
payload.plot_path("Payload Path")
plt.legend()

rocket.display('drift', 'Rocket')
payload.display('drift', 'Payload', append=True)
print()
rocket.display('velocity', 'Rocket')
payload.display('velocity', 'Payload', append=True)
print()
rocket.display('time', 'Rocket')
payload.display('time', 'Payload', append=True)
print()
rocket.display('ke', 'Rocket', sections=["Aft", "Mid"])
payload.display('ke', 'Payload', append=True, sections=["Payload", "Nose Cone"])
print()
