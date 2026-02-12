"""Quality & Security Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_quality_security_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Quality & Security domain: FactQualityTests, FactSecurityEvents"""
    np.random.seed(seed)
    
    quality_config = config.get('quality_security', {})
    num_defects = quality_config.get('defects', {}).get('count', 80000)
    num_events = 1500  # Security events
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    
    print(f"  Generating {num_defects} quality defects and {num_events} security events...")
    
    # Quality Defects
    product_samples = dim_product.sample(n=num_defects, replace=True, random_state=seed)
    defect_dates = dim_date.sample(n=num_defects, replace=True, random_state=seed + 1)
    
    defect_config = quality_config.get('defects', {})
    severity_dist = defect_config.get('severity_distribution', {})
    type_dist = defect_config.get('type_distribution', {})
    
    df_quality = pd.DataFrame({
        'defect_id': [f'DEF-{i+1:08d}' for i in range(num_defects)],
        'product_id': product_samples['product_id'].values,
        'detection_date': defect_dates['date'].values,
        'defect_type': np.random.choice(
            list(type_dist.keys()),
            num_defects,
            p=list(type_dist.values())
        ) if type_dist else np.random.choice(['Cosmetic', 'Functional', 'Safety'], num_defects),
        'severity': np.random.choice(
            list(severity_dist.keys()),
            num_defects,
            p=list(severity_dist.values())
        ) if severity_dist else np.random.choice(['Critical', 'Major', 'Minor'], num_defects),
        'resolved': np.random.random(num_defects) < defect_config.get('resolution_rate', 0.95)
    })
    
    # Security Events
    event_dates = dim_date.sample(n=num_events, replace=True, random_state=seed + 2)
    
    df_security = pd.DataFrame({
        'event_id': [f'SEC-{i+1:08d}' for i in range(num_events)],
        'event_date': event_dates['date'].values,
        'event_type': np.random.choice(['Intrusion Attempt', 'Malware', 'Phishing', 'Policy Violation'], num_events, p=[0.30, 0.25, 0.35, 0.10]),
        'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], num_events, p=[0.50, 0.30, 0.15, 0.05]),
        'resolved': np.random.random(num_events) < 0.95
    })
    
    return {'FactDefects': df_quality, 'FactSecurityEvents': df_security}
