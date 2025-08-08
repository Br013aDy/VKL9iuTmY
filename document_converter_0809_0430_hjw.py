# 代码生成时间: 2025-08-09 04:30:51
import os
import celery
from celery import Celery, states
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError
from docx import Document
from pdf2docx import Converter

# 设置Celery配置
app = Celery('document_converter',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)

# 配置日志
logger = get_task_logger(__name__)

# 文档转换器任务
@app.task(bind=True, default_retry_delay=5 * 60, max_retries=5)
def convert_document(self, input_file_path, output_file_path):
    """
    将文档从PDF转换为DOCX格式。

    参数:
    input_file_path (str): 输入文件的路径
    output_file_path (str): 输出文件的路径

    返回:
    bool: 转换是否成功
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Input file {input_file_path} does not exist.")
        
        # 创建PDF到DOCX转换器实例
        cv = Converter(input_file_path)
        cv.convert(output_file_path, start=0, end=None)
        cv.close()
        
        # 检查输出文件是否成功创建
        if not os.path.exists(output_file_path):
            raise Exception(f"Failed to create output file at {output_file_path}.")
        
        # 如果一切顺利，返回True
        return True
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise
        
    except MaxRetriesExceededError as e:
        logger.error(f"Maximum retries exceeded: {e}")
        self.retry(exc=e)

# 检查Celery任务是否正在运行
@app.task
def check_task_status(task_id):
    """
    检查给定任务ID的状态。

    参数:
    task_id (str): 任务ID

    返回:
    dict: 包含任务状态和结果的字典
    """
    try:
        task = app.AsyncResult(task_id)
        return {'status': task.status, 'result': task.result}
    
    except Exception as e:
        logger.error(f"Error checking task status: {e}")
        return {'status': 'failed', 'result': None}
