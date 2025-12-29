from datetime import datetime, timedelta
from flask import jsonify

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    """
    Returns low stock alerts for a company across all warehouses.
    Assumptions:
    - Recent sales = last 30 days
    - Threshold is defined per product type
    """

    recent_sales_cutoff = datetime.utcnow() - timedelta(days=30)

    query = """
        SELECT
            p.id AS product_id,
            p.name AS product_name,
            p.sku,
            w.id AS warehouse_id,
            w.name AS warehouse_name,
            i.quantity AS current_stock,
            t.threshold,
            s.id AS supplier_id,
            s.name AS supplier_name,
            s.contact_email,
            COALESCE(AVG(sa.quantity), 0) AS avg_daily_sales
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        JOIN warehouses w ON i.warehouse_id = w.id
        JOIN product_thresholds t ON p.type = t.product_type
        JOIN product_suppliers ps ON p.id = ps.product_id
        JOIN suppliers s ON ps.supplier_id = s.id
        LEFT JOIN sales sa
            ON sa.product_id = p.id
           AND sa.created_at >= :recent_sales_cutoff
        WHERE p.company_id = :company_id
          AND i.quantity < t.threshold
        GROUP BY
            p.id, w.id, i.quantity, t.threshold,
            s.id, s.name, s.contact_email
    """

    results = db.session.execute(query, {
        "company_id": company_id,
        "recent_sales_cutoff": recent_sales_cutoff
    })

    alerts = []

    for row in results:
        if row.avg_daily_sales == 0:
            continue  # Skip products without recent sales

        days_until_stockout = int(row.current_stock / row.avg_daily_sales)

        alerts.append({
            "product_id": row.product_id,
            "product_name": row.product_name,
            "sku": row.sku,
            "warehouse_id": row.warehouse_id,
            "warehouse_name": row.warehouse_name,
            "current_stock": row.current_stock,
            "threshold": row.threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": row.supplier_id,
                "name": row.supplier_name,
                "contact_email": row.contact_email
            }
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })
