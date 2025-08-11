# 代码生成时间: 2025-08-11 14:14:49
import logging
from celery import Celery

# Configure the logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='error.log',
    filemode='a'
)

# Initialize Celery
app = Celery('error_logger',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

@app.task(bind=True)
def error_log_task(self, error_message):
    """
    A Celery task that logs errors to a file.

    :param self: The task instance
    :param error_message: The error message to be logged
    """
    try:
        # Attempt to log the error message
        logging.error(error_message)
        return f'Logged error: {error_message}'
    except Exception as e:
        # If logging fails, raise an exception
        raise self.retry(exc=e, countdown=60)

if __name__ == '__main__':
    # Manually start a worker if the script is run directly
    app.start()
