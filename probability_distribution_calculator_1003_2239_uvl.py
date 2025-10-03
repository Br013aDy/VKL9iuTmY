# 代码生成时间: 2025-10-03 22:39:46
import numpy as np
from scipy.stats import norm
from celery import Celery

# 配置Celery
app = Celery('probability_distribution_calculator',
             broker='pyamqp://guest@localhost//')

@app.task
def calculate_normal_distribution(mean, std_dev, num_samples):
    """
    Calculate the normal distribution for a given mean and standard deviation.
    
    Args:
        mean (float): The mean of the normal distribution.
        std_dev (float): The standard deviation of the normal distribution.
        num_samples (int): The number of samples to generate.
    
    Returns:
        tuple: A tuple containing the mean and standard deviation of the generated samples.
    
    Raises:
        ValueError: If any of the input parameters are invalid.
    """
    
    # 输入参数验证
    if not isinstance(mean, (int, float)) or not isinstance(std_dev, (int, float)):
        raise ValueError("Mean and standard deviation must be numbers.")
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("Number of samples must be a positive integer.")
    
    # 生成正态分布样本
    samples = np.random.normal(loc=mean, scale=std_dev, size=num_samples)
    
    # 计算样本的均值和标准差
    sample_mean = np.mean(samples)
    sample_std_dev = np.std(samples)
    
    return (sample_mean, sample_std_dev)

# 示例用法
if __name__ == '__main__':
    # 调用异步任务
    result = calculate_normal_distribution.delay(0, 1, 1000)
    
    # 获取结果
    mean, std_dev = result.get()
    print(f"Generated samples mean: {mean}, standard deviation: {std_dev}")