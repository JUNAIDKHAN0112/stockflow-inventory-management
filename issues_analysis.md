# Code Review – Issues & Production Risks

This document lists technical and business logic problems found in the original
`create_product` API and explains why they fail in a real production environment.

---

## ❌ Identified Issues

### 1. No Transaction Safety
- Two separate `commit()` calls are used.
- If inventory creation fails, product remains saved.

🔴 **Impact:**  
Partial data persistence leads to inconsistent inventory and orphan records.

---

### 2. Product Incorrectly Coupled with Warehouse
- Product model contains `warehouse_id`.
- Products must exist across multiple warehouses.

🔴 **Impact:**  
Impossible to scale inventory across warehouses.

---

### 3. SKU Uniqueness Not Enforced
- No validation or DB constraint check.

🔴 **Impact:**  
Duplicate SKUs break catalog, integrations, and order processing.

---

### 4. No Input Validation
- Missing required fields cause runtime crashes.

🔴 **Impact:**  
API returns 500 errors instead of user-friendly responses.

---

### 5. Price Stored Without Precision Handling
- Price likely stored as float.

🔴 **Impact:**  
Floating-point rounding errors affect billing and reporting.

---

### 6. Inventory Creation Is Mandatory
- Assumes `initial_quantity` always exists.

🔴 **Impact:**  
Fails when products are created before stocking.

---

### 7. No Company Context (Multi-Tenancy Risk)
- No `company_id` usage or validation.

🔴 **Impact:**  
Data leakage between tenants in SaaS environment.

---

### 8. No Error Handling
- Integrity or DB failures not caught.

🔴 **Impact:**  
Unclear API failures and poor user experience.

---

## ✅ Summary

The original code works only in ideal conditions.
In production, it causes:
- Data corruption
- Scalability limitations
- Security risks
- Poor API reliability
