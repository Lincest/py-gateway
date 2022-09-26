from flask import Flask, jsonify, request, make_response
from flask_cors import *
import consul
import requests

consul_client = consul.Consul("127.0.0.1", 8500)


def create_app():
    app = Flask(__name__)
    CORS(app)  # 跨域

    @app.route('/')
    def index():
        return jsonify({"code": 1, "message": "gateway started successfully"})

    @app.route('/<service_name>/<path:api>', methods=['POST', 'GET', 'DELETE', 'PUT', 'PATCH'])
    def gateway_proxy(service_name, api):
        service = consul_client.agent.services().get(service_name)
        if service is None:
            return jsonify({"code": -1, "message": "service [{}] is not found".format(service_name)})
        service = '%s:%s' % (service.get('Address'), service.get('Port'))
        url = f"http://{service}/{api}"
        print('url = {}, method = {}'.format(url, request.method))
        try:
            headers = {k: v for k, v in request.headers.items()}
            response = None
            if request.method == 'GET':
                response = requests.get(url, params=request.args.to_dict(), headers=headers, data=request.get_data())
            elif request.method == 'POST':
                response = requests.post(url, params=request.args.to_dict(), headers=headers,
                                         data=request.get_data())
            elif request.method == 'PUT':
                response = requests.put(url, params=request.args.to_dict(), headers=headers,
                                        data=request.get_data())
            elif request.method == 'DELETE':
                response = requests.delete(url, params=request.args.to_dict(), headers=headers,
                                           data=request.get_data())
            elif request.method == 'PATCH':
                response = requests.patch(url, params=request.args.to_dict(), headers=headers,
                                          data=request.get_data())
            else:
                return jsonify({"code": -1, "message": "不支持的方法: " + request.method})
            result = make_response(response.content)
            result.headers = {k: v for k, v in response.headers.items()}
            return result
        except Exception as e:
            print('Exception: ', e)
            return jsonify({"code": -1, "message": "api: {} failed".format(url)})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5050)
