# 代码生成时间: 2025-08-20 23:07:54
import os
from celery import Celery

# 配置Celery
os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
app = Celery('inventory', broker=os.environ['CELERY_BROKER_URL'])

# 库存数据存储结构
inventory = {}

@app.task
def add_item(item_name, quantity):
    """添加库存项
    
    参数：
    item_name (str): 物品名称
    quantity (int): 数量
    
    返回：
    bool: 是否添加成功
    """
    try:
        if item_name in inventory:
            inventory[item_name] += quantity
        else:
            inventory[item_name] = quantity
        return True
    except Exception as e:
        print(f"Error adding item: {e}")
        return False

@app.task
def remove_item(item_name, quantity):
    """移除库存项
    
    参数：
    item_name (str): 物品名称
    quantity (int): 数量
    
    返回：
    bool: 是否移除成功
    """
    try:
        if item_name in inventory and inventory[item_name] >= quantity:
            inventory[item_name] -= quantity
            return True
        else:
            print(f"Error: Item '{item_name}' not found or quantity insufficient.")
            return False
    except Exception as e:
        print(f"Error removing item: {e}")
        return False

@app.task
def check_item(item_name):
    """检查物品库存
    
    参数：
    item_name (str): 物品名称
    
    返回：
    int: 物品库存数量
    """
    try:
        return inventory.get(item_name, 0)
    except Exception as e:
        print(f"Error checking item: {e}")
        return 0

if __name__ == '__main__':
    # 测试库存管理系统
    add_item.delay('Apple', 10)
    add_item.delay('Banana', 20)
    print(f"Apple stock: {check_item('Apple')}")
    print(f"Banana stock: {check_item('Banana')}")
    remove_item.delay('Apple', 5)
    print(f"Apple stock after removal: {check_item('Apple')}")
    