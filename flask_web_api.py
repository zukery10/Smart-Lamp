from flask import Flask
import requests
from flask_cors import CORS
from datetime import datetime
import json,os



BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #get current directory
STATIC_DIR = os.path.join(BASE_DIR, "static") #set static directory path
IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg") #set image path

#https://sunrise-sunset.org/api
app = Flask(__name__)
CORS(app)
@app.route('/sunset', methods=['GET'])
def sunset_time():
    params = {"lng": -7, "lat": 52, 'tzid': "Europe/Dublin" }
    #Input a variable into url - https://www.reddit.com/r/learnpython/comments/edbp0z/how_to_insert_a_variable_string_in_middle_of_url/

    response = requests.get("https://api.sunrise-sunset.org/json?",params=params)
    data = response.json()
    response = json.dumps(data, indent=2)
    response = json.loads(response)
    #r = request.endpoint("https://api.sunrise-sunset.org/json?"+lng+"&"+lat)
    t = response['results']['sunset']
    t = datetime.strptime(t, '%I:%M:%S %p' ) # convert 12 to 24 hour
    #https://www.geeksforgeeks.org/python/python-program-convert-time-12-hour-24-hour-format/
    t = t.strftime('%H:%M:%S')
    
    return t



def upload_image():

    url = "http://127.0.0.1:5000"

    files = {
        "media": open("static/last_visitor.jpg", "rb")
    }

    response = requests.post(url, files=files)

    print(response.json())



upload_image()
