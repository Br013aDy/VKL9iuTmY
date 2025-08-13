# 代码生成时间: 2025-08-13 16:14:57
from flask import Flask, jsonify, request
from celery import Celery


# 设置 Flask 应用
app = Flask(__name__)

# 设置 Celery
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# RESTful API 接口
@app.route('/api/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    获取异步任务状态
    :param task_id: 异步任务的唯一标识符
    :return: 异步任务的状态信息
    """
    result = celery.AsyncResult(task_id)
    if result:
        return jsonify(result.get()), 200
    else:
        return jsonify({'error': 'Task not found'}), 404


# 异步任务定义
@celery.task(bind=True, name='my_task')
def my_task(self, params):
    """
    定义一个简单的异步任务
    :param self: Celery 任务实例
    :param params: 任务参数
    :return: None
    """
    with app.app_context():
        # 任务逻辑，例如：执行数据库操作、文件处理等
        print(f'Task {self.request.id} started with params {params}')
        # 模拟长时间运行的任务
        import time
        time.sleep(10)
        print(f'Task {self.request.id} finished')
        return {'status': 'done', 'result': 'Task completed successfully'}


if __name__ == '__main__':
    app.run(debug=True)
