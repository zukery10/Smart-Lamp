import socket
import time
import json

#https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
#https://www.youtube.com/watch?v=wyoYbMRIAFE



def sendUDP(payload):
    UDP_IP_PLUG = "192.168.2.182"  # Plug IP
    UDP_PORT = 38899 # Port it uses from the Github ref
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # opens a new socket
    message = str(json.dumps(payload))
    message = message.encode('utf-8')
    sock.sendto(message,(UDP_IP_PLUG,UDP_PORT))
    time.sleep(.3)

def getLightState(): #not working yet
    response = None
    
    payload = {
            "method": "getPilot",
        }
    UDP_IP_PLUG = "192.168.2.182"  # Plug IP
    UDP_PORT = 38899 # Port it uses from the Github ref
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # opens a new socket
    message = str(json.dumps(payload))
    message = message.encode('utf-8')
    sock.sendto(message,(UDP_IP_PLUG,UDP_PORT))
    message = sock.recv(1024)# amount of bytes to reciece
    jdata = json.loads(message.decode('utf-8'))#https://www.reddit.com/r/Python/comments/486nl3/anyone_know_how_to_get_json_from_a_socket/
    stateValue = jdata['result']['state']#https://stackoverflow.com/questions/12934699/selecting-fields-from-json-output
    return stateValue
   

def setLightState(state):
    payload = {
            "method": "setPilot",
            "params":{
                "state": state
            }
        }
    return payload

def setLightWarmth(temp): #temp range 2200 - 6500 https://www.reddit.com/r/wiz/comments/1ia3aiv/anyone_wish_it_could_go_warmer/
    payload = {
            "method": "setPilot",
            "params":{
                "temp" : temp,
            }
        }
    return payload
