# Agent Development Conventions

## Overview

This document defines conventions for GitHub Copilot Agent interactions when working on the **Full Enterprise Data Platform** demo repository.

---

## 🎯 Project Context

**Goal:** Create a comprehensive Microsoft Fabric demo showcasing:
- 15+ business domains with synthetic data
- Medallion architecture (Bronze → Silver → Gold)
- OneLake Shortcuts + AI Transformations
- Power BI Semantic Model (Direct Lake)
- Fabric Data Agent with natural language queries
- Power BI MCP Server integration in VS Code

**Audience:** Data Engineers, Analytics Engineers, Solution Architects, Business Analysts

---

## 📋 Coding Conventions

### Python

1. **Style Guide:** Follow PEP 8
   - Use `snake_case` for variables, functions, and module names
   - Use `PascalCase` for class names
   - Maximum line length: 120 characters

2. **Imports:** Group and order imports
   ```python
   # Standard library
   import os
   from datetime import datetime
   
   # Third-party
   import pandas as pd
   import numpy as np
   from faker import Faker
   
   # Local modules
   from utils.conformed_dimensions import generate_dim_date
   ```

3. **Documentation:** Use docstrings for all functions
   ```python
   def generate_sales_orders(num_records: int, start_date: str, end_date: str) -> pd.DataFrame:
       """
       Generate synthetic sales orders with realistic patterns.
       
       Args:
           num_records: Number of order records to generate
           start_date: Start of date range (YYYY-MM-DD)
           end_date: End of date range (YYYY-MM-DD)
       
       Returns:
           DataFrame with columns: order_id, customer_id, order_date, total_amount, status
       """
   ```

4. **Error Handling:** Always validate inputs
   ```python
   if num_records <= 0:
       raise ValueError("num_records must be positive")
   ```

5. **Type Hints:** Use type annotations
   ```python
   def calculate_revenue(df: pd.DataFrame, date_column: str = 'order_date') -> float:
   ```

### SQL / DAX

1. **Table Names:** Use `PascalCase` for dimension and fact tables
   - Dimensions: `DimCustomer`, `DimProduct`, `DimDate`
   - Facts: `FactSales`, `FactInventory`, `FactSupport`

2. **Column Names:** Use `snake_case` for column names
   - `customer_id`, `order_date`, `total_amount`

3. **DAX Measures:** Use `PascalCase` with descriptive names
   - `Total Revenue`, `Gross Margin %`, `YTD Sales`

4. **Comments:** Explain business logic
   ```dax
   // Calculate revenue with returns excluded
   Net Revenue = 
   CALCULATE(
       SUM(FactSales[amount]),
       FactSales[status] <> "Returned"
   )
   ```

### YAML Configuration

1. **Structure:** Organize by domain
   ```yaml
   # config.yml
   domains:
     sales:
       orders: 100000
       order_lines_per_order: 2.5
     crm:
       accounts: 50000
       contacts_per_account: 2
   ```

2. **Comments:** Explain non-obvious parameters
   ```yaml
   seed: 42  # Fixed seed for reproducibility across runs
   ```

---

## 📂 File Organization

### Data Generation Scripts

```
data-gen/
├── generate_all.py          # Main orchestrator
├── config.yml               # Central configuration
├── generators/              # Domain-specific generators
│   ├── crm_generator.py
│   └── sales_generator.py
└── utils/                   # Shared utilities
    ├── conformed_dimensions.py
    └── data_quality.py
```

**Convention:** Each domain has its own generator module with a consistent interface:

```python
def generate_domain_data(config: dict, seed: int) -> dict[str, pd.DataFrame]:
    """
    Returns:
        Dictionary of {table_name: dataframe}
    """
```

### Documentation

```
docs/
├── demo-script.md           # Step-by-step demo walkthrough
├── data-catalog.md          # Data dictionary
├── security-and-governance.md
└── shortcuts-and-ai-transforms.md
```

**Convention:** 
- Use Markdown with clear headings
- Include code examples in fenced blocks
- Add diagrams using Mermaid syntax
- Cross-reference other docs with relative links

---

## 🧪 Data Quality Principles

### Synthetic Data Requirements

1. **No Real PII:** Never use actual names, emails, addresses
   - ✅ Use Faker library with seed for consistency
   - ❌ Never scrape real data

2. **Referential Integrity:** All foreign keys must exist
   ```python
   # Validate before saving
   assert all(df_orders['customer_id'].isin(df_customers['customer_id']))
   ```

3. **Realistic Distributions:**
   - Revenue: Log-normal distribution (80/20 rule)
   - Dates: Higher volume in recent periods
   - Categories: Weighted random (not uniform)

4. **Data Volume Balance:**
   - Keep fact tables manageable (<5M rows per table)
   - Dimensions should support realistic cardinality

### Testing

1. **Unit Tests:** Test each generator function
   ```python
   def test_generate_sales_orders_returns_correct_shape():
       df = generate_sales_orders(100, '2023-01-01', '2023-12-31')
       assert len(df) == 100
       assert 'order_id' in df.columns
   ```

2. **Data Quality Checks:** Validate output
   ```python
   # Check for nulls in required fields
   assert df['customer_id'].notna().all()
   
   # Check date ranges
   assert df['order_date'].min() >= pd.to_datetime('2023-01-01')
   ```

---

## 📊 Semantic Model Conventions

### Naming Standards

1. **Tables:**
   - Fact tables: `Fact<DomainName>` (e.g., `FactSales`, `FactSupport`)
   - Dimension tables: `Dim<DimensionName>` (e.g., `DimCustomer`, `DimProduct`)
   - Bridge tables: `Bridge<Name>` (e.g., `BridgeProductCategory`)

2. **Columns:**
   - Primary keys: `<table>_id` (e.g., `customer_id`, `product_id`)
   - Foreign keys: Match dimension primary key name
   - Dates: `<event>_date` (e.g., `order_date`, `ship_date`)
   - Amounts: `<metric>_amount` (e.g., `sales_amount`, `discount_amount`)

3. **Measures:**
   - Base measures: `Total <Metric>` (e.g., `Total Revenue`)
   - Time intelligence: `<Metric> YTD`, `<Metric> QTD`, `<Metric> MoM`
   - Ratios: `<Metric> %` (e.g., `Gross Margin %`)

### AI Readiness

1. **Descriptions:** Add to all tables and columns
   ```
   DimCustomer: "Customer master data including industry classification and geographic location"
   ```

2. **Synonyms:** Support natural language
   ```
   Total Revenue → Synonyms: "sales", "income", "turnover"
   ```

3. **Verified Answers:** Pre-define common queries
   ```
   Q: "What was revenue last quarter?"
   A: "Total Revenue = $42.3M (Q4 2024)"
   ```

---

## 🤖 Data Agent Guidelines

### System Instructions

1. **Scope Definition:** Clearly define which tables to use for which questions
   ```
   For revenue/sales questions → Use FactSales, DimCustomer, DimProduct
   For support/CSAT questions → Use FactSupport, DimCustomer
   ```

2. **Context Limits:** Don't add all tables
   - Maximum 5-7 tables per Data Agent
   - Use multiple agents for distinct domains if needed

3. **Example Responses:** Provide 10+ high-quality examples
   ```
   Q: "Why did revenue drop in EMEA?"
   A: [Expected response format with specific metrics]
   ```

---

## 🔄 Version Control

### Git Conventions

1. **Commits:** Use conventional commit format
   ```
   feat(sales): add order returns table
   fix(hr): correct attrition rate calculation
   docs(readme): update quick start guide
   ```

2. **Branches:** 
   - `main` - stable, working demo
   - `dev` - active development
   - `feature/<name>` - new capabilities

3. **Ignored Files:**
   ```gitignore
   # Generated data
   data-gen/output/
   
   # Python
   __pycache__/
   *.pyc
   .pytest_cache/
   
   # Jupyter
   .ipynb_checkpoints/
   
   # IDEs
   .vscode/
   .idea/
   ```

---

## 📝 Documentation Standards

### Markdown Files

1. **Structure:**
   - Use H1 (`#`) for title
   - Use H2 (`##`) for major sections
   - Use H3 (`###`) for subsections
   - Include table of contents for long docs

2. **Code Blocks:** Always specify language
   ````markdown
   ```python
   import pandas as pd
   ```
   ````

3. **Tables:** Use for structured data
   ```markdown
   | Column | Type | Description |
   |--------|------|-------------|
   | order_id | string | Unique identifier |
   ```

4. **Cross-References:** Use relative links
   ```markdown
   See [demo-script.md](docs/demo-script.md) for walkthrough.
   ```

### Notebooks

1. **Cell Order:**
   - Markdown: Objective and context
   - Code: Imports
   - Code: Configuration
   - Code: Main logic
   - Markdown: Results summary

2. **Comments:** Explain "why" not "what"
   ```python
   # Apply log transformation to handle revenue outliers (top 1% customers)
   df['log_revenue'] = np.log1p(df['revenue'])
   ```

---

## 🎓 Agent Interaction Patterns

### When Asked to Generate Data

1. **Always validate config first:** Check `config.yml` for volumes
2. **Generate conformed dimensions first:** Then domain-specific tables
3. **Validate referential integrity:** Before saving to disk
4. **Show sample output:** First 5 rows + schema

### When Asked to Create Documentation

1. **Follow existing templates:** Match structure of similar docs
2. **Include examples:** Real code snippets, not pseudo-code
3. **Add diagrams:** Use Mermaid for relationships
4. **Cross-reference:** Link to related docs

### When Asked to Modify Code

1. **Explain impact:** What will change and why
2. **Update tests:** If logic changes
3. **Update docs:** If interface changes
4. **Run validation:** Show that output is still valid

---

## ✅ Quality Checklist

Before committing changes:

- [ ] Code follows PEP 8 (run `black` and `flake8`)
- [ ] All functions have docstrings
- [ ] Type hints are present
- [ ] Unit tests pass (`pytest`)
- [ ] Data quality checks pass
- [ ] Documentation updated
- [ ] No hardcoded paths (use relative paths)
- [ ] No credentials or secrets in code
- [ ] Generated data is in `.gitignore`

---

## 🚀 Demo Readiness

The repository should be **demo-ready** at all times:

1. **Quick Start works:** Someone can clone and run in <15 minutes
2. **Documentation is complete:** No "TODO" or placeholder sections
3. **Examples are realistic:** Not "foo/bar" but actual business scenarios
4. **Scripts are idempotent:** Running twice gives same result (with same seed)

---

## 📞 Getting Help

If you're unsure about a convention:

1. Check existing code in `data-gen/generators/` for patterns
2. Review documentation in `docs/` for examples
3. Look at similar domains for consistency

**Principle:** Consistency > Perfection. Follow the established patterns even if you'd do it differently.
