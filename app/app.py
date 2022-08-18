import json
import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
from flask_cors import CORS
from flask import Flask, request, send_file, make_response,jsonify
from flask_cors import cross_origin, CORS
from werkzeug.utils import secure_filename
import os
import io
import cv2
import numpy as np
from PIL import Image
from numpy import asarray
import base64


def segmentimg(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixel_vals = img.reshape((-1,3))
    pixel_vals = np.float32(pixel_vals)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)

    k = 5
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]

    segmented_image = segmented_data.reshape((img.shape))
    return segmented_image

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = set(['jpg','jpeg','JPG','JPEG'])
app.config['MAX_CONTENT_LENGTH'] = 256*256



@app.route("/atcoder", methods=['GET'])
def atcoder_contest():
    url = "https://atcoder.jp/contests/"
    response = requests.get(url)
    result = BeautifulSoup(response.content, 'html5lib')
    dom = etree.HTML(str(result))
    # data = dom.xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/div/div/table/tbody/tr[1]/td[2]/a')
    data = dom.xpath(
        '/html/body/div[1]/div/div[1]/div[3]/div[2]/div/div/table/tbody')
    res = []
    for tbody in data:
        for tr in tbody:
            ls = {}
            for i in range(0, 4):
                if i == 0:
                    for a in tr[i]:
                        for time in a:
                            ls['start'] = time.text
                if i == 1:
                    for a in tr[i]:
                        ls['name'] = a.text
            res.append(ls)
    return jsonify(res)


@app.route("/uploadimg", methods = ['GET', 'POST'])
def uploadimg():

    if request.method == 'POST':

        if 'file' not in request.files:
            return {"status":"No file selected","data":""}

        file = request.files['file']

        if file.filename == '':
            return {"status":"No file selected","data":""}

        ext = file.filename.split('.')
        ext = ext[len(ext)-1]

        if ext not in ALLOWED_EXTENSIONS:
            return {"status":"Only JPG is allowed","data":""}
        
        img = Image.open(file.stream)
        img = asarray(img)
        file2 = segmentimg(img)
        fil2img = Image.fromarray(file2)
        output = io.BytesIO()
        fil2img.save(output,format="JPEG")
        output.seek(0)
        data = output.read()
        data = base64.b64encode(data).decode()
        return f'{data}'
    
    if request.method == 'GET':
        return {"status":"Hi from Harsh"}
    
