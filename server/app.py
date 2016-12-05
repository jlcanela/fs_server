import json
from datetime import datetime

from pprint import pprint

from flask import Flask, request, jsonify, abort

COVERS = {
    'basic': 1.8,
    'extra': 2.4,
    'premium': 4.2,
}
COUNTRIES = {
    'pl': 1.4,
}

app = Flask(__name__)


class OrderException(Exception): pass


def get_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def get_days(days):
    return 7 if days < 7 else days

def get_age_risks(ages):
    return 1

def get_quote(order):
    try:
        cover = COVERS[order['cover'].lower()]
        print 'cover:', cover
        country = COUNTRIES[order['country'].lower()]
        print 'country:', country

        delta = get_date(order['returnDate']) - get_date(order['departureDate'])
        days = get_days(delta.days)
        print 'nb days:', days

        ages_risk = get_age_risks(order['travellerAges'])
        print 'ages risk:', ages_risk

        value = cover * country * ages_risk * days
    except Exception, e:
        raise OrderException('invalid order %s: %s' % (order, str(e)))
    return {'quote': value}

# @app.route("/", methods=['GET', 'POST'])
# @app.route("/<path:path>", methods=['GET'])
# def index2(path=''):
#     return "hello world"

# @app.route('/quote', methods=['POST'])
# def quote():
#     # data = request.get_data()

#     # print 'POST data:'
#     # pprint(data)

#     # try:
#     #     order = json.loads(data)
#     # except ValueError, e:
#     #     print str(e)
#     #     abort(400)
#     try:
#         order = request.get_json()
#     except Exception, e:
#         print str(e)
#         abort(400)
#     try:
#         quote = get_quote(order)
#     except OrderException, e:
#         print str(e)
#         abort(400)

#     return jsonify(quote)

# @app.route('/feedback', methods=['POST'])
# def feedback():
#     # TODO: do something!
#     return 'Thank you dude, you rule!'




@app.route("/quote", methods=['POST'])
def quote():
    try:
        quote = request.get_json()
    except Exception, e:
        print str(e)

    print 'raw data:'
    pprint(quote)

    result = get_quote(quote)
    # result = {'total': 1000}
    return jsonify(result)

@app.route("/feedback", methods=['POST'])
def feedback():
    feedback = request.get_json()
    return jsonify(feedback)

@app.route("/", methods=['GET'])
@app.route("/<path:path>", methods=['GET'])
def index2(path=''):
    return "hello world"

@app.route("/ping", methods=['POST'])
def ping():
    return "pong"


@app.route("/", methods=['GET'])
@app.route("/<path:path>", methods=['GET'])
def test(path=''):
    return 'OK'
