import re
from copy import deepcopy
import json

from pprint import pprint

from flask import Flask, request, jsonify, abort

app = Flask(__name__)


class OrderException(Exception): pass


def get_quote(order):
    try:
        value = 1.8 * order['nb_days'] * order['nb_travelers']
    except Exception:
        raise OrderException('invalid order %s' % order)

    quote = {'quote': value}
    return quote

@app.route("/", methods=['GET', 'POST'])
@app.route("/<path:path>", methods=['GET'])
def index2(path=''):
    return "hello world"

@app.route('/quote', methods=['POST'])
def quote():
    data = deepcopy(request.data)

    print 'POST data:'
    pprint(data)

    try:
        order = json.loads(data)
    except ValueError:
        abort(400)
    try:
        quote = get_quote(order)
    except OrderException, e:
        abort(400)

    return jsonify(quote)

@app.route('/feedback', methods=['POST'])
def feedback():
    # TODO: do something!
    return 'Thank you dude, you rule!'


@app.route("/", methods=['GET'])
@app.route("/<path:path>", methods=['GET'])
def test(path=''):
    return 'OK'
