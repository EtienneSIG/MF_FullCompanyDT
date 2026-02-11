# Bronze Layer - Source to Raw Data Mapping

## 🎯 Overview

The **Bronze Layer** ingests raw data from source systems with minimal transformation. Data is stored in Delta format for ACID guarantees and time travel.

**Principles:**
- Preserve source data exactly as received
- Add metadata columns: `_source_file`, `_ingestion_time`, `_batch_id`
- No business logic transformations
- No data cleaning (except unloadable records)
- Enable reprocessing from source at any time

---

## 📊 Data Sources

### Source Systems Inventory

| Source System | Type | Tables | Refresh Frequency | Owner |
|--------------|------|--------|-------------------|-------|
| **Salesforce** | SaaS CRM | Accounts, Opportunities, Contacts | Real-time (CDC) | Sales Ops |
| **NetSuite** | SaaS ERP | Customers, Orders, Invoices | Daily 2 AM | Finance |
| **Zendesk** | Support | Tickets, Agents, SLA | Hourly | Customer Support |
| **Workday** | HR | Employees, Departments, Payroll | Daily 6 AM | HR |
| **Azure SQL** | On-Prem DB | ProductCatalog, Inventory | Real-time (CDC) | IT |
| **CSV Files** | SFTP | Campaign Data, Partner Data | Weekly | Marketing |
| **API** | REST | Social Media, Reviews | Daily | Marketing |

### Generated Data (For Demo)

Since this is a demo with synthetic data, we generate CSV files that simulate these sources:

| CSV File | Simulates | Records | Size |
|----------|-----------|---------|------|
| `customers.csv` | Salesforce Accounts | 50,000 | ~10 MB |
| `products.csv` | ProductCatalog DB | 5,000 | ~2 MB |
| `orders.csv` | NetSuite Orders | 500,000 | ~50 MB |
| `order_lines.csv` | NetSuite Order Lines | 2,000,000 | ~150 MB |
| `employees.csv` | Workday Employees | 10,000 | ~5 MB |
| `support_tickets.csv` | Zendesk Tickets | 100,000 | ~30 MB |
| `campaigns.csv` | Marketing Data | 1,000 | ~500 KB |

---

## 🗂️ Bronze Folder Structure

```
EnterpriseLakehouse/
  Files/
    Bronze/
      CRM/
        Customers/
          _metadata/
          part-00000-*.parquet  # Delta files
          part-00001-*.parquet
        Opportunities/
        Contacts/
      
      ERP/
        Orders/
        OrderLines/
        Invoices/
      
      Support/
        Tickets/
        Agents/
        SLA/
      
      HR/
        Employees/
        Departments/
        Payroll/
      
      ProductCatalog/
        Products/
        Categories/
        Suppliers/
      
      Marketing/
        Campaigns/
        Leads/
        WebAnalytics/
      
      Unstructured/
        SupportTickets/  # JSON with full text
        Emails/
        CallTranscripts/
```

---

## 📥 Ingestion Patterns

### Pattern 1: Batch CSV Ingestion

**Source:** SFTP or Azure Blob Storage  
**Frequency:** Daily  
**Example:** Customer data from Salesforce export

**Notebook Code:**

```python
from pyspark.sql.functions import current_timestamp, input_file_name, lit
from delta.tables import DeltaTable

# Define source and target
source_path = "/lakehouse/default/Files/landing/crm/customers/*.csv"
bronze_path = "Tables/Bronze_CRM_Customers"

# Read CSV with schema inference
df_source = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(source_path)

# Add metadata columns
df_bronze = df_source \
    .withColumn("_source_file", input_file_name()) \
    .withColumn("_ingestion_time", current_timestamp()) \
    .withColumn("_batch_id", lit("2024-01-15"))

# Write to Delta (append mode)
df_bronze.write.format("delta") \
    .mode("append") \
    .save(bronze_path)

print(f"✅ Loaded {df_bronze.count()} customer records to Bronze")
```

### Pattern 2: CDC from Azure SQL

**Source:** Azure SQL Database  
**Frequency:** Real-time via Change Data Capture  
**Example:** Product catalog updates

**Data Factory Pipeline:**
1. Detect changes in SQL table using `sys.dm_cdc_fn_cdc_get_all_changes`
2. Copy changed rows to Bronze
3. Flag operation: `INSERT`, `UPDATE`, `DELETE`

**Bronze Schema:**
```
product_id          STRING
name                STRING
category            STRING
price               DECIMAL(10,2)
_operation          STRING      # I/U/D
_change_time        TIMESTAMP
_ingestion_time     TIMESTAMP
```

### Pattern 3: API Ingestion

**Source:** REST API (e.g., Twitter, Google Analytics)  
**Frequency:** Hourly  
**Example:** Social media mentions

**Python Script:**
```python
import requests
import json
from datetime import datetime

# Call API
response = requests.get("https://api.social.com/mentions", headers={"Authorization": "Bearer <token>"})
data = response.json()

# Convert to DataFrame
df_api = spark.createDataFrame(data)

# Add metadata
df_bronze = df_api \
    .withColumn("_api_call_time", lit(datetime.utcnow())) \
    .withColumn("_ingestion_time", current_timestamp())

# Write to Delta
df_bronze.write.format("delta").mode("append").save("Tables/Bronze_Marketing_SocialMentions")
```

---

## 🗺️ Source-to-Bronze Mapping

### CRM Domain

#### Customers Table

**Source:** Salesforce `Account` object  
**Bronze Table:** `Bronze_CRM_Customers`

| Source Column | Bronze Column | Data Type | Notes |
|--------------|---------------|-----------|-------|
| `Id` | `account_id` | STRING | Salesforce 18-char ID |
| `Name` | `account_name` | STRING | |
| `Industry` | `industry` | STRING | |
| `BillingCountry` | `billing_country` | STRING | |
| `BillingState` | `billing_state` | STRING | |
| `AnnualRevenue` | `annual_revenue` | DECIMAL(15,2) | |
| `NumberOfEmployees` | `employee_count` | INT | |
| `CreatedDate` | `created_date` | TIMESTAMP | |
| `LastModifiedDate` | `last_modified_date` | TIMESTAMP | |
| - | `_source_file` | STRING | Metadata: source file path |
| - | `_ingestion_time` | TIMESTAMP | Metadata: when loaded |

**Sample Data:**
```csv
account_id,account_name,industry,billing_country,annual_revenue,employee_count
001xx000003DHl1AAG,Acme Corp,Technology,USA,50000000,500
001xx000003DHl2AAG,Widget Inc,Manufacturing,Canada,20000000,200
```

#### Opportunities Table

**Source:** Salesforce `Opportunity` object  
**Bronze Table:** `Bronze_CRM_Opportunities`

| Source Column | Bronze Column | Data Type |
|--------------|---------------|-----------|
| `Id` | `opportunity_id` | STRING |
| `AccountId` | `account_id` | STRING |
| `Name` | `opportunity_name` | STRING |
| `Amount` | `amount` | DECIMAL(15,2) |
| `StageName` | `stage` | STRING |
| `CloseDate` | `close_date` | DATE |
| `Probability` | `probability_pct` | INT |
| `IsClosed` | `is_closed` | BOOLEAN |
| `IsWon` | `is_won` | BOOLEAN |

---

### ERP Domain

#### Orders Table

**Source:** NetSuite `SalesOrder` record  
**Bronze Table:** `Bronze_ERP_Orders`

| Source Column | Bronze Column | Data Type | Notes |
|--------------|---------------|-----------|-------|
| `tranid` | `order_number` | STRING | NS-12345 |
| `entity` | `customer_id` | STRING | FK to Customer |
| `trandate` | `order_date` | DATE | |
| `subtotal` | `subtotal` | DECIMAL(12,2) | |
| `taxtotal` | `tax_amount` | DECIMAL(12,2) | |
| `total` | `total_amount` | DECIMAL(12,2) | |
| `status` | `order_status` | STRING | Pending/Approved/Shipped/Invoiced |
| `location` | `fulfillment_location` | STRING | Warehouse code |

#### Order Lines Table

**Source:** NetSuite `SalesOrder:item` sub-record  
**Bronze Table:** `Bronze_ERP_OrderLines`

| Source Column | Bronze Column | Data Type |
|--------------|---------------|-----------|
| `tranid` | `order_number` | STRING |
| `line` | `line_number` | INT |
| `item` | `product_id` | STRING |
| `quantity` | `quantity` | INT |
| `rate` | `unit_price` | DECIMAL(10,2) |
| `amount` | `line_total` | DECIMAL(12,2) |

---

### Support Domain

#### Support Tickets Table

**Source:** Zendesk Tickets  
**Bronze Table:** `Bronze_Support_Tickets`

| Source Column | Bronze Column | Data Type | Notes |
|--------------|---------------|-----------|-------|
| `id` | `ticket_id` | INT | |
| `requester_id` | `customer_id` | INT | |
| `assignee_id` | `agent_id` | INT | |
| `subject` | `subject` | STRING | |
| `description` | `description` | STRING | Full text (unstructured) |
| `status` | `status` | STRING | new/open/pending/solved/closed |
| `priority` | `priority` | STRING | low/normal/high/urgent |
| `created_at` | `created_at` | TIMESTAMP | |
| `updated_at` | `updated_at` | TIMESTAMP | |
| `solved_at` | `solved_at` | TIMESTAMP | Nullable |

**Unstructured Data:**
- `description` field contains free text
- In Silver layer, we'll apply AI to extract:
  - Sentiment
  - Category (Technical/Billing/Account)
  - Urgency

---

### HR Domain

#### Employees Table

**Source:** Workday Employee export  
**Bronze Table:** `Bronze_HR_Employees`

| Source Column | Bronze Column | Data Type | Notes |
|--------------|---------------|-----------|-------|
| `Worker_ID` | `employee_id` | STRING | EMP-12345 |
| `First_Name` | `first_name` | STRING | |
| `Last_Name` | `last_name` | STRING | |
| `Email` | `email` | STRING | |
| `Department` | `department` | STRING | |
| `Job_Title` | `job_title` | STRING | |
| `Manager_ID` | `manager_id` | STRING | Self-join FK |
| `Hire_Date` | `hire_date` | DATE | |
| `Termination_Date` | `termination_date` | DATE | Nullable |
| `Salary_Band` | `salary_band` | STRING | Sensitive - will apply CLS |
| `Location` | `location` | STRING | Office city |
| `Employment_Status` | `employment_status` | STRING | Active/Terminated/LOA |

---

### Product Catalog Domain

#### Products Table

**Source:** Azure SQL `dbo.Products`  
**Bronze Table:** `Bronze_ProductCatalog_Products`

| Source Column | Bronze Column | Data Type | Notes |
|--------------|---------------|-----------|-------|
| `ProductID` | `product_id` | STRING | PRD-001 |
| `ProductName` | `product_name` | STRING | |
| `CategoryID` | `category_id` | STRING | FK to Categories |
| `SupplierID` | `supplier_id` | STRING | FK to Suppliers |
| `UnitPrice` | `list_price` | DECIMAL(10,2) | MSRP |
| `CostPrice` | `cost_price` | DECIMAL(10,2) | Confidential |
| `UnitsInStock` | `units_in_stock` | INT | |
| `UnitsOnOrder` | `units_on_order` | INT | |
| `ReorderLevel` | `reorder_level` | INT | |
| `Discontinued` | `is_discontinued` | BOOLEAN | |

---

## 🔄 Data Refresh Strategy

### Daily Full Load

**Tables:**
- Customers (50K rows - manageable)
- Products (5K rows)
- Employees (10K rows)

**Approach:**
```python
# Overwrite entire table daily
df.write.format("delta").mode("overwrite").save("Tables/Bronze_CRM_Customers")
```

**Pros:** Simple, always consistent  
**Cons:** Loses history (unless using Delta time travel)

### Incremental Append

**Tables:**
- Orders (growing indefinitely)
- Order Lines
- Support Tickets

**Approach:**
```python
# Load only yesterday's data
df_new = df_source.filter(col("order_date") == lit("2024-01-15"))
df_new.write.format("delta").mode("append").save("Tables/Bronze_ERP_Orders")
```

**Pros:** Efficient, preserves all history  
**Cons:** Need to track "last processed" watermark

### CDC / Merge

**Tables:**
- Products (need to track price changes)
- Employees (track promotions, terminations)

**Approach:**
```python
from delta.tables import DeltaTable

# Merge (upsert) based on primary key
bronze_table = DeltaTable.forPath(spark, "Tables/Bronze_HR_Employees")

bronze_table.alias("target").merge(
    df_source.alias("source"),
    "target.employee_id = source.employee_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

**Pros:** Keeps only latest version + history via Delta  
**Cons:** More complex logic

---

## 🧪 Data Quality Checks (Bronze)

### Validation Rules

Even though Bronze is "raw", we validate **loadability**:

| Check | Description | Action if Failed |
|-------|-------------|------------------|
| **Schema Match** | Columns match expected schema | Log error, quarantine file |
| **Non-Empty** | File has > 0 rows | Alert, skip file |
| **Date Format** | Date columns parseable | Log rows with bad dates |
| **Duplicates** | Check for duplicate PKs | Log warning (don't reject) |

**Notebook Example:**

```python
# Check for nulls in PK
null_count = df.filter(col("customer_id").isNull()).count()
if null_count > 0:
    print(f"⚠️ Warning: {null_count} records with null customer_id")

# Check for duplicates
dup_count = df.groupBy("customer_id").count().filter(col("count") > 1).count()
if dup_count > 0:
    print(f"⚠️ Warning: {dup_count} duplicate customer_ids")
```

---

## 📋 Bronze Tables Summary

| Bronze Table | Source System | Records (Demo) | Refresh | PK |
|-------------|---------------|----------------|---------|-----|
| `Bronze_CRM_Customers` | Salesforce | 50,000 | Daily | account_id |
| `Bronze_CRM_Opportunities` | Salesforce | 100,000 | Daily | opportunity_id |
| `Bronze_ERP_Orders` | NetSuite | 500,000 | Daily | order_number |
| `Bronze_ERP_OrderLines` | NetSuite | 2,000,000 | Daily | order_number + line_number |
| `Bronze_Support_Tickets` | Zendesk | 100,000 | Hourly | ticket_id |
| `Bronze_HR_Employees` | Workday | 10,000 | Daily | employee_id |
| `Bronze_ProductCatalog_Products` | Azure SQL | 5,000 | CDC | product_id |
| `Bronze_Marketing_Campaigns` | CSV Upload | 1,000 | Weekly | campaign_id |

**Total Bronze Records:** ~2.8 million  
**Total Bronze Storage:** ~250 MB (uncompressed), ~50 MB (Delta compressed)

---

## 🚀 Demo Execution

### Step 1: Generate Source Data

```bash
cd data-gen
python generate_all.py
```

**Output:**
```
data/generated/
  customers.csv
  products.csv
  orders.csv
  order_lines.csv
  employees.csv
  ...
```

### Step 2: Upload to OneLake

```python
# Option 1: Upload via Fabric UI
# Files → Upload → Select all CSVs → Upload to /Files/landing/

# Option 2: Upload via Azure Storage Explorer
# Connect to OneLake via ADLS Gen2 endpoint
# Copy files to lakehouse
```

### Step 3: Run Bronze Ingestion Notebook

**Notebook:** `01_ingest_to_bronze.ipynb`

```python
# This notebook reads all CSV files and creates Delta tables
spark.read.csv("Files/landing/customers.csv", header=True) \
    .write.format("delta").mode("overwrite").save("Tables/Bronze_CRM_Customers")

# Repeat for all source files
```

**Validation:**
```python
# Count records
spark.read.format("delta").load("Tables/Bronze_CRM_Customers").count()
# Expected: 50,000
```

---

## 📊 Monitoring & Logging

### Ingestion Metrics

**Track in Table:** `Bronze_IngestionLog`

| Column | Type | Description |
|--------|------|-------------|
| `table_name` | STRING | Bronze_CRM_Customers |
| `source_file` | STRING | customers_2024-01-15.csv |
| `records_loaded` | INT | 50,000 |
| `load_time_sec` | DECIMAL | 12.5 |
| `status` | STRING | Success/Failed |
| `error_message` | STRING | Nullable |
| `ingestion_time` | TIMESTAMP | 2024-01-15 08:00:00 |

**Query:**
```sql
SELECT 
    table_name,
    SUM(records_loaded) AS total_records,
    COUNT(*) AS load_count,
    AVG(load_time_sec) AS avg_load_time
FROM Bronze_IngestionLog
WHERE ingestion_time >= CURRENT_DATE()
GROUP BY table_name
ORDER BY total_records DESC
```

---

## ✅ Bronze Layer Checklist

Before moving to Silver:

- [ ] All source files uploaded to `/Files/landing/`
- [ ] Bronze ingestion notebook executed successfully
- [ ] All Bronze tables exist with expected record counts
- [ ] Metadata columns (`_source_file`, `_ingestion_time`) populated
- [ ] Ingestion log table updated
- [ ] No schema mismatches logged
- [ ] Delta tables queryable via SQL endpoint

---

**Bronze layer complete! Ready for transformation to Silver ➡️**
