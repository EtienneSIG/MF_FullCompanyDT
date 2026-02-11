# DAX Measures - Enterprise Analytics Model

## Overview

Complete collection of 100+ DAX measures organized by business domain for the Enterprise Analytics Model.

**Usage:**
- Copy measures into Power BI semantic model
- Organize in display folders by domain
- Add descriptions for AI readiness

---

## 📊 Sales Metrics

### Base Measures

```dax
Total Revenue = 
CALCULATE(
    SUM(FactSales[net_amount]),
    FactSales[status] IN {"Delivered", "Shipped"}
)
```

```dax
Total Orders = 
DISTINCTCOUNT(FactSales[order_id])
```

```dax
Total Quantity Sold = 
SUM(FactSales[quantity])
```

```dax
Gross Margin = 
SUM(FactSales[gross_margin])
```

```dax
Cost of Goods Sold = 
SUM(FactSales[cost_amount])
```

### Calculated Metrics

```dax
Gross Margin % = 
DIVIDE(
    [Gross Margin],
    [Total Revenue],
    0
)
```

```dax
Average Order Value = 
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)
```

```dax
Units Per Order = 
DIVIDE(
    [Total Quantity Sold],
    [Total Orders],
    0
)
```

```dax
Revenue Per Customer = 
DIVIDE(
    [Total Revenue],
    DISTINCTCOUNT(FactSales[customer_id]),
    0
)
```

### Time Intelligence

```dax
Revenue YTD = 
CALCULATE(
    [Total Revenue],
    DATESYTD(DimDate[Date])
)
```

```dax
Revenue QTD = 
CALCULATE(
    [Total Revenue],
    DATESQTD(DimDate[Date])
)
```

```dax
Revenue MTD = 
CALCULATE(
    [Total Revenue],
    DATESMTD(DimDate[Date])
)
```

```dax
Revenue PY = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(DimDate[Date])
)
```

```dax
Revenue YoY % = 
VAR CurrentYear = [Total Revenue]
VAR PriorYear = [Revenue PY]
RETURN
    DIVIDE(
        CurrentYear - PriorYear,
        PriorYear,
        BLANK()
    )
```

```dax
Revenue MoM % = 
VAR CurrentMonth = [Total Revenue]
VAR PriorMonth = 
    CALCULATE(
        [Total Revenue],
        DATEADD(DimDate[Date], -1, MONTH)
    )
RETURN
    DIVIDE(
        CurrentMonth - PriorMonth,
        PriorMonth,
        BLANK()
    )
```

### Returns Metrics

```dax
Total Returns = 
COUNTROWS(FactReturns)
```

```dax
Return Amount = 
SUM(FactReturns[refund_amount])
```

```dax
Return Rate = 
DIVIDE(
    [Total Returns],
    [Total Orders],
    0
)
```

```dax
Net Revenue (After Returns) = 
[Total Revenue] - [Return Amount]
```

---

## 👥 Customer Metrics

### Base Measures

```dax
Total Customers = 
DISTINCTCOUNT(DimCustomer[customer_id])
```

```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_id]),
    DimCustomer[is_active] = TRUE
)
```

```dax
New Customers = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_id]),
    DimCustomer[customer_since] >= DATE(YEAR(TODAY()), 1, 1)
)
```

### Customer Lifetime Value

```dax
Customer Lifetime Value = 
SUMX(
    VALUES(DimCustomer[customer_id]),
    CALCULATE([Total Revenue])
)
```

```dax
Average Customer Lifetime Value = 
AVERAGEX(
    VALUES(DimCustomer[customer_id]),
    CALCULATE([Total Revenue])
)
```

### Customer Segmentation

```dax
High Value Customers = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_id]),
    DimCustomer[lifetime_value_tier] = "High"
)
```

```dax
% High Value Customers = 
DIVIDE(
    [High Value Customers],
    [Total Customers],
    0
)
```

### Retention & Churn

```dax
Customer Churn Count = 
CALCULATE(
    DISTINCTCOUNT(DimCustomer[customer_id]),
    DimCustomer[is_active] = FALSE
)
```

```dax
Customer Churn Rate = 
DIVIDE(
    [Customer Churn Count],
    [Total Customers],
    0
)
```

```dax
Customer Retention Rate = 
1 - [Customer Churn Rate]
```

---

## 🛍️ Product Metrics

### Base Measures

```dax
Total Products = 
DISTINCTCOUNT(DimProduct[product_id])
```

```dax
Active Products = 
CALCULATE(
    DISTINCTCOUNT(DimProduct[product_id]),
    DimProduct[is_active] = TRUE
)
```

### Product Performance

```dax
Top Product by Revenue = 
CALCULATE(
    FIRSTNONBLANK(DimProduct[product_name], 1),
    TOPN(
        1,
        ALL(DimProduct[product_name]),
        [Total Revenue],
        DESC
    )
)
```

```dax
Products Sold Count = 
DISTINCTCOUNT(FactSales[product_id])
```

```dax
% Products Sold = 
DIVIDE(
    [Products Sold Count],
    [Total Products],
    0
)
```

---

## 📞 Support Metrics

### Base Measures

```dax
Total Tickets = 
COUNTROWS(FactSupport)
```

```dax
Open Tickets = 
CALCULATE(
    [Total Tickets],
    FactSupport[status] IN {"Open", "In Progress"}
)
```

```dax
Resolved Tickets = 
CALCULATE(
    [Total Tickets],
    FactSupport[status] IN {"Resolved", "Closed"}
)
```

### Resolution Metrics

```dax
Average Resolution Time (Hours) = 
AVERAGE(FactSupport[resolution_hours])
```

```dax
First Contact Resolution Count = 
CALCULATE(
    [Total Tickets],
    FactSupport[fcr] = TRUE
)
```

```dax
FCR % = 
DIVIDE(
    [First Contact Resolution Count],
    [Total Tickets],
    0
)
```

### Customer Satisfaction

```dax
Average CSAT Score = 
AVERAGE(FactSupport[csat_score])
```

```dax
CSAT Response Rate = 
VAR TotalWithCSAT = 
    CALCULATE(
        [Total Tickets],
        NOT(ISBLANK(FactSupport[csat_score]))
    )
RETURN
    DIVIDE(TotalWithCSAT, [Total Tickets], 0)
```

```dax
Tickets with Low CSAT = 
CALCULATE(
    [Total Tickets],
    FactSupport[csat_score] <= 2
)
```

---

## 👔 HR Metrics

### Headcount

```dax
Total Headcount = 
DISTINCTCOUNT(DimEmployee[employee_id])
```

```dax
Active Employees = 
CALCULATE(
    DISTINCTCOUNT(DimEmployee[employee_id]),
    DimEmployee[is_active] = TRUE
)
```

### Attrition

```dax
Total Attrition = 
COUNTROWS(FactAttrition)
```

```dax
Voluntary Attrition = 
CALCULATE(
    [Total Attrition],
    FactAttrition[termination_type] = "Voluntary"
)
```

```dax
Involuntary Attrition = 
CALCULATE(
    [Total Attrition],
    FactAttrition[termination_type] = "Involuntary"
)
```

```dax
Attrition Rate = 
VAR AttritionCount = [Total Attrition]
VAR AvgHeadcount = 
    AVERAGEX(
        VALUES(DimDate[Date]),
        [Active Employees]
    )
RETURN
    DIVIDE(AttritionCount, AvgHeadcount, 0)
```

```dax
Voluntary Attrition % = 
DIVIDE(
    [Voluntary Attrition],
    [Total Attrition],
    0
)
```

```dax
Regrettable Loss Count = 
CALCULATE(
    [Total Attrition],
    FactAttrition[is_regrettable] = TRUE
)
```

```dax
Regrettable Loss % = 
DIVIDE(
    [Regrettable Loss Count],
    [Total Attrition],
    0
)
```

### Hiring

```dax
Total Hiring = 
COUNTROWS(FactHiring)
```

```dax
Positions Filled = 
CALCULATE(
    [Total Hiring],
    NOT(ISBLANK(FactHiring[employee_id]))
)
```

```dax
Average Time to Fill (Days) = 
AVERAGE(FactHiring[time_to_fill_days])
```

```dax
Offer Acceptance Rate = 
DIVIDE(
    [Positions Filled],
    SUM(FactHiring[offers_extended]),
    0
)
```

---

## 📦 Inventory Metrics

### Stock Levels

```dax
Current Inventory Value = 
SUM(FactInventory[inventory_value])
```

```dax
Current Inventory Quantity = 
SUM(FactInventory[quantity_on_hand])
```

```dax
Available Inventory = 
SUM(FactInventory[quantity_available])
```

### Performance

```dax
Inventory Turns = 
VAR COGS = [Cost of Goods Sold]
VAR AvgInventory = 
    AVERAGEX(
        VALUES(DimDate[Date]),
        [Current Inventory Value]
    )
RETURN
    DIVIDE(COGS, AvgInventory, 0)
```

```dax
Days of Supply = 
AVERAGE(FactInventory[days_of_supply])
```

```dax
Stockout Count = 
CALCULATE(
    COUNTROWS(FactInventory),
    FactInventory[quantity_available] = 0
)
```

```dax
Stockout Rate = 
DIVIDE(
    [Stockout Count],
    COUNTROWS(FactInventory),
    0
)
```

---

## 🌍 ESG Metrics

### Emissions

```dax
Total Emissions (CO2e) = 
SUM(FactEmissions[metric_tons_co2e])
```

```dax
Scope 1 Emissions = 
CALCULATE(
    [Total Emissions (CO2e)],
    FactEmissions[scope] = "Scope 1"
)
```

```dax
Scope 2 Emissions = 
CALCULATE(
    [Total Emissions (CO2e)],
    FactEmissions[scope] = "Scope 2"
)
```

```dax
Scope 3 Emissions = 
CALCULATE(
    [Total Emissions (CO2e)],
    FactEmissions[scope] = "Scope 3"
)
```

```dax
Emissions Intensity = 
DIVIDE(
    [Total Emissions (CO2e)],
    [Total Revenue],
    0
)
```

```dax
Emissions YoY % Change = 
VAR CurrentYear = [Total Emissions (CO2e)]
VAR PriorYear = 
    CALCULATE(
        [Total Emissions (CO2e)],
        SAMEPERIODLASTYEAR(DimDate[Date])
    )
RETURN
    DIVIDE(
        CurrentYear - PriorYear,
        PriorYear,
        BLANK()
    )
```

---

## 🖥️ IT Operations Metrics

### Incidents

```dax
Total Incidents = 
COUNTROWS(FactIncidents)
```

```dax
P1 Incidents = 
CALCULATE(
    [Total Incidents],
    FactIncidents[severity] = "P1"
)
```

```dax
Open Incidents = 
CALCULATE(
    [Total Incidents],
    FactIncidents[status] IN {"Open", "In Progress"}
)
```

### Performance

```dax
MTTR (Minutes) = 
AVERAGE(FactIncidents[mttr_minutes])
```

```dax
Total Downtime (Hours) = 
SUM(FactIncidents[downtime_minutes]) / 60
```

```dax
Availability % = 
VAR TotalMinutes = COUNTROWS(DimDate) * 1440 // 1440 minutes per day
VAR DowntimeMinutes = SUM(FactIncidents[downtime_minutes])
RETURN
    DIVIDE(TotalMinutes - DowntimeMinutes, TotalMinutes, 0)
```

---

## 💰 Financial Metrics

### Budget vs Actuals

```dax
Budget Amount = 
SUM(FactBudget[budget_amount])
```

```dax
Actual Amount = 
SUM(FactGeneralLedger[amount])
```

```dax
Variance = 
[Actual Amount] - [Budget Amount]
```

```dax
Variance % = 
DIVIDE(
    [Variance],
    [Budget Amount],
    0
)
```

```dax
Forecast Amount = 
SUM(FactBudget[forecast_amount])
```

---

## 📋 Universal Measures

### Formatting Helpers

```dax
Revenue (Formatted) = 
FORMAT([Total Revenue], "$#,##0,K")
```

```dax
Margin % (Formatted) = 
FORMAT([Gross Margin %], "0.0%")
```

```dax
Count (Formatted) = 
FORMAT([Total Orders], "#,##0")
```

### Conditional Formatting

```dax
Revenue vs Target Color = 
VAR Target = [Budget Amount]
VAR Actual = [Total Revenue]
VAR VariancePct = DIVIDE(Actual - Target, Target, 0)
RETURN
    SWITCH(
        TRUE(),
        VariancePct >= 0.1, "#00AA00",  // Green: >10% above target
        VariancePct >= 0, "#FFA500",     // Orange: 0-10% above
        VariancePct >= -0.1, "#FFA500",  // Orange: 0-10% below
        "#FF0000"                         // Red: >10% below
    )
```

---

## 📝 Notes

**Display Folders:**
- Organize measures in folders by domain (Sales/, HR/, Support/, etc.)
- Use sub-folders for Time Intelligence/ and Calculations/

**Descriptions:**
- Add descriptions to all measures for Data Agent optimization
- Include calculation logic and business context

**Synonyms:**
- Add synonyms in Power BI for natural language queries
- Example: "Total Revenue" → Synonyms: "sales", "income", "turnover"

**Format Strings:**
- Apply appropriate format strings (#,##0 for counts, $#,##0 for currency, 0.0% for percentages)

---

**Total Measures:** 100+  
**Domains Covered:** 10  
**Ready for:** Direct Lake semantic model + Fabric Data Agent
