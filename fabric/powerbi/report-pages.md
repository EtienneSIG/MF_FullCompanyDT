# Power BI Report Pages - Design Specifications

## 🎯 Overview

This document outlines the suggested **Power BI report pages** for the Enterprise Data Platform demo. Each page focuses on a specific business domain or KPI area.

**Report Name:** `EnterprisePlatform_ExecutiveDashboard`  
**Pages:** 8 interactive pages + 1 overview  
**Target Audience:** Executives, business analysts, data-literate users

---

## 📊 Report Structure

### Page Navigation

**Tab Order:**
1. 🏠 Executive Overview
2. 💰 Sales Performance
3. 👥 Customer Insights
4. 🎯 Support & Service
5. 📦 Inventory & Supply Chain
6. 🧑‍💼 HR & Workforce
7. 📢 Marketing Performance
8. 🔍 Data Quality Dashboard
9. ℹ️ About & Help

---

## Page 1: 🏠 Executive Overview

**Purpose:** High-level KPIs across all domains for C-suite

### Layout

**Top Row (KPI Cards):**
- Total Revenue (vs. PY)
- Gross Margin %
- Active Customers
- CSAT Score (Customer Satisfaction)
- Headcount
- Inventory Turnover

**Middle Row:**
- **Left:** Revenue Trend (Line chart, last 12 months)
- **Right:** Revenue by Region (Map visual)

**Bottom Row:**
- **Left:** Top 10 Products by Revenue (Bar chart)
- **Right:** Support Tickets by Status (Donut chart)

### Visuals Details

#### Revenue Trend
- **Type:** Line chart
- **X-Axis:** Date[Calendar Hierarchy] (Month level)
- **Y-Axis:** [Total Revenue]
- **Legend:** None
- **Tooltip:** Month, Revenue, Revenue PY, Revenue YoY %
- **Format:** Accent color = Company primary (blue)

#### Revenue by Region
- **Type:** Map (Azure Maps)
- **Location:** Customer[region]
- **Size:** [Total Revenue]
- **Tooltip:** Region, Revenue, Customer Count
- **Format:** Bubble size = proportional, Color = single shade

#### Top 10 Products
- **Type:** Horizontal bar chart
- **Y-Axis:** Product[product_name]
- **X-Axis:** [Total Revenue]
- **Data Labels:** On
- **Top N Filter:** TOP 10 by [Total Revenue]
- **Format:** Sort descending, data labels = $#,##0K

### Slicers
- Year (Date[year]) - Dropdown
- Region (Customer[region]) - Dropdown with "Select All"

---

## Page 2: 💰 Sales Performance

**Purpose:** Deep dive into sales metrics for sales leadership

### Layout

**Top Row (KPIs):**
- Total Revenue
- Gross Profit
- Gross Margin %
- Average Order Value
- Total Orders
- Win Rate % (Opportunities won / total)

**Middle Row:**
- **Left (60%):** Revenue by Month (Column + Line combo chart)
  - Columns: Current Year Revenue
  - Line: Prior Year Revenue
- **Right (40%):** Revenue by Customer Segment (Donut chart)

**Bottom Row:**
- **Left:** Revenue by Sales Rep (Table visual)
  - Columns: Employee Name, Revenue, Gross Profit, Margin %, Orders
  - Conditional formatting: Margin % (color scale)
- **Right:** Revenue by Product Category (Treemap)

### Visuals Details

#### Revenue by Month (Combo Chart)
- **Type:** Clustered Column + Line
- **Shared X-Axis:** Date[month_name]
- **Column Y-Axis:** [Total Revenue]
- **Line Y-Axis:** [Revenue PY]
- **Tooltip:** Add [Revenue YoY %]
- **Format:** 
  - Columns = blue gradient
  - Line = dashed, gray
  - Data labels on line only

#### Revenue by Sales Rep (Table)
- **Type:** Table
- **Columns:**
  - Employee[full_name]
  - [Total Revenue]
  - [Gross Profit]
  - [Gross Margin %]
  - [Total Orders]
- **Sort:** Total Revenue descending
- **Conditional Formatting:**
  - Gross Margin %: Color scale (red < 30%, yellow 30-40%, green > 40%)
  - Total Revenue: Data bars (blue)
- **Totals:** Show grand total row

### Slicers
- Date[fiscal_year] - Dropdown
- Customer[region] - Multi-select dropdown
- Product[category_l1] - Tile slicer (visual icons)

### Interactions
- Clicking a sales rep in table → filters all visuals to show their deals
- Clicking a month in combo chart → shows drill-through to Sales Details page

---

## Page 3: 👥 Customer Insights

**Purpose:** Customer analytics for marketing/sales strategy

### Layout

**Top Row (KPIs):**
- Active Customers
- New Customers (This Year)
- Customer Churn Rate %
- Average Lifetime Value
- Customer Acquisition Cost (CAC)
- LTV:CAC Ratio

**Middle Row:**
- **Left:** Customer Count by Segment (Column chart)
- **Center:** Revenue by Industry (Bar chart)
- **Right:** Top 10 Customers by LTV (Table)

**Bottom Row:**
- **Full Width:** Customer Cohort Analysis (Matrix visual)
  - Rows: First Purchase Month
  - Columns: Months Since First Purchase (0-12)
  - Values: Retention Rate %

### Visuals Details

#### Customer Cohort Analysis (Matrix)
- **Type:** Matrix
- **Rows:** Date[month_name] (of first purchase date)
- **Columns:** [Months Since First Purchase] (calculated column)
- **Values:** [Retention Rate %]
  - Formula: `Customers who purchased again / Total cohort customers * 100`
- **Conditional Formatting:** Heatmap
  - 0% = Red
  - 50% = Yellow
  - 100% = Green

#### Top 10 Customers by LTV
- **Type:** Table
- **Columns:**
  - Customer[customer_name]
  - [Customer Lifetime Value]
  - [Total Orders]
  - [Average Order Value]
  - Customer[industry]
- **Sort:** Customer Lifetime Value descending
- **Top N:** 10

### Slicers
- Customer[customer_segment] - Tile slicer (SMB, Mid-Market, Enterprise)
- Customer[region] - Dropdown
- Date[fiscal_year] - Dropdown

### Drill-Through
- From any visual → Customer Details page (shows all transactions for selected customer)

---

## Page 4: 🎯 Support & Service

**Purpose:** Support team performance and customer satisfaction

### Layout

**Top Row (KPIs):**
- Total Tickets
- Avg Resolution Time (Hours)
- SLA Met %
- First Contact Resolution %
- CSAT Score (1-5)
- Tickets Reopened %

**Middle Row:**
- **Left:** Tickets by Status (Funnel chart: New → Open → Pending → Resolved)
- **Right:** Tickets by Category (Donut chart)

**Bottom Row:**
- **Left:** Resolution Time by Priority (Box and Whisker plot)
- **Center:** Agent Performance (Table)
  - Columns: Agent Name, Tickets Resolved, Avg Resolution Time, CSAT Score
- **Right:** Ticket Volume Trend (Area chart by week)

### Visuals Details

#### Agent Performance Table
- **Type:** Table
- **Columns:**
  - Employee[full_name] (filtered to Support agents only)
  - [Tickets Resolved]
  - [Avg Resolution Time Hours]
  - [CSAT Score]
  - [SLA Met %]
- **Conditional Formatting:**
  - CSAT Score: 
    - < 3.0 = Red
    - 3.0-4.0 = Yellow
    - > 4.0 = Green
  - SLA Met %:
    - < 80% = Red
    - 80-95% = Yellow
    - > 95% = Green

#### Resolution Time by Priority
- **Type:** Box and Whisker
- **Category:** Support[ticket_priority]
- **Values:** Support[resolution_time_hours]
- **Format:** Show median, quartiles, outliers
- **Tooltip:** Min, Q1, Median, Q3, Max

### Slicers
- Date[month_name] - Dropdown
- Support[ticket_category] - Multi-select
- Employee[department] = "Support" (auto-applied filter)

### AI Insights
- **Anomaly Detection:** Enable on Ticket Volume Trend visual
  - Alert if ticket volume spikes > 2 standard deviations

---

## Page 5: 📦 Inventory & Supply Chain

**Purpose:** Inventory management and stockout prevention

### Layout

**Top Row (KPIs):**
- Total Inventory Value
- Inventory Turnover Ratio
- Days of Supply (Avg)
- Stockout Rate %
- Units On Order
- Slow-Moving Items Count

**Middle Row:**
- **Left:** Inventory Value by Category (Treemap)
- **Right:** Stockout Events (Line chart over time)

**Bottom Row:**
- **Full Width:** Inventory Status by Product (Table with sparklines)
  - Columns: Product Name, Category, Units On Hand, Days of Supply, Reorder Point, Status
  - Sparkline: Last 30 days inventory level

### Visuals Details

#### Inventory Status Table
- **Type:** Table
- **Columns:**
  - Product[product_name]
  - Product[category_l1]
  - [Units On Hand]
  - [Days of Supply]
  - Product[reorder_point]
  - [Inventory Status] (Calculated: "Healthy" | "Low" | "Stockout")
  - [30-Day Trend] (Sparkline)
- **Conditional Formatting:**
  - Inventory Status:
    - "Healthy" = Green
    - "Low" = Yellow
    - "Stockout" = Red
- **Sparkline:** Line chart of units_on_hand over last 30 days

#### Inventory Value by Category
- **Type:** Treemap
- **Category:** Product[category_l1]
- **Values:** [Inventory Value]
- **Tooltip:** Category, Inventory Value, % of Total
- **Color Saturation:** By Inventory Value (darker = higher)

### Slicers
- Product[category_l1] - Tile slicer
- Geography[warehouse_location] - Dropdown
- Date[month_name] - Dropdown

### Alerts
- **Data Alerts:** Notify if Stockout Rate % > 5%

---

## Page 6: 🧑‍💼 HR & Workforce

**Purpose:** Workforce analytics for HR leadership

### Layout

**Top Row (KPIs):**
- Headcount (Active)
- Attrition Rate % (YTD)
- Avg Tenure (Years)
- New Hires (This Year)
- Open Positions
- Time to Fill (Avg Days)

**Middle Row:**
- **Left:** Headcount Trend (Line chart, last 24 months)
- **Right:** Headcount by Department (Column chart)

**Bottom Row:**
- **Left:** Attrition by Department (Bar chart)
- **Center:** Tenure Distribution (Histogram)
- **Right:** Diversity Metrics (Donut charts: Gender, Ethnicity)

### Visuals Details

#### Headcount Trend
- **Type:** Area chart
- **X-Axis:** Date[month_name]
- **Y-Axis:** [Headcount]
- **Legend:** Employee[employment_status] (Active, Terminated, LOA)
- **Format:** Stacked area, color = green (Active), red (Terminated), yellow (LOA)

#### Attrition by Department
- **Type:** Horizontal bar chart
- **Y-Axis:** Employee[department]
- **X-Axis:** [Attrition Rate %]
- **Data Labels:** Show %
- **Benchmark Line:** Company avg attrition rate (12%)
- **Format:** Bars > benchmark = red, bars < benchmark = green

#### Tenure Distribution
- **Type:** Histogram
- **X-Axis:** Employee[tenure_years] (binned: 0-1, 1-3, 3-5, 5-10, 10+)
- **Y-Axis:** COUNT(Employees)
- **Format:** Blue gradient

### Slicers
- Date[fiscal_year] - Dropdown
- Employee[department] - Multi-select
- Employee[location] - Dropdown

### Drill-Through
- From any visual → Employee Details page (shows individual employee history)

---

## Page 7: 📢 Marketing Performance

**Purpose:** Campaign ROI and lead generation metrics

### Layout

**Top Row (KPIs):**
- Marketing Spend
- Revenue Attributed
- ROAS (Return on Ad Spend)
- Impressions
- Clicks
- Conversions
- CTR % (Click-Through Rate)

**Middle Row:**
- **Left:** ROAS by Campaign Type (Column chart)
- **Right:** Spend vs. Revenue (Scatter plot)

**Bottom Row:**
- **Full Width:** Campaign Performance Table
  - Columns: Campaign Name, Type, Spend, Revenue, ROAS, Impressions, Clicks, CTR, Conversions

### Visuals Details

#### Spend vs. Revenue Scatter Plot
- **Type:** Scatter chart
- **X-Axis:** [Marketing Spend]
- **Y-Axis:** [Revenue Attributed]
- **Legend:** Marketing[campaign_type]
- **Size:** [Conversions]
- **Format:** Bubbles colored by campaign type
- **Reference Line:** Break-even line (ROAS = 1.0)

#### Campaign Performance Table
- **Type:** Table
- **Columns:**
  - Marketing[campaign_id]
  - Marketing[campaign_type]
  - [Marketing Spend]
  - [Revenue Attributed]
  - [ROAS]
  - [Impressions]
  - [Clicks]
  - [CTR %]
  - [Conversions]
- **Conditional Formatting:**
  - ROAS: Color scale (red < 1.0, green > 3.0)
  - CTR %: Data bars
- **Sort:** ROAS descending

### Slicers
- Date[fiscal_quarter] - Dropdown
- Marketing[campaign_type] - Tile slicer (Email, Social, Search, Display)

### What-If Parameter
- **Parameter:** Budget Allocation %
- **Use Case:** Adjust spend % across campaign types, see projected ROAS

---

## Page 8: 🔍 Data Quality Dashboard

**Purpose:** Monitor data pipeline health and quality metrics

### Layout

**Top Row (KPIs):**
- Tables Loaded Today
- Total Records Loaded
- Failed Loads (Count)
- Avg Load Time (Seconds)
- Data Quality Score (0-100)
- Last Refresh Time

**Middle Row:**
- **Left:** Load Success Rate by Table (Bar chart)
- **Right:** Data Quality Issues (Waterfall chart)
  - Nulls, Duplicates, Referential Integrity Errors, Schema Mismatches

**Bottom Row:**
- **Full Width:** Load History Table
  - Columns: Load Date, Table Name, Records Loaded, Load Time, Status, Error Message

### Visuals Details

#### Load Success Rate by Table
- **Type:** Horizontal bar chart
- **Y-Axis:** Table Name
- **X-Axis:** [Load Success Rate %]
- **Benchmark Line:** 99.9% target
- **Data Labels:** Show %
- **Conditional Formatting:** Red < 95%, Yellow 95-99%, Green > 99%

#### Data Quality Issues Waterfall
- **Type:** Waterfall chart
- **Category:** Issue Type (Nulls, Duplicates, Ref Integrity, Schema Errors)
- **Values:** COUNT(Issues)
- **Format:** Starting point = Total Records, decreasing bars = issues found
- **Color:** Red for issues, green for clean records

### Slicers
- Date[full_date] - Date range picker (last 7 days default)
- Table Name - Multi-select

### Alerts
- **Data Alerts:** Email if Failed Loads > 0

---

## Page 9: ℹ️ About & Help

**Purpose:** User guide and model documentation

### Layout

**Sections:**

1. **Report Overview**
   - Text box: Description of report purpose, data sources, refresh schedule
   - Last Refresh: Dynamic text showing `MAX(Sales[_ingestion_time])`

2. **How to Use This Report**
   - Text box: Instructions on slicers, drill-through, tooltips
   - Video embed (optional): 3-minute walkthrough

3. **Glossary**
   - Table: Term | Definition
     - Examples: ROAS, CSAT, SLA, LTV, CAC, YoY, YTD

4. **Contact Support**
   - Text box: Email, Teams channel, phone number
   - Button: "Request New Feature" (opens Power Automate form)

5. **Data Lineage**
   - Image: Embed data flow diagram (Bronze → Silver → Gold)

---

## 🎨 Design System

### Color Palette

**Primary Colors:**
- Blue: #0078D4 (Microsoft Azure blue) - Used for main visuals
- Dark Blue: #004E8C - Headers, accents
- Light Blue: #50E6FF - Highlights

**Secondary Colors:**
- Green: #107C10 - Positive KPIs, success states
- Red: #D83B01 - Negative KPIs, alerts
- Yellow: #FFB900 - Warnings, neutral

**Neutrals:**
- Dark Gray: #323130 - Text
- Medium Gray: #605E5C - Secondary text
- Light Gray: #F3F2F1 - Backgrounds

### Typography

**Titles:** Segoe UI Semibold, 18pt  
**KPI Values:** Segoe UI Bold, 32pt  
**Labels:** Segoe UI Regular, 10pt  
**Tooltips:** Segoe UI Regular, 9pt

### KPI Card Template

**Background:** White with light gray border  
**KPI Value:** 32pt, bold, primary color  
**Variance Indicator:** ▲/▼ icon, green/red  
**Variance Text:** "vs. PY" 10pt, gray  
**Icon:** Left-aligned, 24x24px, colored (revenue = 💰, customers = 👥, etc.)

---

## 🔧 Advanced Features

### Bookmarks

**Saved Views:**
1. "Executive View" - Only KPI cards and high-level trends
2. "Analyst View" - All visuals, data tables shown
3. "Mobile View" - Simplified layout for phone screens

**How to Use:**
- View → Bookmarks → Add
- Assign to button on each page: "Switch to Analyst View"

### Drill-Through Pages

**Customer Details:**
- Filters: Customer Name (auto-applied)
- Visuals: All orders, revenue trend, product mix, support tickets

**Product Details:**
- Filters: Product Name
- Visuals: Sales trend, inventory levels, margin analysis

**Employee Details:**
- Filters: Employee Name
- Visuals: Sales performance, support tickets handled, tenure timeline

### Tooltips

**Custom Tooltip Pages:**

**Sales Tooltip:**
- Shows: Product image, margin %, units sold, YoY change
- Applied to: Product visuals across all pages

**Customer Tooltip:**
- Shows: Industry, segment, LTV, last purchase date
- Applied to: Customer visuals

---

## 📱 Mobile Layout

**Optimize for Phone:**
- All KPI pages get mobile-optimized layout
- Stack visuals vertically
- Hide complex tables (show simplified KPI cards only)
- Larger touch targets (slicers, buttons)

**Mobile-Specific Pages:**
- "Mobile Overview" - Just top 6 KPIs
- "Mobile Sales" - Revenue trend + top products

---

## ✅ Report Checklist

Before publishing:

- [ ] All visuals load data (no errors)
- [ ] Slicers affect all relevant visuals
- [ ] Drill-through pages configured
- [ ] Tooltips customized
- [ ] Bookmarks created for different views
- [ ] Mobile layout optimized
- [ ] Filters set to correct defaults
- [ ] Data alerts configured
- [ ] Report description added (File → Info)
- [ ] Tested with RLS (View As → Select role)

---

## 🚀 Publishing

**Steps:**
1. File → Publish → Select workspace
2. In Fabric workspace → Open report
3. Set refresh schedule (if not Direct Lake)
4. Share report link with stakeholders
5. Pin key visuals to dashboard (optional)

**Permissions:**
- Workspace Viewer role = can view report
- Workspace Contributor = can edit report
- RLS applies automatically based on user login

---

**This completes the report page specifications! Ready to build in Power BI Desktop 📊**
