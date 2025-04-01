from app import create_app, db
from app.models import Product, Order, OrderItem
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Product': Product,
        'Order': Order,
        'OrderItem': OrderItem
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 