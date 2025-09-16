# 代码生成时间: 2025-09-17 00:47:18
from celery import Celery
# 配置Celery
app = Celery('math_toolbox', broker='pyamqp://guest@localhost//')

# 配置Celery的时区
app.conf.timezone = 'UTC'

# 定义一个加法任务
@app.task
def add(x, y):
    """Add two numbers"""
    return x + y

# 定义一个减法任务
@app.task
def subtract(x, y):
    """Subtract one number from another"""
    return x - y

# 定义一个乘法任务
@app.task
def multiply(x, y):
    """Multiply two numbers"""
    return x * y

# 定义一个除法任务
@app.task
def divide(x, y):
    """Divide one number by another"""
    try:
        result = x / y
    except ZeroDivisionError:
        # 处理除法中的除数为零的情况
        raise ZeroDivisionError("Cannot divide by zero")
    return result

# 定义一个求幂运算任务
@app.task
def power(x, y):
    """Calculate the power of a number"""
    return x ** y

# 定义一个开方运算任务
@app.task
def square_root(x):
    """Calculate the square root of a number"""
    if x < 0:
        # 处理开方中的负数情况
        raise ValueError("Cannot calculate the square root of a negative number")
    return x ** 0.5

# 定义一个最大值任务
@app.task
def max_value(x, y):
    """Find the maximum of two numbers"""
    return max(x, y)

# 定义一个最小值任务
@app.task
def min_value(x, y):
    """Find the minimum of two numbers"""
    return min(x, y)

# 定义一个求绝对值任务
@app.task
def absolute_value(x):
    """Find the absolute value of a number"""
    return abs(x)

# 定义一个求阶乘任务
@app.task
def factorial(x):
    """Calculate the factorial of a number"""
    if x < 0:
        # 处理阶乘中的负数情况
        raise ValueError("Cannot calculate factorial of a negative number")
    if x == 0:
        return 1
    result = 1
    for i in range(1, x + 1):
        result *= i
    return result
