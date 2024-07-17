import requests
from config.celery_config import celery

backend_servers = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083"
]
current_server = 0

def get_next_server():
    global current_server
    server = backend_servers[current_server]
    current_server = (current_server + 1) % len(backend_servers)
    return server

@celery.task(bind=True)
def forward_request(self, request_data, method, path):
    backend_server = get_next_server()
    url = f"{backend_server}/{path}"
    headers = request_data['headers']
    data = request_data['data']
    params = request_data['params']
    
    try:
        timeout = 5
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=timeout)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=timeout)
        else:
            return {"error": "Method not supported"}, 405
        
        return response.content, response.status_code, dict(response.headers)
    except Exception as e:
        return {"error": str(e)}, 500
