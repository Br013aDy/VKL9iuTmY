# 代码生成时间: 2025-08-27 06:28:51
import json
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from flask import Flask, request, jsonify

# Initialize Celery
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest:guest@localhost//'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# API Response Formatter Task
@celery.task(soft_time_limit=10)
def format_api_response(data, status_code, message):
    """Format API response with given data, status code and message."""
    try:
        # Assuming data is a dictionary to be converted into JSON response
        response = {
            'status_code': status_code,
            'message': message,
            'data': data
        }
        return jsonify(response)
    except Exception as e:
        # Handle unexpected errors during response formatting
        return jsonify({'error': str(e)}), 500

# Flask route to trigger API response formatting task
@app.route('/format_response', methods=['POST'])
def trigger_response_formatting():
    """Trigger the API response formatting task."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Extract status code and message from request arguments
    status_code = request.args.get('status_code', 200, type=int)
    message = request.args.get('message', 'Success', type=str)

    # Trigger the Celery task and return the result
    try:
        task = format_api_response.delay(data, status_code, message)
        result = task.get(timeout=5)  # Set a timeout for the task
        return result
    except SoftTimeLimitExceeded:
        return jsonify({'error': 'Task timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)