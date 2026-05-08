from picamera2 import Picamera2
import time, os
from picamera2.encoders import H264Encoder




#use os to set up base and static folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #get current directory
STATIC_DIR = os.path.join(BASE_DIR, "static") #set static directory path
os.makedirs(STATIC_DIR, exist_ok=True) #create static directory if it doesn't exist
IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg") #set image path



output = "lastVisitor.h264"
encoder = H264Encoder()
backgroundFrame = None


def capture_video(camera,filename="lastVisitor.h264", duration=2):
    print("Recording video...")
    camera.start_recording(encoder,output)
    time.sleep(duration)
    print("Stopped video...")
    camera.stop_recording()
    #camera.stop()
    
def capture_photo(camera,sense):
    print("Capturing visitor photo...")
    camera.capture_file(IMAGE_PATH)
    sense.clear(0, 255, 0)  # flash green
    #time.sleep(2)
    #sense.clear(0, 0, 0)
    print("Photo saved to:", IMAGE_PATH)