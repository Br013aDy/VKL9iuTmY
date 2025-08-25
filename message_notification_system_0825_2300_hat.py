# 代码生成时间: 2025-08-25 23:00:25
import os
from celery import Celery
from celery.signals import worker_ready

# 设置Celery的配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('message_notification')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 定义一个任务，用于发送消息通知
@app.task
def send_notification(message, recipient):
    """
    发送消息通知给指定的接收者。
    
    :param message: 要发送的消息内容
    :param recipient: 接收消息的接收者（可以是邮箱、手机号等）
    """
    try:
        # 这里模拟发送消息的过程
        print(f"Sending message to {recipient}: {message}")
        # 实际应用中，这里可以是发送邮件、短信等操作
        # 例如：send_email.delay(message, recipient)
    except Exception as e:
        # 处理可能发生的错误
        print(f"Error sending message to {recipient}: {e}")


# 消息通知系统的启动器
if __name__ == '__main__':
    # 设置Celery的Beat定时器
    app.conf.beat_schedule = {
        'send_daily_notifications': {
            'task': 'send_notification',
            'schedule': 60.0,  # 每分钟执行一次
            'args': ('Daily update: Check your tasks!', 'example@example.com')
        },
    }
    
    # 启动Celery Worker
    app.start()
