# 代码生成时间: 2025-10-11 02:01:24
import celery
from celery import Celery
from celery.exceptions import Reject
from kombu import Queue, Exchange

# 定义配置参数
BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "rpc://"

# 定义通知队列
EXCHANGE = 'notification_exchange'
QUEUE = 'notification_queue'
ROUTING_KEY = 'notification_key'

app = Celery('notification_system',
             broker=BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['tasks'])

# 配置队列
app.conf.task_queues = (Queue(QUEUE, Exchange(EXCHANGE, type='direct'), routing_key=ROUTING_KEY),)
app.conf.task_always_eager = True  # 开发环境使用

# 定义通知任务
@app.task(bind=True, autoretry=True, retry_kwargs={'max_retries': 3})
def send_notification(self, message):
    """
    发送通知消息的任务

    :param self: Celery任务实例
    :param message: 通知消息内容
    :return: None
    """
    try:
        # 模拟发送通知
        print(f"Sending notification: {message}")
        # 这里可以添加实际的通知发送代码，例如邮件、短信等
    except Exception as e:
        # 错误处理
        print(f"Failed to send notification: {e}")
        raise Reject("Notification failed", requeue=True)

# 示例任务
@app.task
def test_notification():
    """
    测试通知任务

    :return: None
    """
    send_notification.delay("Test notification message")

if __name__ == '__main__':
    # 启动Celery worker
    app.worker_main()