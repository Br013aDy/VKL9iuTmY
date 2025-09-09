# 代码生成时间: 2025-09-09 21:41:40
import json
# 扩展功能模块
from celery import Celery
from celery import shared_task
# 扩展功能模块
from django.core.exceptions import ValidationError

# Celery configuration
# FIXME: 处理边界情况
app = Celery('form_data_validator')
# 改进用户体验
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define a decorator to handle task exceptions and return errors in JSON format
def handle_task_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
# NOTE: 重要实现细节
            return json.dumps({'error': str(e)})
    return wrapper

# Define a Celery task for form data validation
@shared_task(bind=True)
@handle_task_exceptions
def validate_form_data(self, data):
    '''
    Validate form data using Django's form validation system.
    :param self: Celery task instance
# 添加错误处理
    :param data: JSON string containing form data
    :return: JSON response indicating the validation result
    '''
    # Try to parse the JSON data
    try:
# 扩展功能模块
        data = json.loads(data)
    except json.JSONDecodeError as e:
        return json.dumps({'error': 'Invalid JSON data', 'details': str(e)})

    # Validate the form data
    for field, value in data.items():
        # Here you can add custom validation logic for each field
        # For demonstration, let's assume we only check if the value is not empty
        if not value:
            raise ValidationError(f'{field} cannot be empty')

    # If no validation errors were raised, return a success message
    return json.dumps({'message': 'Form data is valid'})

# Example usage:
# result = validate_form_data.delay(json.dumps({'name': 'John', 'age': '30'}))
# print(result.get())
