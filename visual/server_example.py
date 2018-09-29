#!flask/bin/python

import json
import random
import sys

from flask import Flask, Response, redirect, render_template, request

app = Flask(__name__)


@app.route('/')
def output():
    # serve index template
    return render_template('index.html', name='Joe')


@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json(force=True)
    print data
    result = ''

    for item in data:
        # loop over every row
        result += str(item['make']) + '\n'

    return result


if __name__ == '__main__':
    # run!
    app.run()
