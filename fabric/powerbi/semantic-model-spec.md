# Semantic Model Specification

## 🎯 Overview

This document specifies the **Power BI semantic model** (formerly "dataset") for the Enterprise Data Platform demo. The model uses **Direct Lake mode** to query Gold layer Delta tables directly from OneLake.

**Model Name:** `EnterprisePlatform_SemanticModel`  
**Mode:** Direct Lake (no data import, live query to OneLake)  
**Lakehouse:** EnterpriseLakehouse (Gold layer tables)  
**Expected Performance:** Sub-second queries for < 10M rows

**Contents:**
- **23 fact tables** across 15 business domains (Sales, CRM, Call Center, Marketing, HR, Finance, FinOps, IT Ops, Manufacturing, Supply Chain, ESG, Risk & Compliance, R&D, Quality, Security)
- **8 conformed dimension tables** (Date, Customer, Product, Employee, Geography, Facility, Project, Account)
- Star schema relationships with role-playing dimensions
- ~100+ DAX measures organized by domain
- Row-level security (RLS) for multi-tenant access
- Column-level security (CLS) on sensitive fields

---

## 📊 Tables in Model

### Fact Tables (23)

#### **Sales & CRM Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Sales** | Gold_FactSales | 500K | Sales order line items (revenue, units, discounts) |
| **Returns** | Gold_FactReturns | 25K | Product returns and refunds |
| **Opportunities** | Gold_FactOpportunities | 15K | Sales pipeline opportunities |
| **Activities** | Gold_FactActivities | 45K | Sales rep activities (calls, meetings, emails) |

#### **Customer Service Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Support** | Gold_FactSupport | 50K | Support tickets (incidents, service requests) |

#### **Marketing Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Campaigns** | Gold_FactCampaigns | 1.2K | Marketing campaign performance |

#### **Human Resources Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Hiring** | Gold_FactHiring | 2.5K | New hire onboarding records |
| **Attrition** | Gold_FactAttrition | 1.5K | Employee attrition/termination events |

#### **Finance Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **GeneralLedger** | Gold_FactGeneralLedger | 175K | GL transactions (journal entries) |
| **Budget** | Gold_FactBudget | 13K | Budget allocations by account/month |

#### **FinOps Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **CloudCosts** | Gold_FactCloudCosts | 73K | Cloud consumption costs (Azure/AWS/GCP) |

#### **IT Operations Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Incidents** | Gold_FactIncidents | 30K | IT incidents (P1-P4, application/infrastructure) |

#### **Manufacturing & Operations Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Production** | Gold_FactProduction | 54K | Production output by facility/product |
| **WorkOrders** | Gold_FactWorkOrders | 13.5K | Manufacturing work orders |

#### **Supply Chain Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Inventory** | Gold_FactInventory | 912K | Daily inventory snapshots by facility/product |
| **PurchaseOrders** | Gold_FactPurchaseOrders | 30K | Purchase order line items from suppliers |

#### **ESG Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Emissions** | Gold_FactEmissions | 3.8K | Carbon emissions by facility/month (Scope 1-3) |

#### **Risk, Compliance & Audit Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Risks** | Gold_FactRisks | 1.5K | Enterprise risk register |
| **Audits** | Gold_FactAudits | 1.8K | Audit findings and remediation |
| **ComplianceChecks** | Gold_FactComplianceChecks | 2.7K | Compliance controls testing |

#### **R&D Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Experiments** | Gold_FactExperiments | 3.6K | R&D experiments and trials |

#### **Quality & Security Domain**
| Table | Source | Approx. Rows | Business Purpose |
|-------|--------|--------------|------------------|
| **Defects** | Gold_FactDefects | 9K | Product quality defects |
| **SecurityEvents** | Gold_FactSecurityEvents | 18K | Security incidents and vulnerabilities |

---

### Dimension Tables (8)

| Table | Source | Rows | Role in Model | Snowflake |
|-------|--------|------|---------------|-----------|
| **Date** | Gold_DimDate | 4,380 | Shared calendar dimension (12 years: 2015-2026) | No |
| **Customer** | Gold_DimCustomer | 50K | Customer master data (B2B accounts) | No |
| **Product** | Gold_DimProduct | 5K | Product catalog with categories | No |
| **Employee** | Gold_DimEmployee | 8.5K | Employee roster with org hierarchy | No |
| **Geography** | Gold_DimGeography | 500 | Country/region hierarchy | No |
| **Facility** | Gold_DimFacility | 100 | Physical locations (plants, warehouses, offices, DCs) | No |
| **Project** | Gold_DimProject | 200 | Projects for R&D, IT, and business initiatives | No |
| **Account** | Gold_DimAccount | 150 | Chart of accounts for Finance GL | No |

**Note:** All dimensions are conformed (shared across multiple fact tables). No snowflake dimensions (fully denormalized for Direct Lake performance).

---

## 🔗 Relationships

### Star Schema Relationships

All relationships follow **Many-to-One** cardinality from fact tables (many) to dimension tables (one), with **Single** cross-filter direction unless noted. Role-playing dimensions (e.g., Date with multiple date keys) use **inactive** relationships activated via DAX.

#### **Sales & CRM Domain**

**Sales Fact:**
- Sales[order_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Sales[ship_date_id] → Date[date_id] (Many-to-One, Single) **Inactive** *(use USERELATIONSHIP in DAX)*
- Sales[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Sales[product_key] → Product[product_key] (Many-to-One, Single)
- Sales[salesperson_key] → Employee[employee_key] (Many-to-One, Single)
- Sales[ship_to_geography_key] → Geography[geography_key] (Many-to-One, Single)

**Returns Fact:**
- Returns[return_date_id] → Date[date_id] (Many-to-One, Single)
- Returns[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Returns[product_key] → Product[product_key] (Many-to-One, Single)

**Opportunities Fact:**
- Opportunities[create_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Opportunities[close_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Opportunities[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Opportunities[owner_key] → Employee[employee_key] (Many-to-One, Single)

**Activities Fact:**
- Activities[activity_date_id] → Date[date_id] (Many-to-One, Single)
- Activities[employee_key] → Employee[employee_key] (Many-to-One, Single)
- Activities[customer_key] → Customer[customer_key] (Many-to-One, Single)

---

#### **Customer Service Domain**

**Support Fact:**
- Support[create_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Support[resolved_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Support[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Support[agent_key] → Employee[employee_key] (Many-to-One, Single)
- Support[product_key] → Product[product_key] (Many-to-One, Single)

---

#### **Marketing Domain**

**Campaigns Fact:**
- Campaigns[start_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Campaigns[end_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Campaigns[owner_key] → Employee[employee_key] (Many-to-One, Single)

---

#### **Human Resources Domain**

**Hiring Fact:**
- Hiring[hire_date_id] → Date[date_id] (Many-to-One, Single)
- Hiring[employee_id] → Employee[employee_key] (Many-to-One, Single)

**Attrition Fact:**
- Attrition[termination_date_id] → Date[date_id] (Many-to-One, Single)
- Attrition[employee_key] → Employee[employee_key] (Many-to-One, Single)

---

#### **Finance Domain**

**GeneralLedger Fact:**
- GeneralLedger[transaction_date_id] → Date[date_id] (Many-to-One, Single)
- GeneralLedger[account_key] → Account[account_key] (Many-to-One, Single)
- GeneralLedger[employee_key] → Employee[employee_key] (Many-to-One, Single) *(for expense transactions)*

**Budget Fact:**
- Budget[budget_date_id] → Date[date_id] (Many-to-One, Single)
- Budget[account_key] → Account[account_key] (Many-to-One, Single)

---

#### **FinOps Domain**

**CloudCosts Fact:**
- CloudCosts[usage_date_id] → Date[date_id] (Many-to-One, Single)
- CloudCosts[account_key] → Account[account_key] (Many-to-One, Single) *(cost center)*

---

#### **IT Operations Domain**

**Incidents Fact:**
- Incidents[reported_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Incidents[resolved_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Incidents[assigned_to_key] → Employee[employee_key] (Many-to-One, Single)

---

#### **Manufacturing & Operations Domain**

**Production Fact:**
- Production[production_date_id] → Date[date_id] (Many-to-One, Single)
- Production[product_key] → Product[product_key] (Many-to-One, Single)
- Production[facility_key] → Facility[facility_key] (Many-to-One, Single)

**WorkOrders Fact:**
- WorkOrders[create_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- WorkOrders[complete_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- WorkOrders[product_key] → Product[product_key] (Many-to-One, Single)
- WorkOrders[facility_key] → Facility[facility_key] (Many-to-One, Single)

---

#### **Supply Chain Domain**

**Inventory Fact:**
- Inventory[snapshot_date_id] → Date[date_id] (Many-to-One, Single)
- Inventory[product_key] → Product[product_key] (Many-to-One, Single)
- Inventory[facility_key] → Facility[facility_key] (Many-to-One, Single)

**PurchaseOrders Fact:**
- PurchaseOrders[order_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- PurchaseOrders[delivery_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- PurchaseOrders[product_key] → Product[product_key] (Many-to-One, Single)
- PurchaseOrders[facility_key] → Facility[facility_key] (Many-to-One, Single)

---

#### **ESG Domain**

**Emissions Fact:**
- Emissions[reporting_date_id] → Date[date_id] (Many-to-One, Single)
- Emissions[facility_key] → Facility[facility_key] (Many-to-One, Single)

---

#### **Risk, Compliance & Audit Domain**

**Risks Fact:**
- Risks[identified_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Risks[review_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Risks[owner_key] → Employee[employee_key] (Many-to-One, Single)

**Audits Fact:**
- Audits[audit_date_id] → Date[date_id] (Many-to-One, Single)
- Audits[auditor_key] → Employee[employee_key] (Many-to-One, Single)

**ComplianceChecks Fact:**
- ComplianceChecks[check_date_id] → Date[date_id] (Many-to-One, Single)

---

#### **R&D Domain**

**Experiments Fact:**
- Experiments[start_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Experiments[end_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Experiments[project_key] → Project[project_key] (Many-to-One, Single)
- Experiments[lead_scientist_key] → Employee[employee_key] (Many-to-One, Single)

---

#### **Quality & Security Domain**

**Defects Fact:**
- Defects[found_date_id] → Date[date_id] (Many-to-One, Single) **Active**
- Defects[resolved_date_id] → Date[date_id] (Many-to-One, Single) **Inactive**
- Defects[product_key] → Product[product_key] (Many-to-One, Single)
- Defects[facility_key] → Facility[facility_key] (Many-to-One, Single)

**SecurityEvents Fact:**
- SecurityEvents[event_date_id] → Date[date_id] (Many-to-One, Single)
- SecurityEvents[assigned_to_key] → Employee[employee_key] (Many-to-One, Single)

---

### Relationship Summary

- **Total Relationships:** ~80 (varies by model configuration)
- **Date Role-Playing:** Date dimension used in 40+ relationships (one active per fact)
- **Employee Role-Playing:** Employee dimension in multiple roles (salesperson, agent, manager, owner)
- **Facility Usage:** Manufacturing, Supply Chain, ESG, Quality domains
- **Project Usage:** R&D domain
- **Account Usage:** Finance and FinOps domains

**Best Practice:** Use `USERELATIONSHIP()` in DAX measures to activate inactive relationships temporarily:

```dax
Revenue by Ship Date = 
CALCULATE(
    [Total Revenue],
    USERELATIONSHIP(Sales[ship_date_id], Date[date_id])
)
```
- Marketing[activity_date_id] → Date[date_id] (Many-to-One, Single)

### Relationship Diagram

```
                    Date
                     |
       +-------------+-------------+-------------+-------------+
       |             |             |             |             |
     Sales       Support          HR        Inventory      Marketing
       |             |             |             |
       +------+------+             |             |
              |                    |             |
         Customer                  |             |
              |                    |             |
              +--------------------+-------------+
                                   |
                              Employee
                                   |
                              Geography
                                   |
                              Product
```

---

## 🏷️ Table Details

### Sales (Fact)

**Visibility:** Shown  
**Storage Mode:** Direct Lake  
**Source Query:** `SELECT * FROM FactSales`

**Columns:**

| Column | Data Type | Visible | Description | Format String |
|--------|-----------|---------|-------------|---------------|
| sales_key | Int64 | Hidden | Surrogate key | - |
| order_date_id | Int32 | Hidden | FK to Date | - |
| ship_date_id | Int32 | Hidden | FK to Date | - |
| customer_key | Int32 | Hidden | FK to Customer | - |
| product_key | Int32 | Hidden | FK to Product | - |
| employee_key | Int32 | Hidden | FK to Employee | - |
| geography_key | Int32 | Hidden | FK to Geography | - |
| order_number | String | Visible | Order ID | - |
| line_number | Int32 | Visible | Line # | - |
| quantity | Int32 | Visible | Units sold | #,##0 |
| unit_price | Decimal | Visible | Price per unit | $#,##0.00 |
| unit_cost | Decimal | Hidden | Cost per unit | $#,##0.00 |
| discount_amount | Decimal | Visible | Discount | $#,##0.00 |
| line_total | Decimal | Hidden | Use measure instead | $#,##0.00 |
| line_cost | Decimal | Hidden | Use measure instead | $#,##0.00 |
| line_margin | Decimal | Hidden | Use measure instead | $#,##0.00 |
| tax_amount | Decimal | Visible | Sales tax | $#,##0.00 |

**Key Measures:**
- Total Revenue = SUM(Sales[line_total])
- Total Cost = SUM(Sales[line_cost])
- Gross Profit = SUM(Sales[line_margin])
- Gross Margin % = DIVIDE([Gross Profit], [Total Revenue])

---

### Date (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake  
**Mark as Date Table:** Yes (on `full_date` column)

**Columns:**

| Column | Data Type | Visible | Description | Sort By |
|--------|-----------|---------|-------------|---------|
| date_id | Int32 | Hidden | Surrogate key (PK) | - |
| full_date | Date | Visible | Actual date | - |
| year | Int32 | Visible | Calendar year | - |
| quarter | Int32 | Visible | Quarter (1-4) | - |
| month | Int32 | Visible | Month (1-12) | - |
| month_name | String | Visible | Month name | month |
| week_of_year | Int32 | Visible | Week # | - |
| day_of_week | Int32 | Hidden | Day # (1-7) | - |
| day_name | String | Visible | Day name | day_of_week |
| is_weekend | Boolean | Visible | Weekend flag | - |
| is_holiday | Boolean | Visible | Holiday flag | - |
| holiday_name | String | Visible | Holiday name | - |
| fiscal_year | Int32 | Visible | Fiscal year | - |
| fiscal_quarter | String | Visible | FY quarter | - |
| fiscal_month | Int32 | Visible | Fiscal month | - |

**Hierarchies:**

**Calendar Hierarchy:**
- Level 1: Year
- Level 2: Quarter
- Level 3: Month (display: month_name, sort by: month)
- Level 4: Full Date

**Fiscal Hierarchy:**
- Level 1: Fiscal Year
- Level 2: Fiscal Quarter
- Level 3: Fiscal Month
- Level 4: Full Date

**Week Hierarchy:**
- Level 1: Year
- Level 2: Week of Year
- Level 3: Full Date

---

### Customer (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description | Format String |
|--------|-----------|---------|-------------|---------------|
| customer_key | Int32 | Hidden | Surrogate key (PK) | - |
| customer_id | String | Visible | Business key | - |
| customer_name | String | Visible | Company name | - |
| industry | String | Visible | Industry | - |
| customer_segment | String | Visible | SMB/Mid/Enterprise | - |
| country_code | String | Hidden | ISO code | - |
| country_name | String | Visible | Country | - |
| region | String | Visible | Geographic region | - |
| annual_revenue | Decimal | Visible | Annual revenue | $#,##0 |
| employee_count | Int32 | Visible | # of employees | #,##0 |
| credit_limit | Decimal | Hidden | Credit limit (CLS) | $#,##0 |
| is_active | Boolean | Visible | Active customer | - |
| first_purchase_date | Date | Visible | First order date | - |
| lifetime_value | Decimal | Hidden | Use measure instead | - |

**Hierarchies:**

**Geography Hierarchy:**
- Level 1: Region
- Level 2: Country Name
- Level 3: Customer Name

**Segment Hierarchy:**
- Level 1: Customer Segment
- Level 2: Industry
- Level 3: Customer Name

---

### Product (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description | Format String |
|--------|-----------|---------|-------------|---------------|
| product_key | Int32 | Hidden | Surrogate key (PK) | - |
| product_id | String | Visible | SKU | - |
| product_name | String | Visible | Product name | - |
| category_l1 | String | Visible | Top category | - |
| category_l2 | String | Visible | Sub-category | - |
| category_l3 | String | Visible | Product family | - |
| supplier_name | String | Visible | Supplier | - |
| list_price | Decimal | Visible | MSRP | $#,##0.00 |
| cost_price | Decimal | Hidden | Cost (CLS) | $#,##0.00 |
| gross_margin_pct | Decimal | Hidden | Use measure instead | - |
| is_discontinued | Boolean | Visible | Discontinued | - |
| product_lifecycle | String | Visible | Lifecycle stage | - |
| launch_date | Date | Visible | Launch date | - |

**Hierarchies:**

**Category Hierarchy:**
- Level 1: Category L1
- Level 2: Category L2
- Level 3: Category L3
- Level 4: Product Name

**Lifecycle Hierarchy:**
- Level 1: Product Lifecycle
- Level 2: Product Name

---

### Employee (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description |
|--------|-----------|---------|-------------|
| employee_key | Int32 | Hidden | Surrogate key (PK) |
| employee_id | String | Visible | Employee ID |
| full_name | String | Visible | Full name |
| email | String | Hidden | Email (PII) |
| department | String | Visible | Department |
| job_title | String | Visible | Job title |
| manager_name | String | Visible | Manager |
| hire_date | Date | Visible | Hire date |
| tenure_years | Decimal | Visible | Years employed |
| salary_band | String | Hidden | Salary band (CLS) |
| location | String | Visible | Office location |
| region | String | Visible | Office region |

**Hierarchies:**

**Organization Hierarchy:**
- Level 1: Department
- Level 2: Manager Name
- Level 3: Full Name

**Geography Hierarchy:**
- Level 1: Region
- Level 2: Location
- Level 3: Full Name

---

### Geography (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description |
|--------|-----------|---------|-------------|
| geography_key | Int32 | Hidden | Surrogate key (PK) |
| geography_id | String | Visible | Geography code |
| country_code | String | Visible | ISO country code |
| country_name | String | Visible | Country |
| region | String | Visible | Geographic region |
| city | String | Visible | City |
| postal_code | String | Visible | ZIP/Postal code |

**Hierarchies:**

**Geography Hierarchy:**
- Level 1: Region
- Level 2: Country Name
- Level 3: City

---

### Facility (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description |
|--------|-----------|---------|-------------|
| facility_key | Int32 | Hidden | Surrogate key (PK) |
| facility_id | String | Visible | Facility code |
| facility_name | String | Visible | Facility name |
| facility_type | String | Visible | Plant, Warehouse, DC, Office |
| geography_key | Int32 | Hidden | FK to Geography |
| country_name | String | Visible | Country |
| region | String | Visible | Region |
| capacity | Int32 | Visible | Capacity (units/sqft) |
| is_active | Boolean | Visible | Active facility |
| opened_date | Date | Visible | Opened date |

**Hierarchies:**

**Location Hierarchy:**
- Level 1: Region
- Level 2: Country Name
- Level 3: Facility Name

**Type Hierarchy:**
- Level 1: Facility Type
- Level 2: Facility Name

**Use Cases:**
- Manufacturing production tracking
- Inventory management by warehouse/DC
- Carbon emissions by facility (ESG)
- Quality defects by manufacturing plant

---

### Project (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description |
|--------|-----------|---------|-------------|
| project_key | Int32 | Hidden | Surrogate key (PK) |
| project_id | String | Visible | Project code |
| project_name | String | Visible | Project name |
| project_type | String | Visible | R&D, IT, Business |
| project_status | String | Visible | Active, Completed, On Hold |
| start_date | Date | Visible | Project start |
| end_date | Date | Visible | Project end |
| budget | Decimal | Visible | Total budget | $#,##0 |
| owner_key | Int32 | Hidden | FK to Employee |
| owner_name | String | Visible | Project owner |

**Hierarchies:**

**Project Hierarchy:**
- Level 1: Project Type
- Level 2: Project Status
- Level 3: Project Name

**Use Cases:**
- R&D experiment tracking
- IT incident assignment to projects
- Cross-domain project analytics

---

### Account (Dimension)

**Visibility:** Shown  
**Storage Mode:** Direct Lake

**Columns:**

| Column | Data Type | Visible | Description |
|--------|-----------|---------|-------------|
| account_key | Int32 | Hidden | Surrogate key (PK) |
| account_id | String | Visible | Account number |
| account_name | String | Visible | Account description |
| account_type | String | Visible | Asset, Liability, Equity, Revenue, Expense |
| account_category | String | Visible | Category (OpEx, CapEx, COGS, etc.) |
| parent_account_id | String | Visible | Parent account |
| is_active | Boolean | Visible | Active account |

**Hierarchies:**

**GL Hierarchy:**
- Level 1: Account Type
- Level 2: Account Category
- Level 3: Account Name

**Use Cases:**
- Finance general ledger reporting
- Budget vs actuals tracking
- Cloud cost allocation (FinOps)
- Expense analysis

---

## 📏 Measures

**Measure Tables:**
- Create separate "Measures" tables for organization
- Group by domain: `_Sales Measures`, `_Support Measures`, `_HR Measures`

### Core Sales Measures

```dax
Total Revenue = SUM(Sales[line_total])

Total Cost = SUM(Sales[line_cost])

Gross Profit = [Total Revenue] - [Total Cost]

Gross Margin % = DIVIDE([Gross Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(Sales[order_number])

Total Units Sold = SUM(Sales[quantity])

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Revenue YTD = 
TOTALYTD([Total Revenue], Date[full_date])

Revenue PY = 
CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Date[full_date]))

Revenue YoY % = 
DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0)
```

*See [dax-measures.md](./dax-measures.md) for full list (100+ measures)*

---

## 🔒 Row-Level Security (RLS)

### Roles Defined

**Role: Regional Sales Manager**

Apply to: `Customer` table

```dax
[region] = USERPRINCIPALNAME()
```

**Better approach with lookup table:**

Create table: `SecurityUserRegion`
- Columns: UserEmail (String), Region (String)
- Data: hr.manager@company.com | North America

```dax
Customer[region] IN 
VALUES(
    FILTER(
        SecurityUserRegion,
        SecurityUserRegion[UserEmail] = USERPRINCIPALNAME()
    )
)
```

**Role: Finance Team (Full Access)**

No filter = sees all data

**Role: External Auditor (Read-Only Historical)**

Apply to: `Date` table

```dax
Date[full_date] < DATE(2024, 1, 1)
```

---

## 🚫 Column-Level Security (CLS)

**Hide from non-HR roles:**
- Employee[salary_band]
- Employee[email]
- Product[cost_price]
- Customer[credit_limit]

**Implementation:**
1. Power BI Desktop → Select column
2. Column Tools → Advanced → Object-level security
3. Check "Hide from" → Select roles

---

## ⚙️ Model Configuration

### General Settings

- **Name:** EnterprisePlatform_SemanticModel
- **Compatibility Level:** 1605 (SQL Server 2022 / Power BI 2023+)
- **Default Mode:** Direct Lake
- **Locale:** en-US
- **Collation:** Latin1_General_100_CI_AS_KS_SC

### Performance Settings

**Direct Lake:**
- Max Memory: Auto (use Fabric capacity settings)
- Query Timeout: 600 seconds
- Enable Query Interleaving: Yes

**Refresh:**
- Not applicable (Direct Lake is live query)
- Metadata refresh: Daily at 6 AM (to pick up schema changes)

---

## 🎨 Display Folders

Organize measures and columns into folders for better UX.

**Sales Table Folders:**
- 📁 Key Fields: order_number, line_number
- 📁 Quantities: quantity
- 📁 Prices: unit_price, discount_amount
- 📁 Dates: order_date_id, ship_date_id (hidden)

**Date Table Folders:**
- 📁 Calendar: year, quarter, month, day_name
- 📁 Fiscal: fiscal_year, fiscal_quarter, fiscal_month
- 📁 Flags: is_weekend, is_holiday

**Customer Table Folders:**
- 📁 Identification: customer_id, customer_name
- 📁 Classification: industry, customer_segment
- 📁 Geography: country_name, region
- 📁 Metrics: annual_revenue, employee_count

---

## 📊 Calculation Groups

### Time Intelligence

**Table:** `Time Calculations`  
**Column:** `Calculation`

**Items:**
- Current Period (Ordinal: 0)
- Prior Period (Ordinal: 1)
- Year to Date (Ordinal: 2)
- Prior Year (Ordinal: 3)
- Year over Year % (Ordinal: 4)

**Format String Expression:**
```dax
SWITCH(
    SELECTEDVALUE('Time Calculations'[Calculation]),
    "Year over Year %", "0.0%",
    "$#,##0"
)
```

**Calculation Expression:**
```dax
SWITCH(
    SELECTEDVALUE('Time Calculations'[Calculation]),
    "Current Period", SELECTEDMEASURE(),
    "Prior Period", CALCULATE(SELECTEDMEASURE(), DATEADD(Date[full_date], -1, MONTH)),
    "Year to Date", TOTALYTD(SELECTEDMEASURE(), Date[full_date]),
    "Prior Year", CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(Date[full_date])),
    "Year over Year %", 
        VAR CurrentValue = SELECTEDMEASURE()
        VAR PYValue = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR(Date[full_date]))
        RETURN DIVIDE(CurrentValue - PYValue, PYValue)
)
```

**Usage:**
- Drag any measure to a visual
- Add `Time Calculations[Calculation]` to columns/legend
- Instantly see Current, PY, YTD, YoY %

---

## 🧪 Model Validation

### Checklist

- [ ] All relationships active and correct cardinality
- [ ] Mark as Date Table set on Date[full_date]
- [ ] All hierarchies defined with correct sort orders
- [ ] All measures use DIVIDE (not /) to handle divide-by-zero
- [ ] RLS roles created and tested
- [ ] CLS applied to sensitive columns
- [ ] No circular dependencies (Analyze → View Dependency)
- [ ] Performance Analyzer shows queries < 1 second
- [ ] Direct Lake mode verified (not imported)
- [ ] Metadata refresh scheduled

### Testing Queries

**Total Revenue (should match SQL):**
```dax
EVALUATE
SUMMARIZE(
    Sales,
    "Total Revenue", SUM(Sales[line_total])
)
```

**Cross-Check with SQL:**
```sql
SELECT SUM(line_total) AS total_revenue FROM FactSales
```

**Relationship Test:**
```dax
EVALUATE
SUMMARIZE(
    Sales,
    Customer[customer_name],
    "Revenue", SUM(Sales[line_total])
)
ORDER BY [Revenue] DESC
```

---

## 📝 Deployment Notes

### Using Power BI Desktop

1. Open new Power BI Desktop file
2. Get Data → More → OneLake data hub
3. Select EnterpriseLakehouse → Gold layer tables
4. Select all Gold tables:
   - **8 Dimensions:** Gold_DimDate, Gold_DimCustomer, Gold_DimProduct, Gold_DimEmployee, Gold_DimGeography, Gold_DimFacility, Gold_DimProject, Gold_DimAccount
   - **23 Fact Tables:** Gold_FactSales, Gold_FactReturns, Gold_FactOpportunities, Gold_FactActivities, Gold_FactSupport, Gold_FactCampaigns, Gold_FactHiring, Gold_FactAttrition, Gold_FactGeneralLedger, Gold_FactBudget, Gold_FactCloudCosts, Gold_FactIncidents, Gold_FactProduction, Gold_FactWorkOrders, Gold_FactInventory, Gold_FactPurchaseOrders, Gold_FactEmissions, Gold_FactRisks, Gold_FactAudits, Gold_FactComplianceChecks, Gold_FactExperiments, Gold_FactDefects, Gold_FactSecurityEvents
5. Load tables (Direct Lake mode is automatic for Fabric Lakehouse)
6. Create relationships (Model view):
   - Auto-detect will find most relationships
   - Review and set inactive relationships for role-playing dimensions (Date)
7. Mark Date table: Modeling → Mark as Date Table (on Date[full_date])
8. Create dimension hierarchies
9. Import DAX measures from [dax-measures.md](./dax-measures.md)
10. Configure RLS roles (Modeling → Manage Roles)
11. Test model with sample queries
12. Publish to Fabric workspace: Home → Publish

**Estimated Setup Time:** 30-45 minutes (relationships, hierarchies, measures)

### Using XMLA Endpoint (Advanced)

1. Create .bim file with model definition
2. Deploy via Tabular Editor, ALM Toolkit, or TMSL script
3. Connect to workspace XMLA endpoint
4. Execute CreateOrReplace TMSL command

### Using Power BI MCP Extension (VS Code)

See [powerbi-mcp.md](./powerbi-mcp.md) for detailed steps.

---

## � Model Summary

### Tables Overview

**Total Tables:** 31 (8 dimensions + 23 facts)  
**Total Relationships:** ~80  
**Total Expected Rows:** ~1.8M fact records + ~64K dimension records  
**Domains Covered:** 15 business domains across the enterprise

### Fact Tables by Domain (23)

| # | Domain | Fact Table | Key Dimensions |
|---|--------|-----------|----------------|
| 1 | Sales | FactSales | Date, Customer, Product, Employee, Geography |
| 2 | Sales | FactReturns | Date, Customer, Product |
| 3 | CRM | FactOpportunities | Date, Customer, Employee |
| 4 | CRM | FactActivities | Date, Customer, Employee |
| 5 | Customer Service | FactSupport | Date, Customer, Product, Employee |
| 6 | Marketing | FactCampaigns | Date, Employee |
| 7 | HR | FactHiring | Date, Employee |
| 8 | HR | FactAttrition | Date, Employee |
| 9 | Finance | FactGeneralLedger | Date, Account, Employee |
| 10 | Finance | FactBudget | Date, Account |
| 11 | FinOps | FactCloudCosts | Date, Account |
| 12 | IT Ops | FactIncidents | Date, Employee |
| 13 | Manufacturing | FactProduction | Date, Product, Facility |
| 14 | Manufacturing | FactWorkOrders | Date, Product, Facility |
| 15 | Supply Chain | FactInventory | Date, Product, Facility |
| 16 | Supply Chain | FactPurchaseOrders | Date, Product, Facility |
| 17 | ESG | FactEmissions | Date, Facility |
| 18 | Risk & Compliance | FactRisks | Date, Employee |
| 19 | Risk & Compliance | FactAudits | Date, Employee |
| 20 | Risk & Compliance | FactComplianceChecks | Date |
| 21 | R&D | FactExperiments | Date, Project, Employee |
| 22 | Quality | FactDefects | Date, Product, Facility |
| 23 | Security | FactSecurityEvents | Date, Employee |

### Dimension Usage Matrix

| Dimension | # of Fact Tables | Primary Use Cases |
|-----------|------------------|-------------------|
| **Date** | 23 (all) | Universal time dimension with role-playing (40+ relationships) |
| **Employee** | 11 | Sales, CRM, Support, HR, Finance, IT, Risk, R&D, Security |
| **Customer** | 5 | Sales, Returns, CRM, Support |
| **Product** | 7 | Sales, Returns, Support, Production, WorkOrders, Inventory, PO, Defects |
| **Facility** | 6 | Production, WorkOrders, Inventory, PO, Emissions, Defects |
| **Account** | 3 | GeneralLedger, Budget, CloudCosts |
| **Project** | 1 | Experiments (R&D) |
| **Geography** | 1 | Sales (ship-to location) |

### Key Metrics by Domain

- **Sales:** Revenue, Margin, Units, Orders, Returns Rate
- **CRM:** Pipeline Value, Win Rate, Activity Volume
- **Customer Service:** Ticket Volume, Resolution Time, CSAT, SLA Compliance
- **Marketing:** Campaign ROI, Leads, Conversions, Cost per Lead
- **HR:** Headcount, Attrition Rate, Time to Hire, Retention
- **Finance:** Budget vs Actual, Variance %, GL Balances
- **FinOps:** Cloud Spend, Cost per Service, Variance
- **IT Ops:** Incident Count, MTTR, Availability %
- **Manufacturing:** Production Volume, Yield %, Downtime
- **Supply Chain:** Inventory Turns, Stock Levels, Lead Time
- **ESG:** Carbon Emissions (Scope 1-3), Emissions Intensity
- **Risk & Compliance:** Risk Score, Audit Findings, Compliance Rate
- **R&D:** Experiment Success Rate, Project Budget Utilization
- **Quality:** Defect Rate, PPM, Cost of Quality
- **Security:** Security Events, Vulnerabilities, Response Time

---

## 🚀 Next Steps

1. **Upload CSV Files:**
   - Upload generated CSV files to Fabric Lakehouse: `Files/bronze/`
   - Use Fabric UI or OneLake File Explorer

2. **Execute Fabric Notebooks:**
   - Run [01_ingest_to_bronze.ipynb](../notebooks/01_ingest_to_bronze.ipynb) to create Bronze Delta tables
   - Run [02_transform_to_silver.ipynb](../notebooks/02_transform_to_silver.ipynb) to create Silver tables
   - Run [03_build_gold_star_schema.ipynb](../notebooks/03_build_gold_star_schema.ipynb) to create Gold star schema

3. **Create Semantic Model:**
   - Use Power BI Desktop (recommended for first-time setup)
   - Or use Tabular Editor 3 via XMLA endpoint

4. **Build Reports:**
   - See [report-pages.md](./report-pages.md) for report design
   - Import visuals and templates

5. **Configure Data Agent:**
   - See [../data-agent/data-agent-setup.md](../data-agent/data-agent-setup.md)
   - Test with sample questions from [../data-agent/example-questions.md](../data-agent/example-questions.md)

6. **Deploy to Production:**
   - Configure deployment pipelines
   - Set up scheduled metadata refresh
   - Enable monitoring and usage metrics

---

**This semantic model specification is ready for implementation! 📊**

**Last Updated:** 2026-02-19  
**Version:** 2.0 (Complete Enterprise Model - 23 Facts, 8 Dimensions)  
**Status:** ✅ Complete and validated


