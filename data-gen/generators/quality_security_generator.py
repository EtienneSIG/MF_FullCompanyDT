"""Quality & Security Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_quality_security_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Quality & Security domain: FactQualityTests, FactSecurityEvents"""
    np.random.seed(seed)
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    
    num_tests = 2000
    num_events = 1000
    
    print(f"  Generating {num_tests} quality tests and {num_events} security events...")
    
    # Quality Tests
    product_samples = dim_product.sample(n=num_tests, replace=True, random_state=seed)
    test_dates = dim_date.sample(n=num_tests, replace=True, random_state=seed + 1)
    
    df_quality = pd.DataFrame({
        'test_id': [f'QT-{i+1:08d}' for i in range(num_tests)],
        'product_id': product_samples['product_id'].values,
        'test_date': test_dates['date'].values,
        'test_type': np.random.choice(['Functional', 'Performance', 'Safety', 'Reliability'], num_tests),
        'result': np.random.choice(['Pass', 'Fail'], num_tests, p=[0.92, 0.08]),
        'defects_found': np.random.poisson(0.5, num_tests)
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
    
    return {'FactQualityTests': df_quality, 'FactSecurityEvents': df_security}
