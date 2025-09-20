# 代码生成时间: 2025-09-20 10:00:14
from celery import Celery
import random
from typing import Tuple

# 定义 Celery 应用
app = Celery('random_number_generator', broker='pyamqp://guest@localhost//')

# 配置 Celery 应用
app.conf.update(
    result_backend='rpc://',
)

# 随机数生成器任务
@app.task(name='generate_random_number')
def generate_random_number(min_value: int = 1, max_value: int = 100) -> Tuple[bool, int]:
    """
    生成一个介于 min_value 和 max_value 之间的随机数。

    :param min_value: 随机数的最小值，默认为 1
    :param max_value: 随机数的最大值，默认为 100
    :return: 一个包含布尔值和随机数的元组，布尔值表示生成是否成功
    """
    try:
        # 验证输入值是否合法
        if not isinstance(min_value, int) or not isinstance(max_value, int):
            raise ValueError('min_value 和 max_value 必须是整数')
        if min_value < 0 or max_value < 0:
            raise ValueError('min_value 和 max_value 不能为负数')
        if min_value >= max_value:
            raise ValueError('min_value 必须小于 max_value')

        # 生成随机数
        random_number = random.randint(min_value, max_value)
        return True, random_number
    except Exception as e:
        # 处理异常并返回错误信息
        return False, str(e)

# 测试代码
if __name__ == '__main__':
    # 启动 Celery worker
    app.start()
    # 调用随机数生成器任务
    result = generate_random_number.delay(10, 50)
    # 获取结果
    success, random_number = result.get()
    if success:
        print(f'生成的随机数是: {random_number}')
    else:
        print(f'生成随机数失败: {random_number}')