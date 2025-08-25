# 代码生成时间: 2025-08-25 18:59:58
from celery import Celery
from typing import List

# 设置Celery配置
app = Celery('sort_service', broker='pyamqp://guest@localhost//')


@app.task
def sort_numbers(numbers: List[int]) -> List[int]:
    """
    对列表中的数字进行排序
    
    参数:
    - numbers: 一个包含整数的列表
    
    返回:
    - 排序后的列表
    
    异常:
    - ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("列表不能为空")
    return sorted(numbers)


# 用于测试的代码
if __name__ == '__main__':
    try:
        # 测试数据
        test_numbers = [5, 2, 9, 1, 5, 6]
        # 调用排序任务
        sorted_numbers = sort_numbers.delay(test_numbers)
        # 获取任务结果
        result = sorted_numbers.get()
        print(f"排序后的结果: {result}")
    except Exception as e:
        print(f"发生错误: {e}")