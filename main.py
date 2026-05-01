from motion_sensor_v1 import sense_motion
from rules_engine import if_motion_detected
from light_controller import lightState, getLightState



while True:
    #light_state = getLightState()
    payload = if_motion_detected(sense_motion(), False)

    lightState(payload)
    #print(light_state)





