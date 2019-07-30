'''

Runs the Flask App and Holds the Routes.

'''

from __future__ import division
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import Response
from flask import jsonify
import simplejson as json
import threading
import boto3
import boto
import os
from random import randint
import random
from datetime import datetime
import time
from quantex import Quantex, WIN, DRAW, LOSS
from decimal import *
import db_interfacing
import core_manager
import configureEnvs
import sys
sys.path.append('/home/ec2-user/.local/lib/python2.7/site-packages')
from jose import jwt, jwk
from jose.utils import base64url_decode
from constants import REFERRAL_DISCOUNT

application = app = Flask(__name__)

DEV_ENV = "DEV_ENV"
PROD_ENV = "PROD_ENV"
ENV = DEV_ENV

CORS_ORIGIN_DEV = '*'
CORS_HEADER_DEV = '*'
CORS_ORIGIN_PROD = 'https://symbol.co'
CORS_HEADER_PROD = '*, SYMBOL-HEADER, origin, x-requested-with, content-type, accept, Access-Control-Allow-Origin'

CORS_ORIGIN = CORS_ORIGIN_DEV if ENV == DEV_ENV else CORS_ORIGIN_PROD
CORS_HEADER = CORS_HEADER_DEV if ENV == DEV_ENV else CORS_HEADER_PROD

# @app.after_request
# def set_cors_header(response):
#     r = request.referrer[:-1]
#     allowedOrigins = ['https://symbol.co','https://staging.symbol.co', 'http://localhost:3000/']
#     print("setting cors header, checking if ", r)
#     if r in allowedOrigins:
#         print("just set cors header")
#         CORS_ORIGIN = r


def sendOptionsHeaders():
    resp = Response("options")
    resp.headers['Access-Control-Allow-Origin'] = CORS_ORIGIN
    resp.headers['Access-Control-Allow-Headers'] = CORS_HEADER
    return resp


def sendResponse(response):
    return jsonify(response), 201, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': CORS_ORIGIN, 'Access-Control-Allow-Headers': CORS_HEADER}


@app.route('/changeCardData', methods=['POST', 'OPTIONS'])
def changeCardData():
    if (request.method == "OPTIONS"):
        return sendOptionsHeaders()

    userId = request.form["userId"]
    jwtToken = request.form["jwtToken"]
    stripeToken = request.form["stripeToken"]
    print("My Stripe Token " + stripeToken)

    validation = validateToken(jwtToken, userId)
    # check that the user is who they say they are
    if validation is False:
        print("bad validation")
        response = {"status": "error", "message": "invalid jwt token"}
        return sendResponse(response)

    response = core_manager.changeCardData(userId, stripeToken)
    print(response)
    return sendResponse(response)


# Non - REST API Functions


if __name__ == "__main__":
    configureEnvs.setEnvironmentVars()
    # resetProjectReviews()
    # configureEnvs.printEnvironmentVars()
    # printProjectsRanking()

    app.run(host="0.0.0.0", port=80)
