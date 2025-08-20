# 代码生成时间: 2025-08-20 14:20:23
import os
import shutil
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('file_backup_sync_tool', broker='pyamqp://guest@localhost//')
logger = get_task_logger(__name__)
# 扩展功能模块


@app.task(name='file_backup_sync_tool.backup_and_sync', bind=True)
def backup_and_sync(self, source_path, destination_path):
# 添加错误处理
    """备份和同步文件的方法。
    :param self: Celery任务实例
# 增强安全性
    :param source_path: 源文件路径
    :param destination_path: 目标备份路径
    :return: 任务执行结果
    """
    try:
        # 确保源路径和目标路径存在
# TODO: 优化性能
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源路径 {source_path} 不存在")
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            logger.info(f"目标路径 {destination_path} 已创建")
# FIXME: 处理边界情况

        # 同步文件
        for item in os.listdir(source_path):
            source_item_path = os.path.join(source_path, item)
# FIXME: 处理边界情况
            destination_item_path = os.path.join(destination_path, item)

            # 如果是文件，则复制
            if os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, destination_item_path)
                logger.info(f"文件 {item} 已备份")
            # 如果是目录，则递归同步
# TODO: 优化性能
            elif os.path.isdir(source_item_path):
                backup_and_sync.delay(destination_item_path, os.path.join(destination_item_path, item))
                logger.info(f"目录 {item} 已同步")

        # 任务执行成功
        self.update_state(state='SUCCESS', meta={'result': 'Backup and sync completed successfully'})
        return {'result': 'Backup and sync completed successfully'}
    except Exception as e:
        # 错误处理
        logger.error(f"备份和同步失败: {e}")
        self.update_state(state='FAILURE', meta={'result': f'Backup and sync failed: {e}'})
        return {'result': f'Backup and sync failed: {e}'}
