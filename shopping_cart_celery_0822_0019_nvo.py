# 代码生成时间: 2025-08-22 00:19:47
import celery
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

# 初始化Flask应用和数据库
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义商品模型
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

# 定义购物车模型
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='cart_items')

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }

# 配置Celery
celery_app = celery.Celery(
    app.name,
    broker='amqp://guest@localhost//'
)

# 异步任务：添加商品到购物车
@shared_task(bind=True)
def add_product_to_cart(self, cart_id, product_id, quantity):
    try:
        cart = Cart.query.get(cart_id)
        if not cart:
            raise ValueError('Cart not found')

        product = Product.query.get(product_id)
        if not product:
            raise ValueError('Product not found')

        cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        return cart_item.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError("Error adding product to cart: " + str(e))
    except Exception as e:
        raise ValueError("Error adding product to cart: " + str(e))

# 异步任务：计算购物车总价
@shared_task(bind=True)
def calculate_cart_total(self, cart_id):
    try:
        cart = Cart.query.get(cart_id)
        if not cart:
            raise ValueError('Cart not found')

        total = 0
        for item in cart.products:
            product = Product.query.get(item.product_id)
            total += product.price * item.quantity

        return {"total": total}
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError("Error calculating cart total: " + str(e))
    except Exception as e:
        raise ValueError("Error calculating cart total: " + str(e))

# 定义路由：添加商品到购物车
@app.route('/add_product/<int:cart_id>/<int:product_id>/<int:quantity>', methods=['POST'])
def add_product(cart_id, product_id, quantity):
    result = add_product_to_cart.delay(cart_id, product_id, quantity)
    if result.ready():
        return jsonify(result.get())
    else:
        return jsonify({'error': 'Task not completed'}), 400

# 定义路由：计算购物车总价
@app.route('/calculate_total/<int:cart_id>', methods=['GET'])
def calculate_total(cart_id):
    result = calculate_cart_total.delay(cart_id)
    if result.ready():
        return jsonify(result.get())
    else:
        return jsonify({'error': 'Task not completed'}), 400

# 初始化数据库
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)