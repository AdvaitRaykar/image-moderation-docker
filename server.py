#!/usr/bin/env python

import urlparse
import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import classify_nsfw
from flask import Flask
from flask import request
import StringIO
from PIL import Image
import base64
import cStringIO
 
app = Flask(__name__) 
  

@app.route('/url/<path:url>', methods=['GET']) 
def parse_from_url(url):
    print(url)
    try:
        message = classify_nsfw.get_score(url)
    except Exception as e:
        logging.exception("ok")
        message = "exception: " + e.message

    return str(message)

@app.route('/image', methods=['POST'])
def parse_from_image():
    image = request.files['file'].stream
    buffer = cStringIO.StringIO()
    # image.save(buffer, format="JPEG")
    # img_str = base64.b64encode(buffer.getvalue())
    message = classify_nsfw.get_score_from_image(image.read())
    # classify_nsfw.resize_image(image.read())
    # message = 'test'
    return str(message)    

if __name__ == '__main__':  
    app.run(host='0.0.0.0')