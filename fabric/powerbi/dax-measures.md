# DAX Measures - Enterprise Analytics Model

## Overview

Complete collection of **150+ DAX measures** organized by business domain for the Enterprise Analytics Model covering **15 business domains** and **23 fact tables**.

**Usage:**
- Copy measures into Power BI semantic model
- Organize in display folders by domain
- Add descriptions for AI readiness (Fabric Data Agent)

**Domains Covered:**
1. Sales & CRM (Sales, Returns, Opportunities, Activities)
2. Customer Service (Support)
3. Marketing (Campaigns)
4. Human Resources (Hiring, Attrition)
5. Finance (General Ledger, Budget)
6. FinOps (Cloud Costs)
7. IT Operations (Incidents)
8. Manufacturing (Production, Work Orders)
9. Supply Chain (Inventory, Purchase Orders)
10. ESG (Emissions)
11. Risk & Compliance (Risks, Audits, Compliance Checks)
12. R&D (Experiments)
13. Quality (Defects)
14. Security (Security Events)
15. Product (Product Performance)

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

## 🤝 CRM Metrics

### Opportunities

```dax
Total Opportunities = 
COUNTROWS(FactOpportunities)
```

```dax
Open Opportunities = 
CALCULATE(
    [Total Opportunities],
    FactOpportunities[stage] IN {"Prospecting", "Qualification", "Proposal"}
)
```

```dax
Closed Won Opportunities = 
CALCULATE(
    [Total Opportunities],
    FactOpportunities[stage] = "Closed Won"
)
```

```dax
Closed Lost Opportunities = 
CALCULATE(
    [Total Opportunities],
    FactOpportunities[stage] = "Closed Lost"
)
```

```dax
Pipeline Value = 
SUM(FactOpportunities[opportunity_value])
```

```dax
Weighted Pipeline = 
SUMX(
    FactOpportunities,
    FactOpportunities[opportunity_value] * FactOpportunities[win_probability]
)
```

```dax
Win Rate = 
DIVIDE(
    [Closed Won Opportunities],
    [Closed Won Opportunities] + [Closed Lost Opportunities],
    0
)
```

```dax
Average Deal Size = 
AVERAGEX(
    FILTER(FactOpportunities, FactOpportunities[stage] = "Closed Won"),
    FactOpportunities[opportunity_value]
)
```

```dax
Average Sales Cycle (Days) = 
AVERAGEX(
    FILTER(FactOpportunities, FactOpportunities[stage] = "Closed Won"),
    FactOpportunities[days_to_close]
)
```

### Sales Activities

```dax
Total Activities = 
COUNTROWS(FactActivities)
```

```dax
Calls Made = 
CALCULATE(
    [Total Activities],
    FactActivities[activity_type] = "Call"
)
```

```dax
Meetings Held = 
CALCULATE(
    [Total Activities],
    FactActivities[activity_type] = "Meeting"
)
```

```dax
Emails Sent = 
CALCULATE(
    [Total Activities],
    FactActivities[activity_type] = "Email"
)
```

```dax
Activities Per Rep = 
DIVIDE(
    [Total Activities],
    DISTINCTCOUNT(FactActivities[employee_key]),
    0
)
```

```dax
Activity Completion Rate = 
DIVIDE(
    CALCULATE([Total Activities], FactActivities[outcome] = "Completed"),
    [Total Activities],
    0
)
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

### SLA Metrics

```dax
SLA Compliance Rate = 
DIVIDE(
    CALCULATE([Total Tickets], FactSupport[sla_met] = TRUE),
    [Total Tickets],
    0
)
```

```dax
SLA Breaches = 
CALCULATE(
    [Total Tickets],
    FactSupport[sla_met] = FALSE
)
```

---

## 📢 Marketing Metrics

### Campaign Performance

```dax
Total Campaigns = 
COUNTROWS(FactCampaigns)
```

```dax
Active Campaigns = 
CALCULATE(
    [Total Campaigns],
    FactCampaigns[status] = "Active"
)
```

```dax
Campaign Spend = 
SUM(FactCampaigns[budget_spent])
```

```dax
Campaign Budget = 
SUM(FactCampaigns[budget_allocated])
```

```dax
Budget Utilization % = 
DIVIDE(
    [Campaign Spend],
    [Campaign Budget],
    0
)
```

### Lead Generation

```dax
Total Leads = 
SUM(FactCampaigns[leads_generated])
```

```dax
Qualified Leads = 
SUM(FactCampaigns[leads_qualified])
```

```dax
Lead Qualification Rate = 
DIVIDE(
    [Qualified Leads],
    [Total Leads],
    0
)
```

```dax
Conversions = 
SUM(FactCampaigns[conversions])
```

```dax
Conversion Rate = 
DIVIDE(
    [Conversions],
    [Total Leads],
    0
)
```

### ROI Metrics

```dax
Campaign Revenue = 
SUM(FactCampaigns[revenue_attributed])
```

```dax
Campaign ROI = 
DIVIDE(
    [Campaign Revenue] - [Campaign Spend],
    [Campaign Spend],
    0
)
```

```dax
Cost Per Lead = 
DIVIDE(
    [Campaign Spend],
    [Total Leads],
    0
)
```

```dax
Cost Per Acquisition = 
DIVIDE(
    [Campaign Spend],
    [Conversions],
    0
)
```

```dax
Revenue Per Lead = 
DIVIDE(
    [Campaign Revenue],
    [Total Leads],
    0
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

```dax
Carbon Reduction Target Achievement = 
VAR Baseline = CALCULATE([Total Emissions (CO2e)], DimDate[year] = 2023)
VAR Current = [Total Emissions (CO2e)]
VAR Target = Baseline * 0.95 // 5% reduction target
RETURN
    DIVIDE(Baseline - Current, Baseline - Target, 0)
```

---

## ⚖️ Risk & Compliance Metrics

### Risk Management

```dax
Total Risks = 
COUNTROWS(FactRisks)
```

```dax
Active Risks = 
CALCULATE(
    [Total Risks],
    FactRisks[status] IN {"Open", "Under Review"}
)
```

```dax
High Risk Count = 
CALCULATE(
    [Total Risks],
    FactRisks[risk_level] = "High"
)
```

```dax
Critical Risk Count = 
CALCULATE(
    [Total Risks],
    FactRisks[risk_level] = "Critical"
)
```

```dax
Average Risk Score = 
AVERAGE(FactRisks[risk_score])
```

```dax
Risk Mitigation Rate = 
DIVIDE(
    CALCULATE([Total Risks], FactRisks[status] = "Mitigated"),
    [Total Risks],
    0
)
```

```dax
Financial Impact at Risk = 
SUM(FactRisks[financial_impact_amount])
```

### Audit Management

```dax
Total Audits = 
COUNTROWS(FactAudits)
```

```dax
Completed Audits = 
CALCULATE(
    [Total Audits],
    FactAudits[status] = "Completed"
)
```

```dax
Total Findings = 
SUM(FactAudits[findings_count])
```

```dax
Critical Findings = 
SUM(FactAudits[critical_findings])
```

```dax
High Findings = 
SUM(FactAudits[high_findings])
```

```dax
Remediated Findings = 
SUM(FactAudits[remediated_findings])
```

```dax
Remediation Rate = 
DIVIDE(
    [Remediated Findings],
    [Total Findings],
    0
)
```

```dax
Average Remediation Time (Days) = 
AVERAGE(FactAudits[avg_remediation_days])
```

### Compliance Checks

```dax
Total Compliance Checks = 
COUNTROWS(FactComplianceChecks)
```

```dax
Passed Checks = 
CALCULATE(
    [Total Compliance Checks],
    FactComplianceChecks[result] = "Pass"
)
```

```dax
Failed Checks = 
CALCULATE(
    [Total Compliance Checks],
    FactComplianceChecks[result] = "Fail"
)
```

```dax
Compliance Rate = 
DIVIDE(
    [Passed Checks],
    [Total Compliance Checks],
    0
)
```

```dax
Compliance by Framework = 
CALCULATE(
    [Compliance Rate],
    VALUES(FactComplianceChecks[compliance_framework])
)
```

---

## 🔬 R&D Metrics

### Experiment Performance

```dax
Total Experiments = 
COUNTROWS(FactExperiments)
```

```dax
Active Experiments = 
CALCULATE(
    [Total Experiments],
    FactExperiments[status] = "In Progress"
)
```

```dax
Completed Experiments = 
CALCULATE(
    [Total Experiments],
    FactExperiments[status] = "Completed"
)
```

```dax
Successful Experiments = 
CALCULATE(
    [Total Experiments],
    FactExperiments[outcome] = "Success"
)
```

```dax
Experiment Success Rate = 
DIVIDE(
    [Successful Experiments],
    [Completed Experiments],
    0
)
```

```dax
Total R&D Cost = 
SUM(FactExperiments[cost])
```

```dax
Average Experiment Cost = 
AVERAGE(FactExperiments[cost])
```

```dax
Average Experiment Duration (Days) = 
AVERAGEX(
    FILTER(FactExperiments, FactExperiments[status] = "Completed"),
    FactExperiments[duration_days]
)
```

### Project Performance

```dax
R&D Projects = 
DISTINCTCOUNT(FactExperiments[project_key])
```

```dax
Active R&D Projects = 
CALCULATE(
    DISTINCTCOUNT(FactExperiments[project_key]),
    FactExperiments[status] = "In Progress"
)
```

```dax
Cost per Project = 
DIVIDE(
    [Total R&D Cost],
    [R&D Projects],
    0
)
```

---

## ✅ Quality Metrics

### Defect Management

```dax
Total Defects = 
COUNTROWS(FactDefects)
```

```dax
Open Defects = 
CALCULATE(
    [Total Defects],
    FactDefects[status] IN {"Open", "In Progress"}
)
```

```dax
Resolved Defects = 
CALCULATE(
    [Total Defects],
    FactDefects[status] = "Resolved"
)
```

```dax
Critical Defects = 
CALCULATE(
    [Total Defects],
    FactDefects[severity] = "Critical"
)
```

```dax
Defect Rate per 1000 Units = 
DIVIDE(
    [Total Defects] * 1000,
    [Total Production Quantity],
    0
)
```

```dax
Defect Resolution Rate = 
DIVIDE(
    [Resolved Defects],
    [Total Defects],
    0
)
```

```dax
Average Defect Resolution Time (Days) = 
AVERAGEX(
    FILTER(FactDefects, FactDefects[status] = "Resolved"),
    FactDefects[resolution_days]
)
```

```dax
Cost of Quality = 
SUM(FactDefects[cost_impact])
```

```dax
First Pass Yield = 
DIVIDE(
    [Total Production Quantity] - [Total Defects],
    [Total Production Quantity],
    0
)
```

---

## 🔒 Security Metrics

### Security Event Management

```dax
Total Security Events = 
COUNTROWS(FactSecurityEvents)
```

```dax
Active Security Events = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[status] IN {"Open", "Investigating"}
)
```

```dax
Resolved Security Events = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[status] = "Resolved"
)
```

```dax
Critical Security Events = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[severity] = "Critical"
)
```

```dax
High Security Events = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[severity] = "High"
)
```

### Incident Categories

```dax
Malware Incidents = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[event_type] = "Malware"
)
```

```dax
Phishing Attempts = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[event_type] = "Phishing"
)
```

```dax
Unauthorized Access = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[event_type] = "Unauthorized Access"
)
```

```dax
Data Breach Count = 
CALCULATE(
    [Total Security Events],
    FactSecurityEvents[event_type] = "Data Breach"
)
```

### Response Metrics

```dax
Average Response Time (Hours) = 
AVERAGE(FactSecurityEvents[response_time_hours])
```

```dax
Average Remediation Time (Hours) = 
AVERAGE(FactSecurityEvents[remediation_time_hours])
```

```dax
Security Event Resolution Rate = 
DIVIDE(
    [Resolved Security Events],
    [Total Security Events],
    0
)
```

```dax
Security Events by Month = 
CALCULATE(
    [Total Security Events],
    VALUES(DimDate[month_name])
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

## ☁️ FinOps Metrics

### Cloud Cost Management

```dax
Total Cloud Costs = 
SUM(FactCloudCosts[cost])
```

```dax
Azure Costs = 
CALCULATE(
    [Total Cloud Costs],
    FactCloudCosts[provider] = "Azure"
)
```

```dax
AWS Costs = 
CALCULATE(
    [Total Cloud Costs],
    FactCloudCosts[provider] = "AWS"
)
```

```dax
GCP Costs = 
CALCULATE(
    [Total Cloud Costs],
    FactCloudCosts[provider] = "GCP"
)
```

### Cost Optimization

```dax
Cloud Cost MoM Change = 
VAR CurrentMonth = [Total Cloud Costs]
VAR PriorMonth = 
    CALCULATE(
        [Total Cloud Costs],
        DATEADD(DimDate[Date], -1, MONTH)
    )
RETURN
    CurrentMonth - PriorMonth
```

```dax
Cloud Cost MoM % = 
DIVIDE(
    [Cloud Cost MoM Change],
    CALCULATE([Total Cloud Costs], DATEADD(DimDate[Date], -1, MONTH)),
    0
)
```

```dax
Average Daily Cloud Cost = 
DIVIDE(
    [Total Cloud Costs],
    DISTINCTCOUNT(FactCloudCosts[usage_date_id]),
    0
)
```

```dax
Cost by Service Type = 
CALCULATE(
    [Total Cloud Costs],
    VALUES(FactCloudCosts[service_type])
)
```

```dax
Reserved vs On-Demand Ratio = 
DIVIDE(
    CALCULATE([Total Cloud Costs], FactCloudCosts[pricing_model] = "Reserved"),
    CALCULATE([Total Cloud Costs], FactCloudCosts[pricing_model] = "On-Demand"),
    0
)
```

---

## 🏭 Manufacturing Metrics

### Production Performance

```dax
Total Production Quantity = 
SUM(FactProduction[quantity_produced])
```

```dax
Target Production Quantity = 
SUM(FactProduction[quantity_target])
```

```dax
Production Achievement % = 
DIVIDE(
    [Total Production Quantity],
    [Target Production Quantity],
    0
)
```

```dax
Production Yield % = 
AVERAGE(FactProduction[yield_percentage])
```

```dax
Defect Rate % = 
AVERAGE(FactProduction[defect_rate])
```

```dax
Scrap Quantity = 
SUM(FactProduction[scrap_quantity])
```

```dax
Scrap Rate % = 
DIVIDE(
    [Scrap Quantity],
    [Total Production Quantity] + [Scrap Quantity],
    0
)
```

### Facility Performance

```dax
Machine Uptime % = 
AVERAGE(FactProduction[machine_uptime_pct])
```

```dax
OEE (Overall Equipment Effectiveness) = 
AVERAGE(FactProduction[oee_score])
```

### Work Orders

```dax
Total Work Orders = 
COUNTROWS(FactWorkOrders)
```

```dax
Completed Work Orders = 
CALCULATE(
    [Total Work Orders],
    FactWorkOrders[status] = "Completed"
)
```

```dax
In Progress Work Orders = 
CALCULATE(
    [Total Work Orders],
    FactWorkOrders[status] = "In Progress"
)
```

```dax
Work Order Completion Rate = 
DIVIDE(
    [Completed Work Orders],
    [Total Work Orders],
    0
)
```

```dax
Average Work Order Duration (Days) = 
AVERAGEX(
    FILTER(FactWorkOrders, FactWorkOrders[status] = "Completed"),
    FactWorkOrders[actual_duration_days]
)
```

```dax
Work Orders On Time = 
CALCULATE(
    [Completed Work Orders],
    FactWorkOrders[actual_duration_days] <= FactWorkOrders[planned_duration_days]
)
```

```dax
On-Time Completion Rate = 
DIVIDE(
    [Work Orders On Time],
    [Completed Work Orders],
    0
)
```

---

## 📦 Supply Chain Metrics (Extended)

### Purchase Orders

```dax
Total Purchase Orders = 
COUNTROWS(FactPurchaseOrders)
```

```dax
PO Line Items = 
SUM(FactPurchaseOrders[quantity_ordered])
```

```dax
Total PO Value = 
SUM(FactPurchaseOrders[line_total])
```

```dax
Average PO Value = 
DIVIDE(
    [Total PO Value],
    [Total Purchase Orders],
    0
)
```

```dax
Received Quantity = 
SUM(FactPurchaseOrders[quantity_received])
```

```dax
Fill Rate = 
DIVIDE(
    [Received Quantity],
    [PO Line Items],
    0
)
```

```dax
Average Lead Time (Days) = 
AVERAGE(FactPurchaseOrders[lead_time_days])
```

```dax
On-Time Delivery Rate = 
DIVIDE(
    CALCULATE([Total Purchase Orders], FactPurchaseOrders[delivered_on_time] = TRUE),
    [Total Purchase Orders],
    0
)
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

## 📝 Notes & Best Practices

### Display Folders

Organize measures in display folders for better user experience:

**Recommended Folder Structure:**
```
📁 1. Sales & CRM/
   📁 Sales Metrics/
   📁 Returns/
   📁 Opportunities/
   📁 Activities/
   📁 Time Intelligence/

📁 2. Customer Service/
   📁 Ticket Metrics/
   📁 Resolution/
   📁 CSAT/
   📁 SLA/

📁 3. Marketing/
   📁 Campaign Performance/
   📁 Lead Generation/
   📁 ROI/

📁 4. Human Resources/
   📁 Headcount/
   📁 Attrition/
   📁 Hiring/

📁 5. Finance/
   📁 Budget vs Actual/
   📁 Variance/
   📁 General Ledger/

📁 6. FinOps/
   📁 Cloud Costs/
   📁 Cost Optimization/

📁 7. IT Operations/
   📁 Incidents/
   📁 Performance/

📁 8. Manufacturing/
   📁 Production/
   📁 Work Orders/
   📁 Quality/

📁 9. Supply Chain/
   📁 Inventory/
   📁 Purchase Orders/

📁 10. ESG/
   📁 Emissions/
   📁 Targets/

📁 11. Risk & Compliance/
   📁 Risks/
   📁 Audits/
   📁 Compliance Checks/

📁 12. R&D/
   📁 Experiments/
   📁 Projects/

📁 13. Quality/
   📁 Defects/
   📁 First Pass Yield/

📁 14. Security/
   📁 Security Events/
   📁 Incident Response/

📁 Universal/
   📁 Time Intelligence/
   📁 Conditional Formatting/
```

### Measure Descriptions

Add descriptions to all measures for better Data Agent performance:

**Example:**
```dax
Total Revenue = 
CALCULATE(
    SUM(FactSales[net_amount]),
    FactSales[status] IN {"Delivered", "Shipped"}
)
```
**Description:** "Total revenue from delivered and shipped sales orders. Excludes cancelled and pending orders."

### Synonyms for Natural Language

Configure synonyms in Power BI for natural language queries:

| Measure | Synonyms |
|---------|----------|
| Total Revenue | sales, income, turnover, revenue |
| Gross Margin % | profit margin, margin percentage, profitability |
| Total Customers | customer count, number of customers |
| Attrition Rate | turnover rate, churn rate, employee loss |
| Total Defects | quality issues, product defects, failures |
| Security Events | security incidents, threats, vulnerabilities |

### Format Strings

Apply appropriate format strings for better visualization:

| Type | Format String | Example |
|------|---------------|---------|
| Currency (Thousands) | $#,##0,K | $1,234K |
| Currency (Millions) | $#,##0.0,,M | $12.3M |
| Percentage | 0.0% | 45.6% |
| Whole Number | #,##0 | 1,234 |
| Decimal (1 place) | #,##0.0 | 1,234.5 |

### Time Intelligence Best Practices

1. **Always use CALCULATE** when filtering dates
2. **Use USERELATIONSHIP** for inactive date relationships
3. **Handle BLANK()** values in year-over-year calculations
4. **Test edge cases** (first month, leap years, fiscal year boundaries)

### DAX Performance Tips

1. **Use variables (VAR)** to avoid recalculation
2. **Filter early** in CALCULATE expressions
3. **Avoid iterators** (SUMX, AVERAGEX) when possible
4. **Use measure branching** instead of calculated columns
5. **Test with Performance Analyzer** in Power BI Desktop

### Data Agent Optimization

For optimal Fabric Data Agent performance:

1. ✅ Add clear descriptions to all measures
2. ✅ Configure synonyms for common business terms
3. ✅ Use consistent naming conventions
4. ✅ Group related measures in folders
5. ✅ Document assumptions and business rules
6. ✅ Test measures with natural language questions

### Conditional Formatting

Example color coding for KPIs:

```dax
KPI Color = 
VAR Actual = [Total Revenue]
VAR Target = [Budget Amount]
VAR Variance = DIVIDE(Actual - Target, Target, 0)
RETURN
    SWITCH(
        TRUE(),
        Variance >= 0.1, "#00AA00",   // Dark Green: >10% above target
        Variance >= 0.05, "#90EE90",  // Light Green: 5-10% above
        Variance >= 0, "#FFA500",     // Orange: 0-5% above
        Variance >= -0.05, "#FFA500", // Orange: 0-5% below
        Variance >= -0.1, "#FF6347",  // Light Red: 5-10% below
        "#FF0000"                     // Dark Red: >10% below
    )
```

---

## 📊 Summary

**Total Measures:** 150+  
**Fact Tables Covered:** 23  
**Dimension Tables:** 8  
**Business Domains:** 15  

**Domains Included:**
1. ✅ Sales & CRM (Sales, Returns, Opportunities, Activities)
2. ✅ Customer Service (Support Tickets)
3. ✅ Marketing (Campaigns)
4. ✅ Human Resources (Hiring, Attrition, Headcount)
5. ✅ Finance (General Ledger, Budget, Variance)
6. ✅ FinOps (Cloud Costs, Cost Optimization)
7. ✅ IT Operations (Incidents, MTTR, Availability)
8. ✅ Manufacturing (Production, Work Orders, OEE)
9. ✅ Supply Chain (Inventory, Purchase Orders, Fill Rate)
10. ✅ ESG (Carbon Emissions, Scope 1-3)
11. ✅ Risk & Compliance (Risks, Audits, Compliance Checks)
12. ✅ R&D (Experiments, Project Performance)
13. ✅ Quality (Defects, First Pass Yield, Cost of Quality)
14. ✅ Security (Security Events, Incident Response)
15. ✅ Product (Product Performance, Profitability)

**Ready for:**
- ✅ Power BI Direct Lake semantic model
- ✅ Fabric Data Agent integration
- ✅ Natural language queries
- ✅ Executive dashboards
- ✅ Operational reporting
- ✅ AI-powered analytics

---

**Last Updated:** 2026-02-19  
**Version:** 2.0 (Complete Enterprise Coverage)  
**Status:** ✅ Production Ready
