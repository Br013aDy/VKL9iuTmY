# 代码生成时间: 2025-09-21 12:35:49
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery.result import AsyncResult
import logging

# 配置Celery
app = Celery('inventory_manager', broker='pyamqp://guest@localhost//')

# 库存管理器类
class InventoryManager:
    def __init__(self):
        # 初始化库存数据
        self.inventory = {}

    def add_item(self, item_id, quantity):
        """
        添加库存项
        :param item_id: 库存项ID
        :param quantity: 数量
        """
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity
        return self.inventory[item_id]

    def remove_item(self, item_id, quantity):
        """
        移除库存项
        :param item_id: 库存项ID
        :param quantity: 移除数量
        """
        if item_id not in self.inventory or self.inventory[item_id] < quantity:
            raise ValueError('Insufficient stock')
        self.inventory[item_id] -= quantity
        return self.inventory[item_id]

# 异步任务：添加库存项
@app.task(soft_time_limit=60)
def add_inventory_async(item_id, quantity):
    try:
        manager = InventoryManager()
        result = manager.add_item(item_id, quantity)
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# 异步任务：移除库存项
@app.task(soft_time_limit=60)
def remove_inventory_async(item_id, quantity):
    try:
        manager = InventoryManager()
        result = manager.remove_item(item_id, quantity)
        return {'status': 'success', 'result': result}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# 设置日志记录
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # 运行Celery worker
    app.start()