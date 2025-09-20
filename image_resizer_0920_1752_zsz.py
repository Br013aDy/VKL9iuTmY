# 代码生成时间: 2025-09-20 17:52:33
import os
from celery import Celery
from PIL import Image

# 配置Celery
app = Celery('tasks',
# FIXME: 处理边界情况
              broker='pyamqp://guest@localhost//')


@app.task
def resize_image(image_path, output_path, size):
    """
# 改进用户体验
    调整图片尺寸
    :param image_path: 原始图片路径
# NOTE: 重要实现细节
    :param output_path: 调整尺寸后的图片保存路径
# 添加错误处理
    :param size: 目标尺寸 (宽, 高)
    """
    # 检查图片路径是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found at {}".format(image_path))

    # 打开图片
    try:
        with Image.open(image_path) as img:
            # 调整图片尺寸
            img = img.resize(size, Image.ANTIALIAS)
# NOTE: 重要实现细节
            # 保存调整后的图片
            img.save(output_path)
            print("Image resized and saved to {}".format(output_path))
    except IOError:
# 优化算法效率
        raise Exception("Error opening or processing the image file.")
# TODO: 优化性能


if __name__ == '__main__':
    # 程序入口，这里可以添加命令行参数解析等逻辑
    pass