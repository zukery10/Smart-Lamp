## Smart Lamp and Security system

A Raspberry Pi-based smart home system that combines motion-activated lighting, a wake-up alarm, a security mode with photo capture, and a web dashboard. It integrates with WiZ smart bulbs over UDP, Blynk for mobile control, Cloudinary for cloud image storage, and a Flask web interface for local monitoring.


 - GitHub Link : https://github.com/zukery10/Smart-Lamp
 - YouTube Demo Link : https://www.youtube.com/watch?v=QiUAdOl5ICw

 ## Screenshots

 - Laptop Dashboard
![Alt text](static/Laptopdash.png)

 - Mobile Dashboard
![Alt text](static/Mobiledash.png)

## Features

- Motion Activated Lighting : Detects movement via a camera and in a hard coded region of interest to turn off and on a Wiz smart bulb
- Security Mode : Detects intruders when activated. Captures image of intruder and logs movement
- Wake-Up Alarm : gradually brightens the lamp from 0–100% at a user-set time
- Temperature-Based Colour Temperature : reads temperature and humidity from the Sense HAT and adjusts bulb warmth accordingly
- Blynk Mobile control : Can control via the Blynk Mobile App
- Flask Web Interface : view the last captured visitor photo and a movement log


## File Structure
```
Smart-Lamp/
├── main.py                  # Main entry point and control loop
├── motion_sensor_v1.py      # Camera-based motion detection (OpenCV)
├── rules_engine.py          # Motion event logic, alarm, time checks
├── light_controller.py      # UDP communication with WiZ bulb
├── sense_reader.py          # Sense HAT temperature & humidity reader
├── pi_camera_capture.py     # Photo and video capture helpers
├── cloudinary_upload.py     # Cloudinary image upload
├── flask_web_api.py         # Flask web server and sunset API call
├── static/
│   ├── last_visitor.jpg     # Most recent captured visitor photo
│   └── movement_log.txt     # Timestamped movement event log
└── templates/
    └── index.html           # Web dashboard template
```
## Python Files

 - main.py:
    - Runs Blynk and Flask
    - Handles the motion detection return value and inputs into corresponding function
    - Handles input from Blynk for alarm and security mode
    - Logs all movement to .txt file
- motion_sensor_v1.py:
    - Uses OpenCV to detect motion within an ROI (region of interest)
    - Compares frames to static background frame and returns motion detection
    - Triggers when motion goes above 3000 pixels across two frames
    - Makes adaptive background
- rules_engine.py:
    - Decides whether to turn the light on/off or trigger security mode
    - Converts temperature and humidity into a Kelvin colour temperature value
    - Compares current time against a target
    - Returns brightness values stepping from 0 to 99 for the alarm
    - Returns alternating random colours for a flashing effect (Not used - but is a replacement for slow alarm)
- light_controller.py:
    - Sends commands to Wiz bulb
    - Receives light state
- sense_reader.py:
    - Captures temperature and humidity from the sense hat on the RPI
- pi_camera_capture.py:
    - Captures photo/video from PiCamera2 and saves image
- cloudinary_upload.py:
    - Uploads image to cloudinary
- flask_web_api.py:
    - Gets the sunset time from sunrise-sunset.org API
    - Serves the dashboard with the last visitor photo and the movement log

## Dependencies

- Ensure the following are pip installed:
    - flask (for web dashboard)
    - flask-cors (for web dashboard)
    - blynklib (for control)
    - cloudinary (to upload image)
    - picamera2 (for capturing image and motion detection)
    - sense-hat (for temperature and humidity)
    - opencv-python-headless (for motion detection)
    - numpy (for motion detection)
    - python-dotenv (for enviroment variables)
    - requests (for http request)

## Enviroment Variables

- Create a .env file in the root of the project and add : 

- BLYNK_AUTH_TOKEN=`YOUR BLYNK AUTH TOKEN`
- cloud_name= `YOUR CLOUDINARY NAME`
- cloud_api_key=`YOU CLOUDINARY API KEY`
- cloud_api_secret=`YOUR CLOUDINARY API SECRET`
- UDP_IP_PLUG = `YOUR BULB IP ADDRESS`

- Then add to .gitignore : `.env`


## Run Project

- In the bash script of the RPI
- Navigate to /Smart-Lamp
- Run : python main.py


## Notes

- The motion detection ROI is hardcoded to `x=700, y=20, w=200, h=120`. Adjust these values in motion_sensor_v1.py to match your camera angle.
- The sunset API call uses fixed coordinates for Waterford, Ireland. Update the "lat" and "lng" values in flask_web_api.py for a different location.
- The Cloudinary upload always overwrites the same image ID, so only the most recent visitor photo is stored in the cloud.

## References

https://github.com/UselessMnemonic/OpenWiz
- WiZ bulb UDP protocol reference

https://www.reddit.com/r/learnpython/comments/mz31yw/how_can_i_append_write_a_line_to_the_top_and/
- How to prepend new lines to the top of a text file

https://www.pythontutorial.net/python-basics/python-write-text-file/
- Writing to a text file in Python

https://www.programiz.com/python-programming/datetime/strftime
- Formatting datetime objects with strftime

https://www.youtube.com/watch?v=STEOavXqXqQ
- Running Flask in a background thread with threading

https://sunrise-sunset.org/api
- Sunset/sunrise time API reference

https://www.reddit.com/r/learnpython/comments/edbp0z/how_to_insert_a_variable_string_in_middle_of_url/
- Inserting variables into a URL string for API requests

https://www.geeksforgeeks.org/python/python-program-convert-time-12-hour-24-hour-format/
- Converting 12-hour time format to 24-hour format

https://stackoverflow.com/questions/40246702/displaying-a-txt-file-in-my-html-using-python-flask
- Displaying a text file's contents in a Flask HTML template

https://www.youtube.com/shorts/u53hez-dWn8
- Passing variables into Flask render_template

https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
- Python socket documentation for UDP communication

https://www.youtube.com/watch?v=wyoYbMRIAFE
- Sending UDP messages in Python

https://www.reddit.com/r/wiz/comments/1ia3aiv/anyone_wish_it_could_go_warmer/
- WiZ bulb colour temperature range (2200–6500K)

https://pip-assets.raspberrypi.com/categories/652-raspberry-pi-camera-module-2/documents/RP-008156-DS-2-picamera2-manual.pdf
- Picamera2 official manual

https://pixspy.com/
- Finding x,y pixel coordinates for the camera ROI

https://www.photopea.com/
- Online image editor used to help define ROI boundaries

https://forums.raspberrypi.com/viewtopic.php?t=363106#p2178171
- Capturing frames from Picamera2 as a numpy array

https://learnopencv.com/cropping-an-image-using-opencv/
- Cropping a region of interest from a frame using OpenCV

https://www.geeksforgeeks.org/python/python-grayscaling-of-images-using-opencv/
- Converting frames to grayscale with OpenCV

https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga6fef31bc8c4071cbc114a758a2b79c14
- OpenCV absdiff for comparing two frames

https://techskillguru.com/opencv/motion-detector-and-alert-system-in-opencv
- Thresholding and counting changed pixels for motion detection

https://numpy.org/devdocs/reference/generated/numpy.sum.html
- NumPy sum for counting motion pixels

https://www.w3schools.com/python/python_variables_global.asp
- Using global variables across functions in Python

https://www.w3schools.com/python/python_dictionaries.asp
- Returning and accessing Python dictionaries

https://stackoverflow.com/questions/12934699/selecting-fields-from-json-output
- Accessing specific fields from a JSON/dictionary response

https://www.reddit.com/r/Python/comments/486nl3/anyone_know_how_to_get_json_from_a_socket/
- Decoding JSON data received from a UDP socket