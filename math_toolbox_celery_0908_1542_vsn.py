# 代码生成时间: 2025-09-08 15:42:10
import celery
import math
from celery import shared_task
from typing import Union

# 定义一个 Celery 配置
app = celery.Celery('math_toolbox', broker='pyamqp://guest@localhost//')


# 定义一个数学计算任务，异步执行加法运算
@shared_task
def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    try:
        result = a + b
        return result
    except Exception as e:
        raise ValueError(f"Error occurred during addition: {e}")


# 定义一个数学计算任务，异步执行减法运算
@shared_task
def subtract(a: float, b: float) -> float:
    """Subtract one number from another.

    Args:
        a (float): The first number.
        b (float): The number to subtract from the first.

    Returns:
        float: The difference between the two numbers.
    """
    try:
        result = a - b
        return result
    except Exception as e:
        raise ValueError(f"Error occurred during subtraction: {e}")


# 定义一个数学计算任务，异步执行乘法运算
@shared_task
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    try:
        result = a * b
        return result
    except Exception as e:
        raise ValueError(f"Error occurred during multiplication: {e}")


# 定义一个数学计算任务，异步执行除法运算
@shared_task
def divide(a: float, b: float) -> Union[float, str]:
    """Divide one number by another.

    Args:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The quotient if division is possible.
        str: Error message if division by zero occurs.
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Cannot divide by zero."
    except Exception as e:
        raise ValueError(f"Error occurred during division: {e}")


# 定义一个数学计算任务，异步计算一个数的平方根
@shared_task
def sqrt(a: float) -> Union[float, str]:
    """Calculate the square root of a number.

    Args:
        a (float): The number for which the square root is to be calculated.

    Returns:
        float: The square root of the number if it is non-negative.
        str: Error message if the number is negative.
    """
    try:
        if a < 0:
            return "Cannot calculate the square root of a negative number."
        result = math.sqrt(a)
        return result
    except Exception as e:
        raise ValueError(f"Error occurred during square root calculation: {e}")


# 定义一个数学计算任务，异步计算一个数的阶乘
@shared_task
def factorial(n: int) -> Union[int, str]:
    """Calculate the factorial of a number.

    Args:
        n (int): The number for which the factorial is to be calculated.

    Returns:
        int: The factorial of the number if it is non-negative.
        str: Error message if the number is negative.
    """
    try:
        if n < 0:
            return "Cannot calculate the factorial of a negative number."
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    except Exception as e:
        raise ValueError(f"Error occurred during factorial calculation: {e}")
