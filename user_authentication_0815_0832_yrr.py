# 代码生成时间: 2025-08-15 08:32:35
import celery
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import SoftTimeLimitExceeded

# 引入数据库操作相关库
from your_app.models import User
from your_app.exceptions import AuthenticationError
from django.core.mail import send_mail
from django.conf import settings

# 配置Celery
app = celery.Celery('tasks',
                 broker='pyamqp://guest@localhost//',
                 backend='rpc://')
app.conf.update(CELERY_BROKER_URL='pyamqp://guest@localhost//',
                CELERY_RESULT_BACKEND='rpc://')

logger = get_task_logger(__name__)

# 用户身份认证任务
@shared_task(bind=True, soft_time_limit=10)  # 设置任务超时时间为10秒
def authenticate_user(self, username, password):
    """
    用户身份认证的异步任务。
    
    :param self: Celery任务实例
    :param username: 用户名
    :param password: 用户密码
    :return: 认证结果
    """
    try:
        # 查询数据库中是否存在该用户
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户不存在时抛出AuthenticationError异常
        raise AuthenticationError("User not found.")
    except Exception as e:
        # 处理其他异常
        logger.error(f"Error: {e}")
        raise e

    # 校验密码是否正确
    if user.check_password(password):
        # 密码正确，返回成功消息
        return {"status": "success", "message": "User authenticated successfully."}
    else:
        # 密码错误，抛出AuthenticationError异常
        raise AuthenticationError("Invalid password.")

# 异常处理
class AuthenticationError(Exception):
    pass
