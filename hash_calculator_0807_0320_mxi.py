# 代码生成时间: 2025-08-07 03:20:35
import hashlib
from celery import Celery

# 配置Celery使用的broker和backend
app = Celery('hash_calculator', broker='pyamqp://guest@localhost//', backend='rpc://')

# 定义一个哈希值计算的任务
@app.task
def calculate_hash(data, algorithm='sha256'):
    """
    计算给定数据的哈希值。

    参数:
    data (str): 要计算哈希值的原始数据。
    algorithm (str): 哈希算法名称，默认为'sha256'。

    返回:
    str: 计算得到的哈希值。

    异常:
    ValueError: 如果指定的哈希算法不受支持。
    """
    # 检查哈希算法是否受支持
    supported_algorithms = {'sha1', 'sha256', 'md5'}  # 可以根据需要添加更多算法

    if algorithm not in supported_algorithms:
        raise ValueError(f'Unsupported hash algorithm: {algorithm}')

    # 创建哈希对象并计算哈希值
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data.encode('utf-8'))  # 确保数据是字节形式

    # 返回计算得到的哈希值
    return hash_obj.hexdigest()

# 定义一个示例函数，用于演示任务的调用
def example_usage():
    """
    演示如何调用哈希值计算任务。

    这个函数将计算一个字符串的哈希值，并打印结果。
    """
    # 创建Celery应用实例
    app = Celery('hash_calculator', broker='pyamqp://guest@localhost//', backend='rpc://')

    # 定义要计算哈希值的数据
    data = 'Hello, world!'

    # 调用任务并等待结果
    result = calculate_hash.delay(data)

    # 打印结果
    print(f'The hash of \'{data}\' is: {result.get()}
')

if __name__ == '__main__':
    example_usage()