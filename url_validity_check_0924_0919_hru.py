# 代码生成时间: 2025-09-24 09:19:51
import requests
from celery import Celery
from urllib.parse import urlparse
from celery.utils.log import get_task_logger

# Configure Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')

# Get a logger for the current task
logger = get_task_logger(__name__)

@app.task(name='url_validity_check', bind=True)
def url_validity_check(self, url):
    """
    Check if a URL is valid by attempting to make a request to it.

    :param url: The URL to check
    :type url: str
    :return: A dictionary containing the status of the URL and the HTTP status code
    :rtype: dict
    """
    try:
        # Parse the URL to ensure the scheme and netloc are present
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return {"valid": False, "error": "Invalid URL format"}

        # Attempt to make a request to the URL
        response = requests.head(url, timeout=10)

        # Check if the request was successful
        if response.status_code < 400:
            return {"valid": True, "status_code": response.status_code}
        else:
            return {"valid": False, "status_code": response.status_code}
    except requests.ConnectionError:
        logger.error(f"Connection error when checking URL: {url}")
        return {"valid": False, "error": "Connection error"}
    except requests.Timeout:
        logger.error(f"Timeout error when checking URL: {url}")
        return {"valid": False, "error": "Timeout error"}
    except requests.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return {"valid": False, "error": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"valid": False, "error": str(e)}
