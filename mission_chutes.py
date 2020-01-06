import chute
from tools import tofeet, toslugs

g = 32.17405
rho = 0.0023769

# Defining Parachutes

###################### Drogues ######################
diam = tofeet(24.0, 'in')  # ft
cd = 0.75
drg24 = chute.parachute(cd, None)
drg24.circular_area(diam, update=True)

diam = tofeet(36.0, 'in')  # ft
cd = 0.75
drg36 = chute.parachute(cd, None)
drg36.circular_area(diam, update=True)

###################### Mains ######################
cd = 2.59
certXL = chute.parachute(cd, None)
certXL.effective_area(17.0, toslugs(32.6, 'lb'), rho, g, update=True)

cd = 2.92
certXXL = chute.parachute(cd, None)
certXXL.effective_area(17.0, toslugs(60.0, 'lb'), rho, g, update=True)

###################### Payload ######################
cd = 0.5 + 0.3
diam = tofeet(7.5, 'in')
pay_free = chute.parachute(cd, None)
pay_free.circular_area(diam, update=True)

diam = tofeet(58.0, 'in')
cd = 1.75
pay = chute.parachute(cd, None)
pay.circular_area(diam, update=True)

drogue_chutes = {"24": drg24,
                 "36": drg36}

main_chutes = {"certXL": certXL,
               "certXXL": certXXL}

payload_chutes = {"main": pay,
                  "freefall": pay_free}
