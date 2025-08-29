# 代码生成时间: 2025-08-29 19:05:07
import celery
from celery import shared_task
from celery import Celery
from math import *
from operator import *
import sys

# 定义Celery应用
app = Celery('math_calculator',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
)

# 数学计算工具集任务
@shared_task
def add(x, y):
    """
    加法计算
    :param x: 第一个加数
    :param y: 第二个加数
    :return: 两个数的和
    """
    try:
        result = x + y
        return result
    except Exception as e:
        raise ValueError(f"Addition error: {str(e)}")

@shared_task
def subtract(x, y):
    """
    减法计算
    :param x: 被减数
    :param y: 减数
    :return: 两个数的差
    """
    try:
        result = x - y
        return result
    except Exception as e:
        raise ValueError(f"Subtraction error: {str(e)}")

@shared_task
def multiply(x, y):
    """
    乘法计算
    :param x: 乘数
    :param y: 被乘数
    :return: 两个数的积
    """
    try:
        result = x * y
        return result
    except Exception as e:
        raise ValueError(f"Multiplication error: {str(e)}")

@shared_task
def divide(x, y):
    """
    除法计算
    :param x: 被除数
    :param y: 除数
    :return: 两个数的商
    :raises ValueError: 如果除数为0
    """
    if y == 0:
        raise ValueError("Cannot divide by zero")
    try:
        result = x / y
        return result
    except Exception as e:
        raise ValueError(f"Division error: {str(e)}")

@shared_task
def power(x, y):
    """
    幂运算
    :param x: 底数
    :param y: 指数
    :return: 幂运算结果
    """
    try:
        result = x ** y
        return result
    except Exception as e:
        raise ValueError(f"Power calculation error: {str(e)}")

@shared_task
def sqrt(x):
    """
    平方根计算
    :param x: 被开方数
    :return: 平方根结果
    :raises ValueError: 如果被开方数为负数
    """
    if x < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    try:
        result = sqrt(x)
        return result
    except Exception as e:
        raise ValueError(f"Square root calculation error: {str(e)}")

if __name__ == '__main__':
    # 启动Celery worker
    app.start()
