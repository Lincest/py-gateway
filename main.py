from flask import Flask, jsonify, request, make_response
from flask_cors import *
import consul
import requests

app = Flask(__name__)
consul_client = consul.Consul("127.0.0.1", 8500)
CORS(app)  # 跨域


@app.route('/')
def index():
    return jsonify({"code": 1, "message": "gateway started successfully"})


@app.route('/<service_name>/<path:api>', methods=['POST', 'GET', 'DELETE', 'PUT'])
def gateway_proxy(service_name, api):
    service = consul_client.agent.services().get(service_name)
    if service is None:
        return jsonify({"code": -1, "message": "service [{}] is not found".format(service_name)})
    service = '%s:%s' % (service.get('Address'), service.get('Port'))
    try:
        result = None
        url = f"http://{service}/{api}"
        print('url = ', url)
        print('headers = ', request.headers)
        headers = {}
        for k, v in request.headers:
            headers[k] = v
        print('args = ', request.args)
        print('json = ', request.get_json(silent=True))
        if request.method == 'GET':
            response = requests.get(url, params=request.args.to_dict(), headers=headers)
            content = response.content
            resp_headers = response.headers
            result = make_response(content)
            for k, v in resp_headers:
                result.headers[k] = v
        return result, 200
    except Exception as e:
        print('Exception: ', e)
        return jsonify({"code": -1, "message": "api: {} failed".format(url)})


if __name__ == '__main__':
    app.run(port=5050)
