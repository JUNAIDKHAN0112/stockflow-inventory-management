-- ===============================
-- StockFlow Inventory DB Schema
-- ===============================

CREATE TABLE companies (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE warehouses (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id),
    warehouse_id BIGINT REFERENCES warehouses(id),
    quantity INT NOT NULL CHECK (quantity >= 0),
    UNIQUE (product_id, warehouse_id)
);

CREATE TABLE inventory_movements (
    id BIGSERIAL PRIMARY KEY,
    inventory_id BIGINT REFERENCES inventory(id),
    change INT NOT NULL,
    reason VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE suppliers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);

CREATE TABLE product_suppliers (
    product_id BIGINT REFERENCES products(id),
    supplier_id BIGINT REFERENCES suppliers(id),
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE bundles (
    parent_product_id BIGINT REFERENCES products(id),
    child_product_id BIGINT REFERENCES products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (parent_product_id, child_product_id)
);
