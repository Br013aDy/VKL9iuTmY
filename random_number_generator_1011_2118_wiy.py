# 代码生成时间: 2025-10-11 21:18:44
import celery
from celery import shared_task
import random

# 配置Celery
app = celery.Celery('tasks',
                   broker='amqp://guest@localhost//')

@app.task(name='generate_random_number')
def generate_random_number(min_value, max_value):
    """
    异步任务用于生成一个介于min_value和max_value之间的随机整数。
    
    参数:
    min_value (int): 随机数的最小值
    max_value (int): 随机数的最大值
    
    返回值:
    random_number (int): 一个随机生成的整数
    """
    # 检查输入值是否合法
    if not isinstance(min_value, int) or not isinstance(max_value, int):
        raise ValueError("Both min_value and max_value must be integers.")
    if min_value >= max_value:
        raise ValueError("max_value must be greater than min_value.")
    
    # 生成随机数
    random_number = random.randint(min_value, max_value)
    return random_number

# 以下代码用于启动Celery worker，实际部署时应运行Celery worker进程
# if __name__ == '__main__':
#     app.start()