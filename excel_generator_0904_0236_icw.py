# 代码生成时间: 2025-09-04 02:36:04
import os
from celery import Celery
from celery.bin import worker
from openpyxl import Workbook

# 配置Celery
app = Celery('excel_generator', broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 创建Excel表格的任务
@app.task(name='generate_excel')
def generate_excel(file_name, data):
    """
    生成Excel表格文件。
    
    参数:
    file_name: str - 要生成的Excel文件的名称。
    data: list of list - 要写入文件的数据，以二维列表形式提供。
    
    返回:
    file_path: str - 生成的Excel文件的路径。
    """
    try:
        # 创建Workbook对象
        wb = Workbook()
        # 激活第一个worksheet
        ws = wb.active
        # 写入数据
        for row in data:
            ws.append(row)
        # 保存Workbook
        file_path = os.path.join(os.getcwd(), file_name)
        wb.save(file_path)
        return file_path
    except Exception as e:
        # 错误处理
        print(f'An error occurred: {e}')
        return None

# 如果脚本被直接运行，以下是启动Celery worker的代码
if __name__ == '__main__':
    worker_app = worker.worker(app=app)
    worker_app.run()