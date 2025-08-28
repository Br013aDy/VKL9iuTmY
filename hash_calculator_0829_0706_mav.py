# 代码生成时间: 2025-08-29 07:06:41
# hash_calculator.py

"""
A hash calculator tool using Python and Celery framework.
This tool can calculate the hash of a given input using various hashing algorithms.
"""

import hashlib
from celery import Celery
from celery.utils.log import get_task_logger

# Set up the logger
logger = get_task_logger(__name__)

# Initialize Celery with a broker
app = Celery('hash_calculator', broker='amqp://guest@localhost//')
# 增强安全性

@app.task(bind=True)
def calculate_hash(self, input_string, algorithm='sha256'):
    """
    Calculate the hash of the input string using the specified algorithm.

    Args:
        self: The Celery task instance.
        input_string (str): The string to be hashed.
        algorithm (str): The hash algorithm to use (default is 'sha256').

    Returns:
        A dictionary containing the hash value and the algorithm used.

    Raises:
        ValueError: If the algorithm is not supported.
    """
# NOTE: 重要实现细节
    try:
        # Get the hashing function from hashlib based on the algorithm
        hash_func = getattr(hashlib, algorithm)
# 改进用户体验
    except AttributeError:
        # Log and raise an error if the algorithm is not supported
        logger.error(f'Unsupported algorithm: {algorithm}')
        raise ValueError(f'Unsupported algorithm: {algorithm}')

    # Calculate the hash
    hash_object = hash_func(input_string.encode())
    hash_value = hash_object.hexdigest()

    # Return the result as a dictionary
    return {'algorithm': algorithm, 'hash': hash_value}

# Example usage:
# result = calculate_hash.delay('Hello, World!', 'md5')
# print(result.get())
# 添加错误处理