# 代码生成时间: 2025-08-19 21:11:32
import os
import signal
from celery import Celery
from celery.signals import worker_process_init

"""
A simple process manager using Python and Celery framework.
This module initializes a Celery app, sets up signal handlers for process management,
and uses Celery signals for initializing custom process behavior."""

# Initialize a Celery instance
app = Celery('process_manager',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://')

# Define a function to handle process initialization
def on_process_init(signal, frame):
    """
    Function to execute when a worker process is initialized.
    For demonstration purposes, we'll just print a message.
    This can be extended to include custom initialization logic.
    """
    print(f'Worker process {os.getpid()} initialized.')

# Hook the process initialization function into Celery's worker process init signal
worker_process_init.connect(on_process_init)

# Define a function to handle graceful shutdown
def graceful_shutdown(pid, sig, frame):
    """
    Function to execute when a graceful shutdown is requested.
    This function sends a SIGTERM to the process with the given PID.
    """
    try:
        os.kill(pid, signal.SIGTERM)
        print(f'Graceful shutdown requested for process {pid}.')
    except Exception as e:
        print(f'Error shutting down process {pid}: {e}')

# Set up signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Define a task that can be used to demonstrate the process manager
@app.task
def example_task():
    """
    Example Celery task that prints a message.
    This task can be expanded to perform actual work.
    """
    print('Example task executed.')

if __name__ == '__main__':
    # Start the Celery worker
    app.worker_main()