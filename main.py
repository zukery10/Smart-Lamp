from motion_sensor_v1 import sense_motion
from rules_engine import if_motion_detected, checkTime
from light_controller import setLightState, getLightState

lamp_on_time = "19:00:00"

while True:
    light_state = getLightState()
    #print(light_state)

    if checkTime(lamp_on_time) == True: # checks if time set by user for motion/daytime 
        print("On time")
        payload = if_motion_detected(sense_motion(), light_state)
        setLightState(payload)





