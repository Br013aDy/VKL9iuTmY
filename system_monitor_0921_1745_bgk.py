# 代码生成时间: 2025-09-21 17:45:14
import time
from celery import Celery
import psutil
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义Celery应用
app = Celery('system_monitor', broker='pyamqp://guest@localhost//')

@app.task
def monitor_system_performance():
    """
    监控系统性能，包括CPU使用率，内存使用率，磁盘使用率等。
    """
    try:
        # 收集CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        logger.info(f"CPU Usage: {cpu_usage}%")

        # 收集内存使用率
        mem = psutil.virtual_memory()
        mem_usage = mem.percent
        logger.info(f"Memory Usage: {mem_usage}%")

        # 收集磁盘使用率
        disk_usage = psutil.disk_usage('/')
        disk_usage_percent = disk_usage.percent
        logger.info(f"Disk Usage: {disk_usage_percent}%")

    except Exception as e:
        # 错误处理
        logger.error(f"Error monitoring system performance: {e}")

# 运行Celery worker
if __name__ == '__main__':
    app.start()
