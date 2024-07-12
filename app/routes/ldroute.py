from flask import Blueprint

bp = Blueprint('loadBalance', __name__)

@bp.route('/<path:path>')
def loadBalance():
    pass