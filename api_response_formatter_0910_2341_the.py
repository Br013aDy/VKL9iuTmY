# 代码生成时间: 2025-09-10 23:41:06
import json
from celery import Celery
from celery.result import AsyncResult
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置Celery
app = Celery('api_response_formatter',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')


# 任务函数，用于格式化API响应
@app.task
def format_api_response(data, status_code, message):
    """
    格式化API响应的函数。
    
    参数:
    data (dict): 要格式化的数据。
    status_code (int): HTTP状态码。
    message (str): 操作结果的消息。
    
    返回:
    dict: 格式化后的API响应。
    
    异常:
    ValueError: 如果status_code不是有效的HTTP状态码。
    """
    if not isinstance(data, dict):
        raise ValueError("data必须是字典类型")
    
    if not isinstance(status_code, int) or status_code < 100 or status_code > 599:
        raise ValueError("status_code必须是有效的HTTP状态码")
    
    if not isinstance(message, str):
        raise ValueError("message必须是字符串类型")
    
    # 构建API响应格式
    response = {
        'status': status_code,
        'message': message,
        'data': data
    }
    return response


# 异步执行示例
if __name__ == '__main__':
    # 测试数据和状态码
    test_data = {'key': 'value'}
    test_status_code = 200
    test_message = '操作成功'
    
    # 异步执行任务
    task = format_api_response.delay(test_data, test_status_code, test_message)
    
    # 获取结果
    try:
        result = task.get(timeout=10)
        logger.info(f"格式化后的API响应: {json.dumps(result, indent=4)}")
    except Exception as e:
        logger.error(f"任务执行失败: {str(e)}")