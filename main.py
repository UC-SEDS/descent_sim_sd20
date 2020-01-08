from tools import toslugs, tofeet
from mission import Mission
from payload_setup import payload_setup
from rocket_setup import rocket_setup
import matplotlib.pyplot as plt

# call mission setups
rocket_mission = rocket_setup()
pay_mission = payload_setup()


# setup the missions class for each independent section
rocket = Mission(rocket_mission)
payload = Mission(pay_mission)

# run simulation
rocket.run_mission()
payload.run_mission()

# Print results to console
mid_section = toslugs(17.81, 'lb')
aft_section = toslugs(19.3, 'lb')
rocket.results("Rocket", masses=[mid_section, aft_section])
payload.results("Payload", masses=[toslugs(5.795, 'lb'), toslugs(1.875, 'lb')])

# Plotting results
plt.figure(1)
rocket.plot_path("Rocket Path")
payload.plot_path("Payload Path")
plt.legend()

plt.figure(2)
rocket.plot_vel("Rocket Velocity")
payload.plot_vel("Payload Velocity")
plt.legend()
