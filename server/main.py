from flask import Flask, jsonify, request, make_response
from flask_cors import *
import consul
import socket

PORT = 5051
CONSUL_PORT = 8500
HOST = '127.0.0.1'

app = Flask(__name__)
consul_client = consul.Consul(HOST, CONSUL_PORT)
CORS(app)  # 跨域


@app.route('/get-test', methods=['GET'])
def get_test():
    return jsonify({'msg': 'success', 'code': 1})


def register_service():
    cursor = consul.Consul(host=HOST, port=CONSUL_PORT, scheme='http')
    service_address = socket.gethostbyname(socket.gethostname())  # consul在docker中, 不可以使用localhost
    cursor.agent.service.register(
        name='gateway-test-server', address=service_address, port=PORT,
        check=consul.Check().tcp(host=service_address, port=PORT,
                                 interval='5s',
                                 timeout='30s', deregister='30s')
    )


if __name__ == '__main__':
    # 注册服务到consul
    register_service()
    app.run(host='0.0.0.0', port=PORT)
