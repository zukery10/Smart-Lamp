from motion_sensor_v1 import sense_motion
from rules_engine import if_motion_detected, checkTime
from light_controller import setLightState, getLightState
from sense_hat import SenseHat
from picamera2 import Picamera2

sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()

lamp_on_time = "13:00:00"
# Next task - seperate the while loop from the motion function
while True:
    light_state = getLightState()
    #print(light_state)

    if checkTime(lamp_on_time) == True: # checks if time set by user for motion/daytime 
        #print("On time")
        payload = if_motion_detected(sense_motion(camera), light_state)
        setLightState(payload)





