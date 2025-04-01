from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace
from app.config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Order Management API",
    version="1.0",
    description="API for managing products and orders",
    doc="/api/docs"
)

# Create namespaces
products_ns = Namespace('products', description='Product operations')
orders_ns = Namespace('orders', description='Order operations')

# Add namespaces to API
api.add_namespace(products_ns, path='/api/products')
api.add_namespace(orders_ns, path='/api/orders')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS to allow requests from any origin
    CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Import routes with API namespaces
    from app.routes.products import register_routes as register_product_routes
    from app.routes.orders import register_routes as register_order_routes
    
    # Register routes with namespaces
    register_product_routes(products_ns)
    register_order_routes(orders_ns)
    
    # Initialize API with the app
    api.init_app(app)
    
    # Add basic endpoints
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    @app.route('/api')
    def api_root():
        return jsonify({
            'message': 'Welcome to the API',
            'endpoints': {
                'products': '/api/products',
                'orders': '/api/orders',
                'health': '/api/health',
                'documentation': '/api/docs'
            },
            'version': '1.0'
        })
    
    @app.route('/')
    def app_root():
        return jsonify({
            'message': 'API server is running',
            'api_root': '/api',
            'api_docs': '/api/docs'
        })
    
    # Initialize database if it doesn't exist
    with app.app_context():
        if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')):
            db.create_all()
    
    return app 