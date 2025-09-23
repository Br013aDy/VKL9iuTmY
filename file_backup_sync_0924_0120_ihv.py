# 代码生成时间: 2025-09-24 01:20:24
import os
import shutil
from celery import Celery

# Define the Celery app
app = Celery('file_backup_sync',
             broker='pyamqp://guest@localhost//')

# Define the backup and sync function
@app.task(bind=True,
           max_retries=3,
           default_retry_delay=60)
def backup_and_sync(self, source_path, destination_path):
    """Backup and sync files from source to destination."""
    try:
        # Check if source exists
        if not os.path.exists(source_path):
            raise FileNotFoundError("Source path does not exist.")
        
        # Check if destination exists, if not create it
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        # Copy file/directory from source to destination
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
        
        # Return success message
        return f"Backup and sync successful from {source_path} to {destination_path}"
        
    except FileNotFoundError as e:
        # Handle file not found error
        self.retry(exc=e)
    except Exception as e:
        # Handle other errors
        raise e

# Example usage:
# backup_and_sync.delay('path/to/source', 'path/to/destination')
