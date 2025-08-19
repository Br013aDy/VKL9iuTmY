# 代码生成时间: 2025-08-19 11:12:10
import json
from celery import Celery
from celery import shared_task
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_cart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the CartItem model
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        """Convert cart item to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'quantity': self.quantity
        }

# Initialize Celery
celery_app = Celery(
    __name__,
    broker='amqp://guest@localhost//'
)

# Define a Celery task to add a product to the cart
@shared_task
def add_product_to_cart(user_id, product_id, quantity):
    """Add a product to the cart."""
    try:
        # Create a new CartItem instance
        item = CartItem(
            product_id=product_id,
            user_id=user_id,
            quantity=quantity
        )
        db.session.add(item)
        db.session.commit()
        return item.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Database error: {e}")

# Define a Flask route to handle cart creation
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add a product to the cart."""
    data = request.get_json()
    try:
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']
        
        # Execute the Celery task
        result = add_product_to_cart.delay(user_id, product_id, quantity)
        return jsonify({'message': 'Product added to cart', 'task_id': result.id}), 200
    except KeyError as e:
        return jsonify({'error': f'Missing data: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create the database tables
    db.create_all()
    # Start the Flask development server
    app.run(debug=True)