# 代码生成时间: 2025-09-01 06:26:03
import json
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError

# 设置Celery
app = Celery('form_validator',
             broker='pyamqp://guest@localhost//')

# 表单验证函数
def validate_form(data):
    """
    验证表单数据。
    
    参数:
    data (dict): 表单数据。
    
    返回:
    tuple: (bool, str) 验证结果和错误信息。
    """
    errors = []
    
    # 检查是否提供了所有必需的字段
    required_fields = ['name', 'email', 'age']
    for field in required_fields:
        if field not in data:
            errors.append(f'Missing field: {field}')
            continue
        
    # 验证字段内容
    if 'name' in data and not data['name'].strip():
        errors.append('Name cannot be empty.')
    if 'email' in data and '@' not in data['email']:
        errors.append('Invalid email format.')
    if 'age' in data and (not isinstance(data['age'], int) or data['age'] < 0):
        errors.append('Age must be a non-negative integer.')
    
    if errors:
        return False, ', '.join(errors)
    return True, ''

# Celery任务函数
@app.task
def validate_form_task(data):
    """
    一个异步任务，用于验证表单数据。
    
    参数:
    data (dict): 表单数据。
    
    返回:
    str: JSON字符串，包含验证结果。
    """
    try:
        result, error_message = validate_form(data)
        return json.dumps({'success': result, 'message': error_message})
    except Exception as e:
        return json.dumps({'success': False, 'message': str(e)})

# 测试表单数据
if __name__ == '__main__':
    test_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'age': 30
    }
    
    # 同步调用验证函数
    success, message = validate_form(test_data)
    print(f'Sync result: {success}, {message}')
    
    # 异步调用验证函数
    result = validate_form_task.delay(test_data)
    try:
        # 等待异步任务完成
        async_result = result.get(timeout=10)
        print(f'Async result: {async_result}')
    except TimeoutError:
        print('Task timed out.')
    except Exception as e:
        print(f'An error occurred: {e}')