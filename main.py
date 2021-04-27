""" Screen sharing application with python -Flask

  author: ashaf minhaj
  mail  : ashraf_minhaj@yahoo.com
"""

""" install -
$ pip install flask
$ pip install opencv-contrib-python
$ pip install numpy
$ pip install pillow
$ pip install win32api (should come built in)
"""

from flask import Flask, Response
import cv2
from PIL import ImageGrab
import numpy as np 
from win32api import GetSystemMetrics

# get screen size
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

app = Flask(__name__)

@app.route('/')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while 1:
        # get full screen frame
        img = ImageGrab.grab(bbox=(0, 0, width, height))      # bbox - region - (x, y, width, height)
        img_np = np.array(img)                                # convert image into an array
        final_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)   # convert image - BGR to RGb
        
        frame = cv2.imencode('.jpg', final_img)[1].tobytes()  # encode image
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
# to view this link from other deices-
# we need to enable TCP traffic for port 5000
#  in our local network.
# Make sure windows firewall is not requesting our request.
app.run(port = 5000, debug=True)