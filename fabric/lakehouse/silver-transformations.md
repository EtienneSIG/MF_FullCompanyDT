# Silver Layer - Data Quality & Transformation Rules

## 🎯 Overview

The **Silver Layer** is the "cleaned and conformed" zone where we apply:
- Data quality improvements
- Standardization and normalization
- Business rules and validations
- Deduplication
- Slowly Changing Dimension (SCD) logic

**Principles:**
- One source of truth per business entity
- Consistent data types, formats, naming conventions
- Referential integrity enforced
- Audit columns maintained: `_created_at`, `_updated_at`, `_is_current`

---

## 🔄 Bronze → Silver Transformation Pattern

### General Workflow

```python
# 1. Read Bronze table
df_bronze = spark.read.format("delta").load("Tables/Bronze_CRM_Customers")

# 2. Apply transformations
df_silver = df_bronze \
    .dropDuplicates(["account_id"]) \
    .filter(col("account_name").isNotNull()) \
    .withColumn("industry", standardize_industry(col("industry"))) \
    .withColumn("country_code", map_country_to_code(col("billing_country"))) \
    .withColumn("_created_at", current_timestamp()) \
    .withColumn("_updated_at", current_timestamp())

# 3. Write to Silver
df_silver.write.format("delta").mode("overwrite").save("Tables/Silver_Customers")
```

---

## 🧹 Data Quality Rules

### Rule 1: Deduplication

**Problem:** Source system has duplicate records (e.g., same customer ID appears twice)

**Solution:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, desc

# Keep latest record based on last_modified_date
window = Window.partitionBy("customer_id").orderBy(desc("last_modified_date"))

df_deduped = df_bronze \
    .withColumn("row_num", row_number().over(window)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")
```

**Applied To:**
- Customers (Salesforce syncs may create duplicates)
- Products (manual entry errors)
- Employees (Workday exports can have overlapping effective dates)

---

### Rule 2: Null Handling

**Required Fields:** Must not be null

| Table | Required Columns | Action if Null |
|-------|------------------|----------------|
| Customers | customer_id, customer_name | **Reject** record, log error |
| Orders | order_id, order_date, customer_id | **Reject** |
| Products | product_id, product_name, category_id | **Reject** |

**Optional Fields:** Can be null but need defaults

| Column | Default Value | Logic |
|--------|---------------|-------|
| `phone` | "Unknown" | If null, set to "Unknown" |
| `email` | "noemail@company.com" | If null, set placeholder |
| `discount_pct` | 0.0 | If null, assume no discount |

**Code:**

```python
df_cleaned = df_bronze \
    .filter(col("customer_id").isNotNull()) \
    .filter(col("customer_name").isNotNull()) \
    .withColumn("phone", when(col("phone").isNull(), "Unknown").otherwise(col("phone"))) \
    .withColumn("discount_pct", coalesce(col("discount_pct"), lit(0.0)))
```

---

### Rule 3: Data Type Enforcement

**Problem:** CSV files may have wrong types (e.g., dates as strings)

**Solution:**

```python
from pyspark.sql.functions import to_date, to_timestamp, col

df_typed = df_bronze \
    .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd")) \
    .withColumn("created_at", to_timestamp(col("created_at"), "yyyy-MM-dd HH:mm:ss")) \
    .withColumn("total_amount", col("total_amount").cast("decimal(12,2)")) \
    .withColumn("quantity", col("quantity").cast("int"))
```

**Validation:**

```python
# Check for failed conversions (will be null if cast fails)
invalid_dates = df_typed.filter(col("order_date").isNull()).count()
if invalid_dates > 0:
    print(f"⚠️ Warning: {invalid_dates} records with invalid order_date")
```

---

### Rule 4: Standardization

#### Country Names

**Problem:** Inconsistent country names: "USA", "United States", "US", "U.S.A."

**Solution:** Map to ISO codes

```python
country_mapping = {
    "USA": "US",
    "United States": "US",
    "U.S.A.": "US",
    "America": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "UK": "GB",
    "Great Britain": "GB"
}

# Create mapping expression
country_map_expr = create_map([lit(x) for pair in country_mapping.items() for x in pair])

df_standardized = df.withColumn(
    "country_code",
    when(col("billing_country").isin(list(country_mapping.keys())),
         country_map_expr[col("billing_country")]
    ).otherwise("OTHER")
)
```

#### Industry Categories

**Problem:** Free text industry names: "Tech", "Technology", "IT Services", "Software"

**Solution:** Map to standard taxonomy

```python
industry_mapping = {
    "Technology": ["Tech", "IT", "Software", "SaaS", "Cloud"],
    "Manufacturing": ["Manufacturing", "Industrial", "Factory"],
    "Retail": ["Retail", "E-commerce", "Consumer Goods"],
    "Financial Services": ["Banking", "Finance", "Insurance", "FinTech"],
    "Healthcare": ["Healthcare", "Medical", "Pharma", "Biotech"]
}

# Reverse mapping for lookup
industry_lookup = {v: k for k, vals in industry_mapping.items() for v in vals}

# Apply standardization
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def standardize_industry(raw_industry):
    return industry_lookup.get(raw_industry, "Other")

df = df.withColumn("industry_standard", standardize_industry(col("industry")))
```

#### Email Normalization

**Problem:** Emails with different casing: "John.Doe@ACME.com" vs "john.doe@acme.com"

**Solution:**

```python
from pyspark.sql.functions import lower, trim

df = df.withColumn("email", lower(trim(col("email"))))
```

---

### Rule 5: Business Logic Validation

#### Order Totals

**Rule:** `total_amount` must equal `subtotal + tax_amount`

```python
df_validated = df.withColumn(
    "calculated_total",
    col("subtotal") + col("tax_amount")
).withColumn(
    "total_mismatch",
    when(abs(col("total_amount") - col("calculated_total")) > 0.01, True).otherwise(False)
)

# Log mismatches
mismatches = df_validated.filter(col("total_mismatch") == True)
if mismatches.count() > 0:
    print(f"⚠️ {mismatches.count()} orders have total amount discrepancies")
    mismatches.select("order_id", "total_amount", "calculated_total").show(10)
```

#### Date Ranges

**Rule:** `ship_date` must be >= `order_date`

```python
df = df.withColumn(
    "invalid_ship_date",
    when(col("ship_date") < col("order_date"), True).otherwise(False)
)

# Fix: If ship_date < order_date, set ship_date = order_date
df = df.withColumn(
    "ship_date",
    when(col("invalid_ship_date") == True, col("order_date")).otherwise(col("ship_date"))
)
```

---

## 🏗️ Transformation Logic by Domain

### CRM Domain: Customers

**Bronze → Silver Transformations:**

| Step | Transformation | Code |
|------|----------------|------|
| 1 | Deduplicate by customer_id | `dropDuplicates(["customer_id"])` |
| 2 | Remove nulls in PK | `filter(col("customer_id").isNotNull())` |
| 3 | Standardize country | Map to ISO codes |
| 4 | Standardize industry | Map to taxonomy |
| 5 | Normalize email | `lower(trim(col("email")))` |
| 6 | Parse customer_segment | "SMB" if revenue < 1M, "Mid-Market" if < 50M, else "Enterprise" |
| 7 | Add audit columns | `_created_at`, `_updated_at` |

**Full Code:**

```python
from pyspark.sql.functions import *

df_bronze = spark.read.format("delta").load("Tables/Bronze_CRM_Customers")

df_silver = df_bronze \
    .dropDuplicates(["account_id"]) \
    .filter(col("account_id").isNotNull()) \
    .filter(col("account_name").isNotNull()) \
    .withColumn("country_code", country_map_expr[col("billing_country")]) \
    .withColumn("industry_standard", standardize_industry(col("industry"))) \
    .withColumn("email", lower(trim(col("email")))) \
    .withColumn("customer_segment",
        when(col("annual_revenue") < 1000000, "SMB")
        .when(col("annual_revenue") < 50000000, "Mid-Market")
        .otherwise("Enterprise")
    ) \
    .withColumn("_created_at", current_timestamp()) \
    .withColumn("_updated_at", current_timestamp()) \
    .select(
        col("account_id").alias("customer_id"),
        col("account_name").alias("customer_name"),
        "industry_standard",
        "country_code",
        "customer_segment",
        "annual_revenue",
        "employee_count",
        "email",
        "_created_at",
        "_updated_at"
    )

df_silver.write.format("delta").mode("overwrite").save("Tables/Silver_Customers")
```

---

### ERP Domain: Orders

**Bronze → Silver Transformations:**

| Step | Transformation | Code |
|------|----------------|------|
| 1 | Validate order_date not in future | `filter(col("order_date") <= current_date())` |
| 2 | Validate total = subtotal + tax | Add `total_mismatch` flag |
| 3 | Standardize order_status | Map "Pending", "Approved" → "Open"; "Shipped", "Invoiced" → "Closed" |
| 4 | Add fiscal year/quarter | Extract from order_date |
| 5 | Join to customers for validation | Ensure customer_id exists |

**Code:**

```python
df_bronze_orders = spark.read.format("delta").load("Tables/Bronze_ERP_Orders")
df_silver_customers = spark.read.format("delta").load("Tables/Silver_Customers")

df_silver_orders = df_bronze_orders \
    .filter(col("order_date") <= current_date()) \
    .withColumn("order_status_clean",
        when(col("order_status").isin(["Pending", "Approved"]), "Open")
        .when(col("order_status").isin(["Shipped", "Invoiced", "Closed"]), "Closed")
        .otherwise("Cancelled")
    ) \
    .withColumn("fiscal_year", year(col("order_date"))) \
    .withColumn("fiscal_quarter", concat(lit("Q"), quarter(col("order_date")))) \
    .join(
        df_silver_customers.select("customer_id"),
        on="customer_id",
        how="inner"  # Only keep orders with valid customers
    ) \
    .select(
        "order_number",
        "customer_id",
        "order_date",
        "order_status_clean",
        "subtotal",
        "tax_amount",
        "total_amount",
        "fiscal_year",
        "fiscal_quarter",
        current_timestamp().alias("_created_at"),
        current_timestamp().alias("_updated_at")
    )

df_silver_orders.write.format("delta").mode("overwrite").save("Tables/Silver_Orders")
```

---

### Support Domain: Tickets

**Bronze → Silver Transformations:**

| Step | Transformation | Code |
|------|----------------|------|
| 1 | Standardize status | Map "new", "open" → "Active"; "solved", "closed" → "Resolved" |
| 2 | Calculate resolution_time_hours | `(solved_at - created_at) / 3600` |
| 3 | Flag SLA breach | If resolution_time > 24 hours for "urgent" |
| 4 | Extract first response time | From ticket comments table (if available) |

**Code:**

```python
df_bronze_tickets = spark.read.format("delta").load("Tables/Bronze_Support_Tickets")

df_silver_tickets = df_bronze_tickets \
    .withColumn("status_clean",
        when(col("status").isin(["new", "open", "pending"]), "Active")
        .when(col("status").isin(["solved", "closed"]), "Resolved")
        .otherwise("Unknown")
    ) \
    .withColumn("resolution_time_hours",
        when(col("solved_at").isNotNull(),
            (unix_timestamp(col("solved_at")) - unix_timestamp(col("created_at"))) / 3600
        ).otherwise(None)
    ) \
    .withColumn("sla_breach",
        when(
            (col("priority") == "urgent") & (col("resolution_time_hours") > 24),
            True
        ).otherwise(False)
    ) \
    .select(
        "ticket_id",
        "customer_id",
        "agent_id",
        "subject",
        "description",  # Will be AI-enriched later
        "status_clean",
        "priority",
        "created_at",
        "solved_at",
        "resolution_time_hours",
        "sla_breach",
        current_timestamp().alias("_created_at"),
        current_timestamp().alias("_updated_at")
    )

df_silver_tickets.write.format("delta").mode("overwrite").save("Tables/Silver_SupportTickets")
```

---

### HR Domain: Employees

**Bronze → Silver Transformations:**

| Step | Transformation | Code |
|------|----------------|------|
| 1 | Calculate tenure_years | `(current_date - hire_date) / 365` |
| 2 | Flag active employees | `termination_date IS NULL` |
| 3 | Standardize department names | Map variations |
| 4 | Anonymize salary_band | Replace with ranges: "Band A", "Band B" |
| 5 | Validate manager_id exists | Self-join to employees table |

**Code:**

```python
from pyspark.sql.functions import datediff, when, current_date

df_bronze_employees = spark.read.format("delta").load("Tables/Bronze_HR_Employees")

df_silver_employees = df_bronze_employees \
    .withColumn("tenure_years",
        datediff(current_date(), col("hire_date")) / 365
    ) \
    .withColumn("is_active",
        when(col("termination_date").isNull(), True).otherwise(False)
    ) \
    .withColumn("department_clean",
        when(col("department").isin(["IT", "Information Technology", "Tech"]), "Technology")
        .when(col("department").isin(["HR", "Human Resources", "People"]), "Human Resources")
        .when(col("department").isin(["Sales", "Revenue"]), "Sales")
        .otherwise(col("department"))
    ) \
    .withColumn("salary_band_anon",
        when(col("salary_band").between(1, 3), "Band A (Entry)")
        .when(col("salary_band").between(4, 6), "Band B (Mid)")
        .when(col("salary_band").between(7, 9), "Band C (Senior)")
        .when(col("salary_band") >= 10, "Band D (Executive)")
        .otherwise("Unknown")
    ) \
    .select(
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "department_clean",
        "job_title",
        "manager_id",
        "hire_date",
        "termination_date",
        "tenure_years",
        "is_active",
        "salary_band_anon",  # Anonymized
        "location",
        current_timestamp().alias("_created_at"),
        current_timestamp().alias("_updated_at")
    )

df_silver_employees.write.format("delta").mode("overwrite").save("Tables/Silver_Employees")
```

---

## 📐 Slowly Changing Dimensions (SCD Type 2)

### Use Case: Track Product Price Changes

**Scenario:** Product price changes over time. We want to know historical prices.

**SCD Type 2 Logic:**

| product_id | product_name | price | effective_from | effective_to | is_current |
|------------|--------------|-------|----------------|--------------|------------|
| PRD-001 | Widget A | 19.99 | 2023-01-01 | 2023-06-30 | False |
| PRD-001 | Widget A | 24.99 | 2023-07-01 | 2024-12-31 | True |

**Implementation:**

```python
from delta.tables import DeltaTable

# New snapshot from Bronze
df_new = spark.read.format("delta").load("Tables/Bronze_ProductCatalog_Products") \
    .select("product_id", "product_name", "list_price", "cost_price")

# Existing Silver SCD table
silver_table = DeltaTable.forPath(spark, "Tables/Silver_Products_SCD")

# Merge logic
silver_table.alias("target").merge(
    df_new.alias("source"),
    "target.product_id = source.product_id AND target.is_current = TRUE"
).whenMatchedUpdate(
    condition="target.list_price != source.list_price",  # Price changed
    set={
        "is_current": "FALSE",
        "effective_to": "current_date()",
        "_updated_at": "current_timestamp()"
    }
).whenNotMatchedInsert(
    values={
        "product_id": "source.product_id",
        "product_name": "source.product_name",
        "list_price": "source.list_price",
        "cost_price": "source.cost_price",
        "effective_from": "current_date()",
        "effective_to": "to_date('9999-12-31')",
        "is_current": "TRUE",
        "_created_at": "current_timestamp()",
        "_updated_at": "current_timestamp()"
    }
).execute()

# Insert new row for changed products
df_changed = df_new.join(
    silver_table.toDF().filter(col("is_current") == True),
    on="product_id",
    how="inner"
).filter(col("list_price") != col("target.list_price"))

df_changed.select(
    "product_id",
    "product_name",
    "list_price",
    "cost_price",
    current_date().alias("effective_from"),
    to_date(lit("9999-12-31")).alias("effective_to"),
    lit(True).alias("is_current"),
    current_timestamp().alias("_created_at"),
    current_timestamp().alias("_updated_at")
).write.format("delta").mode("append").save("Tables/Silver_Products_SCD")
```

---

## 🧪 Data Quality Metrics (Silver)

### Metrics to Track

| Metric | Formula | Target | Alert Threshold |
|--------|---------|--------|-----------------|
| **Null Rate** | Nulls / Total Rows | < 1% | > 5% |
| **Duplicate Rate** | Duplicates / Total Rows | 0% | > 0.1% |
| **Referential Integrity** | Orphaned FKs / Total Rows | 0% | > 0% |
| **Standardization Coverage** | Standardized / Total | 100% | < 95% |

**Query Example:**

```sql
-- Null rate in customer_name
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_rows,
    (SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS null_rate_pct
FROM Silver_Customers
```

---

## 📋 Silver Tables Summary

| Silver Table | Bronze Source | Transformations Applied | Records (Demo) |
|-------------|---------------|-------------------------|----------------|
| `Silver_Customers` | Bronze_CRM_Customers | Dedup, standardize country/industry, segment | 50,000 |
| `Silver_Orders` | Bronze_ERP_Orders | Date validation, status mapping, fiscal year | 500,000 |
| `Silver_OrderLines` | Bronze_ERP_OrderLines | Join validation, calculate line_margin | 2,000,000 |
| `Silver_SupportTickets` | Bronze_Support_Tickets | Status mapping, SLA calculation, AI enrichment | 100,000 |
| `Silver_Employees` | Bronze_HR_Employees | Tenure calc, department mapping, anonymize salary | 10,000 |
| `Silver_Products` | Bronze_ProductCatalog_Products | Dedup, price validation | 5,000 |
| `Silver_Products_SCD` | Bronze_ProductCatalog_Products | SCD Type 2 (price history) | 7,500 |

---

## ✅ Silver Layer Checklist

- [ ] All Bronze tables have corresponding Silver tables
- [ ] Deduplication applied where needed
- [ ] Nulls handled (rejected or defaulted)
- [ ] Standardization rules applied (country, industry, etc.)
- [ ] Business logic validated (totals, date ranges)
- [ ] Referential integrity enforced (FKs validated)
- [ ] Audit columns added (`_created_at`, `_updated_at`)
- [ ] Data quality metrics measured
- [ ] SCD logic implemented for history-tracked tables

**Silver layer complete! Ready for Gold star schema ➡️**
