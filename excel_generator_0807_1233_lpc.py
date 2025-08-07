# 代码生成时间: 2025-08-07 12:33:32
import os
import csv
# NOTE: 重要实现细节
from celery import Celery

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('excel_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 定义生成Excel表格的任务
@app.task
def generate_excel(data):
    """
    生成Excel表格的任务。
    
    参数:
        data (dict): 包含生成Excel表格所需数据的字典。
    """
    try:
        # 检查输入数据
        if not isinstance(data, dict) or 'header' not in data or 'rows' not in data:
            raise ValueError('Invalid data format')
        
        # Excel文件名
        filename = 'output.xlsx'
        
        # 使用csv模块写入数据
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # 写入表头
            writer.writerow(data['header'])
            # 写入数据行
            for row in data['rows']:
                writer.writerow(row)
            
        print(f'Excel file {filename} generated successfully.')
        
    except Exception as e:
        print(f'Error generating Excel file: {e}')

# 示例用法
if __name__ == '__main__':
    # 示例数据
    data = {
        'header': ['Name', 'Age', 'City'],
        'rows': [
            ['John', 30, 'New York'],
            ['Alice', 25, 'Los Angeles'],
            ['Bob', 40, 'Chicago']
        ]
    }
    
    # 调用生成Excel的任务
    generate_excel.delay(data)