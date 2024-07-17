from flask import Blueprint, request, jsonify
from tasks import forward_request
from celery.result import AsyncResult
import requests

bp = Blueprint('loadBalance', __name__)


@bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def load_balance(path):
    request_data = {
        'headers': dict(request.headers),
        'data': request.get_json() if request.method in ['POST', 'PUT'] else None,
        'params': request.args
    }
    method = request.method

    task = forward_request.delay(request_data, method, path)
    return jsonify({"task_id": task.id}), 202

@bp.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'status': 'Pending...'
        }
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'result': task_result.result
        }
    else:
        response = {
            'state': task_result.state,
            'status': str(task_result.info),  # this is the exception raised
        }
    return jsonify(response)