# 代码生成时间: 2025-09-21 00:46:56
import os
from celery import Celery

# 配置Celery
app = Celery('batch_file_renamer',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

@app.task
def rename_files(directory, prefix, extension=""):
    """
    批量重命名指定目录下的所有文件。
    
    参数:
    directory (str): 需要重命名文件的目录。
    prefix (str): 文件的新前缀。
    extension (str): 文件的新扩展名，默认为空。
    
    返回:
    int: 重命名成功的文件数量。
    """
    renamed_count = 0
    for filename in os.listdir(directory):
        try:
            # 构建新的文件名
            name, ext = os.path.splitext(filename)
            new_name = f"{prefix}{name}{extension}"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            
            # 重命名文件
            os.rename(old_path, new_path)
            renamed_count += 1
        except Exception as e:
            # 错误处理，打印异常信息
            print(f"Error renaming file {filename}: {e}")
    return renamed_count

# 用于测试的示例代码
if __name__ == '__main__':
    # 假设我们有一个目录和前缀
    directory = "/path/to/your/directory"
    prefix = "new_"
    
    # 调用重命名函数
    result = rename_files(directory, prefix)
    print(f"Renamed {result} files.")