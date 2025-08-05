# 代码生成时间: 2025-08-05 15:51:56
import os
from celery import Celery
from cryptography.fernet import Fernet

# 配置Celery
app = Celery('password_encryption_decryption', broker='pyamqp://guest@localhost//')


# Fernet加密的密钥
# 这个密钥应该是从环境变量或者其他安全的地方获取的
# 这里为了示例，我们直接硬编码了密钥
key = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
cipher_suite = Fernet(key)


@app.task
def encrypt_password(password):
    '''
    加密密码
    :param password: 待加密的密码字符串
    :return: 加密后的密码字符串
    '''
    try:
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password.decode()
    except Exception as e:
        # 这里可以根据需要记录日志或者进行错误处理
        raise ValueError(f'Encryption failed: {e}')


@app.task
def decrypt_password(encrypted_password):
    '''
    解密密码
    :param encrypted_password: 待解密的加密密码字符串
    :return: 解密后的密码字符串
    '''
    try:
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except Exception as e:
        # 这里可以根据需要记录日志或者进行错误处理
        raise ValueError(f'Decryption failed: {e}')


def main():
    '''
    主函数，用于测试加密解密功能
    '''
    # 测试数据
    password = 'my_secret_password'
    encrypted = encrypt_password.delay(password)
    decrypted = decrypt_password.delay(encrypted.get())

    # 打印结果
    print(f'Original Password: {password}')
    print(f'Encrypted Password: {encrypted.get()}')
    print(f'Decrypted Password: {decrypted.get()}')


if __name__ == '__main__':
    main()