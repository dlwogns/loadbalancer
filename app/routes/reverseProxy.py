from flask import Blueprint, request, jsonify
import requests

bp = Blueprint('loadBalance', __name__)


# TODO move to Config
# parse with Configparser
backend_servers = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083"
]
current_server = 0

# round robin
def get_next_server():
    global current_server
    server = backend_servers[current_server]
    current_server = (current_server + 1) % len(backend_servers)
    return server


#Reverse Proxy
@bp.route('/<path:path>')
def loadBalance(path):
    backend_server = get_next_server()
    url = f"{backend_server}/{path}"
    
    try:
        if request.method == 'GET':
            response = requests.get(url, headers=request.headers, params=request.args)
        elif request.method == 'POST':
            response = requests.post(url, headers=request.headers, json=request.json)
        elif request.method == 'PUT':
            response = requests.put(url, headers=request.headers, json=request.json)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=request.headers)
        else:
            return jsonify({"error": "Method not supported"}), 405
        
        return (response.content, response.status_code, response.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    pass