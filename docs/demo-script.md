# Demo Script - Full Enterprise Data Platform

## 🎯 Overview

This demo showcases Microsoft Fabric as a comprehensive enterprise data platform, demonstrating:
- Multi-domain data integration (15+ business streams)
- Medallion architecture (Bronze → Silver → Gold)
- AI transformations on unstructured data
- Direct Lake semantic models
- Natural language insights with Fabric Data Agent
- Developer productivity with Power BI MCP Server

**Duration:** 10-15 minutes (core demo) | 5-minute and 30-minute variants included
**Audience Level:** Business and technical stakeholders
**Prerequisites:** Fabric workspace with Premium capacity (F64+ recommended)

---

## 📋 Pre-Demo Setup Checklist

### Before the Demo (30 minutes setup)

- [ ] **Generate synthetic data:**
  ```bash
  cd data-gen
  python generate_all.py
  ```
  
- [ ] **Create Fabric workspace:** `EnterprisePlatformDemo`

- [ ] **Create Lakehouse:** `EnterpriseDataLake`

- [ ] **Upload Bronze data:**
  - Upload all CSV files from `data-gen/output/structured/` to `Files/bronze/`
  - Upload text files from `data-gen/output/unstructured/` to `Files/unstructured/`

- [ ] **Run transformation notebooks:**
  - Execute `01_ingest_to_bronze.ipynb`
  - Execute `02_transform_to_silver.ipynb`
  - Execute `03_build_gold_star_schema.ipynb`

- [ ] **Create OneLake Shortcut:**
  - Link to `Files/unstructured/callcenter_emails/`

- [ ] **Apply AI Transformations:**
  - Sentiment Analysis on call center emails
  - Summarization on support tickets

- [ ] **Create Semantic Model:**
  - Direct Lake connection to Gold tables
  - Import DAX measures from `fabric/powerbi/dax-measures.md`

- [ ] **Configure Data Agent:**
  - Name: `Enterprise Insights Agent`
  - Sources: Select 5-7 key tables (FactSales, FactSupport, DimCustomer, DimProduct, DimEmployee, FactIncidents, FactInventory)
  - Add instructions from `fabric/data-agent/agent-instructions.md`

---

## 🎬 Demo Script (10-15 minutes)

### Introduction (1 minute)

**Talking Points:**

> "Today I'll show you how Microsoft Fabric unifies your entire enterprise data landscape—from sales and supply chain to HR and support—into a single, AI-powered platform."

**Slide/Visual:** Show architecture diagram (from README.md)

> "We've built a synthetic dataset representing 15+ business domains—CRM, Sales, Product, Marketing, HR, Supply Chain, Manufacturing, Finance, ESG, Call Center, IT Ops, FinOps, Risk & Compliance, R&D, and Quality & Security. This mirrors a real enterprise data environment."

---

### Act 1: OneLake - Unified Data Foundation (3 minutes)

**Objective:** Show how OneLake eliminates data silos

**Steps:**

1. **Navigate to Lakehouse:** `EnterpriseDataLake`

2. **Show Bronze layer structure:**
   ```
   Files/
   ├── bronze/
   │   ├── crm/
   │   │   ├── accounts.csv
   │   │   ├── contacts.csv
   │   │   └── opportunities.csv
   │   ├── sales/
   │   │   ├── orders.csv
   │   │   ├── order_lines.csv
   │   │   └── invoices.csv
   │   ├── hr/
   │   │   ├── employees.csv
   │   │   └── attrition.csv
   │   └── [other domains...]
   ```

   **Talking Points:**
   > "This is our Bronze layer—raw data from 15 different systems, all in OneLake. Notice we have structured CSV files for transactional data."

3. **Navigate to Silver layer:**
   ```
   Tables/
   ├── silver_customers (Delta)
   ├── silver_products (Delta)
   ├── silver_orders (Delta)
   └── [other conformed tables...]
   ```

   **Talking Points:**
   > "Our Silver layer applies data quality rules and creates conformed dimensions—single source of truth for customers, products, dates, and employees across all domains."

4. **Navigate to Gold layer:**
   ```
   Tables/
   ├── DimCustomer (Delta)
   ├── DimProduct (Delta)
   ├── DimDate (Delta)
   ├── FactSales (Delta)
   ├── FactSupport (Delta)
   └── [other star schemas...]
   ```

   **Talking Points:**
   > "Gold layer contains analytics-ready star schemas. These Delta tables power our Direct Lake semantic model—no data movement, just pure lakehouse analytics."

**Key Message:** "OneLake provides a single namespace for all enterprise data—no copying, no ETL sprawl."

---

### Act 2: OneLake Shortcuts + AI Transformations (3 minutes)

**Objective:** Demonstrate AI-powered unstructured data processing

**Steps:**

1. **Show unstructured data source:**
   ```
   Files/unstructured/callcenter_emails/
   ├── email_00001.txt
   ├── email_00002.txt
   └── [5,000+ emails...]
   ```

   **Talking Points:**
   > "Here we have 5,000 customer support emails—unstructured text. Traditionally, this would require complex NLP pipelines. Watch what Fabric can do automatically."

2. **Create OneLake Shortcut** (live or show pre-created):
   - Right-click `Tables` → New shortcut → OneLake → Select `callcenter_emails`

3. **Apply AI Transformations:**
   - Select shortcut → AI Transformations → Configure:
     - ✅ Sentiment Analysis
     - ✅ Summarization
     - ✅ PII Detection (mask emails/phone numbers)
     - ✅ Named Entity Recognition (extract product names, customer names)

4. **Show transformed output:**
   ```sql
   SELECT 
       email_id,
       original_text,
       sentiment,           -- "positive", "negative", "neutral"
       sentiment_score,     -- 0.0 to 1.0
       summary,             -- AI-generated summary
       detected_pii,        -- ["email", "phone"]
       masked_text,         -- PII redacted version
       extracted_entities   -- ["Product X", "John Doe"]
   FROM callcenter_emails_transformed
   LIMIT 10;
   ```

   **Talking Points:**
   > "In minutes, Fabric has turned 5,000 raw emails into a query-ready Delta table with sentiment scores, summaries, and PII protection. This table auto-refreshes as new emails arrive."

5. **Show joined query:**
   ```sql
   SELECT 
       p.product_name,
       AVG(e.sentiment_score) as avg_sentiment,
       COUNT(*) as email_count,
       STRING_AGG(e.summary, '; ') as top_issues
   FROM callcenter_emails_transformed e
   JOIN DimProduct p ON e.extracted_product = p.product_name
   WHERE e.sentiment = 'negative'
   GROUP BY p.product_name
   ORDER BY email_count DESC;
   ```

   **Talking Points:**
   > "Now we're correlating unstructured feedback with structured product data—finding which products have the most negative sentiment and why."

**Key Message:** "AI Transformations turn unstructured data into insights automatically—no coding required."

---

### Act 3: Power BI Semantic Model (Direct Lake) (2 minutes)

**Objective:** Show enterprise-grade semantic layer

**Steps:**

1. **Open Semantic Model:** `Enterprise Analytics Model`

2. **Show model diagram:**
   - 15+ fact tables
   - 5 conformed dimensions (Customer, Product, Date, Employee, Geography)
   - Relationships (all one-to-many)

   **Talking Points:**
   > "This is our enterprise semantic model—over 100 DAX measures across all business domains. Notice it's using Direct Lake mode—querying Delta tables directly, no data import."

3. **Highlight key measure groups:**
   - **Sales Metrics:** Total Revenue, Gross Margin %, YTD Sales
   - **Supply Chain:** Inventory Turns, Backorder Rate, On-Time Delivery %
   - **HR:** Attrition Rate, Time to Hire, Training ROI
   - **Support:** CSAT Score, First Contact Resolution %, Avg Resolution Time
   - **ESG:** Total Emissions (Scope 1+2+3), Energy Intensity, Sustainability Score

4. **Show measure example:**
   ```dax
   Total Revenue = 
   CALCULATE(
       SUM(FactSales[net_amount]),
       FactSales[status] <> "Cancelled"
   )
   
   Revenue YTD = 
   CALCULATE(
       [Total Revenue],
       DATESYTD(DimDate[Date])
   )
   ```

   **Talking Points:**
   > "These measures follow enterprise naming conventions, include descriptions and synonyms for AI readiness, and are organized by domain for easy discovery."

**Key Message:** "Direct Lake gives you enterprise BI performance without data duplication."

---

### Act 4: Fabric Data Agent - Natural Language Insights (4 minutes)

**Objective:** Demonstrate multi-domain question answering

**Steps:**

1. **Open Data Agent:** `Enterprise Insights Agent`

2. **Ask Question 1 (Single-domain):**
   ```
   "What was our total revenue last month and how does it compare to the same month last year?"
   ```

   **Expected Response:**
   > "Total revenue in January 2026 was $12.4M, down 8.2% compared to January 2025 ($13.5M). The decline was primarily driven by EMEA region (-15.3%) and APAC (-12.1%), while Americas remained flat (+0.5%)."

   **Talking Points:**
   > "Simple question—but notice it understands 'last month', does year-over-year comparison, and breaks it down by region without being asked."

3. **Ask Question 2 (Multi-domain correlation):**
   ```
   "Why did revenue drop in EMEA last month? Are there supply chain or inventory issues?"
   ```

   **Expected Response:**
   > "EMEA revenue decline correlates with:
   > 1. Inventory stockouts for top 3 products (Product A, B, C) - Backorder Rate increased from 2.1% to 8.7%
   > 2. Supplier delays from Vendor X (12 days late on average) impacting 35% of orders
   > 3. Manufacturing yield issues in Plant DE-Berlin (OEE dropped from 87% to 72%)
   > 
   > Recommendation: Prioritize Vendor X remediation and Berlin plant quality investigation."

   **Talking Points:**
   > "Now it's connecting the dots across Sales, Supply Chain, and Manufacturing. This is the power of a unified semantic model—the agent can reason across domains."

4. **Ask Question 3 (Unstructured + Structured):**
   ```
   "Summarize top customer complaints by product line and link them to quality defects."
   ```

   **Expected Response:**
   > "Top complaints by product line (from 2,347 support emails analyzed):
   > 
   > **Electronics:**
   > - Battery life issues (427 mentions, avg sentiment: -0.72)
   > - Linked to Quality Defect QD-2024-0156 (battery supplier change)
   > 
   > **Home Appliances:**
   > - Noise during operation (312 mentions, avg sentiment: -0.65)
   > - Linked to Defect QD-2024-0189 (motor vibration)
   > 
   > **Furniture:**
   > - Assembly instructions unclear (201 mentions, avg sentiment: -0.58)
   > - No quality defect logged—documentation gap identified"

   **Talking Points:**
   > "Here the agent is combining AI-transformed support emails with structured quality defect data—finding patterns humans might miss."

5. **Ask Question 4 (HR + Operations impact):**
   ```
   "Show me attrition hotspots by manager and analyze impact on delivery SLAs."
   ```

   **Expected Response:**
   > "Attrition hotspots (last 6 months):
   > 
   > 1. **Manager: Sarah Chen (Manufacturing)** - 18% attrition (vs 7% company avg)
   >    - Impact: Plant OEE dropped from 85% to 76%
   >    - Delivery SLA compliance: 82% (down from 94%)
   > 
   > 2. **Manager: Mike Johnson (Customer Support)** - 22% attrition
   >    - Impact: Avg resolution time increased from 4.2 to 6.8 hours
   >    - CSAT score: 3.2/5 (down from 4.1/5)
   > 
   > Recommendation: Conduct retention interviews and backfill hiring for both teams."

   **Talking Points:**
   > "Cross-domain again—HR attrition data linked to operational KPIs. This gives executives actionable insights they couldn't easily get before."

**Key Message:** "Fabric Data Agent turns your semantic model into a conversational analytics assistant—no SQL, no dashboards, just questions and answers."

---

### Act 5: Power BI MCP Server - Developer Productivity (2 minutes)

**Objective:** Show rapid model development in VS Code

**Steps:**

1. **Open VS Code** → Connect to semantic model

2. **Copilot Chat Example 1:**
   ```
   User: "Create all relationships between FactSales and dimension tables"
   
   Copilot: [Shows code to create relationships]
           DimCustomer[customer_id] → FactSales[customer_id]
           DimProduct[product_id] → FactSales[product_id]
           DimDate[date_id] → FactSales[order_date_id]
           ...
   ```

   **Talking Points:**
   > "Instead of clicking through the UI, Copilot creates relationships in bulk. This is the Power BI Modeling MCP Server in action."

3. **Copilot Chat Example 2:**
   ```
   User: "Generate YTD, QTD, and MoM measures for Revenue, Margin, and Inventory Turns"
   
   Copilot: [Generates 9 DAX measures with correct time intelligence]
   ```

4. **Copilot Chat Example 3:**
   ```
   User: "Add descriptions and synonyms to all tables for AI readiness"
   
   Copilot: [Adds metadata to improve Data Agent responses]
   ```

   **Talking Points:**
   > "AI-readiness requires good metadata—descriptions, synonyms, sample values. Copilot can bulk-apply these based on best practices, saving hours of manual work."

**Key Message:** "Power BI MCP Server brings AI assistance to semantic model development—faster, more consistent, and easier to maintain."

---

### Conclusion & Call to Action (1 minute)

**Recap:**

> "In 15 minutes, we've seen:
> 1. **OneLake** unifying 15+ business domains in a single data lake
> 2. **AI Transformations** turning unstructured emails into insights
> 3. **Direct Lake** enabling enterprise BI without data duplication
> 4. **Data Agent** answering complex questions across domains in natural language
> 5. **Power BI MCP** accelerating model development with AI assistance
> 
> This is the future of enterprise data platforms—unified, intelligent, and conversational."

**Call to Action:**

> "Ready to try this in your environment? All the code, notebooks, and documentation are in this GitHub repository. You can have a working demo in under an hour."

**Next Steps:**
1. Clone the repository
2. Run the data generator
3. Follow the setup guide in `docs/demo-script.md`
4. Customize for your business domains

---

## 🎯 Demo Variants

### 5-Minute Executive Demo

**Focus:** Business value, skip technical details

1. **Introduction (30 sec):** Problem statement (data silos)
2. **OneLake (1 min):** Show unified data lake with 15 domains
3. **AI Transformations (1.5 min):** Email sentiment → insights
4. **Data Agent (2 min):** Ask 2 multi-domain questions
5. **Conclusion (30 sec):** ROI and next steps

**Skip:** Power BI MCP Server, technical architecture

---

### 30-Minute Deep Dive

**Audience:** Data engineers, architects

**Additional Topics:**

1. **Data Generation (5 min):**
   - Walk through `generate_all.py`
   - Show conformed dimension logic
   - Explain referential integrity checks

2. **Medallion Architecture (5 min):**
   - Bronze: Raw ingestion patterns
   - Silver: Data quality rules, deduplication, type casting
   - Gold: Star schema design principles

3. **Notebook Walkthrough (5 min):**
   - Open `03_build_gold_star_schema.ipynb`
   - Explain dimension SCD Type 2 logic
   - Show fact table aggregation patterns

4. **Security & Governance (3 min):**
   - Row-level security (RLS) implementation
   - Column-level security (CLS) for PII
   - Workspace separation strategy

5. **Power BI MCP Advanced (3 min):**
   - Show DAX query validation
   - Demonstrate bulk renaming with naming conventions
   - Use semantic search to find related measures

6. **Performance Optimization (2 min):**
   - Delta table partitioning strategy
   - Semantic model aggregations
   - Query folding verification

7. **Q&A (7 min)**

---

## 📊 Demo Assets

### Sample Questions for Data Agent

**Sales & Revenue:**
- "What products have the highest gross margin and which customers buy them?"
- "Show me revenue trend by region for the last 12 months with forecast"

**Supply Chain:**
- "Which suppliers have the worst on-time delivery and how does it impact our SLAs?"
- "Calculate inventory turns by product category and identify slow-moving items"

**HR & Operations:**
- "What's our voluntary attrition rate by department and is it correlated with manager performance ratings?"
- "Show hiring pipeline status and time-to-fill metrics by role"

**Support & Quality:**
- "What are the top 5 product defects and their impact on CSAT scores?"
- "Summarize escalated support tickets and link them to quality CAPAs"

**ESG:**
- "Calculate our Scope 1, 2, and 3 emissions breakdown and compare to our sustainability targets"
- "Which facilities have the highest energy intensity and what's the improvement trend?"

**Finance:**
- "Show budget vs actuals variance by cost center for Q4 2025"
- "Explain cashflow changes month-over-month and identify main drivers"

**Cross-Domain:**
- "Why did customer churn increase in Q4 and does it correlate with support wait times or product quality issues?"
- "Connect R&D experiment failures to manufacturing yield issues and product returns"

---

## 🛠️ Troubleshooting

### Common Issues During Demo

**Issue:** Data Agent gives generic responses

**Fix:** 
- Check that semantic model has descriptions and synonyms
- Verify agent instructions are loaded
- Ensure correct tables are selected as sources

---

**Issue:** Direct Lake model doesn't show data

**Fix:**
- Confirm Gold tables are in Delta format
- Check lakehouse connection in semantic model settings
- Refresh the semantic model

---

**Issue:** AI Transformations fail

**Fix:**
- Verify text files are in correct format (UTF-8)
- Check that shortcut path is accessible
- Ensure workspace has AI features enabled (Premium capacity)

---

**Issue:** Power BI MCP doesn't connect

**Fix:**
- Restart VS Code
- Check that Power BI Modeling MCP extension is installed
- Verify semantic model is published to Fabric workspace

---

## 📝 Speaker Notes

### Handling Questions

**Q: "Is this data real?"**
A: "No, all data is synthetically generated using Python libraries like Faker. This ensures we can demo freely without any privacy concerns while still showing realistic patterns."

**Q: "How long does setup take?"**
A: "Data generation takes 5-10 minutes. Initial Fabric deployment takes about 30 minutes. After that, the environment is persistent—you can reuse it for multiple demos."

**Q: "Can this handle real production scale?"**
A: "Absolutely. We're showing ~4 million records here, but Fabric OneLake can handle petabytes. Direct Lake supports billions of rows with sub-second query times."

**Q: "What about data security?"**
A: "Great question. Fabric supports row-level security (RLS), column-level security (CLS), and encryption at rest. We have templates for all of these in the repository. For multi-tenant scenarios, you'd use workspace separation."

**Q: "How accurate is the Data Agent?"**
A: "Data Agent leverages GPT-4 with grounding in your semantic model. Accuracy depends on metadata quality—descriptions, synonyms, verified answers. We've found 85-90% accuracy for well-documented models. You can also add human-in-the-loop validation."

---

## ✅ Post-Demo Checklist

After the demo:

- [ ] Share repository link: [GitHub URL]
- [ ] Send follow-up email with:
  - Demo recording (if recorded)
  - Link to documentation
  - Setup guide: `docs/demo-script.md`
- [ ] Schedule follow-up for questions
- [ ] Track leads in CRM (if sales demo)

---

**Good luck with your demo! 🚀**
