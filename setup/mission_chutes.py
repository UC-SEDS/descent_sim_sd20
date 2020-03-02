from sim_classes import chute
from tools import tofeet, toslugs

g = 32.17405
rho = 0.0023769

# Defining Parachutes

# Example format
# drag_coefficient = xxx
# reference_area = yyy
# parachute = chute.Parachute(drag_coefficient, reference_area)

# To find surface area call Parachute.circular_area() or Parachute.effective_area()

###################### Drogues ######################
diam = tofeet(24.0, 'in')  # ft
cd = 0.75
drg24 = chute.Parachute(cd, None)
drg24.circular_area(diam, update=True)

diam = tofeet(36.0, 'in')  # ft
cd = 0.75
drg36 = chute.Parachute(cd, None)
drg36.circular_area(diam, update=True)


# cd = 1.21 + 1.17
cd = 4.0
diam = tofeet(7.5, 'in')
pay_free = chute.Parachute(cd, None)
pay_free.circular_area(diam, update=True)

###################### Mains ######################
cd = 1.87
classicII_44 = chute.Parachute(cd, None)
classicII_44.effective_area(17.0, toslugs(4.4, 'lb'), rho, g, update=True)


cd = 1.26
certL = chute.Parachute(cd, None)
certL.effective_area(17.0, toslugs(16.2, 'lb'), rho, g, update=True)


cd = 2.59
certXL = chute.Parachute(cd, None)
certXL.effective_area(17.0, toslugs(32.6, 'lb'), rho, g, update=True)

cd = 2.92
certXXL = chute.Parachute(cd, None)
certXXL.effective_area(17.0, toslugs(60.0, 'lb'), rho, g, update=True)


diam = tofeet(58.0, 'in')
cd = 1.75
para_58 = chute.Parachute(cd, None)
para_58.circular_area(diam, update=True)

parachutes = {"24": drg24,
              "36": drg36,
              "certL": certL,
              "certXL": certXL,
              "certXXL": certXXL,
              "classicII 44": classicII_44,
              "58": para_58,
              "freefall": pay_free}