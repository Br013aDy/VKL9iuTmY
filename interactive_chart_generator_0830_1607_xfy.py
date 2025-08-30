# 代码生成时间: 2025-08-30 16:07:27
import os
import json
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from flask import Flask, request, render_template
from flask_celery import Celery

# Initialize Flask application
app = Flask(__name__)

# Configuration for Flask-Celery
app.config['CELERY_BROKER_URL'] = 'amqp://user:password@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define a task for generating interactive charts
@celery.task(name='generate_chart', bind=True)
def generate_chart(self, data, chart_type):
    """Generate an interactive chart based on provided data and chart type."""
    try:
        # Simulate chart generation with a time-consuming operation
        # Replace this with actual chart generation logic
        import time
        time.sleep(5)

        # Simulate chart generation result
        result = {
            'chart_type': chart_type,
            'data': data,
            'message': 'Chart generated successfully'
        }

        # Save the chart to a file (for demonstration purposes)
        chart_filename = f'{chart_type}_chart.png'
        with open(chart_filename, 'w') as f:
            f.write(json.dumps(result))

        return result
    except Exception as e:
        # Handle any exceptions that occur during chart generation
        self.retry(exc=e)

# Flask route to trigger chart generation
@app.route('/generate_chart', methods=['POST'])
def generate_chart_route():
    "