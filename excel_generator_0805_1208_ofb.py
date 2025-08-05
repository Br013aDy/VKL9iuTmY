# 代码生成时间: 2025-08-05 12:08:30
import os
import pandas as pd
from celery import Celery, Task
from celery.utils.log import get_task_logger

# Configure Celery
app = Celery('excel_generator',
             broker='pyamqp://guest@localhost//')

# Set up logger
logger = get_task_logger(__name__)

# A Celery task that generates an Excel file
class GenerateExcelTask(Task):
    def __init__(self):
        super(GenerateExcelTask, self).__init__()
        self.output_path = 'output'

    def run(self, data, filename, *args, **kwargs):
        # Ensure output directory exists
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # Generate the Excel file
        try:
            df = pd.DataFrame(data)
            full_path = os.path.join(self.output_path, filename)
            df.to_excel(full_path, index=False)
            logger.info(f'Excel file generated successfully: {full_path}')
            return full_path
        except Exception as e:
            logger.error(f'Failed to generate Excel file: {e}')
            raise

# Example usage
if __name__ == '__main__':
    # Sample data for demonstration
    data = {
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    }

    # Create a task instance
    task = GenerateExcelTask()

    # Call the task asynchronously
    result = task.delay(data, 'example.xlsx')
    print(f'Task started with ID: {result.id}')
