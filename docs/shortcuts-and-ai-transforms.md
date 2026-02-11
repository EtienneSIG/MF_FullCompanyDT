# OneLake Shortcuts & AI Transformations

## 🔗 Overview

This guide covers two powerful Microsoft Fabric features:
1. **OneLake Shortcuts** - Link data from external sources without copying
2. **AI Transformations** - Apply GPT-4 to unstructured data for enrichment

Together, these capabilities enable a modern, AI-enhanced data lakehouse architecture.

---

## 📂 OneLake Shortcuts

### What Are Shortcuts?

**Definition:**
- Symbolic links to data stored in external locations
- Appear as folders in OneLake but don't copy data
- Support: Azure Data Lake Storage Gen2, AWS S3, Google Cloud Storage, other OneLake locations

**Benefits:**
- **Zero Data Movement:** No ETL required, data stays in source
- **Always Fresh:** Read directly from source (no sync lag)
- **Cost Savings:** No duplicate storage costs
- **Unified Namespace:** Access heterogeneous data via OneLake paths

**Use Cases:**
1. Legacy data lakes (ADLS Gen2) → Keep in place, query via Fabric
2. Partner data (AWS S3) → Analyze without cross-cloud data transfer
3. Shared enterprise data → Multiple workspaces access same Gold layer
4. Multi-region data → EU workspace shortcuts to US data lake

---

## 🛠️ Creating Shortcuts

### Shortcut to Azure Data Lake Storage Gen2

**Prerequisites:**
- ADLS Gen2 account with hierarchical namespace enabled
- Service Principal or Managed Identity with Storage Blob Data Reader role
- Firewall: Allow Fabric IP ranges

**Steps:**

1. **In Fabric Lakehouse:**
   - Open Lakehouse explorer
   - Navigate to desired folder (e.g., `Bronze/External/`)
   - Click `New shortcut`

2. **Select Source:**
   - Choose `Azure Data Lake Storage Gen2`
   - Enter:
     - **URL:** `https://<storage_account>.dfs.core.windows.net/<container>/<path>`
     - **Connection:** Create new or use existing
     - **Authentication:** Service Principal or Account Key

3. **Configure Connection:**
   - **Service Principal:**
     - Tenant ID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
     - Client ID: `yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy`
     - Client Secret: `<your_secret>`
   - **Or Account Key:**
     - Storage Account Key: `<key_from_azure_portal>`

4. **Select Folder:**
   - Browse ADLS Gen2 hierarchy
   - Select folder to link (e.g., `/raw/sales/`)

5. **Name Shortcut:**
   - Default: Uses folder name
   - Custom: `ADLS_Sales_Archive`

6. **Validate:**
   - Refresh Lakehouse explorer
   - Shortcut appears as folder with link icon
   - Browse contents (should match source)

### Shortcut to AWS S3

**Prerequisites:**
- S3 bucket with appropriate IAM policy
- AWS Access Key ID and Secret Access Key

**Steps:**

1. **Lakehouse → New Shortcut → Amazon S3**

2. **Enter Details:**
   - **URL:** `https://s3.amazonaws.com/<bucket_name>/<prefix>`
   - **Or:** `s3://<bucket_name>/<prefix>`

3. **Authentication:**
   - Access Key ID: `AKIAIOSFODNN7EXAMPLE`
   - Secret Access Key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

4. **Region:** `us-east-1` (or your bucket's region)

5. **Validate & Create**

### Shortcut to Another OneLake Location

**Scenario:** Share Gold layer across workspaces

**Steps:**

1. **Lakehouse → New Shortcut → OneLake**

2. **Select Source:**
   - Workspace: `EnterprisePlatform_PROD`
   - Lakehouse: `EnterpriseLakehouse`
   - Path: `Files/Gold/`

3. **Name:** `Shared_Gold_Layer`

4. **Use Case:**
   - Multiple departmental workspaces can read from shared Gold layer
   - No data duplication
   - Governance applied at source (RLS in semantic model still applies)

---

## 📊 Shortcut Patterns for This Demo

### Pattern 1: Legacy Data Lake Integration

**Scenario:** Company has 5 years of sales data in ADLS Gen2

**Implementation:**
```
EnterpriseLakehouse/
  Bronze/
    Sales_Current/         # New data ingested via Fabric pipeline
    Sales_Archive/         # SHORTCUT → ADLS Gen2 (2019-2023 data)
```

**Notebook Code:**
```python
# Read current + archive as single dataset
df_current = spark.read.format("delta").load("Files/Bronze/Sales_Current/")
df_archive = spark.read.format("parquet").load("Files/Bronze/Sales_Archive/")  # Via shortcut

df_all = df_current.unionByName(df_archive)
```

### Pattern 2: Multi-Region Data Access

**Scenario:** US workspace needs to analyze EU customer data (GDPR: data must stay in EU)

**Implementation:**
```
US_Workspace/Lakehouse/
  Bronze/
    Customers_US/          # Local data
    Customers_EU/          # SHORTCUT → EU OneLake location
```

**Benefits:**
- EU data never leaves EU region (compliance)
- US analysts can still query via shortcut
- Centralized governance in EU workspace

### Pattern 3: Partner Data Sharing

**Scenario:** Supplier shares inventory data via AWS S3

**Implementation:**
```
EnterpriseLakehouse/
  Bronze/
    Supplier_Inventory/    # SHORTCUT → Supplier's S3 bucket
```

**Transformation:**
```python
# Read via shortcut, transform, write to Silver
df = spark.read.format("csv").option("header", True).load("Files/Bronze/Supplier_Inventory/")

df_silver = df.select(
    col("sku").alias("product_sku"),
    col("qty").cast("int").alias("available_qty"),
    current_timestamp().alias("snapshot_time")
)

df_silver.write.format("delta").mode("overwrite").save("Tables/Silver_SupplierInventory")
```

---

## 🤖 AI Transformations

### What Are AI Transformations?

**Definition:**
- Use Azure OpenAI (GPT-4) to process unstructured data
- Available in Fabric notebooks via `SynapseML` library
- Examples: Sentiment analysis, entity extraction, summarization, classification

**Architecture:**
```
Unstructured Data → SynapseML → Azure OpenAI → Enriched Data → Delta Table
```

**Use Cases:**
1. **Support Tickets:** Extract issue category, sentiment, priority
2. **Customer Reviews:** Sentiment + key themes
3. **Emails:** Classify intent (sales, support, billing)
4. **Documents:** Summarize meeting notes, contracts

---

## 🧪 AI Transformation Examples

### Example 1: Support Ticket Classification

**Input Data:**
- `ticket_id`: T001
- `description`: "I can't log in to the portal. Getting error 500."

**Desired Output:**
- `category`: "Authentication"
- `sentiment`: "Frustrated"
- `priority`: "High"

**Notebook Code:**

```python
from synapse.ml.services import OpenAICompletion
from pyspark.sql.functions import col

# Read Bronze data
df_tickets = spark.read.format("delta").load("Tables/Bronze_SupportTickets")

# Configure Azure OpenAI
openai_service = (
    OpenAICompletion()
    .setDeploymentName("gpt-4")  # Your deployment name
    .setCustomServiceName("<your-openai-service>.openai.azure.com")
    .setApiKey("<your-api-key>")
    .setTemperature(0.0)  # Deterministic
    .setMaxTokens(100)
    .setPromptCol("prompt")
    .setOutputCol("ai_response")
)

# Create prompts
df_with_prompt = df_tickets.withColumn(
    "prompt",
    concat(
        lit("Classify this support ticket:\n\n"),
        col("description"),
        lit("\n\nProvide: Category (Technical/Billing/Account), Sentiment (Positive/Neutral/Negative), Priority (Low/Medium/High)\nFormat: Category|Sentiment|Priority")
    )
)

# Apply AI transformation
df_enriched = openai_service.transform(df_with_prompt)

# Parse AI response
from pyspark.sql.functions import split

df_final = df_enriched.withColumn("parts", split(col("ai_response"), "\\|")) \
    .withColumn("category", col("parts")[0]) \
    .withColumn("sentiment", col("parts")[1]) \
    .withColumn("priority", col("parts")[2]) \
    .select("ticket_id", "description", "category", "sentiment", "priority")

# Write to Silver
df_final.write.format("delta").mode("overwrite").save("Tables/Silver_SupportTicketsEnriched")
```

**Output:**
| ticket_id | description | category | sentiment | priority |
|-----------|-------------|----------|-----------|----------|
| T001 | I can't log in... | Technical | Negative | High |

### Example 2: Product Review Sentiment

**Input:**
- `review_id`: R001
- `review_text`: "This product is amazing! Best purchase ever."

**Output:**
- `sentiment_score`: 0.95 (very positive)
- `key_themes`: ["quality", "satisfaction"]

**Code:**

```python
from synapse.ml.services import AnalyzeText

# Use Azure AI Language service for sentiment
sentiment_analyzer = (
    AnalyzeText()
    .setKind("SentimentAnalysis")
    .setLocation("eastus")  # Your Azure AI Language region
    .setSubscriptionKey("<your-key>")
    .setTextCol("review_text")
    .setOutputCol("sentiment")
)

df_reviews = spark.read.format("delta").load("Tables/Bronze_ProductReviews")
df_sentiment = sentiment_analyzer.transform(df_reviews)

# Extract sentiment score
df_final = df_sentiment.withColumn(
    "sentiment_score", 
    col("sentiment.documents.confidenceScores.positive")
).select("review_id", "review_text", "sentiment_score")

df_final.write.format("delta").mode("overwrite").save("Tables/Silver_ReviewsSentiment")
```

### Example 3: Email Intent Classification

**Input:**
- `email_body`: "I'd like to schedule a demo of your product."

**Output:**
- `intent`: "Sales"
- `action_required`: "Schedule Demo"

**Prompt Engineering:**

```python
prompt_template = """
You are an email classifier for a B2B company.

Email: {email_body}

Classify the intent:
- Sales: Product inquiry, demo request, pricing
- Support: Technical issue, bug report
- Billing: Invoice question, payment issue
- General: Other

Output format: Intent|Action Required

Example:
Email: "I need help with login"
Output: Support|Troubleshoot Login
"""

df_emails.withColumn(
    "prompt",
    expr(f"format_string('{prompt_template}', email_body)")
)
```

---

## 🎯 Demo Implementation: Unstructured Data

### Scenario

**Data Sources:**
1. Support tickets (text)
2. Customer emails (text)
3. Call center transcripts (text)
4. Product reviews (text)

**Goal:** Enrich with AI to enable analytics

### Folder Structure

```
EnterpriseLakehouse/
  Files/
    Bronze/
      Unstructured/
        SupportTickets/     # JSON files with ticket descriptions
        Emails/             # Email text files
        CallTranscripts/    # Audio → text transcripts
        ProductReviews/     # Scraped from website
```

### Transformation Pipeline

**Notebook: `05_ai_enrichment.ipynb`**

```python
# ==========================================
# AI Enrichment: Support Tickets
# ==========================================

from synapse.ml.services import OpenAICompletion
from pyspark.sql.functions import *

# 1. Load unstructured data
df_tickets = spark.read.format("json").load("Files/Bronze/Unstructured/SupportTickets/")

# 2. Create classification prompt
classification_prompt = """
Classify this support ticket into one of these categories:
- Login/Authentication
- Performance/Errors
- Billing/Payments
- Feature Request
- Data Issue

Also determine:
- Sentiment: Positive/Neutral/Negative
- Urgency: Low/Medium/High

Ticket: {description}

Output format: Category|Sentiment|Urgency
"""

df_with_prompt = df_tickets.withColumn(
    "prompt",
    format_string(classification_prompt, col("description"))
)

# 3. Apply GPT-4
openai = (
    OpenAICompletion()
    .setDeploymentName("gpt-4")
    .setCustomServiceName("your-openai.openai.azure.com")
    .setApiKey(dbutils.secrets.get("keyvault", "openai-key"))  # Use Key Vault
    .setTemperature(0.0)
    .setMaxTokens(50)
    .setPromptCol("prompt")
    .setOutputCol("classification")
)

df_classified = openai.transform(df_with_prompt)

# 4. Parse results
df_enriched = df_classified \
    .withColumn("parts", split(col("classification"), "\\|")) \
    .withColumn("category", trim(col("parts")[0])) \
    .withColumn("sentiment", trim(col("parts")[1])) \
    .withColumn("urgency", trim(col("parts")[2])) \
    .select("ticket_id", "customer_id", "description", "category", "sentiment", "urgency", "created_at")

# 5. Write to Silver
df_enriched.write.format("delta").mode("overwrite").save("Tables/Silver_SupportTicketsEnriched")

print(f"✅ Enriched {df_enriched.count()} support tickets with AI classification")
```

### Cost Optimization

**Batch Processing:**
- Process in batches of 100-1,000 records
- Use caching to avoid re-processing

**Smart Sampling:**
```python
# Only classify new tickets
df_new = df_tickets.join(
    df_existing_classified, 
    on="ticket_id", 
    how="left_anti"
)
```

**Temperature Control:**
- Use `temperature=0.0` for classification (deterministic)
- Use `temperature=0.7` for creative tasks (summarization)

**Token Limits:**
- `max_tokens=50` for short classifications
- `max_tokens=200` for summaries

---

## 📐 Architecture Patterns

### Pattern 1: Shortcut + AI Enrichment

```
External S3 Bucket (Partner Reviews)
        ↓ [Shortcut]
    Bronze/PartnerReviews/
        ↓ [AI Sentiment]
    Silver/ReviewsEnriched/
        ↓ [Aggregation]
    Gold/ReviewSummary/
        ↓
    Power BI (Sentiment Trends)
```

### Pattern 2: Multi-Source Unstructured

```
Support Tickets (JSON) ──┐
Customer Emails (TXT) ───┤
Call Transcripts (TXT) ──┼─→ AI Classification ─→ Silver/AllFeedbackEnriched/ ─→ Semantic Model
Social Media (JSON) ─────┘
```

### Pattern 3: Incremental AI Processing

```sql
-- Only process new data
CREATE OR REPLACE TABLE Silver_EmailsClassified AS
SELECT 
    e.*,
    ai_classify(e.body) AS intent
FROM Bronze_Emails e
LEFT JOIN Silver_EmailsClassified existing ON e.email_id = existing.email_id
WHERE existing.email_id IS NULL
```

---

## 🧰 SynapseML AI Services

### Available Services

| Service | Use Case | Example |
|---------|----------|---------|
| **OpenAICompletion** | Text classification, generation | Ticket categorization |
| **OpenAIEmbedding** | Semantic search, clustering | Find similar support tickets |
| **AnalyzeText** | Sentiment, key phrases, entities | Review sentiment |
| **Translator** | Multi-language support | Translate tickets to English |
| **FormRecognizer** | Extract data from PDFs/images | Invoice processing |
| **ComputerVision** | Image analysis | Product photo tagging |

### Quick Reference: OpenAICompletion

```python
from synapse.ml.services import OpenAICompletion

openai = (
    OpenAICompletion()
    .setDeploymentName("gpt-4")                  # Required
    .setCustomServiceName("your-service.openai.azure.com")  # Required
    .setApiKey("<key>")                           # Required
    .setTemperature(0.0)                          # 0=deterministic, 1=creative
    .setMaxTokens(100)                            # Response length limit
    .setTopP(1.0)                                 # Nucleus sampling
    .setPromptCol("prompt")                       # Input column name
    .setOutputCol("response")                     # Output column name
)

df_result = openai.transform(df_input)
```

---

## 🔐 Security for AI Services

### Azure OpenAI Best Practices

1. **Store Keys in Key Vault:**
```python
api_key = dbutils.secrets.get("keyvault", "openai-key")
```

2. **Use Managed Identity:**
```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
# Configure OpenAI client with credential
```

3. **Network Security:**
   - Enable private endpoint for Azure OpenAI
   - Restrict Fabric workspace to access via VNet

4. **Content Filtering:**
   - Azure OpenAI has built-in content filters
   - Review logs for harmful content attempts

---

## 📊 Monitoring AI Costs

**Azure OpenAI Billing:**
- Charged per 1,000 tokens (input + output)
- GPT-4: ~$0.03/1K input tokens, ~$0.06/1K output tokens
- GPT-3.5-Turbo: ~$0.002/1K tokens (10x cheaper)

**Example Cost:**
- 10,000 support tickets
- Average 100 tokens input + 50 tokens output = 150 tokens per ticket
- Total: 10,000 * 150 / 1,000 = 1,500K tokens
- Cost: 1,500 * $0.03 = **$45** (GPT-4) or **$3** (GPT-3.5)

**Optimization:**
- Use GPT-3.5-Turbo for simple classification
- Reserve GPT-4 for complex reasoning

---

## ✅ Demo Checklist: Shortcuts & AI

**Shortcuts:**
- [ ] Create ADLS Gen2 shortcut to mock "legacy data lake"
- [ ] Demonstrate reading shortcut data in notebook
- [ ] Show shortcut in OneLake explorer (link icon)

**AI Transformations:**
- [ ] Load sample unstructured data (5-10 support tickets)
- [ ] Run AI classification notebook
- [ ] Show enriched Silver table with categories
- [ ] Visualize sentiment distribution in Power BI

**Talking Points:**
- "No data movement with shortcuts - query in place"
- "AI transforms unstructured text into analytics-ready data"
- "Same GPT-4 model powering ChatGPT, now in your data pipeline"

---

**This completes the Shortcuts & AI Transformations guide! 🚀**
