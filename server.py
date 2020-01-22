#!/usr/bin/env python

import urlparse
import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import classify_nsfw
from flask import Flask

 
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
    image = request.files['file']
    

if __name__ == '__main__':  
    app.run(host='0.0.0.0')