from celery import Celery

def make_celery(app_name=__name__):
    backend = 'redis://127.0.0.1:6379/0'
    broker = 'redis://127.0.0.1:6379/0'
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()
