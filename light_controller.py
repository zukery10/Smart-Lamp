import socket
import time
import json

#https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
#https://www.youtube.com/watch?v=wyoYbMRIAFE

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
    message = sock.recvfrom(1024)
    return message
   



def lightState(payload):
    
    UDP_IP_PLUG = "192.168.2.182"  # Plug IP
    UDP_PORT = 38899 # Port it uses from the Github ref
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # opens a new socket
    message = str(json.dumps(payload))
    message = message.encode('utf-8')
    sock.sendto(message,(UDP_IP_PLUG,UDP_PORT))
    time.sleep(.3)
    print(message)
