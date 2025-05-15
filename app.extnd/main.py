
from elasticapm.contrib.flask import ElasticAPM


from flask import Flask, request, Response, jsonify, current_app

from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"*": {"origins": "localhost:3000"}},
            supports_credentials=True, origins=[
        "localhost:3000","localhost:8086",
        "http://localhost:3000"])

app.config['CORS_HEADERS'] = ['Content-Type',
                              'Access-Control-Allow-Origin', 'Access-Control-Allow-Credentials']
# app = Flask(__name__)
#load the APM agent configuration
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'sso-svc-extnd',
  'SECRET_TOKEN': 'J8Svf1qA0tM4cZ4pv1',
  'SERVER_URL': 'https://fef9fa1f77874d13bcad7d1f6972fa7d.apm.us-east-2.aws.elastic-cloud.com:443',
  'ENVIRONMENT': 'pilot',
}
apm = ElasticAPM(app)


cors.init_app(app=app)
@cross_origin()
@app.route("/v1/call-robot-false", methods=["GET", "POST"])
def test_failure():
    print(10/0)
    return jsonify({"message":"failure"}), 200


@cross_origin()
@app.route("/v1/call-robot", methods=["GET", "POST"])
def ping():
    return jsonify({"message":"success"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=False)
