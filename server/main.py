from flask import Flask, jsonify, request, make_response
from flask_cors import *
import consul
import socket

PORT = 5051
CONSUL_PORT = 8500
HOST = '127.0.0.1'
consul_client = consul.Consul(HOST, CONSUL_PORT)


def create_app():
    app = Flask(__name__)
    CORS(app)  # 跨域

    @app.route('/get-test', methods=['GET'])
    def get_test():
        return jsonify({'msg': 'success', 'code': 1})

    @app.route('/get-test-params', methods=['GET'])
    def get_test_with_params():
        params = request.args.to_dict()
        return jsonify({'msg': 'success', 'code': 1, 'json': params})

    @app.route('/post-test', methods=['POST'])
    def post_test():
        body = request.json
        print('body = ', body)
        return jsonify({'msg': 'success', 'code': 1, 'json': body})

    @app.route('/post-test-form', methods=['POST'])
    def post_test_form():
        body = request.form
        print('body = ', body)
        return jsonify({'msg': 'success', 'code': 1, 'json': body})

    @app.route('/patch/<patch_id>', methods=['PATCH'])
    def patch_test(patch_id):
        return jsonify({'msg': 'success', 'code': 1, 'patch': patch_id})

    @app.route('/other-methods', methods=['PUT', 'DELETE', 'PATCH'])
    def other_test():
        body = request.json
        print('body = ', body)
        return jsonify({'msg': 'success', 'code': 1, 'json': body})

    return app


def register_service():
    cursor = consul.Consul(host=HOST, port=CONSUL_PORT, scheme='http')
    service_address = get_host_ip()  # a better way to get ip
    cursor.agent.service.register(
        name='gateway-test-server', address=service_address, port=PORT,
        check=consul.Check().tcp(host=service_address, port=PORT,
                                 interval='5s',
                                 timeout='30s', deregister='30s')
    )


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    # 注册服务到consul
    app = create_app()
    register_service()
    app.run(host='0.0.0.0', port=PORT)
