# 代码生成时间: 2025-08-14 15:00:47
# network_status_checker_with_celery.py

import os
import socket
from celery import Celery

# Set up the Celery app
app = Celery('network_status_checker',
             broker=os.environ.get('CELERY_BROKER_URL', 'amqp://localhost//'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'rpc://'))

# Define a task to check network connection status
@app.task
# TODO: 优化性能
def check_connection(host, port):
    