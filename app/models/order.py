from app import db
from datetime import datetime

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    
    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unitPrice': self.unit_price,
            'totalPrice': self.quantity * self.unit_price
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  # Pending, InProgress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    @property
    def product_count(self):
        return len(self.items)
    
    @property
    def final_price(self):
        return sum(item.quantity * item.unit_price for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'orderNumber': self.order_number,
            'date': self.date.isoformat(),
            'status': self.status,
            'products': [item.to_dict() for item in self.items],
            'productCount': self.product_count,
            'finalPrice': self.final_price,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        return Order(
            order_number=data.get('orderNumber'),
            status=data.get('status', 'Pending')
        ) 