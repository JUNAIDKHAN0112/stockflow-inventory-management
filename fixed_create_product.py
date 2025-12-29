from decimal import Decimal
from sqlalchemy.exc import IntegrityError

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # ---- Input Validation ----
    required_fields = ['name', 'sku', 'price', 'company_id']
    for field in required_fields:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    try:
        # ---- Atomic Transaction ----
        with db.session.begin():

            # Create product (warehouse independent)
            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=Decimal(data['price']),
                company_id=data['company_id']
            )
            db.session.add(product)
            db.session.flush()  # Ensures product.id is available

            # Optional initial inventory
            if 'warehouse_id' in data and 'initial_quantity' in data:
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=data['warehouse_id'],
                    quantity=data['initial_quantity']
                )
                db.session.add(inventory)

    except IntegrityError:
        return {"error": "SKU already exists"}, 409

    return {
        "message": "Product created successfully",
        "product_id": product.id
    }, 201
