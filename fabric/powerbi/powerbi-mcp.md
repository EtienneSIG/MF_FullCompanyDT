# Power BI MCP Server - VS Code Integration Guide

## 🎯 Overview

The **Power BI Model Context Protocol (MCP) Server** brings AI-powered semantic model development to Visual Studio Code. This integration allows you to:

- **Build models faster** with Copilot-assisted DAX authoring
- **Maintain consistency** through automated naming conventions
- **Improve quality** with built-in validation and best practices
- **Enhance AI readiness** by bulk-adding descriptions and synonyms

**Use Cases:**
- Creating relationships across multiple fact tables
- Generating time intelligence measures (YTD, QTD, MoM)
- Bulk renaming tables/columns for consistency
- Adding metadata for Data Agent optimization
- Validating complex DAX expressions

---

## 🚀 Getting Started

### Prerequisites

- **VS Code** (latest version)
- **Power BI Desktop** (optional - for testing)
- **Microsoft Fabric Workspace** with Premium capacity
- **Semantic Model** (published to Fabric or open in Desktop)

### Installation

1. **Install Power BI Modeling MCP Server Extension:**
   ```
   VS Code → Extensions → Search "Power BI Modeling MCP" → Install
   ```

2. **Verify Installation:**
   - Open Command Palette (Ctrl+Shift+P)
   - Type "Power BI"
   - You should see Power BI MCP commands

3. **Enable Copilot Chat:**
   - Ensure GitHub Copilot extension is installed
   - Sign in with GitHub account

---

## 🔌 Connecting to Semantic Models

### Option 1: Connect to Fabric Workspace

```
1. Open VS Code
2. Ctrl+Shift+P → "Power BI: Connect to Workspace"
3. Sign in with Azure AD
4. Select Workspace: "EnterprisePlatformDemo"
5. Select Semantic Model: "Enterprise Analytics Model"
```

**Copilot Chat Alternative:**
```
User: "Connect to Power BI semantic model in Fabric workspace 'EnterprisePlatformDemo'"
Copilot: [Guides through connection steps]
```

### Option 2: Connect to Power BI Desktop

```
1. Open .pbix file in Power BI Desktop
2. Note the port number (usually localhost:xxxxx)
3. In VS Code: Ctrl+Shift+P → "Power BI: Connect to Desktop"
4. Enter: localhost:<port>
5. Select dataset
```

### Option 3: Connect to PBIP (Power BI Project)

```
1. Open folder containing .pbip files in VS Code
2. VS Code auto-detects Power BI project
3. Copilot Chat: "Show me the semantic model structure"
```

---

## 💬 Using Copilot Chat for Model Development

### 1. Exploring the Model

**Prompt:**
```
"Show me all fact tables and their relationships to dimensions"
```

**Copilot Response:**
```
Found 15 fact tables:

FactSales
├── → DimCustomer (customer_id)
├── → DimProduct (product_id)
├── → DimEmployee (employee_id - Sales Rep)
├── → DimDate (order_date_id)
├── → DimDate (ship_date_id)
└── → DimDate (delivery_date_id)

FactSupport
├── → DimCustomer (customer_id)
├── → DimProduct (product_id)
├── → DimEmployee (agent_employee_id)
├── → DimDate (create_date_id)
└── → DimDate (resolution_date_id)

[... continues for all fact tables]
```

---

### 2. Creating Relationships

**Prompt:**
```
"Create all missing relationships between FactSales and dimension tables using standard naming conventions"
```

**Copilot Response:**
```dax
// Creating relationships for FactSales

// Relationship: DimCustomer → FactSales
EVALUATE
    RELATEDTABLE(
        RELATIONSHIP(DimCustomer[customer_id], FactSales[customer_id]),
        CARDINALITY = ONE_TO_MANY,
        CROSS_FILTER = SINGLE
    )

// Relationship: DimProduct → FactSales
EVALUATE
    RELATEDTABLE(
        RELATIONSHIP(DimProduct[product_id], FactSales[product_id]),
        CARDINALITY = ONE_TO_MANY,
        CROSS_FILTER = SINGLE
    )

// Relationship: DimEmployee → FactSales (Sales Rep role)
EVALUATE
    RELATEDTABLE(
        RELATIONSHIP(DimEmployee[employee_id], FactSales[employee_id]),
        CARDINALITY = ONE_TO_MANY,
        CROSS_FILTER = SINGLE
    )

// Relationship: DimDate → FactSales (Order Date role)
EVALUATE
    RELATEDTABLE(
        RELATIONSHIP(DimDate[date_id], FactSales[order_date_id]),
        CARDINALITY = ONE_TO_MANY,
        CROSS_FILTER = SINGLE
    )

✅ 4 relationships created successfully
```

**Action:** Copilot automatically creates these relationships in the model.

---

### 3. Generating DAX Measures

**Prompt:**
```
"Generate YTD, QTD, and MoM measures for Total Revenue with proper formatting"
```

**Copilot Response:**
```dax
// Base Measure
Total Revenue = 
CALCULATE(
    SUM(FactSales[net_amount]),
    FactSales[status] <> "Cancelled",
    FactSales[status] <> "Returned"
)

// Year-to-Date Revenue
Revenue YTD = 
CALCULATE(
    [Total Revenue],
    DATESYTD(DimDate[Date])
)

// Quarter-to-Date Revenue
Revenue QTD = 
CALCULATE(
    [Total Revenue],
    DATESQTD(DimDate[Date])
)

// Month-over-Month Revenue
Revenue MoM = 
VAR CurrentMonthRevenue = [Total Revenue]
VAR PriorMonthRevenue = 
    CALCULATE(
        [Total Revenue],
        DATEADD(DimDate[Date], -1, MONTH)
    )
RETURN
    DIVIDE(
        CurrentMonthRevenue - PriorMonthRevenue,
        PriorMonthRevenue,
        BLANK()
    )

// Month-over-Month Revenue %
Revenue MoM % = 
FORMAT([Revenue MoM], "0.0%")

✅ 5 measures created in FactSales table
```

---

### 4. Bulk Renaming for Consistency

**Prompt:**
```
"Rename all columns in FactSales to follow snake_case convention and add 'Dim' prefix to all dimension tables"
```

**Copilot Response:**
```
Renaming columns in FactSales:
  OrderID → order_id
  CustomerID → customer_id
  OrderDate → order_date
  TotalAmount → total_amount
  [... 15 columns renamed]

Renaming dimension tables:
  Customer → DimCustomer
  Product → DimProduct
  Date → DimDate
  Employee → DimEmployee
  Geography → DimGeography

✅ 20 objects renamed successfully
```

---

### 5. Adding Descriptions and Synonyms (AI Readiness)

**Prompt:**
```
"Add business-friendly descriptions and synonyms to all tables and top 10 measures for Data Agent optimization"
```

**Copilot Response:**
```
Adding metadata to tables:

DimCustomer:
  Description: "Customer master data including industry, segment, and geographic information"
  Synonyms: ["clients", "accounts", "buyers"]

FactSales:
  Description: "Sales transactions with order details, pricing, and delivery information"
  Synonyms: ["orders", "revenue", "transactions"]

Adding metadata to measures:

Total Revenue:
  Description: "Sum of net sales amount excluding cancelled and returned orders"
  Synonyms: ["sales", "income", "turnover"]
  Format: "$#,##0"

Gross Margin %:
  Description: "Percentage of profit after cost of goods sold"
  Synonyms: ["profit margin", "margin percentage"]
  Format: "0.0%"

✅ Metadata added to 20 tables and 10 measures
```

**Impact:** Data Agent now understands natural language queries like:
- "Show me turnover by client segment" (uses synonyms)
- "What's our profit margin?" (maps to Gross Margin %)

---

### 6. Validating DAX Queries

**Prompt:**
```dax
"Validate this DAX query:
EVALUATE
SUMMARIZECOLUMNS(
    DimProduct[category],
    DimDate[Year],
    'Total Revenue', [Total Revenue],
    'Margin %', DIVIDE([Gross Margin], [Total Revenue])
)
ORDER BY [Total Revenue] DESC
"
```

**Copilot Response:**
```
✅ Query is valid

Suggestions:
1. Consider using TOPN() for better performance if you only need top N results
2. Add filter context for date range to avoid scanning entire table
3. 'Margin %' is not a measure - use [Gross Margin %] or define inline

Optimized version:

EVALUATE
TOPN(
    10,
    SUMMARIZECOLUMNS(
        DimProduct[category],
        DimDate[Year],
        FILTER(DimDate[Year] >= 2024, ALL(DimDate[Year])),
        "Total Revenue", [Total Revenue],
        "Margin %", [Gross Margin %]
    ),
    [Total Revenue], DESC
)
```

---

### 7. Creating Calculated Columns

**Prompt:**
```
"Create a calculated column in DimCustomer for Customer Lifetime Value Bucket based on total revenue"
```

**Copilot Response:**
```dax
Customer LTV Bucket = 
VAR CustomerRevenue = 
    CALCULATE(
        SUM(FactSales[net_amount]),
        ALLEXCEPT(DimCustomer, DimCustomer[customer_id])
    )
RETURN
    SWITCH(
        TRUE(),
        CustomerRevenue >= 1000000, "Platinum",
        CustomerRevenue >= 500000, "Gold",
        CustomerRevenue >= 100000, "Silver",
        "Bronze"
    )

✅ Calculated column added to DimCustomer
⚠️  Note: Consider using a measure instead for better performance in Direct Lake
```

---

### 8. Creating Hierarchies

**Prompt:**
```
"Create date hierarchies for DimDate (Year > Quarter > Month > Date) and product hierarchy for DimProduct (Category > Subcategory > Product)"
```

**Copilot Response:**
```
Creating Date Hierarchy:
  DimDate
  └── Date Hierarchy
      ├── Year
      ├── Quarter
      ├── Month
      └── Date

Creating Product Hierarchy:
  DimProduct
  └── Product Hierarchy
      ├── Category
      ├── Subcategory
      └── Product Name

✅ 2 hierarchies created
```

---

### 9. Applying Row-Level Security (RLS)

**Prompt:**
```
"Create RLS role for regional sales managers who should only see data for their assigned region"
```

**Copilot Response:**
```dax
// Role: Regional Sales Manager

// Filter DimCustomer by Region
[Region] = USERPRINCIPALNAME()

// Filter FactSales through relationship
// (automatic via relationship to DimCustomer)

// Alternative: Dynamic RLS using lookup table
[Region] = 
LOOKUPVALUE(
    DimEmployee[region],
    DimEmployee[email], USERPRINCIPALNAME()
)

✅ RLS role created: "Regional Sales Manager"
⚠️  Remember to add users to this role in Fabric workspace settings
```

---

### 10. Generating Complete Measure Groups

**Prompt:**
```
"Generate a complete measure group for inventory analytics including: Inventory Value, Inventory Turns, Days of Supply, Stockout Rate, and Fill Rate"
```

**Copilot Response:**
```dax
// === INVENTORY ANALYTICS MEASURE GROUP ===

// Base Measures
Inventory Value = 
SUM(FactInventory[inventory_value])

Inventory Quantity = 
SUM(FactInventory[quantity_on_hand])

// Inventory Turns = COGS / Average Inventory
Inventory Turns = 
VAR COGS = SUM(FactSales[cost_amount])
VAR AvgInventory = AVERAGE(FactInventory[inventory_value])
RETURN
    DIVIDE(COGS, AvgInventory, 0)

// Days of Supply
Days of Supply = 
AVERAGEX(
    FactInventory,
    FactInventory[days_of_supply]
)

// Stockout Rate = % of time inventory is zero
Stockout Rate = 
VAR StockoutDays = 
    CALCULATE(
        COUNTROWS(FactInventory),
        FactInventory[quantity_available] = 0
    )
VAR TotalDays = COUNTROWS(FactInventory)
RETURN
    DIVIDE(StockoutDays, TotalDays, 0)

// Fill Rate = % of demand met from stock
Fill Rate = 
VAR DemandMet = SUM(FactSales[quantity])
VAR TotalDemand = 
    SUM(FactSales[quantity]) + 
    SUM(FactBackorders[quantity])
RETURN
    DIVIDE(DemandMet, TotalDemand, 0)

// Format Fill Rate as %
Fill Rate % = 
FORMAT([Fill Rate], "0.0%")

✅ 7 measures created in "Inventory Analytics" folder
```

---

## 🎯 10 Ready-to-Use Prompts for Enterprise Model

### 1. Model Setup
```
"Create all standard relationships between fact tables and conformed dimensions (DimDate, DimCustomer, DimProduct, DimEmployee, DimGeography)"
```

### 2. Time Intelligence
```
"Generate complete time intelligence measures (YTD, QTD, MTD, PY, YoY%, MoM%) for: Revenue, Gross Margin, Order Count, Customer Count"
```

### 3. Sales Analytics
```
"Create sales analytics measures: Average Order Value, Items per Order, Conversion Rate, Win Rate, Pipeline Value"
```

### 4. Customer Analytics
```
"Generate customer measures: Customer Lifetime Value, Churn Rate, Retention Rate, Average Revenue Per Customer, Active Customer Count"
```

### 5. HR Analytics
```
"Create HR measures: Headcount, Attrition Rate, Voluntary Attrition %, Time to Fill, Cost per Hire, Training Hours per Employee"
```

### 6. Supply Chain Analytics
```
"Generate supply chain KPIs: On-Time Delivery %, Inventory Turns, Backorder Rate, Supplier Lead Time, Cost Variance"
```

### 7. Quality & Performance
```
"Create quality measures: Defect Rate, First Pass Yield, OEE (Overall Equipment Effectiveness), CSAT Score, Net Promoter Score"
```

### 8. Financial Analytics
```
"Generate financial measures: Budget vs Actual Variance, Forecast Accuracy, Cash Flow, Operating Margin, EBITDA"
```

### 9. Data Quality & Governance
```
"Add comprehensive descriptions, synonyms, and sample values to all tables and measures for optimal Data Agent performance"
```

### 10. Performance Optimization
```
"Analyze model for performance issues and suggest: aggregations, calculated columns to convert to measures, relationship optimizations"
```

---

## 🔍 Best Practices

### 1. Consistent Naming
```
✅ DO:
  - Measures: "Total Revenue", "Gross Margin %"
  - Tables: "FactSales", "DimCustomer"
  - Columns: "customer_id", "order_date"

❌ DON'T:
  - Measures: "Rev", "GM_Pct"
  - Tables: "tbl_Sales", "Customer_Dim"
  - Columns: "CustID", "OrdDt"
```

### 2. Organize Measures in Display Folders
```
User: "Organize all measures into logical display folders by domain"

Copilot creates:
  Sales Metrics/
    ├── Total Revenue
    ├── Gross Margin %
    └── Average Order Value
  Time Intelligence/
    ├── Revenue YTD
    ├── Revenue QTD
    └── Revenue MoM %
```

### 3. Add FORMAT() for User-Friendly Display
```dax
// Bad
Revenue MoM = [Current Revenue] / [Prior Revenue] - 1

// Good
Revenue MoM % = 
FORMAT(
    DIVIDE([Current Revenue] - [Prior Revenue], [Prior Revenue], 0),
    "0.0%"
)
```

### 4. Use Variables for Readability
```dax
// Bad
Customer LTV = 
CALCULATE(
    SUM(FactSales[amount]),
    ALLEXCEPT(DimCustomer, DimCustomer[customer_id])
) / 
DATEDIFF(
    MIN(FactSales[order_date]),
    MAX(FactSales[order_date]),
    YEAR
)

// Good
Customer LTV = 
VAR TotalRevenue = 
    CALCULATE(
        SUM(FactSales[amount]),
        ALLEXCEPT(DimCustomer, DimCustomer[customer_id])
    )
VAR YearsActive = 
    DATEDIFF(
        MIN(FactSales[order_date]),
        MAX(FactSales[order_date]),
        YEAR
    )
RETURN
    DIVIDE(TotalRevenue, YearsActive, 0)
```

---

## 🚀 Advanced Workflows

### Workflow 1: New Model Setup (30 minutes)

```
1. "Connect to semantic model 'Enterprise Analytics Model'"
2. "Show me model structure and identify missing relationships"
3. "Create all standard relationships"
4. "Generate time intelligence measures for key metrics"
5. "Add descriptions and synonyms to all objects"
6. "Create display folders to organize measures by domain"
7. "Validate all DAX expressions"
8. "Generate model documentation in Markdown format"
```

### Workflow 2: Adding New Domain (15 minutes)

```
1. "I've added new tables: FactSupport, DimSupportCategory"
2. "Create relationships between FactSupport and existing dimensions"
3. "Generate standard measures for support analytics: CSAT, FCR%, Avg Resolution Time"
4. "Add metadata for Data Agent"
5. "Test with sample query"
```

### Workflow 3: Performance Tuning (20 minutes)

```
1. "Analyze model for performance bottlenecks"
2. "Suggest aggregations for FactSales"
3. "Identify calculated columns that should be measures"
4. "Recommend partitioning strategy for large tables"
5. "Validate query folding for DirectLake tables"
```

---

## 📊 Integration with Data Agent

MCP-generated metadata directly improves Data Agent responses:

**Without Metadata:**
```
User: "Show me sales"
Agent: "Which sales data? I see FactSales, FactOpportunities, FactReturns..."
```

**With MCP-Added Metadata:**
```
User: "Show me sales"
Agent: "Here's Total Revenue for the current period: $12.4M
       (using FactSales which tracks completed sales transactions)
       
       Would you also like to see pipeline (FactOpportunities) or returns?"
```

**Metadata Added by MCP:**
- Table descriptions explain purpose
- Synonyms map natural language to technical terms
- Sample values help agent understand data patterns
- Verified answers provide consistent responses

---

## 🛠️ Troubleshooting

### Issue: "Cannot connect to workspace"
**Solution:**
1. Verify you have Contributor/Admin role in Fabric workspace
2. Check that workspace has Premium capacity
3. Try: `az login` in terminal to refresh authentication

### Issue: "DAX validation fails"
**Solution:**
1. Check for typos in table/column names
2. Verify relationships exist for related tables
3. Use `SUMMARIZECOLUMNS` instead of deprecated `SUMMARIZE`

### Issue: "Changes not reflected in Power BI Desktop"
**Solution:**
1. Refresh in Power BI Desktop: File → Options → Preview Features → Enable XMLA read/write
2. Reconnect MCP server
3. Republish model to Fabric

---

## 📚 Additional Resources

- [Power BI MCP Server Documentation](https://learn.microsoft.com/power-bi/mcp)
- [DAX Best Practices](https://dax.tips)
- [Direct Lake Performance Guide](https://learn.microsoft.com/fabric/direct-lake)
- [Data Agent Optimization Tips](../data-agent/agent-instructions.md)

---

**Ready to supercharge your semantic model development? Connect your model and start chatting! 🚀**
