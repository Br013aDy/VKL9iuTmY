# 代码生成时间: 2025-08-27 10:46:22
import os
import json
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('test_report_generator',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_expires=3600,
)

# 日志配置
logger = get_task_logger(__name__)

# 导入测试报告模板
TEST_REPORT_TEMPLATE = """Test Report:
----------------
{test_name}
----------------
{results}
"""

# 任务：生成测试报告
@app.task(bind=True)
def generate_test_report(self, test_name, test_results):
    """
    生成测试报告的任务
    :param self: 任务对象
    :param test_name: 测试名称
    :param test_results: 测试结果
    :return: 生成的报告路径
    """
    try:
        # 检查输入参数
        if not test_name or not test_results:
            raise ValueError('Test name and results are required')

        # 构造测试报告内容
        report_content = TEST_REPORT_TEMPLATE.format(
            test_name=test_name,
            results=json.dumps(test_results, indent=4)
        )

        # 保存测试报告到文件
        report_file_name = f"{test_name}_report.txt"
        with open(report_file_name, 'w') as report_file:
            report_file.write(report_content)

        # 返回报告文件路径
        return f"{os.path.abspath(report_file_name)}"
    except Exception as e:
        # 记录错误日志
        logger.error(f"Failed to generate test report: {e}")
        raise

# 调用示例
if __name__ == '__main__':
    # 测试数据
    test_name = "Sample Test"
    test_results = {
        "passed": 10,
        "failed": 2,
        "skipped": 3,
    }

    # 异步执行任务
    report_path = generate_test_report.delay(test_name, test_results)
    print(f"Report generated at: {report_path.get()}")