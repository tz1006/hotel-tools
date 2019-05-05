#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: flask.py

import json
from flask import Flask,render_template


app = Flask(__name__)

@app.route('/hyatt/<str:date>')
def index():
    path = 'data/%s' % date
    with open(path, 'r') as f:
        data = json.load(f)
    regular_pirce = data[0]
    cup_pirce = data[1]
    return render_template('template.html', date=date, regular_pirce=regular_pirce, cup_pirce=cup_pirce)



if __name__ == '__main__':
    app.run(debug=True)
