import json
from datetime import datetime

#https://github.com/UselessMnemonic/OpenWiz
lamp_on_time = "15:00:00"
format_time  ="%H:%M:%S"

def if_motion_detected(motion, triggered):
    payload = None
    if motion and triggered == False:
        payload = {
            "method": "setPilot",
            "params":{
                "state": True
            }
        }
        triggered = True
    elif motion and triggered:
        triggered = False
        payload = {
            "method": "setPilot",
            "params":{
                "state": False
            }
        }

    print(motion)
    return payload

def checkTime(lamp_on_time):
    #lamp_on_time = "13:00:00" 
    format_time  ="%H:%M:%S"
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    
    if datetime.strptime(now,format_time) > datetime.strptime(lamp_on_time,format_time):
        return True
    else: 
        return False


