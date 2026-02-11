# Demo Checklist - Full Enterprise Data Platform

## 🎯 Pre-Demo Setup (Allow 60 minutes)

### Phase 1: Data Generation (10 minutes)

- [ ] **Clone repository** and navigate to `MF_FullCompanyDT`
- [ ] **Install Python dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- [ ] **Generate synthetic data:**
  ```bash
  cd data-gen
  python generate_all.py
  ```
- [ ] **Verify output:**
  - Check `data-gen/output/structured/` for CSV files
  - Check `data-gen/output/unstructured/` for text files
  - Confirm ~4M structured records + 5K text files

---

### Phase 2: Microsoft Fabric Workspace Setup (15 minutes)

- [ ] **Create Fabric Workspace:**
  - Name: `EnterprisePlatformDemo`
  - Capacity: Premium F64 or higher
  - Permissions: Add demo participants as Contributors

- [ ] **Create Lakehouse:**
  - Name: `EnterpriseDataLake`
  - Description: "Multi-domain enterprise data platform demo"

- [ ] **Upload Bronze Data:**
  - Navigate to Lakehouse → Files → New Folder → `bronze`
  - Upload all CSV files from `data-gen/output/structured/`
  - Upload text files to `Files/unstructured/`
  - Verify file counts match generated data

---

### Phase 3: Data Transformation (20 minutes)

- [ ] **Import Notebooks:**
  - Import `fabric/notebooks/01_ingest_to_bronze.ipynb`
  - Import `fabric/notebooks/02_transform_to_silver.ipynb`
  - Import `fabric/notebooks/03_build_gold_star_schema.ipynb`
  - Import `fabric/notebooks/04_quality_checks.ipynb`

- [ ] **Execute Notebooks in Order:**
  - [ ] Run `01_ingest_to_bronze.ipynb` (creates Delta tables from CSV)
  - [ ] Run `02_transform_to_silver.ipynb` (data quality + conformance)
  - [ ] Run `03_build_gold_star_schema.ipynb` (builds star schemas)
  - [ ] Run `04_quality_checks.ipynb` (validates referential integrity)

- [ ] **Verify Gold Tables:**
  - Check Lakehouse → Tables → Filter for "Dim" and "Fact"
  - Confirm 5 dimension tables + 15 fact tables
  - Sample query each table to verify data

---

### Phase 4: OneLake Shortcuts + AI Transformations (10 minutes)

- [ ] **Create OneLake Shortcut:**
  - Lakehouse → New Shortcut → OneLake
  - Source: `Files/unstructured/callcenter_emails/`
  - Destination: Tables folder

- [ ] **Apply AI Transformations:**
  - Select shortcut → AI Transformations
  - Enable:
    - ✅ Sentiment Analysis
    - ✅ Summarization
    - ✅ PII Detection (mask emails/phones)
    - ✅ Named Entity Recognition
  - Name transformed table: `callcenter_emails_transformed`

- [ ] **Verify Transformation:**
  - Query transformed table
  - Check for columns: `sentiment`, `sentiment_score`, `summary`, `detected_pii`, `masked_text`
  - Verify 2,500 rows processed

---

### Phase 5: Power BI Semantic Model (15 minutes)

- [ ] **Create Semantic Model:**
  - Lakehouse → New Semantic Model
  - Name: `Enterprise Analytics Model`
  - Connection: Direct Lake
  - Select all Dim* and Fact* tables

- [ ] **Create Relationships:**
  - Open in Power BI Desktop or Fabric Model View
  - Create relationships:
    - FactSales → DimCustomer (customer_id)
    - FactSales → DimProduct (product_id)
    - FactSales → DimEmployee (employee_id)
    - FactSales → DimDate (order_date_id, ship_date_id, delivery_date_id)
    - [Repeat for all fact tables]
  - Verify all relationships are one-to-many

- [ ] **Import DAX Measures:**
  - Open `fabric/powerbi/dax-measures.md`
  - Copy measures to appropriate tables
  - Minimum required measures:
    - Total Revenue
    - Gross Margin %
    - Revenue YTD
    - CSAT Score
    - Attrition Rate
    - Inventory Turns

- [ ] **Add Metadata (Use Power BI MCP if available):**
  - Add table descriptions
  - Add measure descriptions
  - Add synonyms for key terms
  - Example: DimCustomer → Synonyms: "clients", "accounts", "buyers"

- [ ] **Publish Model:**
  - Save and publish to Fabric workspace
  - Verify model appears in workspace

---

### Phase 6: Fabric Data Agent Configuration (10 minutes)

- [ ] **Create Data Agent:**
  - Workspace → New → Data Agent
  - Name: `Enterprise Insights Agent`
  - Description: "Multi-domain analytics assistant"

- [ ] **Select Data Sources:**
  - [ ] FactSales
  - [ ] FactSupport
  - [ ] FactInventory
  - [ ] FactAttrition
  - [ ] FactIncidents
  - [ ] DimCustomer
  - [ ] DimProduct
  - [ ] DimDate

- [ ] **Add Instructions:**
  - Copy content from `fabric/data-agent/data-agent-setup.md` (Step 3)
  - Paste into Agent Instructions field
  - Customize for your specific demo scenario

- [ ] **Add Verified Answers:**
  - Add 5-10 common questions with pre-defined answers
  - Example: "What was revenue last quarter?" → "$42.3M"

- [ ] **Test Agent:**
  - Ask: "What was revenue last month?"
  - Ask: "Top 10 products by revenue"
  - Ask: "Why did revenue drop in EMEA?"
  - Verify responses are accurate

---

## 🎬 Demo Execution (10-15 minutes)

### Act 1: OneLake - Unified Data Foundation (3 min)

- [ ] Show Lakehouse structure (Bronze → Silver → Gold)
- [ ] Highlight 15 domains in one location
- [ ] Navigate through dimension and fact tables
- [ ] **Key Message:** "Single namespace for all enterprise data"

---

### Act 2: OneLake Shortcuts + AI Transformations (3 min)

- [ ] Show raw email text files
- [ ] Show OneLake Shortcut configuration
- [ ] Query transformed table with sentiment scores
- [ ] Join with structured data (FactSupport)
- [ ] **Key Message:** "Unstructured data becomes insights automatically"

---

### Act 3: Power BI Semantic Model (Direct Lake) (2 min)

- [ ] Open semantic model in Model View
- [ ] Show 15 fact tables + 5 conformed dimensions
- [ ] Highlight Direct Lake badge
- [ ] Show sample DAX measures
- [ ] **Key Message:** "Enterprise BI without data duplication"

---

### Act 4: Fabric Data Agent (4 min)

- [ ] Ask Question 1 (simple): "What was revenue last month?"
- [ ] Ask Question 2 (multi-domain): "Why did revenue drop in EMEA?"
- [ ] Ask Question 3 (unstructured): "Summarize customer complaints by product"
- [ ] Ask Question 4 (HR + Ops): "Attrition hotspots and impact on SLAs"
- [ ] **Key Message:** "Natural language insights across the enterprise"

---

### Act 5: Power BI MCP (Optional, 2 min)

- [ ] Open VS Code with MCP extension
- [ ] Connect to semantic model
- [ ] Demo: "Create all relationships"
- [ ] Demo: "Generate YTD measures for Revenue"
- [ ] **Key Message:** "AI-assisted model development"

---

### Conclusion (1 min)

- [ ] Recap 5 key capabilities
- [ ] Share repository link
- [ ] Offer Q&A
- [ ] Provide next steps (clone repo, customize, deploy)

---

## 📊 Post-Demo

### Immediate Follow-Up

- [ ] Share demo recording (if recorded)
- [ ] Send repository link: [GitHub URL]
- [ ] Share quick start guide: `docs/demo-script.md`
- [ ] Schedule follow-up for questions

### Optional Deep Dive

- [ ] Walk through data generation scripts
- [ ] Explain medallion architecture choices
- [ ] Demo notebook transformations
- [ ] Show RLS/CLS configuration
- [ ] Discuss productionalization (CI/CD, monitoring)

---

## 🛠️ Troubleshooting Quick Reference

### Issue: Data generation fails
- **Check:** Python version (3.9+)
- **Check:** All dependencies installed (`pip install -r requirements.txt`)
- **Check:** Sufficient disk space (~10GB)

### Issue: Notebooks fail in Fabric
- **Check:** Lakehouse is attached to notebook
- **Check:** Source files exist in `Files/bronze/`
- **Check:** Spark pool is running

### Issue: AI Transformations don't appear
- **Check:** Workspace has Premium capacity (F64+)
- **Check:** AI features enabled in workspace settings
- **Check:** Text files are UTF-8 encoded

### Issue: Direct Lake model shows no data
- **Check:** Gold tables are Delta format
- **Check:** Lakehouse connection is valid
- **Check:** Model refresh completed successfully

### Issue: Data Agent gives wrong answers
- **Check:** Metadata (descriptions/synonyms) exists
- **Check:** Instructions are loaded
- **Check:** Verified answers configured
- **Check:** Test queries against semantic model directly

---

## ✅ Final Pre-Demo Checklist

**30 minutes before demo:**

- [ ] Open browser tabs:
  - [ ] Fabric workspace
  - [ ] Lakehouse
  - [ ] Semantic model
  - [ ] Data Agent
  - [ ] (Optional) VS Code with MCP

- [ ] Test all demo flows:
  - [ ] Navigate lakehouse layers
  - [ ] Query transformed text data
  - [ ] Open semantic model
  - [ ] Ask 3-4 agent questions

- [ ] Prepare:
  - [ ] Demo script printed/open
  - [ ] Backup screenshots (if live demo fails)
  - [ ] Repository link ready to share
  - [ ] Q&A talking points ready

- [ ] Technical checks:
  - [ ] Internet connection stable
  - [ ] Screen sharing tested
  - [ ] Audio/video working
  - [ ] Notifications silenced

---

## 🎓 Key Demo Talking Points

### OneLake
> "OneLake eliminates data silos. All 15 domains—from sales to supply chain to HR—in one unified data lake. No ETL sprawl, no data duplication."

### AI Transformations
> "5,000 customer emails turned into query-ready insights automatically. Sentiment analysis, summarization, PII masking—no coding required."

### Direct Lake
> "Enterprise BI performance without copying data. Query Delta tables directly from Power BI. Billions of rows, sub-second response times."

### Data Agent
> "Ask questions in plain English. The agent reasons across domains—connecting sales drops to inventory stockouts to supplier delays. This is the future of analytics."

### Power BI MCP
> "Build semantic models 10x faster. Copilot creates relationships, generates measures, adds metadata. Developer productivity meets enterprise governance."

---

## 🚀 Success Metrics

**Demo is successful if:**

- ✅ Audience understands OneLake value (unified data lake)
- ✅ AI transformations "wow moment" achieved (unstructured → structured)
- ✅ Data Agent answers 3-4 questions correctly
- ✅ At least 2 follow-up meetings scheduled
- ✅ Repository link shared with 5+ attendees

---

**You're ready to deliver an amazing demo! Go show the world the future of enterprise data platforms! 🚀**
