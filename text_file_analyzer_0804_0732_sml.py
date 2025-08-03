# 代码生成时间: 2025-08-04 07:32:25
import os
import re
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('text_file_analyzer', broker='pyamqp://guest@localhost//')

# 获取任务日志记录器
logger = get_task_logger(__name__)

@app.task
def analyze_file_content(file_path):
    """分析文本文件内容的任务"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'文件{file_path}不存在')

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 统计文本中的单词数量
        word_count = len(re.findall(r'\w+', content))

        # 打印单词数量
        print(f'文件{file_path}中的单词数量为: {word_count}')

        return {'file_path': file_path, 'word_count': word_count}

    except FileNotFoundError as e:
        logger.error(e)
        return {'error': str(e)}
    except Exception as e:
        logger.error(e)
        return {'error': '发生未知错误'}
