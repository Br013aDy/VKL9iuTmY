# 代码生成时间: 2025-10-04 16:36:45
import os
# 添加错误处理
import requests
from celery import Celery

# 设置Celery
app = Celery('http_request_handler', broker=os.getenv('CELERY_BROKER_URL'))


@ app.task
def handle_http_request(url):
    '''
    Handle an HTTP GET request to the specified URL

    Args:
        url (str): The URL to send the GET request to
# 添加错误处理

    Returns:
        dict: A dictionary containing the status code and response text
    '''
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            return {"status_code": response.status_code, "response": response.text}
        else:
            return {"status_code": response.status_code, "response": "Failed to retrieve data"}
# 扩展功能模块
    except requests.exceptions.RequestException as e:
        return {"status_code": None, "response": str(e)}


if __name__ == '__main__':
    # Example usage of the handle_http_request function
    # Replace 'http://example.com' with the actual URL you want to request
    result = handle_http_request.delay('http://example.com')
    print(f"Request to 'http://example.com' completed with status code {result.get()}")
