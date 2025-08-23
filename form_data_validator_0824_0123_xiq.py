# 代码生成时间: 2025-08-24 01:23:16
import logging
from celery import Celery
from celery import shared_task
from marshmallow import Schema, fields, ValidationError, EXCLUDE


# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery配置
app = Celery('form_data_validator',
             broker='pyamqp://guest@localhost//')

# 表单数据验证器
class FormDataValidator(Schema):
    # 定义需要验证的字段
    username = fields.Str(required=True, validate=lambda x: len(x) > 3)
    email = fields.Email(required=True)
    age = fields.Int(missing=0, validate=lambda x: x >= 0)

    class Meta:
        unknown = EXCLUDE  # 忽略未定义的字段

# Celery异步任务
@app.task
def validate_form_data(data):
    """
    异步验证表单数据的任务
    :param data: 表单提交的数据，一个字典对象
    :return: None
    """
    try:
        # 创建表单验证器实例
        validator = FormDataValidator()
        # 验证数据
        result = validator.load(data)
        logger.info(f'表单验证成功: {result}')
    except ValidationError as err:
        # 处理验证错误
        logger.error(f'表单验证失败: {err}')
        return {
            'success': False,
            'message': '表单验证失败',
            'errors': err.messages
        }
    return {
        'success': True,
        'message': '表单验证成功',
        'data': result
    }


# 测试代码
if __name__ == '__main__':
    # 测试数据
    test_data = {
        'username': 'John',
        'email': 'john@example.com',
        'age': 30
    }
    # 调用异步任务
    result = validate_form_data.delay(test_data)
    # 获取任务结果
    result.get()
