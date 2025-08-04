# 代码生成时间: 2025-08-05 07:44:05
import celery
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义Celery应用
app = Celery('scheduled_task_scheduler',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 定义一个周期性任务，每10秒执行一次
@periodic_task(run_every=crontab(minute='*/10'))
def my_periodic_task():
    """周期性执行的任务"""
    try:
        # 在这里可以添加需要周期性执行的代码
        logger.info('Periodic task executed.')
    except Exception as e:
        logger.error(f'Error executing periodic task: {e}')

# 启动Celery Worker
if __name__ == '__main__':
    logger.info('Starting Celery worker...')
    app.start()
