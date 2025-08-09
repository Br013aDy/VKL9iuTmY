# 代码生成时间: 2025-08-10 04:26:10
import celery
from celery import shared_task
from typing import List, Dict

# 商品信息
class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

# 购物车类
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product: Product, quantity: int):
        """添加商品到购物车"""
        self.items.append({'product': product, 'quantity': quantity})

    def remove_product(self, product_id: int):
        """从购物车中移除商品"""
        self.items = [item for item in self.items if item['product'].id != product_id]

    def get_total_price(self) -> float:
        """计算购物车中所有商品的总价"""
        return sum(item['product'].price * item['quantity'] for item in self.items)

# Celery配置
app = celery.Celery('shopping_cart_celery_app',
                    broker='pyamqp://guest@localhost//',
                    backend='rpc://')

# 使用Celery装饰器定义异步任务
@app.task
def add_product_to_cart_async(cart_id: int, product_id: int, quantity: int):
    """异步添加商品到购物车"""
    try:
        cart = ShoppingCart()  # 假设这里是从数据库获取购物车实例
        product = Product(product_id, "Product Name", 10.99)  # 假设这里是从数据库获取商品实例
        cart.add_product(product, quantity)
        return {"cart_id": cart_id, "product_id": product_id, "quantity": quantity}
    except Exception as e:
        return {"error": str(e)}

# 示例：添加商品到购物车
# result = add_product_to_cart_async(1, 100, 2)
# print(result)

if __name__ == '__main__':
    # 这里可以运行Celery worker
    app.start()