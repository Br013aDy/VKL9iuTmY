# 代码生成时间: 2025-09-01 15:25:59
import os
import csv
from celery import Celery
from celery.utils.log import get_task_logger
from openpyxl import Workbook

# Configure Celery task broker and backend
os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery('excel_generator', broker=os.environ['CELERY_BROKER_URL'], backend=os.environ['CELERY_RESULT_BACKEND'])
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Get logger
logger = get_task_logger(__name__)


@app.task(name='excel_generator.create_excel', bind=True)
def create_excel(self, data, filename="Generated.xlsx"):
    """
    Create an Excel file with the given data.

    :param data: A list of dictionaries where each dictionary represents a row in the Excel file.
    :param filename: The name of the Excel file to be created.
    :return: None
    """
    try:
        # Create a workbook and select the active worksheet
        wb = Workbook()
        ws = wb.active
        
        # Write data to the worksheet
        for row_num, row_data in enumerate(data, 1):
            for col_num, value in enumerate(row_data.values(), 1):
                ws.cell(row=row_num, column=col_num, value=value)
        
        # Save the workbook to the specified filename
        wb.save(filename=filename)
        logger.info(f"Excel file {filename} created successfully.")
        return f"Excel file {filename} created successfully."
    except Exception as e:
        logger.error("Failed to create Excel file: ", exc_info=True)
        raise self.retry(exc=e, countdown=10)

# Example usage of the Celery task
# create_excel.apply_async((your_data,))
