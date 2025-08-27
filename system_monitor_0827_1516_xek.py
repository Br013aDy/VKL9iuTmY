# 代码生成时间: 2025-08-27 15:16:51
import psutil
from celery import Celery
from celery.schedules import crontab
import os

# 定义Celery应用
app = Celery('system_monitor',
             broker='pyamqp://guest@localhost//')

app.conf.beat_schedule = {
    'monitor-system-every-minute': {
        'task': 'system_monitor.tasks.monitor',
        'schedule': crontab(),  # 每分钟执行一次
    },
}

# 定义监控任务
@app.task
def monitor():
    """监控系统性能，并记录日志"""
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取内存使用率
        memory_usage = psutil.virtual_memory().percent
        # 获取磁盘使用率
        disk_usage = psutil.disk_usage('/').percent

        # 打印监控结果
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")

        # 将监控结果记录到日志文件
        with open("system_monitor.log", "a") as f:
            f.write(f"{cpu_usage}%, {memory_usage}%, {disk_usage}%
")

    except Exception as e:
        # 错误处理
        print(f"Error occurred: {e}")

# 启动Celery Worker
if __name__ == '__main__':
    app.start()
