from motion_sensor_v1 import sense_motion
from rules_engine import  checkTime, processMotionEvent, processTemp
from light_controller import setLightState, getLightState,setLightWarmth,sendUDP
from sense_reader import capture_humidity, capture_temp
from sense_hat import SenseHat
from picamera2 import Picamera2
#https://github.com/UselessMnemonic/OpenWiz
sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()


#need to figure out method to adapt sensitivity to lighting - brighter light sets off motion

lamp_on_time = "13:00:00"
while True:
    light_state = getLightState()
    print(light_state)
    if checkTime(lamp_on_time) == True: # checks if time set by user for motion/daytime 


        #print("On time")
        event = processMotionEvent(sense_motion(camera))
        sendUDP(setLightState(event))

        #sendUDP(setLightWarmth(processTemp(capture_temp(),capture_humidity())))

    






