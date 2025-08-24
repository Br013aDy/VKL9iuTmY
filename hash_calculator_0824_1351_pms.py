# 代码生成时间: 2025-08-24 13:51:40
import hashlib
cfrom celery import Celery
from celery import shared_task
def calculate_hash(input_string):
    """
    Calculates the SHA256 hash of a given input string.
    
    Args:
        input_string (str): The string to calculate the hash for.
    
    Returns:
        str: The SHA256 hash of the input string.
    """
    try:
        # Create a new SHA256 hash object
        hash_object = hashlib.sha256()
        # Update the hash object with the bytes of the input string
        hash_object.update(input_string.encode())
        # Return the hexadecimal representation of the hash
        return hash_object.hexdigest()
    except Exception as e:
        # Handle any exceptions that occur during hash calculation
        print(f"An error occurred: {e}")
        return None

# Configure Celery
app = Celery('hash_calculator',
             broker='amqp://guest@localhost//')

# Define a Celery task to calculate the hash
@app.task
def hash_task(input_string):
    """
    A Celery task that calculates the SHA256 hash of a given input string.
    
    Args:
        input_string (str): The string to calculate the hash for.
    
    Returns:
        str: The SHA256 hash of the input string.
    """
    return calculate_hash(input_string)