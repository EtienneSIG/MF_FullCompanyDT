"""Risk & Compliance Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_risk_compliance_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Risk & Compliance domain: FactRisks, FactAudits, FactComplianceChecks"""
    np.random.seed(seed)
    
    risk_config = config.get('risk_compliance', {})
    num_risks = risk_config.get('incidents', {}).get('count', 200)
    num_audits = 150  # Roughly half of controls as audits
    num_checks = risk_config.get('controls', {}).get('count', 150) * 12  # Monthly checks
    
    dim_date = dimensions['DimDate']
    dim_employee = dimensions['DimEmployee']
    
    print(f"  Generating {num_risks} risks, {num_audits} audits, {num_checks} compliance checks...")
    
    # FactRisks
    risk_dates = dim_date.sample(n=num_risks, replace=True, random_state=seed)
    risk_owners = dim_employee.sample(n=num_risks, replace=True, random_state=seed + 1)
    
    risk_categories = np.random.choice(
        ['Operational', 'Financial', 'Strategic', 'Compliance', 'Cybersecurity'],
        num_risks,
        p=[0.25, 0.20, 0.15, 0.25, 0.15]
    )
    
    risk_impacts = np.random.choice(['Low', 'Medium', 'High', 'Critical'], num_risks, p=[0.30, 0.40, 0.25, 0.05])
    risk_likelihoods = np.random.choice(['Rare', 'Unlikely', 'Possible', 'Likely', 'Almost Certain'], num_risks, p=[0.15, 0.25, 0.35, 0.20, 0.05])
    
    df_risks = pd.DataFrame({
        'risk_id': [f'RISK-{i+1:06d}' for i in range(num_risks)],
        'risk_date': risk_dates['date'].values,
        'risk_category': risk_categories,
        'impact': risk_impacts,
        'likelihood': risk_likelihoods,
        'risk_score': np.random.randint(1, 101, num_risks),
        'status': np.random.choice(['Open', 'Mitigated', 'Closed'], num_risks, p=[0.40, 0.35, 0.25]),
        'owner_id': risk_owners['employee_id'].values
    })
    
    # FactAudits
    audit_dates = dim_date.sample(n=num_audits, replace=True, random_state=seed + 2)
    auditors = dim_employee.sample(n=num_audits, replace=True, random_state=seed + 3)
    
    audit_types = np.random.choice(
        ['Internal', 'External', 'Regulatory', 'IT'],
        num_audits,
        p=[0.45, 0.25, 0.20, 0.10]
    )
    
    df_audits = pd.DataFrame({
        'audit_id': [f'AUDIT-{i+1:06d}' for i in range(num_audits)],
        'audit_date': audit_dates['date'].values,
        'audit_type': audit_types,
        'auditor_id': auditors['employee_id'].values,
        'findings_count': np.random.poisson(5, num_audits),
        'critical_findings': np.random.poisson(0.5, num_audits),
        'status': np.random.choice(['Planned', 'In Progress', 'Complete'], num_audits, p=[0.20, 0.30, 0.50])
    })
    
    # FactComplianceChecks
    check_dates = dim_date.sample(n=num_checks, replace=True, random_state=seed + 4)
    
    frameworks = np.random.choice(
        ['SOX', 'GDPR', 'HIPAA', 'ISO 27001', 'PCI DSS'],
        num_checks,
        p=[0.25, 0.25, 0.15, 0.20, 0.15]
    )
    
    df_checks = pd.DataFrame({
        'check_id': [f'CHK-{i+1:08d}' for i in range(num_checks)],
        'check_date': check_dates['date'].values,
        'framework': frameworks,
        'control_id': [f'CTRL-{np.random.randint(1, 501):04d}' for _ in range(num_checks)],
        'result': np.random.choice(['Pass', 'Fail'], num_checks, p=[0.92, 0.08]),
        'automated': np.random.random(num_checks) < 0.70
    })
    
    return {
        'FactRisks': df_risks,
        'FactAudits': df_audits,
        'FactComplianceChecks': df_checks
    }

