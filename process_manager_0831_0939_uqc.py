# 代码生成时间: 2025-08-31 09:39:11
import os
import time
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery.signals import task_failure

# 配置Celery
app = Celery('process_manager', broker='pyamqp://guest@localhost//')

# 进程管理器任务
@app.task(bind=True, soft_time_limit=10)  # 设置软时间限制为10秒
def manage_process(self, command):
    """
    执行系统命令并管理进程。

    :param self: Celery任务实例
    :param command: 要执行的系统命令
    :return: 命令执行结果
    """
    try:
        # 执行系统命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 等待进程完成
        stdout, stderr = process.communicate()
        # 检查进程退出代码
        if process.returncode == 0:
            return {'status': 'success', 'output': stdout.decode('utf-8')}
        else:
            return {'status': 'error', 'error': stderr.decode('utf-8')}
    except SoftTimeLimitExceeded:
        return {'status': 'timeout', 'message': '任务执行超时'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

# 错误处理
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """
    任务失败时的回调函数。

    :param sender: 任务实例
    :param task_id: 任务ID
    :param exception: 异常信息
    """
    print(f'Task {task_id} failed: {exception}')

# 主函数
if __name__ == '__main__':
    # 启动Celery worker
    app.start()
