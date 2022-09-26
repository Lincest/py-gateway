from flask import Flask, jsonify, request, make_response
from flask_cors import *
import consul

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
    cursor.agent.service.register(
        name='gateway-test-server', address=HOST, port=PORT,
        check=consul.Check().tcp(host=HOST, port=PORT,
                                 interval='5s',
                                 timeout='30s', deregister='30s')
    )


if __name__ == '__main__':
    # 注册服务到consul
    register_service()
    app.run(port=PORT)
