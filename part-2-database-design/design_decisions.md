# Database Design Decisions & Reasoning

This document explains key architectural decisions made for the StockFlow database.

---

## Product vs Inventory Separation
Products are warehouse-independent.
Inventory is tracked per warehouse.

This allows:
- Multi-warehouse support
- Stock transfers
- Centralized catalog

---

## SKU Uniqueness
SKU is globally unique.

Prevents:
- Duplicate products
- Order fulfillment issues

---

## Inventory Audit Trail
Inventory changes are logged.

Enables:
- Compliance
- Debugging
- Analytics

---

## Multi-Tenant Safety
Entities reference company_id.

Ensures:
- Data isolation
- SaaS scalability

---

## Supplier Modeling
Products can have multiple suppliers.

Supports:
- Backup vendors
- Reordering workflows

---

## Bundles
Bundles are self-referencing products.

Allows:
- Kits
- Combos
- Nested inventory

---

## Open Questions
- Can suppliers be shared across companies?
- Are bundles sellable?
- Is backordering allowed?
