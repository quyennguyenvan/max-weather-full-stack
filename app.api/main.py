
from elasticapm.contrib.flask import ElasticAPM
import requests

from flask import Flask, request, Response, jsonify, current_app

import jwt
import json

from flask_cors import CORS, cross_origin

from app.authnz.authrz import UserLoginVerify
from functools import wraps
from app.appconfig import app
from helper.logger_config import logger


#this field also implementation at authrz.py
#just for dev testing only
SECRET_KEY = "fPQdwZzXkrD4AvFB68g4"

cors = CORS(app, resources={r"*": {"origins": "https://weathear-api.quyennv.com, http://localhost:3000, localhost:3000"}},
            supports_credentials=True, origins=[
        "https://weathear-api.quyennv.com",
        "localhost:3000",
        "http://localhost:3000"])

app.config['CORS_HEADERS'] = ['Content-Type',
                              'Access-Control-Allow-Origin', 'Access-Control-Allow-Credentials']
# app = Flask(__name__)
#load the APM agent configuration
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'sso-svc-prod',
  'SECRET_TOKEN': 'J8Svf1qA0tM4cZ4pv1',
  'SERVER_URL': 'https://fef9fa1f77874d13bcad7d1f6972fa7d.apm.us-east-2.aws.elastic-cloud.com:443',
  'ENVIRONMENT': 'pilot',
}
apm = ElasticAPM(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

cors.init_app(app=app)

def VerifyJWTToken(f):
    @ wraps(f)
    def decorated(*args, **kwargs):
    # return decorated
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if token is None:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            token = token.split(' ')[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'],options={"verify_signature": False})
            current_user = decoded_token['user_id']
            print(current_user)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)
    return decorated

@cross_origin()
@app.route("/v1/ping", methods=["GET", "POST"])
def ping():
    current_app.logger.info('ping')
    #call to external app - success call
    uri = "http://127.0.0.1:8087/v1/call-robot"
    response = requests.get(uri)
    return jsonify({"message":"success","version":"14", "response-ext": response.status_code}), 200

@cross_origin()
@app.route("/v1/damage", methods=["GET", "POST"])
def damage():
    current_app.logger.info('ping')
    #call to external app - success call
    uri = "http://127.0.0.1:8087/v1/call-robot-false"
    response = requests.get(uri)
    return jsonify({"message":"failure","version":"14"}), 200

@cross_origin()
@ app.route("/v1/login", methods=["GET", "POST"])
def login():
    req = request.json
    username = req.get('username', None)
    password = req.get('password', None)
    user_verify_result = UserLoginVerify.verify_user_account_access(username=username, password=password, SECRET_KEY=SECRET_KEY)
    if user_verify_result.get('code') == 1:
        return  jsonify(Data=user_verify_result),401
    return jsonify(Data=user_verify_result),200

@cross_origin
@ app.route("/v1/resources", methods=["GET"])
@ VerifyJWTToken
def resources_weather():
    return jsonify({"code": 0, "msg": "welcome to skynet"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086, debug=False)
