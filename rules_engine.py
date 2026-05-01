import json

#https://github.com/UselessMnemonic/OpenWiz


def if_motion_detected(motion, triggered):
    payload = None
    if motion and not triggered:
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