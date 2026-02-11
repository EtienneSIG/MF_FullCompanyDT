# Gold Layer - Star Schema Specifications

## 🎯 Overview

The **Gold Layer** contains analytics-ready **star schemas** optimized for:
- Fast query performance (pre-aggregated where needed)
- Business user-friendly naming
- Power BI Direct Lake semantic models
- Consistent grain and relationships

**Star Schema Pattern:**
```
        DimCustomer
              |
        DimProduct ── FactSales ── DimDate
              |            |
        DimEmployee  DimGeography
```

**Principles:**
- **Fact Tables:** Contain measures (revenue, quantity, costs) and foreign keys
- **Dimension Tables:** Contain descriptive attributes (names, categories, hierarchies)
- **Grain:** Clearly defined (e.g., one row per order line, one row per ticket)
- **Conformed Dimensions:** Shared across multiple facts (DimDate, DimCustomer, DimProduct)

---

## 🗂️ Conformed Dimensions

These dimensions are shared across all fact tables to enable cross-domain analysis.

### DimDate

**Grain:** One row per calendar date  
**Range:** 2019-01-01 to 2030-12-31  
**Records:** ~4,380

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date_id` | INT | YYYYMMDD surrogate key | 20240115 |
| `full_date` | DATE | Actual date | 2024-01-15 |
| `year` | INT | Calendar year | 2024 |
| `quarter` | INT | Calendar quarter (1-4) | 1 |
| `month` | INT | Month number (1-12) | 1 |
| `month_name` | STRING | Full month name | January |
| `week_of_year` | INT | ISO week (1-53) | 3 |
| `day_of_week` | INT | Day number (1=Monday, 7=Sunday) | 1 |
| `day_name` | STRING | Full day name | Monday |
| `is_weekend` | BOOLEAN | Saturday or Sunday | False |
| `is_holiday` | BOOLEAN | US federal holiday | False |
| `holiday_name` | STRING | Holiday name (if applicable) | NULL |
| `fiscal_year` | INT | Fiscal year (starts July 1) | 2024 |
| `fiscal_quarter` | STRING | Fiscal quarter | FY24-Q3 |
| `fiscal_month` | INT | Fiscal month (1-12) | 7 |

**Hierarchies:**
- Calendar: Year → Quarter → Month → Date
- Fiscal: Fiscal Year → Fiscal Quarter → Fiscal Month → Date

**SQL:**
```sql
CREATE TABLE DimDate AS
SELECT 
    CAST(date_format(date_col, 'yyyyMMdd') AS INT) AS date_id,
    date_col AS full_date,
    year(date_col) AS year,
    quarter(date_col) AS quarter,
    month(date_col) AS month,
    date_format(date_col, 'MMMM') AS month_name,
    weekofyear(date_col) AS week_of_year,
    dayofweek(date_col) AS day_of_week,
    date_format(date_col, 'EEEE') AS day_name,
    CASE WHEN dayofweek(date_col) IN (1, 7) THEN TRUE ELSE FALSE END AS is_weekend,
    FALSE AS is_holiday,  -- Populate via lookup table
    NULL AS holiday_name,
    CASE WHEN month(date_col) >= 7 THEN year(date_col) + 1 ELSE year(date_col) END AS fiscal_year,
    CONCAT('FY', 
        CASE WHEN month(date_col) >= 7 THEN year(date_col) + 1 ELSE year(date_col) END,
        '-Q',
        CASE 
            WHEN month(date_col) BETWEEN 7 AND 9 THEN 1
            WHEN month(date_col) BETWEEN 10 AND 12 THEN 2
            WHEN month(date_col) BETWEEN 1 AND 3 THEN 3
            ELSE 4
        END
    ) AS fiscal_quarter,
    CASE WHEN month(date_col) >= 7 THEN month(date_col) - 6 ELSE month(date_col) + 6 END AS fiscal_month
FROM (SELECT explode(sequence(to_date('2019-01-01'), to_date('2030-12-31'), interval 1 day)) AS date_col)
```

---

### DimCustomer

**Grain:** One row per unique customer (SCD Type 1 - current state only)  
**Source:** Silver_Customers  
**Records:** ~50,000

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `customer_key` | INT | Surrogate key (auto-increment) | 1 |
| `customer_id` | STRING | Business key from CRM | CUST-000123 |
| `customer_name` | STRING | Company or person name | Acme Corporation |
| `industry` | STRING | Standardized industry | Technology |
| `customer_segment` | STRING | SMB/Mid-Market/Enterprise | Enterprise |
| `country_code` | STRING | ISO 2-letter code | US |
| `country_name` | STRING | Full country name | United States |
| `region` | STRING | Geographic region | North America |
| `annual_revenue` | DECIMAL(15,2) | Annual revenue ($) | 50000000.00 |
| `employee_count` | INT | Number of employees | 500 |
| `credit_limit` | DECIMAL(12,2) | Credit limit ($) | 100000.00 |
| `is_active` | BOOLEAN | Currently active customer | True |
| `first_purchase_date` | DATE | Date of first order | 2020-05-10 |
| `lifetime_value` | DECIMAL(15,2) | Total revenue to date | 2500000.00 |

**Hierarchies:**
- Geography: Region → Country → Customer
- Segment: Segment → Industry → Customer

---

### DimProduct

**Grain:** One row per unique product (SCD Type 1)  
**Source:** Silver_Products  
**Records:** ~5,000

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `product_key` | INT | Surrogate key | 1 |
| `product_id` | STRING | Business key (SKU) | PRD-12345 |
| `product_name` | STRING | Product name | Widget Pro 3000 |
| `category_l1` | STRING | Top-level category | Electronics |
| `category_l2` | STRING | Sub-category | Computers |
| `category_l3` | STRING | Product family | Laptops |
| `supplier_name` | STRING | Primary supplier | TechSupply Inc |
| `list_price` | DECIMAL(10,2) | MSRP | 1299.99 |
| `cost_price` | DECIMAL(10,2) | Cost per unit | 799.99 |
| `gross_margin_pct` | DECIMAL(5,2) | (List - Cost) / List * 100 | 38.47 |
| `is_discontinued` | BOOLEAN | No longer sold | False |
| `product_lifecycle` | STRING | Introduction/Growth/Maturity/Decline | Growth |
| `launch_date` | DATE | Product launch date | 2023-03-15 |

**Hierarchies:**
- Category: L1 → L2 → L3 → Product
- Lifecycle: Lifecycle → Product

---

### DimEmployee

**Grain:** One row per employee (SCD Type 1 - active employees only)  
**Source:** Silver_Employees (filtered to is_active = True)  
**Records:** ~8,500 (excludes 1,500 terminated)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `employee_key` | INT | Surrogate key | 1 |
| `employee_id` | STRING | Business key | EMP-12345 |
| `full_name` | STRING | First + Last name | Jane Smith |
| `email` | STRING | Work email | jane.smith@company.com |
| `department` | STRING | Standardized department | Sales |
| `job_title` | STRING | Job title | Account Executive |
| `manager_name` | STRING | Direct manager | John Doe |
| `hire_date` | DATE | Hire date | 2019-06-01 |
| `tenure_years` | DECIMAL(5,2) | Years employed | 4.58 |
| `salary_band` | STRING | Anonymized band | Band B (Mid) |
| `location` | STRING | Office location | New York, NY |
| `region` | STRING | Office region | Northeast |

**Hierarchies:**
- Org: Department → Manager → Employee
- Geography: Region → Location → Employee

---

### DimGeography

**Grain:** One row per unique location (city level)  
**Source:** Derived from Silver_Customers and Silver_Employees  
**Records:** ~500

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `geography_key` | INT | Surrogate key | 1 |
| `city` | STRING | City name | San Francisco |
| `state` | STRING | State/province | California |
| `country_code` | STRING | ISO code | US |
| `country_name` | STRING | Full country name | United States |
| `region` | STRING | Business region | West |
| `continent` | STRING | Continent | North America |
| `latitude` | DECIMAL(9,6) | Latitude | 37.774929 |
| `longitude` | DECIMAL(9,6) | Longitude | -122.419418 |
| `timezone` | STRING | Timezone | America/Los_Angeles |

**Hierarchies:**
- Geo: Continent → Region → Country → State → City

---

## 📊 Fact Tables

### FactSales

**Grain:** One row per order line (product sold in an order)  
**Source:** Silver_Orders + Silver_OrderLines  
**Records:** ~2,000,000

| Column | Type | Description | FK To |
|--------|------|-------------|-------|
| **Keys** | | | |
| `sales_key` | BIGINT | Surrogate key (PK) | - |
| `order_date_id` | INT | Order date | DimDate.date_id |
| `ship_date_id` | INT | Ship date | DimDate.date_id |
| `customer_key` | INT | Customer | DimCustomer.customer_key |
| `product_key` | INT | Product sold | DimProduct.product_key |
| `employee_key` | INT | Sales rep | DimEmployee.employee_key |
| `geography_key` | INT | Ship-to location | DimGeography.geography_key |
| **Degenerate Dimensions** | | | |
| `order_number` | STRING | Order ID (no separate dim) | - |
| `line_number` | INT | Line within order | - |
| **Measures** | | | |
| `quantity` | INT | Units sold | - |
| `unit_price` | DECIMAL(10,2) | Selling price per unit | - |
| `unit_cost` | DECIMAL(10,2) | Cost per unit | - |
| `discount_amount` | DECIMAL(10,2) | Total discount | - |
| `line_total` | DECIMAL(12,2) | Gross revenue (qty * unit_price) | - |
| `line_cost` | DECIMAL(12,2) | Total cost (qty * unit_cost) | - |
| `line_margin` | DECIMAL(12,2) | Gross profit (line_total - line_cost) | - |
| `tax_amount` | DECIMAL(10,2) | Sales tax | - |

**Indexes:**
- Clustered by: `order_date_id` (partitioned by year/month)
- Covering: customer_key, product_key

**SQL to Create:**
```sql
CREATE TABLE FactSales AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY o.order_number, ol.line_number) AS sales_key,
    CAST(date_format(o.order_date, 'yyyyMMdd') AS INT) AS order_date_id,
    CAST(date_format(o.ship_date, 'yyyyMMdd') AS INT) AS ship_date_id,
    dc.customer_key,
    dp.product_key,
    de.employee_key,
    dg.geography_key,
    o.order_number,
    ol.line_number,
    ol.quantity,
    ol.unit_price,
    ol.unit_cost,
    ol.discount_amount,
    (ol.quantity * ol.unit_price - ol.discount_amount) AS line_total,
    (ol.quantity * ol.unit_cost) AS line_cost,
    (ol.quantity * ol.unit_price - ol.discount_amount - ol.quantity * ol.unit_cost) AS line_margin,
    ol.tax_amount
FROM Silver_Orders o
INNER JOIN Silver_OrderLines ol ON o.order_number = ol.order_number
INNER JOIN DimCustomer dc ON o.customer_id = dc.customer_id
INNER JOIN DimProduct dp ON ol.product_id = dp.product_id
INNER JOIN DimEmployee de ON o.sales_rep_id = de.employee_id
INNER JOIN DimGeography dg ON o.ship_to_city = dg.city
```

---

### FactSupport

**Grain:** One row per support ticket  
**Source:** Silver_SupportTickets (AI-enriched)  
**Records:** ~100,000

| Column | Type | Description | FK To |
|--------|------|-------------|-------|
| **Keys** | | | |
| `support_key` | BIGINT | Surrogate key (PK) | - |
| `created_date_id` | INT | Ticket created date | DimDate.date_id |
| `resolved_date_id` | INT | Ticket resolved date | DimDate.date_id |
| `customer_key` | INT | Customer | DimCustomer.customer_key |
| `agent_key` | INT | Assigned agent | DimEmployee.employee_key |
| **Degenerate Dimensions** | | | |
| `ticket_id` | STRING | Ticket number | - |
| `ticket_category` | STRING | AI-classified category | - |
| `ticket_priority` | STRING | low/normal/high/urgent | - |
| `sentiment` | STRING | AI-detected sentiment | - |
| **Measures** | | | |
| `resolution_time_hours` | DECIMAL(10,2) | Time to resolve (hours) | - |
| `first_response_time_hours` | DECIMAL(10,2) | Time to first reply | - |
| `sla_target_hours` | INT | SLA target based on priority | - |
| `is_sla_met` | BOOLEAN | Resolved within SLA | - |
| `csat_score` | INT | Customer satisfaction (1-5) | - |
| `is_reopened` | BOOLEAN | Ticket reopened after close | - |

**Business Rules:**
- SLA Target: Urgent=4h, High=8h, Normal=24h, Low=48h
- is_sla_met: `resolution_time_hours <= sla_target_hours`

---

### FactHR

**Grain:** One row per employee per month (headcount snapshot)  
**Source:** Silver_Employees (historical snapshots)  
**Records:** ~60,000 (10K employees × 12 months × 0.5 avg tenure)

| Column | Type | Description | FK To |
|--------|------|-------------|-------|
| **Keys** | | | |
| `hr_key` | BIGINT | Surrogate key (PK) | - |
| `snapshot_date_id` | INT | End of month date | DimDate.date_id |
| `employee_key` | INT | Employee | DimEmployee.employee_key |
| `manager_key` | INT | Manager (self-join) | DimEmployee.employee_key |
| **Measures** | | | |
| `is_active` | BOOLEAN | Still employed | - |
| `tenure_months` | INT | Months employed | - |
| `attrition_flag` | BOOLEAN | Left this month | - |
| `promotion_flag` | BOOLEAN | Promoted this month | - |
| `salary_band_numeric` | INT | Anonymized band (1-10) | - |

**Use Case:**
- Headcount trends: COUNT(DISTINCT employee_key) WHERE is_active = True
- Attrition rate: SUM(attrition_flag) / COUNT(employee_key)

---

### FactInventory

**Grain:** One row per product per day (snapshot)  
**Source:** Silver_Inventory (daily snapshots)  
**Records:** ~1,800,000 (5K products × 365 days)

| Column | Type | Description | FK To |
|--------|------|-------------|-------|
| **Keys** | | | |
| `inventory_key` | BIGINT | Surrogate key (PK) | - |
| `snapshot_date_id` | INT | Snapshot date | DimDate.date_id |
| `product_key` | INT | Product | DimProduct.product_key |
| `warehouse_key` | INT | Warehouse location | DimGeography.geography_key |
| **Measures** | | | |
| `units_on_hand` | INT | Current stock level | - |
| `units_on_order` | INT | Incoming from suppliers | - |
| `reorder_point` | INT | Min stock before reorder | - |
| `is_stockout` | BOOLEAN | units_on_hand = 0 | - |
| `days_of_supply` | DECIMAL(5,1) | On-hand / avg daily demand | - |
| `inventory_value` | DECIMAL(12,2) | units_on_hand * cost_price | - |

---

### FactMarketing

**Grain:** One row per campaign per day  
**Source:** Silver_Campaigns + Silver_WebAnalytics  
**Records:** ~365,000 (1K campaigns × 365 days)

| Column | Type | Description | FK To |
|--------|------|-------------|-------|
| **Keys** | | | |
| `marketing_key` | BIGINT | Surrogate key (PK) | - |
| `activity_date_id` | INT | Activity date | DimDate.date_id |
| `campaign_id` | STRING | Campaign identifier | - |
| `campaign_type` | STRING | Email/Social/Search/Display | - |
| **Measures** | | | |
| `impressions` | INT | Ad impressions | - |
| `clicks` | INT | Ad clicks | - |
| `conversions` | INT | Leads/sales | - |
| `spend_amount` | DECIMAL(12,2) | Campaign cost | - |
| `revenue_amount` | DECIMAL(12,2) | Attributed revenue | - |
| `ctr_pct` | DECIMAL(5,2) | Click-through rate | - |
| `cpc` | DECIMAL(8,2) | Cost per click | - |
| `roas` | DECIMAL(8,2) | Return on ad spend | - |

---

## 🔗 Relationships

### Relationship Matrix

| From (Fact) | To (Dimension) | Cardinality | Filter Direction |
|------------|----------------|-------------|------------------|
| FactSales | DimDate | Many-to-One | Single |
| FactSales | DimCustomer | Many-to-One | Single |
| FactSales | DimProduct | Many-to-One | Single |
| FactSales | DimEmployee | Many-to-One | Single |
| FactSupport | DimDate | Many-to-One | Single |
| FactSupport | DimCustomer | Many-to-One | Single |
| FactSupport | DimEmployee | Many-to-One | Single |
| FactHR | DimDate | Many-to-One | Single |
| FactHR | DimEmployee | Many-to-One | Single |
| FactInventory | DimDate | Many-to-One | Single |
| FactInventory | DimProduct | Many-to-One | Single |

**Visual:**
```
DimDate (date_id) ─────┬─── FactSales (order_date_id)
                       ├─── FactSupport (created_date_id)
                       ├─── FactHR (snapshot_date_id)
                       └─── FactInventory (snapshot_date_id)

DimCustomer (customer_key) ─┬─── FactSales
                             └─── FactSupport

DimProduct (product_key) ────┬─── FactSales
                              └─── FactInventory

DimEmployee (employee_key) ──┬─── FactSales (sales_rep)
                              ├─── FactSupport (agent)
                              └─── FactHR (employee)
```

---

## ⚡ Optimization Techniques

### Delta Table Optimization

**Z-Ordering:**
```sql
OPTIMIZE FactSales ZORDER BY (order_date_id, customer_key)
```
- Benefits: Faster filtering on date and customer
- Run: Weekly or after large loads

**Partitioning:**
```python
df_fact_sales.write \
    .format("delta") \
    .partitionBy("year", "month") \
    .save("Tables/FactSales")
```
- Benefits: Partition pruning for date range queries
- Trade-off: More files = slower listing (keep partitions > 1GB)

**Vacuuming:**
```sql
VACUUM FactSales RETAIN 168 HOURS  -- 7 days
```
- Removes old file versions to save storage

---

### Aggregation Tables

**Pre-Aggregate for Common Queries:**

**Example: Daily Sales Summary**
```sql
CREATE TABLE FactSalesSummary_Daily AS
SELECT 
    order_date_id,
    customer_key,
    product_key,
    SUM(quantity) AS total_quantity,
    SUM(line_total) AS total_revenue,
    SUM(line_margin) AS total_margin,
    COUNT(DISTINCT order_number) AS order_count
FROM FactSales
GROUP BY order_date_id, customer_key, product_key
```

**Benefits:**
- 100x faster queries (2M rows → 20K rows)
- Use for dashboards, not detailed drilldowns

---

## 📋 Gold Tables Summary

| Table | Type | Grain | Records | Size (MB) |
|-------|------|-------|---------|-----------|
| DimDate | Dimension | One row per date | 4,380 | <1 |
| DimCustomer | Dimension | One row per customer | 50,000 | 5 |
| DimProduct | Dimension | One row per product | 5,000 | 1 |
| DimEmployee | Dimension | One row per employee | 8,500 | 1 |
| DimGeography | Dimension | One row per city | 500 | <1 |
| FactSales | Fact | One row per order line | 2,000,000 | 120 |
| FactSupport | Fact | One row per ticket | 100,000 | 8 |
| FactHR | Fact | One row per employee per month | 60,000 | 4 |
| FactInventory | Fact | One row per product per day | 1,800,000 | 80 |
| FactMarketing | Fact | One row per campaign per day | 365,000 | 20 |

**Total Gold Storage:** ~240 MB (uncompressed), ~60 MB (Delta compressed)

---

## ✅ Gold Layer Checklist

- [ ] All dimensions created with surrogate keys
- [ ] DimDate populated with full date range (2019-2030)
- [ ] All fact tables reference dimensions via surrogate keys
- [ ] Relationships validated (no orphaned foreign keys)
- [ ] Indexes/z-ordering applied for performance
- [ ] Aggregation tables created for common queries
- [ ] Tables partitioned by date where appropriate
- [ ] Data validated: COUNT, SUM matches Silver layer
- [ ] Semantic model created with relationships configured
- [ ] Direct Lake mode verified (no import-only tables)

**Gold layer complete! Ready for Power BI semantic model ➡️**
