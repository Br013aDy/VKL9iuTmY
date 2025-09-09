# 代码生成时间: 2025-09-09 10:27:11
import os
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
broker_url = 'amqp://localhost//'
app = Celery('batch_rename_tool', broker=broker_url)
logger = get_task_logger(__name__)

class FileRenamer:
    def __init__(self, directory, new_prefix):
        """初始化文件重命名工具

        :param directory: 需要批量重命名文件的目录
        :param new_prefix: 新文件名的前缀
        """
        self.directory = directory
        self.new_prefix = new_prefix

    def rename_files(self):
        """在指定目录下批量重命名文件

        :return: None
        """
        try:
            for index, filename in enumerate(os.listdir(self.directory)):
                file_path = os.path.join(self.directory, filename)
                # 确保是文件而不是目录
                if os.path.isfile(file_path):
                    new_filename = f"{self.new_prefix}_{index + 1}{os.path.splitext(filename)[1]}"
                    new_file_path = os.path.join(self.directory, new_filename)
                    os.rename(file_path, new_file_path)
                    logger.info(f"Renamed {filename} to {new_filename}")
        except FileNotFoundError:
            logger.error(f"Directory {self.directory} not found")
        except PermissionError:
            logger.error(f"Permission denied to access {self.directory}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

@app.task
def batch_rename(directory, new_prefix):
    """Celery任务，用于批量重命名文件

    :param directory: 需要批量重命名文件的目录
    :param new_prefix: 新文件名的前缀
    """
    renamer = FileRenamer(directory, new_prefix)
    renamer.rename_files()

# 示例用法
if __name__ == '__main__':
    # 确保Celery工作在主线程中，否则任务将不会被执行
    batch_rename.delay('/path/to/directory', 'new_prefix')
