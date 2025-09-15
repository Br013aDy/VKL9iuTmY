# 代码生成时间: 2025-09-15 20:48:58
# process_manager.py

"""
进程管理器，使用CELERY框架实现进程的监控和管理。
"""

import os
import psutil
from celery import Celery
from celery.signals import worker_process_init

app = Celery('process_manager',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')
app.config_from_object('celeryconfig')


# 定义一个字典，用于存储进程信息
process_pool = {}


# 定义一个信号处理器，用于初始化进程池
@worker_process_init.connect
def init_process_pool(**kwargs):
    """
    当CELERY工作进程初始化时，执行此函数。
    """
    process_pool.clear()  # 清空进程池
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_pool[proc.info['pid']] = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# 定义一个CELERY任务，用于获取当前进程列表
@app.task
def get_process_list():
    """
    获取当前进程列表。
    """
    return process_pool.copy()


# 定义一个CELERY任务，用于启动一个进程
@app.task(bind=True)
def start_process(self, command):
    """
    启动一个进程。
    
    参数:
    command -- 要启动的进程的命令行字符串。
    
    返回:
    进程的PID。
    """
    try:
        pid = os.fork()
        if pid == 0:
            # 子进程
            os.execvp(command, command.split())
        else:
            # 父进程
            return pid
    except Exception as e:
        self.retry(exc=e)


# 定义一个CELERY任务，用于终止一个进程
@app.task(bind=True)
def terminate_process(self, pid):
    """
    终止一个进程。
    
    参数:
    pid -- 要终止的进程的PID。
    
    返回:
    True如果进程被成功终止，否则False。
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False
    except Exception as e:
        self.retry(exc=e)


# 定义一个CELERY任务，用于重启一个进程
@app.task(bind=True)
def restart_process(self, pid):
    """
    重启一个进程。
    
    参数:
    pid -- 要重启的进程的PID。
    """
    try:
        self.terminate_process(pid)
        self.start_process(process_pool[pid])
    except Exception as e:
        self.retry(exc=e)



# 以下是一个示例任务，用于演示如何使用进程管理器
@app.task
def example_task():
    """
    一个示例任务，演示如何使用进程管理器。
    """
    print("获取进程列表：")
    process_list = get_process_list().get()
    print(process_list)

    print("启动一个新的进程：")
    pid = start_process("ping localhost").get()
    print("新进程的PID：", pid)

    print("终止进程：")
    if terminate_process(pid).get():
        print("进程被成功终止")
    else:
        print("进程终止失败")

    print("重启进程：")
    restart_process(pid).get()
    print("进程被重启")


if __name__ == '__main__':
    app.start()
