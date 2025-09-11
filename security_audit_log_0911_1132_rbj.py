# 代码生成时间: 2025-09-11 11:32:36
import logging
import os
from celery import Celery
from celery.signals import task_prerun, task_postrun
from celery.utils.log import get_task_logger

# 配置日志
logging.basicConfig(filename='security_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Celery配置
app = Celery('security_audit',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 获取任务日志器
task_logger = get_task_logger(__name__)

# 任务前置运行信号
@task_prerun.connect
def prerun_task(task_id, task, *args, **kwargs):
    """记录任务前置运行信息到安全审计日志中。"""
    task_logger.info(f'Task {task.name} started with id {task_id}')

# 任务后置运行信号
@task_postrun.connect
def postrun_task(task_id, task, *args, **kwargs, state):
    """记录任务后置运行信息到安全审计日志中。"""
    if state == 'FAILURE':
        task_logger.error(f'Task {task.name} failed with id {task_id}')
    else:
        task_logger.info(f'Task {task.name} completed with id {task_id}')

# 示例任务
@app.task
def example_task(data):
    """示例任务，执行一些操作并记录安全审计日志。"""
    try:
        # 模拟一些操作
        result = data.upper()
        logger.info(f'Task processed data: {data}')
        return result
    except Exception as e:
        logger.error(f'Error processing task: {e}')
        raise

if __name__ == '__main__':
    # 运行worker
    app.start()