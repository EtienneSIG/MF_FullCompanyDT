# Semantic Model Specification

## 🎯 Overview

This document specifies the **Power BI semantic model** (formerly "dataset") for the Enterprise Data Platform demo. The model uses **Direct Lake mode** to query Gold layer Delta tables directly from OneLake.

**Model Name:** `EnterprisePlatform_SemanticModel`  
**Mode:** Direct Lake (no data import, live query to OneLake)  
**Lakehouse:** EnterpriseLakehouse (Gold layer tables)  
**Expected Performance:** Sub-second queries for < 10M rows

---

## 📊 Tables in Model

### Fact Tables

| Table | Source | Rows | Role in Model |
|-------|--------|------|---------------|
| **Sales** | FactSales | 2M | Transactions (order lines) |
| **Support** | FactSupport | 100K | Support tickets |
| **HR** | FactHR | 60K | Headcount snapshots |
| **Inventory** | FactInventory | 1.8M | Inventory snapshots |
| **Marketing** | FactMarketing | 365K | Campaign performance |

### Dimension Tables

| Table | Source | Rows | Role in Model |
|-------|--------|------|---------------|
| **Date** | DimDate | 4,380 | Shared date dimension |
| **Customer** | DimCustomer | 50K | Customer attributes |
| **Product** | DimProduct | 5K | Product catalog |
| **Employee** | DimEmployee | 8.5K | Employee roster |
| **Geography** | DimGeography | 500 | Locations |

### Supporting Tables

| Table | Type | Purpose |
|-------|------|---------|
| **Targets** | Static | Sales/support/HR targets by month |
| **Parameters** | Static | User-selectable parameters (Year, Region) |
| **SecurityRoles** | Static | RLS user-to-role mapping |

---

## 🔗 Relationships

### Star Schema Relationships

**From → To (Cardinality, Filter Direction)**

#### Sales Star
- Sales[order_date_id] → Date[date_id] (Many-to-One, Single)
- Sales[ship_date_id] → Date[date_id] (Many-to-One, Single) *Inactive by default*
- Sales[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Sales[product_key] → Product[product_key] (Many-to-One, Single)
- Sales[employee_key] → Employee[employee_key] (Many-to-One, Single)
- Sales[geography_key] → Geography[geography_key] (Many-to-One, Single)

#### Support Star
- Support[created_date_id] → Date[date_id] (Many-to-One, Single)
- Support[resolved_date_id] → Date[date_id] (Many-to-One, Single) *Inactive*
- Support[customer_key] → Customer[customer_key] (Many-to-One, Single)
- Support[agent_key] → Employee[employee_key] (Many-to-One, Single)

#### HR Star
- HR[snapshot_date_id] → Date[date_id] (Many-to-One, Single)
- HR[employee_key] → Employee[employee_key] (Many-to-One, Single)
- HR[manager_key] → Employee[employee_key] (Many-to-One, Single) *Role-playing dimension*

#### Inventory Star
- Inventory[snapshot_date_id] → Date[date_id] (Many-to-One, Single)
- Inventory[product_key] → Product[product_key] (Many-to-One, Single)
- Inventory[warehouse_key] → Geography[geography_key] (Many-to-One, Single)

#### Marketing Star
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
4. Import tables: FactSales, DimDate, DimCustomer, etc.
5. Switch to Direct Lake mode: File → Options → Current File → Direct Lake
6. Create relationships (Model view)
7. Create measures (Data view)
8. Publish to workspace: Home → Publish

### Using XMLA Endpoint (Advanced)

1. Create .bim file with model definition
2. Deploy via Tabular Editor, ALM Toolkit, or TMSL script
3. Connect to workspace XMLA endpoint
4. Execute CreateOrReplace TMSL command

### Using Power BI MCP Extension (VS Code)

See [powerbi-mcp.md](./powerbi-mcp.md) for detailed steps.

---

## 🚀 Next Steps

1. **Create Semantic Model:** Use Power BI Desktop or XMLA
2. **Build Reports:** See [report-pages.md](./report-pages.md)
3. **Configure Data Agent:** See [../data-agent/data-agent-setup.md](../data-agent/data-agent-setup.md)
4. **Test with Sample Questions:** See [../data-agent/example-questions.md](../data-agent/example-questions.md)

---

**This semantic model specification is ready for implementation! 📊**
