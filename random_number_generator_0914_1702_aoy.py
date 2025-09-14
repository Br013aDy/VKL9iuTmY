# 代码生成时间: 2025-09-14 17:02:28
# random_number_generator.py

"""
A simple random number generator using Celery framework.
"""

from celery import Celery
import random

# Configuration for Celery
app = Celery('random_number_generator',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

@app.task
def generate_random_number() -> int:
    '''
    Generates a random integer between 1 and 100.
    
    Returns:
        int: A random number between 1 and 100.
    '''
    try:
        # Generate a random number between 1 and 100
        number = random.randint(1, 100)
        return number
    except Exception as e:
        # In case of any error, print the error message and re-raise the exception
        print(f'An error occurred: {e}')
        raise