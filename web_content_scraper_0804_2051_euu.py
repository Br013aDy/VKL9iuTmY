# 代码生成时间: 2025-08-04 20:51:48
import requests
from bs4 import BeautifulSoup
from celery import Celery

# 定义Celery应用
app = Celery('web_content_scraper', broker='pyamqp://guest@localhost//')

# 定义任务函数，用于抓取网页内容
@app.task
def scrape_web_content(url):
    """
    抓取指定URL的网页内容。
    
    参数:
    url -- 要抓取的网页地址
    
    返回:
    网页内容的BeautifulSoup对象或错误信息
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        # 处理请求错误
        return {'error': f'请求错误: {e}'}
    try:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        # 处理解析错误
        return {'error': f'解析错误: {e}'}

# 定义任务函数，用于打印网页内容
@app.task
def print_web_content(task_id):
    """
    打印指定任务ID的网页内容。
    
    参数:
    task_id -- Celery任务ID
    """
    result = scrape_web_content.AsyncResult(task_id)
    if result.ready():
        if result.successful():
            print(result.get())
        else:
            print(f'任务失败: {result.info}')