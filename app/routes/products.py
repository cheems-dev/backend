from flask import request, jsonify
from flask_restx import Resource, fields
from app import db
from app.models.product import Product

# This function will be called from __init__.py
def register_routes(api):
    # Define models for request/response documentation
    product_model = api.model('Product', {
        'id': fields.Integer(readonly=True, description='Product ID'),
        'name': fields.String(required=True, description='Product name'),
        'unitPrice': fields.Float(required=True, description='Product unit price'),
        'createdAt': fields.DateTime(readonly=True),
        'updatedAt': fields.DateTime(readonly=True)
    })
    
    product_input_model = api.model('ProductInput', {
        'name': fields.String(required=True, description='Product name'),
        'unitPrice': fields.Float(required=True, description='Product unit price')
    })
    
    @api.route('/')
    class ProductList(Resource):
        @api.doc('list_products')
        @api.marshal_list_with(product_model)
        def get(self):
            """List all products"""
            products = Product.query.all()
            return [product.to_dict() for product in products]
        
        @api.doc('create_product')
        @api.expect(product_input_model)
        @api.marshal_with(product_model, code=201)
        def post(self):
            """Create a new product"""
            data = request.get_json() or {}
            
            if 'name' not in data or 'unitPrice' not in data:
                api.abort(400, 'Must include name and unitPrice fields')
            
            product = Product.from_dict(data)
            db.session.add(product)
            db.session.commit()
            
            return product.to_dict(), 201
    
    @api.route('/<int:id>')
    @api.param('id', 'The product identifier')
    @api.response(404, 'Product not found')
    class ProductItem(Resource):
        @api.doc('get_product')
        @api.marshal_with(product_model)
        def get(self, id):
            """Get a product by ID"""
            product = Product.query.get_or_404(id)
            return product.to_dict()
        
        @api.doc('update_product')
        @api.expect(product_input_model)
        @api.marshal_with(product_model)
        def put(self, id):
            """Update a product"""
            product = Product.query.get_or_404(id)
            data = request.get_json() or {}
            
            if 'name' in data:
                product.name = data['name']
            if 'unitPrice' in data:
                product.unit_price = data['unitPrice']
            
            db.session.commit()
            return product.to_dict()
        
        @api.doc('delete_product')
        @api.response(204, 'Product deleted')
        def delete(self, id):
            """Delete a product"""
            product = Product.query.get_or_404(id)
            db.session.delete(product)
            db.session.commit()
            return '', 204 