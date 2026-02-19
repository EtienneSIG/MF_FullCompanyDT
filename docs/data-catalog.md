# Data Catalog - Full Enterprise Data Platform

## 📚 Overview

Complete data dictionary for the enterprise data platform covering **15 business domains** with **100+ tables** and **1,000+ columns**.

**Data Lineage:** Bronze (raw) → Silver (conformed) → Gold (star schemas)
**Time Period:** 2023-01-01 to 2026-02-28 (3 years)
**Total Volume:** ~4.2 million records (structured) + 5,000 text files (unstructured)

---

## 🌟 Conformed Dimensions (Shared Across Domains)

### DimDate

**Description:** Date dimension with fiscal calendar support

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `date_id` | int | Surrogate key (YYYYMMDD format) | `20240615` |
| `date` | date | Actual date | `2024-06-15` |
| `year` | int | Calendar year | `2024` |
| `quarter` | int | Calendar quarter (1-4) | `2` |
| `month` | int | Month number (1-12) | `6` |
| `month_name` | string | Month name | `June` |
| `day_of_week` | int | Day of week (1=Monday, 7=Sunday) | `6` |
| `day_name` | string | Day name | `Saturday` |
| `is_weekend` | boolean | Weekend flag | `true` |
| `is_holiday` | boolean | Public holiday flag | `false` |
| `fiscal_year` | int | Fiscal year (starts July 1) | `2025` |
| `fiscal_quarter` | int | Fiscal quarter | `4` |
| `fiscal_month` | int | Fiscal month (1-12) | `12` |
| `week_of_year` | int | ISO week number | `24` |

**Primary Key:** `date_id`
**Records:** 1,095 (3 years)
**Grain:** One row per day

---

### DimCustomer

**Description:** Customer master data (B2B accounts)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `customer_id` | string | Unique customer identifier | `CUST_012345` |
| `customer_name` | string | Legal business name | `Acme Corporation` |
| `industry` | string | Industry classification | `Manufacturing` |
| `segment` | string | Customer segment | `Enterprise`, `SMB`, `Strategic` |
| `country` | string | ISO country code | `US` |
| `region` | string | Geographic region | `Americas`, `EMEA`, `APAC` |
| `city` | string | City | `New York` |
| `account_manager` | string | Assigned sales rep | `John Smith` |
| `customer_since` | date | First transaction date | `2018-03-15` |
| `credit_limit` | decimal(15,2) | Credit limit in USD | `500000.00` |
| `is_active` | boolean | Active status | `true` |
| `lifetime_value_tier` | string | LTV classification | `High`, `Medium`, `Low` |

**Primary Key:** `customer_id`
**Records:** 50,000
**Grain:** One row per customer (SCD Type 1)

**Business Rules:**
- Industry distribution: Manufacturing 25%, Technology 20%, Retail 15%, Healthcare 12%, Finance 10%, Other 18%
- Segment distribution: Enterprise 20%, SMB 60%, Strategic 20%
- Region distribution: Americas 40%, EMEA 35%, APAC 25%

---

### DimProduct

**Description:** Product catalog with hierarchy

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `product_id` | string | Unique product identifier | `PROD_00123` |
| `product_name` | string | Product name | `Widget Pro 3000` |
| `sku` | string | Stock keeping unit | `WP3000-BLK-L` |
| `category` | string | Top-level category | `Electronics` |
| `subcategory` | string | Product subcategory | `Smartphones` |
| `brand` | string | Brand name | `TechCo` |
| `unit_cost` | decimal(10,2) | Standard cost | `125.50` |
| `list_price` | decimal(10,2) | Standard list price | `299.99` |
| `product_line` | string | Product line grouping | `Consumer Electronics` |
| `launch_date` | date | Product launch date | `2023-01-15` |
| `is_active` | boolean | Currently available | `true` |
| `lifecycle_stage` | string | Product lifecycle | `Growth`, `Mature`, `Decline`, `EOL` |
| `supplier_id` | string | Primary supplier | `SUP_456` |
| `weight_kg` | decimal(8,2) | Unit weight | `0.25` |

**Primary Key:** `product_id`
**Records:** 5,000
**Grain:** One row per product (SCD Type 1)

**Hierarchy:** Product Line → Category → Subcategory → Product

---

### DimEmployee

**Description:** Employee master with organizational hierarchy

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `employee_id` | string | Unique employee identifier | `EMP_00123` |
| `full_name` | string | Employee full name | `Jane Doe` |
| `email` | string | Work email | `jane.doe@company.com` |
| `job_title` | string | Current job title | `Senior Data Engineer` |
| `department` | string | Department | `Engineering` |
| `manager_id` | string | Manager employee ID (FK → employee_id) | `EMP_00045` |
| `hire_date` | date | Date of hire | `2020-06-15` |
| `termination_date` | date | Date of termination (NULL if active) | `NULL` |
| `is_active` | boolean | Currently employed | `true` |
| `location` | string | Office location | `Seattle, WA` |
| `employment_type` | string | Employment type | `Full-Time`, `Part-Time`, `Contractor` |
| `salary_band` | string | Salary band (anonymized) | `Band 3` |
| `performance_rating` | string | Latest performance rating | `Exceeds`, `Meets`, `Below` |

**Primary Key:** `employee_id`
**Records:** 2,000
**Grain:** One row per employee (SCD Type 2 for history)

**Hierarchy:** CEO → VP → Director → Manager → Individual Contributor

---

### DimGeography

**Description:** Geographic dimension with hierarchies

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `geography_id` | string | Unique geography identifier | `GEO_US_NY_NYC` |
| `country_code` | string | ISO 3166-1 alpha-2 code | `US` |
| `country_name` | string | Full country name | `United States` |
| `region` | string | Continental region | `Americas` |
| `sub_region` | string | Sub-region | `North America` |
| `state_province` | string | State or province | `New York` |
| `city` | string | City name | `New York City` |
| `postal_code` | string | Postal/ZIP code | `10001` |
| `latitude` | decimal(9,6) | Latitude coordinate | `40.750000` |
| `longitude` | decimal(9,6) | Longitude coordinate | `-73.997000` |

**Primary Key:** `geography_id`
**Records:** 500
**Grain:** One row per city

**Hierarchy:** Region → Sub-Region → Country → State/Province → City

---

### DimFacility

**Description:** Physical facilities (manufacturing plants, warehouses, offices, R&D labs)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `facility_id` | string | Unique facility identifier | `FAC_0001` |
| `facility_name` | string | Facility name | `Seattle Manufacturing 1` |
| `facility_type` | string | Facility type | `Manufacturing`, `Warehouse`, `Office`, `R&D Lab` |
| `city` | string | City location | `Seattle` |
| `country_code` | string | ISO country code | `US` |
| `geography_id` | string | FK → DimGeography | `GEO_US_SEA_001` |
| `square_footage` | int | Facility size in sq ft | `125000` |
| `size_category` | string | Size classification | `Small`, `Medium`, `Large` |
| `opened_date` | date | Facility opening date | `2015-03-15` |
| `is_active` | boolean | Currently operational | `true` |
| `capacity_utilization_pct` | decimal(5,2) | Current capacity utilization % | `85.5` |

**Primary Key:** `facility_id`
**Foreign Keys:** `geography_id`
**Records:** 15
**Grain:** One row per facility

**Business Rules:**
- Type distribution: Manufacturing 40%, Warehouse 30%, Office 20%, R&D Lab 10%
- Size categories: Small (<50K sq ft), Medium (50K-200K sq ft), Large (>200K sq ft)

---

### DimProject

**Description:** Project master data (innovation, infrastructure, process improvement)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `project_id` | string | Unique project identifier | `PRJ_000123` |
| `project_name` | string | Project name | `Innovation: Revolutionary Widget` |
| `category` | string | Project category | `Product Innovation`, `Process Improvement`, `New Technology`, `Infrastructure` |
| `status` | string | Current status | `Planning`, `Research`, `Development`, `Testing`, `Completed` |
| `lead_id` | string | FK → DimEmployee (project lead) | `EMP_00456` |
| `start_date` | date | Project start date | `2024-01-15` |
| `budget_usd` | decimal(15,2) | Approved budget | `450000.00` |
| `actual_spend_usd` | decimal(15,2) | Actual spending to date | `380250.50` |
| `priority` | string | Project priority | `Critical`, `High`, `Medium`, `Low` |

**Primary Key:** `project_id`
**Foreign Keys:** `lead_id`
**Records:** 300
**Grain:** One row per project

**Business Rules:**
- Category distribution: Product Innovation 35%, Process Improvement 30%, New Technology 20%, Infrastructure 15%
- Status distribution: Planning 15%, Research 25%, Development 35%, Testing 15%, Completed 10%
- Budget range: $50K - $2M, average $350K

---

### DimAccount

**Description:** Chart of accounts for financial transactions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `account_id` | string | Unique account identifier | `ACCT_1000` |
| `account_code` | string | GL account code | `1000` |
| `account_name` | string | Account name | `Cash` |
| `account_type` | string | Account classification | `Asset`, `Liability`, `Equity`, `Revenue`, `Expense` |
| `subcategory` | string | Account subcategory | `Current Assets`, `Operating Revenue`, etc. |
| `is_active` | boolean | Currently in use | `true` |
| `normal_balance` | string | Normal balance side | `Debit`, `Credit` |

**Primary Key:** `account_id`
**Records:** 18
**Grain:** One row per GL account

**Account Types:**
- **Assets:** Cash, Accounts Receivable, Inventory, Prepaid Expenses, Fixed Assets
- **Liabilities:** Accounts Payable, Accrued Expenses, Long-term Debt
- **Equity:** Common Stock, Retained Earnings
- **Revenue:** Product Revenue, Service Revenue
- **Expenses:** COGS, Salaries & Wages, Marketing & Advertising, R&D, IT & Technology, Facilities & Utilities

**Normal Balance Rules:**
- Assets and Expenses: Debit
- Liabilities, Equity, and Revenue: Credit

---

## 📊 Domain-Specific Tables

### 1. CRM Domain

#### FactOpportunities

**Description:** Sales opportunities (pipeline)

| Column | Type | Description |
|--------|------|-------------|
| `opportunity_id` | string | Unique opportunity identifier |
| `customer_id` | string | FK → DimCustomer |
| `product_id` | string | FK → DimProduct |
| `owner_employee_id` | string | FK → DimEmployee (sales rep) |
| `create_date_id` | int | FK → DimDate (opportunity creation) |
| `close_date_id` | int | FK → DimDate (expected/actual close) |
| `stage` | string | Opportunity stage (Lead, Qualified, Proposal, Negotiation, Closed Won, Closed Lost) |
| `probability` | decimal(5,2) | Win probability % |
| `amount` | decimal(15,2) | Deal value |
| `deal_type` | string | New Business, Upsell, Renewal |
| `lead_source` | string | Marketing, Referral, Outbound, Partner |
| `competitor` | string | Primary competitor (if known) |

**Primary Key:** `opportunity_id`
**Foreign Keys:** `customer_id`, `product_id`, `owner_employee_id`, `create_date_id`, `close_date_id`
**Records:** ~75,000
**Grain:** One row per opportunity

---

#### FactActivities

**Description:** Sales activities (calls, meetings, emails)

| Column | Type | Description |
|--------|------|-------------|
| `activity_id` | string | Unique activity identifier |
| `opportunity_id` | string | FK → FactOpportunities (nullable) |
| `customer_id` | string | FK → DimCustomer |
| `employee_id` | string | FK → DimEmployee (activity owner) |
| `activity_date_id` | int | FK → DimDate |
| `activity_type` | string | Call, Meeting, Email, Demo |
| `duration_minutes` | int | Activity duration |
| `outcome` | string | Positive, Neutral, Negative, No Answer |
| `notes` | string | Activity notes (truncated) |

**Primary Key:** `activity_id`
**Records:** ~150,000
**Grain:** One row per activity

---

### 2. Sales Domain

#### FactSales

**Description:** Sales transactions (orders)

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier |
| `order_line_id` | string | Line item identifier |
| `customer_id` | string | FK → DimCustomer |
| `product_id` | string | FK → DimProduct |
| `employee_id` | string | FK → DimEmployee (sales rep) |
| `order_date_id` | int | FK → DimDate |
| `ship_date_id` | int | FK → DimDate |
| `delivery_date_id` | int | FK → DimDate |
| `quantity` | int | Quantity ordered |
| `unit_price` | decimal(10,2) | Actual unit price |
| `discount_percent` | decimal(5,2) | Discount % |
| `discount_amount` | decimal(10,2) | Discount amount |
| `net_amount` | decimal(15,2) | Net amount (after discount) |
| `cost_amount` | decimal(15,2) | Cost of goods sold |
| `gross_margin` | decimal(15,2) | Gross margin (net - cost) |
| `tax_amount` | decimal(10,2) | Tax amount |
| `total_amount` | decimal(15,2) | Total including tax |
| `status` | string | Pending, Shipped, Delivered, Cancelled, Returned |
| `channel` | string | Online, Retail, Partner, Direct Sales |

**Primary Key:** (`order_id`, `order_line_id`)
**Records:** ~2,000,000
**Grain:** One row per order line item

**Measures:**
- Total Revenue = SUM(net_amount) WHERE status NOT IN ('Cancelled', 'Returned')
- Gross Margin % = SUM(gross_margin) / SUM(net_amount)
- Average Order Value = SUM(net_amount) / DISTINCTCOUNT(order_id)

---

#### FactReturns

**Description:** Product returns

| Column | Type | Description |
|--------|------|-------------|
| `return_id` | string | Unique return identifier |
| `order_id` | string | FK → FactSales (original order) |
| `customer_id` | string | FK → DimCustomer |
| `product_id` | string | FK → DimProduct |
| `return_date_id` | int | FK → DimDate |
| `return_reason` | string | Defective, Wrong Item, Not Needed, Other |
| `return_quantity` | int | Quantity returned |
| `refund_amount` | decimal(10,2) | Refund amount |
| `restocking_fee` | decimal(10,2) | Restocking fee charged |
| `condition` | string | New, Used, Damaged |

**Primary Key:** `return_id`
**Records:** ~50,000 (2.5% return rate)
**Grain:** One row per return transaction

---

### 3. Product Domain

#### DimProductBOM (Bill of Materials)

**Description:** Product component relationships

| Column | Type | Description |
|--------|------|-------------|
| `parent_product_id` | string | FK → DimProduct (finished good) |
| `component_product_id` | string | FK → DimProduct (component) |
| `quantity_required` | decimal(10,4) | Quantity of component per unit |
| `scrap_factor` | decimal(5,4) | Expected scrap % |
| `is_critical` | boolean | Critical path component |

**Composite Key:** (`parent_product_id`, `component_product_id`)
**Records:** ~20,000
**Grain:** One row per component relationship

---

### 4. Marketing Domain

#### FactCampaigns

**Description:** Marketing campaign performance

| Column | Type | Description |
|--------|------|-------------|
| `campaign_id` | string | Unique campaign identifier |
| `campaign_name` | string | Campaign name |
| `start_date_id` | int | FK → DimDate |
| `end_date_id` | int | FK → DimDate |
| `channel` | string | Email, Social, Display, Search, Events |
| `budget` | decimal(15,2) | Campaign budget |
| `spend` | decimal(15,2) | Actual spend |
| `impressions` | int | Number of impressions |
| `clicks` | int | Number of clicks |
| `conversions` | int | Number of conversions |
| `leads_generated` | int | Leads generated |
| `opportunities_created` | int | Opportunities created |
| `revenue_influenced` | decimal(15,2) | Influenced revenue |

**Primary Key:** `campaign_id`
**Records:** ~5,000
**Grain:** One row per campaign

**Measures:**
- CTR = clicks / impressions
- Conversion Rate = conversions / clicks
- Cost per Lead = spend / leads_generated
- ROI = (revenue_influenced - spend) / spend

---

### 5. HR Domain

#### FactAttrition

**Description:** Employee turnover events

| Column | Type | Description |
|--------|------|-------------|
| `attrition_id` | string | Unique attrition event |
| `employee_id` | string | FK → DimEmployee |
| `manager_id` | string | FK → DimEmployee (manager) |
| `termination_date_id` | int | FK → DimDate |
| `tenure_days` | int | Days employed |
| `termination_type` | string | Voluntary, Involuntary, Retirement |
| `reason` | string | Career Growth, Compensation, Culture, Performance, Other |
| `is_regrettable` | boolean | Regrettable loss flag |
| `exit_interview_completed` | boolean | Exit interview flag |
| `rehire_eligible` | boolean | Eligible for rehire |

**Primary Key:** `attrition_id`
**Records:** ~3,000 (7% annual attrition, 3 years)
**Grain:** One row per termination event

**Measures:**
- Attrition Rate = COUNT(attrition_id) / AVG(active_employees)
- Voluntary Attrition % = COUNT WHERE termination_type = 'Voluntary' / COUNT(*)
- Regrettable Attrition % = COUNT WHERE is_regrettable = TRUE / COUNT(*)

---

#### FactHiring

**Description:** Recruitment and hiring events

| Column | Type | Description |
|--------|------|-------------|
| `requisition_id` | string | Unique job requisition |
| `employee_id` | string | FK → DimEmployee (hired candidate, NULL if not filled) |
| `hiring_manager_id` | string | FK → DimEmployee |
| `open_date_id` | int | FK → DimDate |
| `filled_date_id` | int | FK → DimDate (NULL if open) |
| `job_title` | string | Position title |
| `department` | string | Department |
| `level` | string | Job level |
| `applicants_count` | int | Number of applicants |
| `interviews_count` | int | Number of interviews conducted |
| `offers_extended` | int | Offers made |
| `time_to_fill_days` | int | Days to fill (NULL if open) |
| `source` | string | Referral, LinkedIn, Job Board, Agency |

**Primary Key:** `requisition_id`
**Records:** ~5,000
**Grain:** One row per job requisition

**Measures:**
- Time to Fill = AVG(time_to_fill_days) WHERE filled_date_id IS NOT NULL
- Offer Acceptance Rate = COUNT(employee_id IS NOT NULL) / SUM(offers_extended)

---

### 6. Supply Chain Domain

#### FactInventory

**Description:** Inventory snapshots (daily)

| Column | Type | Description |
|--------|------|-------------|
| `snapshot_date_id` | int | FK → DimDate |
| `product_id` | string | FK → DimProduct |
| `warehouse_id` | string | FK → DimWarehouse |
| `quantity_on_hand` | int | Current quantity |
| `quantity_reserved` | int | Reserved for orders |
| `quantity_available` | int | Available to promise |
| `quantity_in_transit` | int | In transit to warehouse |
| `reorder_point` | int | Reorder trigger level |
| `safety_stock` | int | Minimum safety stock |
| `unit_cost` | decimal(10,2) | Standard cost per unit |
| `inventory_value` | decimal(15,2) | Total value (quantity × cost) |
| `days_of_supply` | int | Days of inventory at current demand rate |

**Composite Key:** (`snapshot_date_id`, `product_id`, `warehouse_id`)
**Records:** ~300,000 (daily snapshots × products × warehouses)
**Grain:** One row per product per warehouse per day

**Measures:**
- Inventory Turns = COGS / AVG(inventory_value)
- Stockout Rate = COUNT WHERE quantity_available = 0 / COUNT(*)

---

#### FactPurchaseOrders

**Description:** Purchase orders to suppliers

| Column | Type | Description |
|--------|------|-------------|
| `po_id` | string | Purchase order ID |
| `po_line_id` | string | PO line item ID |
| `supplier_id` | string | FK → DimSupplier |
| `product_id` | string | FK → DimProduct |
| `order_date_id` | int | FK → DimDate |
| `expected_delivery_date_id` | int | FK → DimDate |
| `actual_delivery_date_id` | int | FK → DimDate (NULL if not delivered) |
| `quantity` | int | Quantity ordered |
| `unit_price` | decimal(10,2) | Purchase price per unit |
| `total_amount` | decimal(15,2) | Total PO line value |
| `status` | string | Draft, Submitted, Approved, Shipped, Received, Cancelled |
| `days_late` | int | Days late (positive) or early (negative) |

**Composite Key:** (`po_id`, `po_line_id`)
**Records:** ~200,000
**Grain:** One row per PO line item

**Measures:**
- On-Time Delivery % = COUNT WHERE days_late <= 0 / COUNT(*)
- Average Lead Time = AVG(actual_delivery_date - order_date)

---

### 7. Manufacturing Domain

#### FactProduction

**Description:** Manufacturing work orders and output

| Column | Type | Description |
|--------|------|-------------|
| `work_order_id` | string | Unique work order ID |
| `product_id` | string | FK → DimProduct |
| `production_date_id` | int | FK → DimDate |
| `plant_id` | string | FK → DimPlant |
| `planned_quantity` | int | Planned production quantity |
| `actual_quantity` | int | Actual quantity produced |
| `good_quantity` | int | Quality-passed quantity |
| `scrap_quantity` | int | Scrap/rework quantity |
| `standard_hours` | decimal(10,2) | Standard labor hours |
| `actual_hours` | decimal(10,2) | Actual labor hours |
| `downtime_hours` | decimal(10,2) | Equipment downtime |
| `yield_percent` | decimal(5,2) | Yield % (good / actual) |
| `efficiency_percent` | decimal(5,2) | Efficiency % (standard / actual) |
| `oee` | decimal(5,2) | Overall Equipment Effectiveness |

**Primary Key:** `work_order_id`
**Records:** ~100,000
**Grain:** One row per work order

**Measures:**
- Average Yield = AVG(yield_percent)
- OEE = AVG(oee)
- Scrap Rate = SUM(scrap_quantity) / SUM(actual_quantity)

---

### 8. Finance Domain

#### FactGeneralLedger

**Description:** General ledger transactions

| Column | Type | Description |
|--------|------|-------------|
| `gl_entry_id` | string | Unique GL entry |
| `transaction_date_id` | int | FK → DimDate |
| `account_id` | string | FK → DimAccount |
| `cost_center_id` | string | FK → DimCostCenter |
| `department` | string | Department |
| `debit_amount` | decimal(15,2) | Debit amount (NULL if credit) |
| `credit_amount` | decimal(15,2) | Credit amount (NULL if debit) |
| `amount` | decimal(15,2) | Signed amount (debit positive, credit negative) |
| `description` | string | Transaction description |
| `vendor_id` | string | Vendor (if applicable) |
| `employee_id` | string | Employee (if expense) |

**Primary Key:** `gl_entry_id`
**Records:** ~500,000
**Grain:** One row per GL line entry

---

#### FactBudget

**Description:** Budget allocations

| Column | Type | Description |
|--------|------|-------------|
| `budget_id` | string | Unique budget entry |
| `fiscal_year` | int | Fiscal year |
| `fiscal_month` | int | Fiscal month |
| `account_id` | string | FK → DimAccount |
| `cost_center_id` | string | FK → DimCostCenter |
| `budget_amount` | decimal(15,2) | Budgeted amount |
| `forecast_amount` | decimal(15,2) | Latest forecast |
| `version` | string | Budget version (Original, Revised Q1, etc.) |

**Composite Key:** (`budget_id`)
**Records:** ~50,000
**Grain:** One row per account per cost center per month per version

---

### 9. ESG Domain

#### FactEmissions

**Description:** Greenhouse gas emissions tracking

| Column | Type | Description |
|--------|------|-------------|
| `emission_id` | string | Unique emission record |
| `measurement_date_id` | int | FK → DimDate |
| `facility_id` | string | FK → DimFacility |
| `scope` | string | Scope 1, Scope 2, Scope 3 |
| `category` | string | Emission category (e.g., Electricity, Fuel, Transport) |
| `metric_tons_co2e` | decimal(15,4) | CO2 equivalent emissions (metric tons) |
| `activity_amount` | decimal(15,2) | Activity data (kWh, liters, km, etc.) |
| `activity_unit` | string | Unit of measurement |
| `emission_factor` | decimal(10,6) | Emission factor used |

**Primary Key:** `emission_id`
**Records:** ~30,000
**Grain:** One row per emission source per measurement period

**Measures:**
- Total Emissions = SUM(metric_tons_co2e)
- Scope 1 % = SUM WHERE scope = 'Scope 1' / SUM(metric_tons_co2e)
- Emissions Intensity = SUM(metric_tons_co2e) / SUM(revenue)

---

### 10. Call Center Domain

#### FactSupport

**Description:** Customer support tickets

| Column | Type | Description |
|--------|------|-------------|
| `ticket_id` | string | Unique ticket identifier |
| `customer_id` | string | FK → DimCustomer |
| `product_id` | string | FK → DimProduct (if product-related) |
| `agent_employee_id` | string | FK → DimEmployee |
| `create_date_id` | int | FK → DimDate |
| `resolution_date_id` | int | FK → DimDate (NULL if open) |
| `channel` | string | Phone, Email, Chat, Portal |
| `category` | string | Technical, Billing, General Inquiry |
| `priority` | string | Critical, High, Medium, Low |
| `status` | string | Open, In Progress, Waiting, Resolved, Closed |
| `first_response_minutes` | int | Minutes to first response |
| `resolution_hours` | decimal(10,2) | Hours to resolution |
| `interactions_count` | int | Number of interactions |
| `escalated` | boolean | Escalation flag |
| `csat_score` | int | Customer satisfaction (1-5, NULL if not rated) |
| `fcr` | boolean | First contact resolution |

**Primary Key:** `ticket_id`
**Records:** ~200,000
**Grain:** One row per support ticket

**Measures:**
- Avg Resolution Time = AVG(resolution_hours) WHERE status IN ('Resolved', 'Closed')
- CSAT Average = AVG(csat_score) WHERE csat_score IS NOT NULL
- FCR % = COUNT WHERE fcr = TRUE / COUNT(*)

---

### 11. IT Ops Domain

#### FactIncidents

**Description:** IT incidents and outages

| Column | Type | Description |
|--------|------|-------------|
| `incident_id` | string | Unique incident identifier |
| `reported_date_id` | int | FK → DimDate |
| `resolved_date_id` | int | FK → DimDate (NULL if open) |
| `affected_system` | string | System/application affected |
| `severity` | string | P1 (Critical), P2 (High), P3 (Medium), P4 (Low) |
| `category` | string | Hardware, Software, Network, Security |
| `root_cause` | string | Root cause category |
| `downtime_minutes` | int | Total downtime |
| `users_impacted` | int | Number of users affected |
| `assigned_to_employee_id` | string | FK → DimEmployee |
| `status` | string | Open, In Progress, Resolved, Closed |
| `mttr_minutes` | int | Mean time to resolution |

**Primary Key:** `incident_id`
**Records:** ~150,000
**Grain:** One row per incident

**Measures:**
- MTTR = AVG(mttr_minutes)
- Availability % = (Total Minutes - SUM(downtime_minutes)) / Total Minutes
- P1 Incidents = COUNT WHERE severity = 'P1'

---

### 12. FinOps Domain

#### FactCloudCosts

**Description:** Cloud spend tracking (Azure, AWS, GCP)

| Column | Type | Description |
|--------|------|-------------|
| `cost_id` | string | Unique cost record |
| `usage_date_id` | int | FK → DimDate |
| `cloud_provider` | string | Azure, AWS, GCP |
| `service_name` | string | Service/SKU name |
| `resource_group` | string | Resource group / project |
| `subscription_id` | string | Subscription / account ID |
| `cost_center_id` | string | FK → DimCostCenter |
| `environment` | string | Production, Development, Test |
| `region` | string | Cloud region |
| `usage_quantity` | decimal(15,4) | Usage quantity |
| `usage_unit` | string | Unit (hours, GB, requests) |
| `unit_price` | decimal(10,6) | Price per unit |
| `cost_amount` | decimal(15,2) | Total cost |
| `currency` | string | Currency code |
| `tags` | string | JSON tags (key-value pairs) |

**Primary Key:** `cost_id`
**Records:** ~100,000
**Grain:** One row per service per day

**Measures:**
- Total Cloud Spend = SUM(cost_amount)
- Cost per Environment = SUM(cost_amount) BY environment
- Month-over-Month % = (Current Month - Prior Month) / Prior Month

---

### 13. Risk & Compliance Domain

*(See MF_RiskComplianceAudit for detailed schema)*

Tables: `controls`, `control_executions`, `incidents`, `remediation_actions`, `vendors`

---

### 14. R&D Domain

#### FactExperiments

**Description:** R&D experiments and test results

| Column | Type | Description |
|--------|------|-------------|
| `experiment_id` | string | Unique experiment identifier |
| `project_id` | string | FK → DimProject |
| `experiment_date_id` | int | FK → DimDate |
| `researcher_id` | string | FK → DimEmployee |
| `experiment_type` | string | Prototype, Performance, Durability, Safety |
| `is_successful` | boolean | Experiment outcome |
| `cost_usd` | decimal(15,2) | Experiment cost |
| `duration_days` | int | Experiment duration |

**Primary Key:** `experiment_id`
**Foreign Keys:** `project_id`, `experiment_date_id`, `researcher_id`
**Records:** ~15,000
**Grain:** One row per experiment

**Measures:**
- Success Rate = COUNT WHERE is_successful = true / COUNT(*)
- Average Experiment Cost = AVG(cost_usd)
- Total R&D Spend = SUM(cost_usd)

---

### 15. Quality & Security Domain

#### FactDefects

**Description:** Product quality defects

| Column | Type | Description |
|--------|------|-------------|
| `defect_id` | string | Unique defect identifier |
| `detection_date_id` | int | FK → DimDate |
| `product_id` | string | FK → DimProduct |
| `lot_number` | string | Manufacturing lot |
| `defect_type` | string | Cosmetic, Functional, Safety |
| `severity` | string | Critical, Major, Minor |
| `quantity_affected` | int | Units affected |
| `root_cause` | string | Root cause (if known) |
| `capa_id` | string | Corrective action ID |
| `status` | string | Open, Under Investigation, Resolved |

**Primary Key:** `defect_id`
**Records:** ~80,000
**Grain:** One row per defect

**Measures:**
- Defect Rate = COUNT(defect_id) / SUM(production_quantity)
- Critical Defects = COUNT WHERE severity = 'Critical'

---

## 🔗 Relationships

### Star Schema Patterns

All fact tables connect to conformed dimensions:

```
FactSales
├── → DimCustomer (customer_id)
├── → DimProduct (product_id)
├── → DimEmployee (employee_id)
├── → DimDate (order_date_id)
├── → DimDate (ship_date_id)
└── → DimDate (delivery_date_id)

FactSupport
├── → DimCustomer (customer_id)
├── → DimProduct (product_id)
├── → DimEmployee (agent_employee_id)
├── → DimDate (create_date_id)
└── → DimDate (resolution_date_id)
```

### Role-Playing Dimensions

**DimDate** plays multiple roles:
- Order Date
- Ship Date
- Delivery Date
- Create Date
- Resolution Date
- etc.

**DimEmployee** plays multiple roles:
- Sales Rep
- Support Agent
- Manager
- Scientist
- etc.

---

## 📝 Naming Conventions

### Tables
- Dimensions: `Dim<Name>` (e.g., `DimCustomer`)
- Facts: `Fact<Name>` (e.g., `FactSales`)

### Columns
- Primary Keys: `<table>_id` (e.g., `customer_id`)
- Foreign Keys: Match dimension primary key
- Dates: `<event>_date` or `<event>_date_id` (for surrogate keys)
- Amounts: `<metric>_amount` (e.g., `total_amount`)
- Counts: `<metric>_count` (e.g., `line_items_count`)
- Flags: `is_<condition>` (e.g., `is_active`)

### Measures (DAX)
- Base: `Total <Metric>` (e.g., `Total Revenue`)
- Time Intelligence: `<Metric> YTD` (e.g., `Revenue YTD`)
- Ratios: `<Metric> %` (e.g., `Gross Margin %`)

---

## 🎯 Data Quality Rules

### Referential Integrity
- All foreign keys must exist in dimension tables
- No orphaned records allowed

### Required Fields
- Primary keys: NOT NULL
- Foreign keys: NOT NULL (unless explicitly nullable)
- Date fields: Valid dates within range (2023-2026)

### Value Constraints
- Amounts: >= 0 (except GL which can be negative)
- Percentages: 0-100
- Ratings/Scores: Within defined range (e.g., CSAT 1-5)

### Business Rules
- Order ship_date >= order_date
- Invoice date >= order_date
- Employee hire_date < termination_date (if terminated)
- Actual < Budget generates variance flag

---

## 📊 Data Volume Summary

| Domain | Tables | Total Records |
|--------|--------|---------------|
| Conformed Dimensions | 5 | 58,595 |
| CRM | 2 | 225,000 |
| Sales | 2 | 2,050,000 |
| Product | 1 | 20,000 |
| Marketing | 1 | 5,000 |
| HR | 2 | 8,000 |
| Supply Chain | 2 | 500,000 |
| Manufacturing | 1 | 100,000 |
| Finance | 2 | 550,000 |
| ESG | 1 | 30,000 |
| Call Center | 1 | 200,000 |
| IT Ops | 1 | 150,000 |
| FinOps | 1 | 100,000 |
| Risk & Compliance | 5 | 3,500 |
| R&D | 1 | 15,000 |
| Quality & Security | 1 | 80,000 |

**Total:** ~4.2 million structured records

**Unstructured:** 5,000 text files (emails, support tickets, lab notes)

---

## 🔍 Usage Examples

### Find Top Products by Revenue
```sql
SELECT 
    p.product_name,
    p.category,
    SUM(s.net_amount) as total_revenue
FROM FactSales s
JOIN DimProduct p ON s.product_id = p.product_id
WHERE s.status NOT IN ('Cancelled', 'Returned')
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
```

### Calculate Attrition Rate by Department
```sql
SELECT 
    e.department,
    COUNT(DISTINCT a.employee_id) as terminations,
    COUNT(DISTINCT e.employee_id) as total_employees,
    (COUNT(DISTINCT a.employee_id) * 100.0 / COUNT(DISTINCT e.employee_id)) as attrition_rate
FROM DimEmployee e
LEFT JOIN FactAttrition a ON e.employee_id = a.employee_id
    AND a.termination_date_id >= 20230101
GROUP BY e.department
ORDER BY attrition_rate DESC;
```

---

For detailed column descriptions and sample data, refer to individual generator scripts in `/data-gen/generators/`.
