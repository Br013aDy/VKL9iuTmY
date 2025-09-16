# 代码生成时间: 2025-09-17 05:05:44
import psutil
import time
from celery import Celery

# 配置Celery
app = Celery('system_monitor', broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 系统性能监控任务
@app.task
def monitor_system_performance():
    """监控系统性能并打印结果。
    这个函数被设计为定期执行，用于监控CPU使用率、内存使用情况等。"""
    try:
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Used: {memory.used / (1024 ** 3)} GB")
        print(f"Disk Usage: {disk_usage.used / (1024 ** 3)} GB")
    except Exception as e:
        print(f"An error occurred: {e}")

# 定时任务设置
def schedule_monitoring(interval=60):
    """设置定时任务，每隔一定时间执行性能监控。
    参数interval是以秒为单位的时间间隔。"""
    monitor_system_performance.apply_async(countdown=interval)
    while True:
        time.sleep(interval)
        schedule_monitoring(interval)
        
# 程序入口
if __name__ == '__main__':
    try:
        # 启动定时监控任务
        schedule_monitoring()
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
