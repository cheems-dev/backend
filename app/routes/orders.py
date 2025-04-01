from flask import request, jsonify
from flask_restx import Resource, fields
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product

# This function will be called from __init__.py
def register_routes(api):
    # Define models for request/response documentation
    order_item_model = api.model('OrderItem', {
        'id': fields.Integer(readonly=True, description='Order item ID'),
        'productId': fields.Integer(required=True, description='Product ID'),
        'name': fields.String(readonly=True, description='Product name'),
        'quantity': fields.Integer(required=True, description='Quantity'),
        'unitPrice': fields.Float(readonly=True, description='Unit price'),
        'totalPrice': fields.Float(readonly=True, description='Total price')
    })
    
    order_model = api.model('Order', {
        'id': fields.Integer(readonly=True, description='Order ID'),
        'orderNumber': fields.String(required=True, description='Order number'),
        'date': fields.DateTime(readonly=True, description='Order date'),
        'status': fields.String(description='Order status'),
        'products': fields.List(fields.Nested(order_item_model), description='Order items'),
        'productCount': fields.Integer(readonly=True, description='Product count'),
        'finalPrice': fields.Float(readonly=True, description='Final price'),
        'createdAt': fields.DateTime(readonly=True),
        'updatedAt': fields.DateTime(readonly=True)
    })
    
    order_input_model = api.model('OrderInput', {
        'orderNumber': fields.String(required=True, description='Order number'),
        'status': fields.String(description='Order status'),
        'products': fields.List(fields.Nested(api.model('OrderItemInput', {
            'id': fields.Integer(required=True, description='Product ID'),
            'quantity': fields.Integer(required=True, description='Quantity')
        })), description='Order items')
    })
    
    @api.route('/')
    class OrderList(Resource):
        @api.doc('list_orders')
        @api.marshal_list_with(order_model)
        def get(self):
            """List all orders"""
            orders = Order.query.all()
            return [order.to_dict() for order in orders]
        
        @api.doc('create_order')
        @api.expect(order_input_model)
        @api.marshal_with(order_model, code=201)
        def post(self):
            """Create a new order"""
            data = request.get_json() or {}
            
            if 'orderNumber' not in data:
                api.abort(400, 'Must include orderNumber field')
            
            # Check if order number already exists
            existing = Order.query.filter_by(order_number=data['orderNumber']).first()
            if existing:
                api.abort(400, 'Order number already exists')
            
            order = Order.from_dict(data)
            
            # Add order items
            if 'products' in data:
                for item_data in data['products']:
                    product_id = item_data.get('id')
                    quantity = item_data.get('quantity', 1)
                    
                    # Get product to get current price
                    product = Product.query.get(product_id)
                    if not product:
                        continue
                        
                    # Create order item
                    order_item = OrderItem(
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=product.unit_price
                    )
                    order.items.append(order_item)
            
            db.session.add(order)
            db.session.commit()
            
            return order.to_dict(), 201
    
    @api.route('/<int:id>')
    @api.param('id', 'The order identifier')
    @api.response(404, 'Order not found')
    class OrderItem(Resource):
        @api.doc('get_order')
        @api.marshal_with(order_model)
        def get(self, id):
            """Get an order by ID"""
            order = Order.query.get_or_404(id)
            return order.to_dict()
        
        @api.doc('update_order')
        @api.expect(order_input_model)
        @api.marshal_with(order_model)
        def put(self, id):
            """Update an order"""
            order = Order.query.get_or_404(id)
            
            # Don't allow editing completed orders
            if order.status == 'Completed':
                api.abort(400, 'Cannot edit completed orders')
                
            data = request.get_json() or {}
            
            if 'orderNumber' in data:
                # Check if new order number already exists (if changed)
                if data['orderNumber'] != order.order_number:
                    existing = Order.query.filter_by(order_number=data['orderNumber']).first()
                    if existing:
                        api.abort(400, 'Order number already exists')
                order.order_number = data['orderNumber']
            
            if 'status' in data:
                order.status = data['status']
            
            # Update order items
            if 'products' in data:
                # Remove existing items
                for item in order.items:
                    db.session.delete(item)
                
                # Add new items
                for item_data in data['products']:
                    product_id = item_data.get('id')
                    quantity = item_data.get('quantity', 1)
                    
                    # Get product to get current price
                    product = Product.query.get(product_id)
                    if not product:
                        continue
                        
                    # Create order item
                    order_item = OrderItem(
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=product.unit_price
                    )
                    order.items.append(order_item)
            
            db.session.commit()
            return order.to_dict()
        
        @api.doc('delete_order')
        @api.response(204, 'Order deleted')
        def delete(self, id):
            """Delete an order"""
            order = Order.query.get_or_404(id)
            
            # Don't allow deleting completed orders
            if order.status == 'Completed':
                api.abort(400, 'Cannot delete completed orders')
                
            db.session.delete(order)
            db.session.commit()
            return '', 204 