# Financial Planning and Analysis Scenario

## Business Context and Objectives

### Overview
The Finance organization oversees financial planning, budgeting, forecasting, and analysis across all business units and geographies. With increasing pressure to optimize costs, improve profitability, and provide strategic financial guidance, the CFO and FP&A teams need real-time visibility into financial performance, variance analysis, and predictive insights to drive informed decision-making.

### Strategic Objectives
1. **Improve Profit Margins**: Increase EBITDA margin from 18% to 22% through cost optimization and revenue mix improvement
2. **Enhance Forecast Accuracy**: Improve quarterly forecast accuracy from 85% to 95%+ to support better capital allocation
3. **Optimize Working Capital**: Reduce Days Sales Outstanding (DSO) from 52 to 40 days and improve cash conversion cycle
4. **Cost Efficiency**: Reduce operating expenses as percentage of revenue from 68% to 62%
5. **Strategic Investment**: Reallocate 15% of budget to high-growth initiatives and digital transformation
6. **Risk Management**: Improve financial risk identification and mitigation across currency, credit, and market exposures

### Key Stakeholders
- Chief Financial Officer (CFO)
- VP of Financial Planning & Analysis
- Controller
- Treasury Director
- Business Unit Finance Leaders
- Board Finance Committee

### Current Challenges
- Budget variance averaging 12% across departments (target: <5%)
- Limited visibility into project-level profitability and ROI
- Manual, time-consuming monthly close process (15 days, target: 5 days)
- Difficulty predicting cash flow needs for strategic investments
- Inconsistent cost allocation methodology across business units
- Rising cloud infrastructure costs outpacing revenue growth (35% YoY increase)

## Key Business Questions

### Strategic Questions
1. What is our current financial trajectory and will we meet annual profit targets?
2. Which business units and product lines are driving profitability vs. consuming capital?
3. How should we allocate capital across competing investment priorities?
4. What is our cash position and ability to fund strategic initiatives?
5. How exposed are we to foreign exchange, interest rate, and credit risks?

### Operational Questions
1. Where are we seeing the largest budget variances and what are the root causes?
2. Which cost categories are trending above plan and require intervention?
3. How accurate are our revenue and expense forecasts by business unit?
4. What is the profitability of each customer segment and sales channel?
5. How efficiently are we converting revenue to cash?

### Analytical Questions
1. What factors drive the strongest correlation with profitability variations?
2. How do seasonal patterns impact our cash flow and working capital needs?
3. Which investments have delivered the highest ROI and what characteristics do they share?
4. What is the sensitivity of our profit margins to changes in key cost drivers?
5. How do our financial metrics compare to industry benchmarks and competitors?

## Scenario 1: Monthly Financial Performance Review

### Business Context
The CFO conducts monthly business reviews with executive leadership to assess financial performance, identify variances, and course-correct. The review must cover revenue trends, profitability by segment, expense management, cash flow, and forecast updates across all dimensions.

### User Questions
1. "What were our total revenue and gross margin for last month compared to plan and prior year?"
2. "Show me revenue performance by product category and region - where are we over/under plan?"
3. "What is driving our expense variance? Which departments are over budget?"
4. "How is our cash flow trending and what is our current cash position?"
5. "What is our updated full-year revenue and EBITDA forecast based on current trends?"

### Expected Data Agent Response
The Data Agent analyzes gold_factgeneralledger, gold_factsales, gold_dimdate, and gold_dimgeography tables to provide:
- Monthly revenue of $127.3M (vs. plan $125M, +1.8% favorable; vs. PY $118M, +7.9%)
- Gross margin of 42.3% (vs. plan 41%, +130bps; vs. PY 40.8%, +150bps)
- Revenue by product: Premium products +12% vs plan, Standard products -3% vs plan
- Revenue by region: North America +5%, Europe -2%, Asia Pacific +8%
- Expense variance: $3.2M unfavorable driven by Cloud Costs (+$1.8M) and Marketing (+$1.1M)
- Cash flow: Operating cash flow $18.5M, ending cash balance $47.2M
- FY forecast: Revenue $1.53B (vs. plan $1.50B), EBITDA $312M (20.4% margin, on track)

### KPIs Demonstrated
- Total Revenue, Revenue vs. Plan %, Revenue YoY Growth %
- Gross Margin, Gross Margin %, EBITDA Margin %
- Operating Expenses, OpEx as % of Revenue
- Cash Flow from Operations, Ending Cash Balance
- Budget Variance by Department

### Insights Generated
- Premium product shift is driving margin expansion ahead of plan
- Cloud cost overruns require immediate review and optimization plan
- Strong Asia Pacific performance offsetting European weakness
- Operating cash flow healthy, supporting investment capacity
- Full-year targets achievable with current trajectory

## Scenario 2: Cloud Cost Optimization Analysis

### Business Context
Cloud infrastructure costs have increased 35% YoY, significantly outpacing revenue growth of 12%. The CFO and CIO need to understand cost drivers, identify optimization opportunities, and implement governance to bring cloud spending in line with business value delivered.

### User Questions
1. "What are our total cloud costs for the year and how do they compare to budget?"
2. "Show me cloud cost trends by month and service category - where is the growth?"
3. "Which business units or projects are consuming the most cloud resources?"
4. "What percentage of our cloud spend is on compute vs. storage vs. data services?"
5. "Identify opportunities to reduce cloud costs without impacting critical workloads"

### Expected Data Agent Response
The Data Agent analyzes gold_factcloudcosts, gold_dimdate, and cross-references with project and workload data:
- Total cloud costs YTD: $42.8M (vs. budget $35M, +22% unfavorable)
- Cost breakdown: Compute 48% ($20.5M), Storage 28% ($12.0M), Data Services 15% ($6.4M), Networking 9% ($3.9M)
- Monthly trend: Accelerating from $2.8M/month (Jan) to $4.2M/month (Dec)
- Top consumers: ML/AI projects (32%), Development environments (25%), Production workloads (43%)
- Optimization opportunities identified:
  - $680K/year in idle development resources running 24/7
  - $420K/year in unattached storage volumes
  - $850K/year in oversized compute instances (avg utilization 23%)
  - $1.2M/year potential savings from reserved instance purchases

### KPIs Demonstrated
- Total Cloud Costs, Cloud Cost Growth Rate
- Cloud Cost by Service Category
- Cloud Cost per Revenue Dollar
- Utilization Metrics by Resource Type
- Cost Optimization Savings Potential

### Insights Generated
- Development and non-production environments driving 57% of cost growth
- Low compute utilization indicates significant rightsizing opportunity
- Reserved instance strategy could save 28% on stable production workloads
- Implementing auto-shutdown policies could reduce costs by $680K annually
- Cost governance and tagging needed to improve accountability

## Scenario 3: Project Profitability and ROI Analysis

### Business Context
The Finance team needs to evaluate the profitability and ROI of major projects and initiatives to inform future capital allocation decisions. Leadership wants to understand which types of investments deliver the best returns and which should be scaled back or restructured.

### User Questions
1. "What is the profitability of our top 10 projects by revenue?"
2. "Show me ROI and payback period for projects completed in the last 2 years"
3. "Which project categories (product development, infrastructure, market expansion) have the highest ROI?"
4. "Compare planned vs. actual project costs and identify projects with significant budget overruns"
5. "What characteristics do our most successful projects have in common?"

### Expected Data Agent Response
The Data Agent analyzes gold_factprojects, gold_factgeneralledger, and cross-references with revenue and cost data:
- Top 10 projects generated $287M revenue against $168M investment (71% ROI)
- Product development projects: Avg ROI 94%, avg payback 18 months
- Infrastructure projects: Avg ROI 42%, avg payback 32 months
- Market expansion projects: Avg ROI 68%, avg payback 24 months
- Budget performance: 65% of projects within 10% of budget, 23% overran by >20%
- Success factors identified:
  - Projects with dedicated executive sponsors: 87% success rate
  - Projects with clear KPIs from inception: 82% met ROI targets
  - Phased implementation approach: 35% better ROI vs. big-bang
  - Cross-functional teams: 28% faster time-to-value

### KPIs Demonstrated
- Project ROI %, Payback Period (months)
- Actual vs. Planned Project Costs
- Revenue Generated per Project Investment Dollar
- Project Success Rate by Category
- Time to Break-Even

### Insights Generated
- Product development investments delivering best returns - priority for future allocation
- Infrastructure projects critical but need better cost management
- Executive sponsorship and clear KPIs are strongest predictors of success
- Phased approaches reduce risk and improve ROI
- 23% of projects with major overruns require enhanced project governance

## KPIs and Metrics Summary

### Financial Performance
| Metric | Description | Calculation | Target |
|--------|-------------|-------------|--------|
| Total Revenue | Total revenue across all sources | SUM(Revenue) | $1.50B (annual) |
| Revenue Growth % | Year-over-year revenue growth | (Current - PY) / PY | 12% |
| Gross Margin % | Gross profit as % of revenue | Gross Profit / Revenue | 42% |
| EBITDA Margin % | Operating profit margin | EBITDA / Revenue | 22% |
| Operating Expense Ratio | OpEx as % of revenue | Operating Expenses / Revenue | 62% |

### Budget and Variance
| Metric | Description | Calculation | Target |
|--------|-------------|-------------|--------|
| Budget Variance % | Actual vs. Plan variance | (Actual - Plan) / Plan | <5% |
| Forecast Accuracy | Accuracy of quarterly forecasts | 1 - ABS(Forecast - Actual) / Actual | >95% |
| Budget Adherence Rate | % of departments within budget | COUNT(Variance <10%) / Total Depts | >80% |

### Cash and Working Capital
| Metric | Description | Calculation | Target |
|--------|-------------|-------------|--------|
| Operating Cash Flow | Cash generated from operations | CFO from statement | $320M (annual) |
| Days Sales Outstanding | Average collection period | (AR / Revenue) * 365 | 40 days |
| Cash Conversion Cycle | Working capital efficiency | DSO + DIO - DPO | 45 days |
| Free Cash Flow | Cash available after CapEx | Operating CF - CapEx | $240M (annual) |

### Cloud Costs
| Metric | Description | Calculation | Target |
|--------|-------------|-------------|--------|
| Total Cloud Costs | Annual cloud spending | SUM(Cloud Costs) | $35M (annual) |
| Cloud Cost Growth % | YoY cloud cost growth | (Current - PY) / PY | 12% (match revenue) |
| Cloud Cost per $Revenue | Cost efficiency metric | Cloud Costs / Revenue | 2.3% |
| Utilization Rate | Resource utilization | Used Capacity / Provisioned | >70% |

### Project Performance
| Metric | Description | Calculation | Target |
|--------|-------------|-------------|--------|
| Average Project ROI % | Return on investment | (Benefit - Cost) / Cost | >75% |
| Payback Period | Time to recover investment | Months to cumulative benefit = cost | <24 months |
| Budget Adherence | Projects on budget | COUNT(Variance <10%) / Total | >75% |
| On-Time Delivery % | Projects delivered on schedule | On-Time Projects / Total | >80% |

## Data Sources

### Primary Tables
- **gold_factgeneralledger**: Complete financial transactions, GL accounts, actuals vs. budget
- **gold_factsales**: Revenue transactions by product, customer, geography
- **gold_factcloudcosts**: Cloud infrastructure costs by service, project, business unit
- **gold_factprojects**: Project investments, revenues, timelines, outcomes
- **gold_dimdate**: Time intelligence for period comparisons
- **gold_dimgeography**: Regional and organizational hierarchy
- **gold_dimproduct**: Product categorization and hierarchy

### Key Dimensions
- Time: Year, Quarter, Month, Day
- Geography: Region, Country, Business Unit
- Product: Category, Line, SKU
- Account: GL Account, Cost Center, Department
- Project: Type, Status, Owner

## Demonstration Steps

### Step 1: Financial Performance Dashboard
1. Connect to Enterprise Analytics Model in Microsoft Fabric
2. Ask: "What was our total revenue and gross margin for last month compared to plan and prior year?"
3. Observe Data Agent query gold_factgeneralledger and gold_factsales
4. Review visualization showing revenue trends, margin analysis, and variance breakdown
5. Drill into specific product categories or regions showing variance

### Step 2: Cloud Cost Analysis
1. Ask: "Show me our cloud cost trends and identify optimization opportunities"
2. Watch Data Agent analyze gold_factcloudcosts across time and service dimensions
3. Review cost trend charts, service breakdown, and business unit allocation
4. Examine optimization recommendations with potential savings quantified
5. Explore utilization metrics and rightsizing opportunities

### Step 3: Project ROI Analysis
1. Ask: "What is the ROI of our top projects and which categories perform best?"
2. Data Agent combines gold_factprojects with financial outcomes
3. Review ROI scatter plots, payback period analysis, category comparisons
4. Identify success factors through pattern analysis
5. Discuss capital allocation recommendations based on ROI insights

### Step 4: Budget Variance Investigation
1. Ask: "Which departments are over budget and what are the drivers?"
2. Data Agent analyzes budget vs. actual across all cost centers
3. Review variance waterfall charts and trend analysis
4. Drill into specific departments with largest variances
5. Identify corrective actions and forecast impact

### Step 5: What-If Scenario Planning
1. Ask: "If we reduce cloud costs by 15% and reallocate to product development, what's the impact?"
2. Data Agent performs scenario modeling with assumptions
3. Review projected P&L impact, ROI expectations, implementation timeline
4. Discuss trade-offs and strategic considerations
5. Export scenario for board presentation

## Expected Insights and Outcomes

### Immediate Insights
- Clear visibility into financial performance vs. targets across all dimensions
- Identification of $3.15M in cloud cost optimization opportunities
- Understanding of project ROI drivers to inform future capital allocation
- Real-time budget variance alerts for proactive management
- Data-driven forecast updates incorporating latest trends

### Strategic Outcomes
- Improved forecast accuracy from 85% to 95%+ through better data integration
- 15% reduction in cloud costs ($6.4M annual savings) through governance and optimization
- Reallocation of budget to high-ROI projects (product development focus)
- Enhanced financial planning cycle with automated reporting (5-day close vs. 15-day)
- Better capital allocation decisions driven by data-driven ROI analysis

### Business Value
- $6.4M in annual cloud cost savings
- 10% improvement in forecast accuracy reducing planning uncertainty
- 20% faster financial close enabling quicker decision-making
- 150 hours/month saved on manual reporting and analysis
- Improved stakeholder confidence through transparent, data-driven insights
- Enhanced ability to achieve 22% EBITDA margin target through cost optimization
