from tools import toslugs
from sim_classes.mission import Mission
from setup.payload_setup import payload_setup
from setup.rocket_setup import rocket_setup
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
aft_section = toslugs(14.67 + 4.06, 'lb')
full_pay_section = toslugs(9.34, 'lb')
nose_section = toslugs(2.4, 'lb')
# rocket.results("Rocket", masses=[mid_section, aft_section])
# payload.results("Payload", masses=[full_pay_section, nose_section])

# Plotting results
plt.figure(1)
rocket.plot_path("Rocket Path")
payload.plot_path("Payload Path")
plt.legend()
