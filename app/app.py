import json
import re
from flask import Flask, jsonify
import requests
from lxml import etree
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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
