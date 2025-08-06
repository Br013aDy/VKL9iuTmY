# 代码生成时间: 2025-08-06 14:15:16
import os
import json
from flask import Flask, request, jsonify
from celery import Celery

# 初始化Flask应用
app = Flask(__name__)

# 配置Celery
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost//'  # 使用RabbitMQ作为消息代理
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 定义一个简单的异步任务
@celery.task
def add(x, y):
    """异步任务，用于计算两个数字的和"""
    return x + y

# 定义RESTful API接口
@app.route('/add', methods=['POST'])
def add_api():
    """处理添加操作的请求"""
    try:
        # 解析请求数据
        data = request.get_json()
        x = data['x']
        y = data['y']
        
        # 调用异步任务
        result = add.delay(x, y)
        
        # 返回任务ID，以便查询结果
        return jsonify({'task_id': result.id}), 202
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 400

# 定义查询任务结果的接口
@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    """根据任务ID查询任务结果"""
    try:
        # 获取任务结果
        result = add.AsyncResult(task_id)
        if result.state == 'PENDING':
            response = {"state": result.state, "status": "PENDING"}
        elif result.state != 'FAILURE':
            response = {"state": result.state, "result": result.get(timeout=3)}
        else:
            # 如果任务失败，返回错误信息
            response = {"state": result.state, "status": "FAILURE", 'info': str(result.info)}
        return jsonify(response)
    except Exception as e:
        # 错误处理
        return jsonify({'error': 'Task not found', 'message': str(e)}), 404

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)