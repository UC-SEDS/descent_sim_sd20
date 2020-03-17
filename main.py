from tools import toslugs
from simulator.mission import Mission
from setup_files.rocket_post_build_space_jam import rocket_setup, payload_setup
import matplotlib.pyplot as plt
import numpy as np

# setup_files the missions class for each independent section
rocket = Mission(rocket_setup)
payload = Mission(payload_setup)

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

# Printing tables for results
rocket.display('drift')
payload.display('drift', append=True)
print()
rocket.display('velocity')
payload.display('velocity', append=True)
print()
rocket.display('time')
payload.display('time', append=True)
print()
rocket.display('ke', sections=["Aft", "Mid"])
payload.display('ke', append=True, sections=["Payload", "Nose Cone"])
print()
