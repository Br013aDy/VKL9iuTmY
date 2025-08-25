# 代码生成时间: 2025-08-26 06:04:51
from celery import Celery
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# 配置Celery
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 用于存储用户信息的字典（在实际应用中应使用数据库）
users = {}

# 用户注册任务
@celery.task
def register_user(username, password):
    if username in users:
        return 'Username already exists'
    password_hash = generate_password_hash(password)
    users[username] = password_hash
    return 'User registered successfully'

# 用户登录任务
@celery.task
def login_user(username, password):
    if username not in users:
        return 'User not found'
    if not check_password_hash(users[username], password):
        return 'Incorrect password'
    return 'Login successful'

# Flask路由：注册用户
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    result = register_user.delay(username, password)
    return jsonify({'message': 'Registration task started', 'task_id': result.id}), 202

# Flask路由：用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    result = login_user.delay(username, password)
    return jsonify({'message': 'Login task started', 'task_id': result.id}), 202

# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True)
