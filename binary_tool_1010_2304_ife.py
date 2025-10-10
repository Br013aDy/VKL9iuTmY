# 代码生成时间: 2025-10-10 23:04:59
import os
from celery import Celery
import logging

# 配置Celery
app = Celery('binary_tool', broker='pyamqp://guest@localhost//')

# 日志配置
logging.basicConfig(level=logging.INFO)

@app.task(name='write_binary_file')
def write_binary_file(file_path, data):
    """
    写入二进制文件
    :param file_path: 文件路径
    :param data: 要写入的二进制数据
    :return: None
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        logging.info(f'成功写入文件: {file_path}')
    except Exception as e:
        logging.error(f'写入文件失败: {e}')

@app.task(name='read_binary_file')
def read_binary_file(file_path):
    """
    读取二进制文件
    :param file_path: 文件路径
    :return: 文件内容的二进制数据
    """
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            logging.info(f'成功读取文件: {file_path}')
            return data
    except Exception as e:
        logging.error(f'读取文件失败: {e}')
        return None

if __name__ == '__main__':
    # 测试写入和读取二进制文件
    file_path = 'test.bin'
    data = b'Hello, World!'
    write_binary_file.delay(file_path, data)
    read_result = read_binary_file.delay(file_path)
    
    # 等待异步任务完成
    read_result.wait()
    if read_result.ready():
        read_data = read_result.get()
        print(f'读取的二进制数据: {read_data}')
