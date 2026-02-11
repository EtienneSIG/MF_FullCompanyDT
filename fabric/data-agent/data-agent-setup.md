# Fabric Data Agent - Setup Guide

## 🎯 Overview

This guide walks through configuring a **Fabric Data Agent** for the Enterprise Data Platform, enabling natural language queries across 15+ business domains.

**Goal:** Create an intelligent agent that can answer complex business questions by reasoning across sales, supply chain, HR, support, and other domains.

**Key Principles:**
- ✅ **Focused scope:** Select 5-7 key tables (not all tables)
- ✅ **Rich metadata:** Tables must have descriptions and synonyms
- ✅ **Clear instructions:** Provide domain guidance
- ✅ **Example questions:** Include 10+ sample Q&A pairs
- ✅ **Verified answers:** Pre-define responses to common queries

---

## 📋 Prerequisites

- **Microsoft Fabric Workspace** with Premium capacity (F64+)
- **Semantic Model** with Direct Lake connection to Gold tables
- **Metadata Enrichment:** Tables/measures with descriptions and synonyms (use Power BI MCP)
- **Sample Data:** Loaded and transformed (Bronze → Silver → Gold)

---

## 🚀 Step-by-Step Setup

### Step 1: Create Data Agent

1. **Navigate to Fabric Workspace:** `EnterprisePlatformDemo`

2. **Click "+ New"** → **Data Agent**

3. **Configure Agent:**
   - **Name:** `Enterprise Insights Agent`
   - **Description:** `Multi-domain analytics agent for sales, support, HR, supply chain, and operational insights`

---

### Step 2: Select Data Sources

**Recommended Approach:** Start with 5-7 core tables covering key business areas.

**Selected Tables:**

| Table | Domain | Purpose |
|-------|--------|---------|
| `FactSales` | Sales | Revenue, orders, customer transactions |
| `FactSupport` | Call Center | Support tickets, CSAT, resolution times |
| `FactInventory` | Supply Chain | Inventory levels, stockouts, turns |
| `FactAttrition` | HR | Employee turnover, retention |
| `FactIncidents` | IT Ops | IT incidents, downtime, MTTR |
| `DimCustomer` | Conformed | Customer master data |
| `DimProduct` | Conformed | Product catalog |
| `DimDate` | Conformed | Date dimension with fiscal calendar |

**Why This Selection?**

- **Cross-domain coverage:** Sales + Support + HR + Operations
- **Customer journey:** Acquisition → Sales → Support → Retention
- **Operational visibility:** Inventory + IT incidents
- **Manageable scope:** 8 tables = faster responses, less hallucination

**Tables to Avoid in Initial Setup:**
- ❌ Bridge tables (add complexity)
- ❌ Staging/silver tables (use Gold only)
- ❌ Rarely-used domains (add later if needed)

---

### Step 3: Add Agent Instructions

**Purpose:** Guide the agent on how to use each table and when to apply specific logic.

**Instructions Template:**

```markdown
# Enterprise Insights Agent - System Instructions

## Role & Scope

You are an enterprise analytics assistant with access to data across Sales, Customer Support, HR, Supply Chain, and IT Operations. Your goal is to provide accurate, actionable insights to business stakeholders.

## Data Sources & Usage Guidelines

### FactSales (Sales Transactions)
**Use for:** Revenue analysis, order trends, customer purchasing behavior, product performance
**Key Metrics:** Total Revenue, Gross Margin %, Average Order Value, Order Count
**Filters:** Always exclude status = 'Cancelled' or 'Returned' unless explicitly asked
**Time Grain:** Daily (order_date)
**Example Questions:**
- "What was revenue last quarter?"
- "Top 10 products by revenue"
- "Revenue trend by region"

### FactSupport (Customer Support Tickets)
**Use for:** Customer satisfaction, support performance, issue tracking
**Key Metrics:** CSAT Score, Avg Resolution Time, FCR % (First Contact Resolution), Ticket Count
**Filters:** Exclude status = 'Spam' or 'Duplicate'
**Time Grain:** Daily (create_date)
**Example Questions:**
- "What's our CSAT score this month?"
- "Top customer complaints by product"
- "Average resolution time by priority"

### FactInventory (Inventory Snapshots)
**Use for:** Stock levels, inventory turns, stockout analysis
**Key Metrics:** Inventory Value, Inventory Turns, Days of Supply, Stockout Rate
**Time Grain:** Daily snapshots
**Example Questions:**
- "Which products are out of stock?"
- "Inventory turns by category"
- "Days of supply for critical items"

### FactAttrition (Employee Turnover)
**Use for:** Attrition analysis, retention trends, manager performance
**Key Metrics:** Attrition Rate, Voluntary Attrition %, Regrettable Loss %
**Filters:** Only count is_active = FALSE employees
**Time Grain:** Monthly aggregation recommended
**Example Questions:**
- "Attrition rate by department"
- "Managers with highest attrition"
- "Voluntary vs involuntary turnover"

### FactIncidents (IT Incidents)
**Use for:** IT reliability, downtime analysis, MTTR tracking
**Key Metrics:** MTTR (Mean Time to Resolution), Downtime Hours, P1 Incident Count
**Filters:** Exclude status = 'Duplicate'
**Time Grain:** Hourly for P1/P2, daily for P3/P4
**Example Questions:**
- "P1 incidents this week"
- "Average MTTR by severity"
- "Downtime impact on users"

## Dimension Tables

### DimCustomer
**Attributes:** Industry, Segment, Region, Customer Since Date
**Hierarchies:** Region → Country → City
**Use for:** Customer segmentation, regional analysis

### DimProduct
**Attributes:** Category, Subcategory, Brand, Lifecycle Stage
**Hierarchies:** Category → Subcategory → Product
**Use for:** Product performance, category trends

### DimDate
**Attributes:** Year, Quarter, Month, Fiscal Year, Is Weekend, Is Holiday
**Use for:** Time-based analysis, fiscal reporting
**Fiscal Year:** Starts July 1

## Cross-Domain Analysis Patterns

### Pattern 1: Revenue ↔ Support
**Question Type:** "How does support quality impact sales?"
**Approach:**
1. Join FactSales and FactSupport on customer_id
2. Correlate CSAT with revenue trends
3. Identify customers with low CSAT and declining sales

### Pattern 2: Inventory ↔ Sales
**Question Type:** "Are stockouts impacting revenue?"
**Approach:**
1. Identify products with stockouts in FactInventory
2. Compare sales before/after stockout period in FactSales
3. Calculate lost revenue opportunity

### Pattern 3: Attrition ↔ Incidents
**Question Type:** "Does IT instability correlate with attrition?"
**Approach:**
1. Group FactIncidents by affected_system and calculate downtime
2. Join with FactAttrition by department
3. Analyze correlation between downtime and turnover

### Pattern 4: Customer Journey
**Question Type:** "Analyze customer lifecycle"
**Approach:**
1. First purchase: MIN(order_date) in FactSales
2. Support interactions: FactSupport filtered by customer
3. Churn: Last order date vs current date

## Response Guidelines

### Format
- **Start with the answer:** Lead with key number/insight
- **Add context:** Compare to benchmarks, prior periods, or targets
- **Suggest actions:** When relevant, recommend next steps
- **Cite sources:** Mention which tables/measures were used

### Example Response Format
```
Q: "What drove revenue drop in EMEA last month?"

A: "EMEA revenue declined 8.2% MoM (from $5.2M to $4.8M).

Key Drivers:
1. Inventory stockouts in top 3 products (FactInventory: stockout rate increased from 2% to 9%)
2. Increased customer complaints (FactSupport: CSAT dropped from 4.2 to 3.6)
3. Delayed shipments (FactSales: avg delivery time +3 days)

Recommendation: Prioritize inventory replenishment for Product A, B, C and investigate support quality issues."
```

### Time References
- "Last month" = Most recent complete month
- "This quarter" = Current fiscal quarter (use DimDate[fiscal_quarter])
- "YTD" = Fiscal year-to-date (starts July 1)
- "Last year" = Prior calendar year

### Number Formatting
- Revenue/Costs: $12.4M (millions), $342K (thousands)
- Percentages: 15.3% (one decimal)
- Large counts: 1.2K, 45.3K
- Ratios: 3.2x (inventory turns), 4.5:1 (pipeline ratio)

## Limitations & Escalation

### Known Limitations
- **No real-time data:** Data refreshed daily (overnight)
- **No PII access:** Employee names/emails anonymized
- **No drill-to-detail:** Can show aggregates, not individual transactions

### When to Escalate
- Questions requiring data not in scope (e.g., "R&D experiments")
- Requests for raw transaction exports
- Complex statistical modeling (regression, clustering)
- Questions about future predictions beyond simple trends

### Escalation Template
```
"I don't have access to [X data]. This question would require [Y table/domain] which isn't currently in my scope. Would you like me to:
1. Answer with available related data ([Z alternative])
2. Suggest requesting access to additional data sources"
```

## Data Refresh Schedule

- **FactSales:** Daily at 2 AM UTC
- **FactSupport:** Daily at 3 AM UTC
- **FactInventory:** Daily snapshots at 1 AM UTC
- **FactAttrition:** Weekly (Mondays)
- **FactIncidents:** Near real-time (5-minute lag)

Always mention data freshness if relevant to the question.

## Verified Answers

For these common questions, use these exact responses:

**Q: "What was revenue last quarter?"**
**A:** "Revenue for Q2 FY2026 (Oct-Dec 2025) was $42.3M, up 12% vs Q2 FY2025 ($37.8M)."

**Q: "What's our customer churn rate?"**
**A:** "Customer churn rate is 5.2% annually, calculated as customers lost / avg active customers over 12 months."

**Q: "How many employees do we have?"**
**A:** "Current headcount is 1,847 active employees (as of latest HR data refresh)."

**Q: "What's our average CSAT score?"**
**A:** "Average CSAT score is 4.1/5 based on 23,456 survey responses in the last 90 days."
```

---

### Step 4: Add Example Questions

Provide 15-20 sample questions covering:
- Single-domain queries
- Multi-domain correlations
- Time-based comparisons
- What-if scenarios

**See:** `example-questions.md` for full list of 50+ questions organized by complexity.

---

### Step 5: Configure Verified Answers

For high-frequency questions, pre-define exact responses:

1. **Navigate to:** Data Agent Settings → Verified Answers
2. **Add entries:**

```yaml
- question: "What was revenue last quarter?"
  answer: "Q2 FY2026 revenue: $42.3M (+12% YoY)"
  
- question: "What's our attrition rate?"
  answer: "7.2% annual attrition rate (vs 7.5% industry average)"
  
- question: "How many support tickets are open?"
  answer: "347 open tickets (avg 4.2 days open)"
```

**Benefits:**
- ✅ Consistent responses
- ✅ Faster query times
- ✅ No hallucination risk

---

### Step 6: Test the Agent

**Test Plan:**

1. **Basic Single-Table Queries:**
   ```
   - "What was revenue last month?"
   - "Top 10 customers by revenue"
   - "CSAT score by product category"
   ```

2. **Time Intelligence:**
   ```
   - "Revenue YTD vs last year"
   - "Quarterly revenue trend"
   - "MoM change in CSAT"
   ```

3. **Cross-Domain Correlations:**
   ```
   - "Does low CSAT correlate with customer churn?"
   - "Impact of inventory stockouts on revenue"
   - "Attrition by manager and impact on support resolution times"
   ```

4. **Complex Multi-Step Reasoning:**
   ```
   - "Why did revenue drop in EMEA and what can we do about it?"
   - "Summarize customer complaints and link to product defects"
   - "Explain the relationship between IT incidents and employee attrition"
   ```

**Success Criteria:**
- ✅ Answers are accurate (verify against known queries)
- ✅ Responses include context and comparisons
- ✅ Agent cites correct sources
- ✅ No hallucinated data
- ✅ Actionable recommendations provided

---

### Step 7: Iterate Based on Usage

**Monitor:**
- Question patterns (what are users asking?)
- Failed queries (where does agent struggle?)
- Feedback scores (thumbs up/down)

**Optimize:**
- Add more metadata to underperforming tables
- Include new verified answers for common questions
- Expand instructions for problematic patterns
- Add/remove tables based on usage

---

## 🎯 Optimization Checklist

Before launching to users:

- [ ] **Metadata Quality:**
  - [ ] All tables have descriptions
  - [ ] All key measures have descriptions
  - [ ] Synonyms added for business terms
  - [ ] Sample values provided where helpful

- [ ] **Instructions:**
  - [ ] Usage guidelines for each table
  - [ ] Cross-domain patterns documented
  - [ ] Response format specified
  - [ ] Limitations clearly stated

- [ ] **Verified Answers:**
  - [ ] Top 10 questions pre-defined
  - [ ] Answers validated against data
  - [ ] Updated for current period

- [ ] **Testing:**
  - [ ] 20+ test questions executed
  - [ ] Accuracy verified
  - [ ] Performance acceptable (<5 sec response)
  - [ ] No hallucinations detected

- [ ] **User Training:**
  - [ ] Example questions shared with users
  - [ ] Demo session conducted
  - [ ] Feedback mechanism in place

---

## 📊 Expected Performance

### Response Times
- **Simple queries** (single table, basic aggregation): 1-3 seconds
- **Medium queries** (multi-table join, time intelligence): 3-7 seconds
- **Complex queries** (multi-step reasoning, correlations): 7-15 seconds

### Accuracy
- **Well-documented tables:** 85-95% accuracy
- **Poorly documented tables:** 50-70% accuracy
- **With verified answers:** 100% accuracy for pre-defined questions

### User Adoption
- **Week 1:** 10-20 queries/day (early adopters)
- **Month 1:** 50-100 queries/day (team adoption)
- **Month 3:** 200+ queries/day (org-wide usage)

---

## 🚨 Common Issues & Solutions

### Issue: "Agent gives wrong numbers"
**Root Cause:** Missing or incorrect filters
**Solution:** Add explicit filter guidance in instructions (e.g., "exclude status = 'Cancelled'")

### Issue: "Agent says 'I don't have access to that data'"
**Root Cause:** User asking about domain not in scope OR table missing metadata
**Solution:** 
1. Check if table is included in sources
2. Verify table has description
3. Update instructions with usage examples

### Issue: "Responses are too slow"
**Root Cause:** Too many tables in scope OR complex semantic model
**Solution:**
1. Reduce tables to 5-7 core tables
2. Create aggregations in semantic model
3. Simplify relationships (remove unused)

### Issue: "Agent gives generic responses"
**Root Cause:** Lacks context/metadata
**Solution:** Use Power BI MCP to bulk-add descriptions and synonyms

---

## 📚 Additional Resources

- **Example Questions:** [example-questions.md](example-questions.md)
- **Agent Instructions Template:** [agent-instructions.md](agent-instructions.md)
- **Metadata Enhancement Guide:** [../powerbi/powerbi-mcp.md](../powerbi/powerbi-mcp.md)
- **Microsoft Fabric Data Agent Docs:** [learn.microsoft.com/fabric/data-agent](https://learn.microsoft.com/fabric/data-agent)

---

**Ready to enable natural language analytics for your organization? Follow this guide and you'll have a production-ready Data Agent in under 2 hours! 🚀**
