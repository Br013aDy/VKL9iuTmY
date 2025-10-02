# 代码生成时间: 2025-10-02 18:24:46
from celery import Celery

"""
Math Toolbox is a Celery-based application designed to perform various mathematical operations.
It provides a set of tasks for calculations such as addition, subtraction, multiplication, and division.
"""

# Initialize Celery app with a broker
app = Celery('mtoolbox', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    """Add two numbers and return the result."""
    try:
        return x + y
    except TypeError:
        raise ValueError("Both arguments must be numbers.")

@app.task
def subtract(x, y):
    """Subtract two numbers and return the result."""
    try:
        return x - y
    except TypeError:
        raise ValueError("Both arguments must be numbers.")

@app.task
def multiply(x, y):
    """Multiply two numbers and return the result."""
    try:
        return x * y
    except TypeError:
        raise ValueError("Both arguments must be numbers.")

@app.task
def divide(x, y):
    """Divide two numbers and return the result."""
    try:
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y
    except TypeError:
        raise ValueError("Both arguments must be numbers.")
    except ZeroDivisionError as e:
        raise ZeroDivisionError(e)

"""
Additional mathematical tasks can be added following the same pattern,
ensuring they are decorated with @app.task and include proper error handling.
"""