# 代码生成时间: 2025-09-23 00:02:30
import psutil
from celery import Celery
import logging

# 配置Celery
app = Celery('memory_usage_analyze', broker='amqp://guest@localhost//')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义Celery任务
@app.task
def analyze_memory_usage():
    """分析系统内存使用情况"""
    try:
        # 获取系统内存信息
        mem = psutil.virtual_memory()
        
        # 计算使用的内存百分比
        used_memory_percent = mem.percent
        
        # 记录内存使用情况
        logger.info(f"Total Memory: {mem.total} bytes")
        logger.info(f"Available Memory: {mem.available} bytes")
        logger.info(f"Used Memory: {mem.used} bytes")
        logger.info(f"Memory Usage Percentage: {used_memory_percent}%")
        
        # 返回内存使用结果
        return {
            "total_memory": mem.total,
            "available_memory": mem.available,
            "used_memory": mem.used,
            "memory_usage_percent": used_memory_percent
        }
    except Exception as e:
        # 处理异常
        logger.error(f"Error analyzing memory usage: {e}")
        raise

# 程序入口点
def main():
    """程序入口点"""
    # 调用Celery任务
    result = analyze_memory_usage.delay()
    # 等待任务完成并获取结果
    memory_usage = result.get()
    # 打印内存使用结果
    print(memory_usage)

if __name__ == '__main__':
    main()