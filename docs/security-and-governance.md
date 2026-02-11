# Security and Governance - Enterprise Data Platform

## 🔒 Overview

Best practices for securing and governing the Microsoft Fabric enterprise data platform, covering data access, compliance, and operational excellence.

**Scope:**
- OneLake security model
- Row-Level Security (RLS)
- Column-Level Security (CLS)
- Workspace separation
- Naming conventions
- Data classification

---

## 🏢 Workspace & Capacity Strategy

### Workspace Separation by Environment

**Production:**
- Workspace: `EnterprisePlatform_PROD`
- Capacity: F64 or higher (dedicated)
- Access: Read-only for most users, Contributor for data engineers

**Development:**
- Workspace: `EnterprisePlatform_DEV`
- Capacity: F64 or shared trial
- Access: Contributors for developers, Admin for leads

**Test/UAT:**
- Workspace: `EnterprisePlatform_TEST`
- Capacity: F64 or shared
- Access: Contributors for QA team

### Workspace Roles

| Role | Permissions | Who |
|------|-------------|-----|
| **Admin** | Full control, workspace settings | Platform team lead |
| **Member** | Create/edit all content | Data engineers, analysts |
| **Contributor** | Create/edit assigned content | Business analysts |
| **Viewer** | Read-only access | Business users, executives |

---

## 🛡️ Data Security Model

### OneLake Security

**Folder-Level Permissions:**
```
/Bronze/
  - Data Engineers: Read/Write
  - Everyone Else: No Access

/Silver/
  - Data Engineers: Read/Write
  - Analysts: Read
  
/Gold/
  - Everyone: Read (filtered by RLS)
```

**Lakehouse-Level Security:**
- Default: No access
- Grant access explicitly per role
- Use Azure AD groups (not individuals)

### Semantic Model Security

**Workspace Access:**
- Controls who can edit model
- Does NOT control data access

**Row-Level Security (RLS):**
- Controls what data users see
- Applied at semantic model level
- Defined in DAX

**Column-Level Security (CLS):**
- Hides specific columns from roles
- Applied in Power BI Desktop
- Cannot be bypassed via DAX

---

## 🔐 Row-Level Security (RLS) Implementation

### Pattern 1: Regional Sales Manager

**Scenario:** Sales managers see only their region's data

**DAX Filter:**
```dax
// Role: Regional_Sales_Manager
// Apply to: DimCustomer

[Region] = USERPRINCIPALNAME()
```

**Better Approach:** Use lookup table
```dax
// Create table: SecurityUserRegion
// Columns: UserEmail, Region

[Region] = 
LOOKUPVALUE(
    SecurityUserRegion[Region],
    SecurityUserRegion[UserEmail], USERPRINCIPALNAME()
)
```

**How to Apply:**
1. Power BI Desktop → Modeling → Manage Roles
2. Create role: `Regional_Sales_Manager`
3. Add filter to `DimCustomer` table
4. Publish model
5. In Fabric workspace → Semantic Model → Security → Add members to role

### Pattern 2: Customer-Specific Access (ISV Scenario)

**Scenario:** Each customer sees only their own data

**DAX Filter:**
```dax
// Role: Customer_A
// Apply to: DimCustomer

[customer_id] = "CUST_000123"
```

**Dynamic Approach:**
```dax
// Table: SecurityUserCustomer
// Columns: UserEmail, customer_id

[customer_id] IN 
VALUES(
    FILTER(
        SecurityUserCustomer,
        SecurityUserCustomer[UserEmail] = USERPRINCIPALNAME()
    )
)
```

### Pattern 3: Department-Based Access

**Scenario:** HR sees all HR data, Finance sees all Finance data

**DAX Filter:**
```dax
// Role: HR_Department
// Apply to: DimEmployee and FactAttrition

USERPRINCIPALNAME() IN {
    "hr.manager@company.com",
    "hr.analyst@company.com"
}
```

**Or use lookup:**
```dax
[department] = 
LOOKUPVALUE(
    SecurityUserDepartment[Department],
    SecurityUserDepartment[UserEmail], USERPRINCIPALNAME()
)
```

### Testing RLS

**In Power BI Desktop:**
- Modeling → View As → Select Role
- Verify correct data appears

**In Fabric:**
- Semantic Model → Security → Test as user
- Enter test user email
- Browse report to verify filtering

---

## 🚫 Column-Level Security (CLS)

### Sensitive Columns to Protect

| Table | Column | Reason |
|-------|--------|--------|
| DimEmployee | salary_band | Compensation data |
| DimCustomer | credit_limit | Financial data |
| FactSupport | customer_email | PII |
| FactSales | employee_id | Sales attribution (competitive) |

### Implementation

**Power BI Desktop:**
1. Select column in Fields pane
2. Column Tools → Advanced → Object-level security
3. Check "Hide from specific roles"
4. Select roles to hide from

**Example Roles:**
- `HR_Full_Access` - Sees all employee data including salary_band
- `HR_Limited` - Sees employee data BUT NOT salary_band
- `Business_Users` - No access to any salary data

---

## 📊 Data Classification

### Sensitivity Labels

| Label | Description | Examples |
|-------|-------------|----------|
| **Public** | No restrictions | Aggregated KPIs, public reports |
| **Internal** | Company employees only | Department reports, non-PII data |
| **Confidential** | Need-to-know basis | Customer details, financial actuals |
| **Highly Confidential** | Executive/legal only | Acquisition plans, salaries |

### Apply Labels in Fabric

**Workspace Level:**
- Workspace Settings → Information Protection
- Set default label for all new content

**Artifact Level:**
- Each semantic model, report, lakehouse can have its own label
- Inherit from workspace or override

### Automatic Labeling

**Microsoft Purview:**
- Scan OneLake for PII
- Auto-apply labels based on content
- Example: Email column detected → Label as "Confidential"

---

## 🏷️ Naming Conventions

### Tables

**Dimensions:**
- Prefix: `Dim`
- PascalCase: `DimCustomer`, `DimProduct`

**Facts:**
- Prefix: `Fact`
- PascalCase: `FactSales`, `FactSupport`

**Bridge Tables:**
- Prefix: `Bridge`
- Example: `BridgeProductCategory`

**Staging:**
- Prefix: `stg_` or `Silver_`
- Example: `Silver_DimCustomer`

### Columns

**Standard Format:**
- snake_case: `customer_id`, `order_date`, `total_amount`

**Primary Keys:**
- `<table>_id`: `customer_id`, `product_id`

**Foreign Keys:**
- Match dimension PK name: `customer_id` (in FactSales) → `customer_id` (in DimCustomer)

**Dates:**
- `<event>_date`: `order_date`, `ship_date`
- For surrogate keys: `<event>_date_id`: `order_date_id`

**Flags:**
- `is_<condition>`: `is_active`, `is_weekend`

### Measures (DAX)

**Base Measures:**
- `Total <Metric>`: `Total Revenue`, `Total Orders`

**Time Intelligence:**
- `<Metric> YTD`: `Revenue YTD`
- `<Metric> PY`: `Revenue PY`
- `<Metric> YoY %`: `Revenue YoY %`

**Ratios:**
- `<Metric> %`: `Gross Margin %`, `Attrition Rate`

---

## 👥 User Management

### Azure AD Groups

**Create Groups:**
```
Data_Engineers
Business_Analysts_Sales
Business_Analysts_HR
Executive_Readers
Finance_Team
```

**Assign to Workspaces:**
- Use groups (not individuals)
- Easier to manage at scale
- Audit trail in Azure AD

**Assign to RLS Roles:**
- Map Azure AD groups to semantic model roles
- Example: `Business_Analysts_Sales` → `Regional_Sales_Manager` role

### Service Principal Access

**For Automation:**
- Create Service Principal in Azure AD
- Grant Contributor/Admin to workspace
- Use for CI/CD pipelines
- Never use personal accounts for automation

---

## 🔍 Monitoring & Auditing

### What to Monitor

**Usage Analytics:**
- Who is accessing which semantic models/reports?
- Which queries are slow?
- Are there any suspicious access patterns?

**Data Refreshes:**
- Are scheduled refreshes succeeding?
- How long do they take?
- Any errors or warnings?

**Capacity Metrics:**
- CPU usage
- Memory pressure
- Throttling events

### Audit Logs

**Fabric Audit Events:**
- Workspace access
- Artifact creation/deletion
- Model refreshes
- Query executions

**Access via:**
- Microsoft Purview Compliance Portal
- Power BI Admin Portal → Audit Logs
- Azure Log Analytics (for long-term retention)

**Key Events to Track:**
- `ViewReport` - Who viewed what
- `ExportReport` - Data exports (potential leakage)
- `UpdateDatasources` - Connection string changes
- `TakeOverDataset` - Ownership changes

---

## 📋 Compliance Checklist

### GDPR Compliance

- [ ] **Data Inventory:** Document all PII in data catalog
- [ ] **Consent Tracking:** Log user consent for data processing
- [ ] **Right to Access:** Enable users to request their data
- [ ] **Right to Erasure:** Process for deleting user data
- [ ] **Data Minimization:** Only collect necessary data
- [ ] **Encryption:** At-rest (OneLake) and in-transit (HTTPS)

### SOX Compliance (Financial Data)

- [ ] **Access Controls:** Segregation of duties (no one user has full control)
- [ ] **Audit Trail:** Log all changes to financial data
- [ ] **Change Management:** Approval process for prod changes
- [ ] **Data Integrity:** Validation checks, referential integrity
- [ ] **Archival:** Retain data for required period (7 years)

### HIPAA Compliance (Healthcare Data)

- [ ] **Encryption:** PHI encrypted at rest and in transit
- [ ] **Access Controls:** Role-based access, MFA required
- [ ] **Audit Logging:** All PHI access logged
- [ ] **Business Associate Agreement:** With Microsoft
- [ ] **Data Residency:** Ensure data stays in required region

---

## 🚨 Incident Response

### Data Breach Procedure

1. **Detect:** Monitor audit logs, user reports
2. **Contain:** Revoke access immediately
3. **Assess:** Determine scope (what data, who accessed)
4. **Notify:** Legal, compliance, affected users (within 72 hours for GDPR)
5. **Remediate:** Patch security gap
6. **Document:** Root cause analysis

### Access Revocation

**When employee leaves:**
1. Remove from all Azure AD groups
2. Check workspace access (should auto-revoke via group)
3. Audit: Did they export any data before leaving?
4. Consider: Rotating shared credentials/API keys

**Emergency Access Removal:**
```powershell
# PowerShell: Remove user from Fabric workspace
Remove-PowerBIWorkspaceUser -Scope Organization -WorkspaceId <ID> -UserPrincipalName user@company.com
```

---

## 🎓 Training & Awareness

### Security Training for Users

**Topics:**
- Don't share workspace links publicly
- Don't export sensitive data to personal devices
- Report suspicious activity
- Understand your RLS role (what you can/can't see)

**Frequency:**
- New hire onboarding
- Annual refresher
- After any security incident

### Platform Team Training

**Topics:**
- RLS/CLS implementation
- PII detection and handling
- Audit log analysis
- Incident response procedures

---

## 📝 Governance Documentation

### Required Documentation

1. **Data Catalog** ✅
   - All tables, columns, relationships
   - Sensitivity classification
   - Owner and steward contacts

2. **Access Control Matrix**
   - Who has access to what
   - RLS role definitions
   - Justification for access

3. **Data Lineage**
   - Source → Bronze → Silver → Gold
   - Transformation logic
   - Data quality rules

4. **Runbooks**
   - How to grant/revoke access
   - How to add new data source
   - Incident response procedures

---

## ✅ Pre-Production Checklist

Before going live:

- [ ] All PII identified and protected (RLS/CLS)
- [ ] Sensitivity labels applied
- [ ] RLS tested with representative users
- [ ] Audit logging enabled
- [ ] Service principal created for automation
- [ ] User groups created in Azure AD
- [ ] Runbooks documented
- [ ] Security training completed
- [ ] Data retention policy defined
- [ ] Backup/disaster recovery tested

---

## 📞 Security Contacts

**Security Incidents:**
- Email: security@company.com
- Teams: Security Response Team

**Compliance Questions:**
- Email: compliance@company.com
- Lead: [Compliance Officer Name]

**Platform Support:**
- Teams: #fabric-platform-support
- Lead: [Platform Team Lead]

---

**This governance framework ensures your enterprise data platform is secure, compliant, and audit-ready! 🔒**
