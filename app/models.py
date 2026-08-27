from datetime import datetime
from app import db


# Association Table for Many-to-Many between Orders and Products
order_items = db.Table(
    'order_items',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False),
    db.Column('quantity', db.Integer, nullable=False, default=1),
    db.Column('unit_price', db.Numeric(10, 2), nullable=False)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, server_default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self, include_products=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        if include_products:
            data['products'] = [product.to_dict() for product in self.products]
        return data


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship linking Products through order_items junction table
    products = db.relationship(
        'Product',
        secondary=order_items,
        backref=db.backref('orders', lazy='dynamic'),
        lazy='dynamic'
    )

    def to_dict(self, include_items=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': float(self.total_amount),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_items:
            # Query order_items for this order
            items = db.session.execute(
                order_items.select().where(order_items.c.order_id == self.id)
            ).fetchall()
            data['items'] = [
                {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'product': Product.query.get(item.product_id).to_dict() if Product.query.get(item.product_id) else None
                }
                for item in items
            ]
        return data
