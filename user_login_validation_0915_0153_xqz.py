# 代码生成时间: 2025-09-15 01:53:59
# 用户登录验证系统
# 使用CELERY框架实现异步处理用户登录请求

from celery import Celery
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

# 配置CELERY
app = Flask(__name__)
CORS(app)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# 定义CELERY实例
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 模拟数据库存储
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

# 用户登录验证函数
def validate_user(username, password):
    """验证用户登录信息"""
    if username in users:
        if check_password_hash(users[username], password):
            return True, "登录成功"
        else:
            return False, "密码错误"
    else:
        return False, "用户不存在"

# 用户登录任务
@celery.task
def user_login_task(username, password):
    """异步处理用户登录"""
    is_valid, message = validate_user(username, password)
    return {
        "is_valid": is_valid,
        "message": message,
    }

# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    """处理用户登录请求"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400

    # 异步执行用户登录任务
    task = user_login_task.delay(username, password)
    return jsonify({'task_id': task.id}), 202

# 获取登录结果接口
@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    """获取用户登录结果"""
    task = user_login_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.result['message'],
            'is_valid': task.result['is_valid'],
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)