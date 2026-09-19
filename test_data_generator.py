"""
UnifiedTrace - Test Data Generator
Generates realistic CDR, bank transaction, and APK metadata for demo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import hashlib
import json

def generate_cdr_data(num_records=500):
    """Generate Call Detail Records (CDR) data"""
    operators = ['Airtel', 'Vodafone', 'Jio', 'BSNL']
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata']
    
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    # Create some suspicious patterns
    mule_imeis = [f'IMEI_{i}' for i in range(1, 6)]
    victim_imeis = [f'IMEI_V{i}' for i in range(1, 4)]
    
    for i in range(num_records):
        is_mule = random.random() < 0.3
        imei = random.choice(mule_imeis) if is_mule else random.choice(victim_imeis)
        
        data.append({
            'CDR_ID': f'CDR_{i:06d}',
            'IMEI': imei,
            'Phone_Number': f'98{random.randint(10000000, 99999999)}',
            'Operator': random.choice(operators),
            'Location': random.choice(locations),
            'Timestamp': base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 24)),
            'Call_Duration': random.randint(10, 3600),
            'Data_Used_MB': random.randint(0, 500),
            'IP_Address': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        })
    
    return pd.DataFrame(data)

def generate_bank_data(num_records=400):
    """Generate bank transaction data"""
    transaction_types = ['CREDIT', 'DEBIT', 'TRANSFER']
    
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    # Create suspicious UPI handles and mule accounts
    mule_upi = [f'mule.{i}@okhdfcbank' for i in range(1, 6)]
    victim_upi = ['victim.sharma@okaxis', 'victim.patel@okidfcbank']
    
    for i in range(num_records):
        is_suspicious = random.random() < 0.25
        upi = random.choice(mule_upi) if is_suspicious else random.choice(victim_upi)
        
        data.append({
            'Transaction_ID': f'TXN_{i:06d}',
            'UPI_Handle': upi,
            'Amount': random.randint(100, 50000),
            'Transaction_Type': random.choice(transaction_types),
            'Timestamp': base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 24)),
            'Recipient_UPI': random.choice(mule_upi + victim_upi),
            'Bank_Name': random.choice(['HDFC', 'ICICI', 'Axis', 'SBI', 'Kotak']),
            'Device_IP': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        })
    
    return pd.DataFrame(data)

def generate_apk_data(num_records=150):
    """Generate APK metadata"""
    data = []
    
    suspicious_packages = ['com.fakebank.app', 'org.malware.trojan', 'com.spyware.rat']
    normal_packages = ['com.whatsapp', 'com.instagram', 'com.twitter', 'com.uber']
    
    for i in range(num_records):
        is_suspicious = random.random() < 0.2
        package = random.choice(suspicious_packages) if is_suspicious else random.choice(normal_packages)
        
        # Generate fake SHA-256 hash
        hash_input = f"{package}_{i}_{datetime.now()}"
        file_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        data.append({
            'APK_ID': f'APK_{i:06d}',
            'Package_Name': package,
            'SHA256_Hash': file_hash,
            'File_Size_MB': random.uniform(5, 200),
            'Install_Date': (datetime.now() - timedelta(days=random.randint(0, 365))).date(),
            'Permissions_Count': random.randint(5, 50),
            'Is_Suspicious': is_suspicious,
            'IMEI': f'IMEI_{random.randint(1, 6)}' if is_suspicious else f'IMEI_V{random.randint(1, 4)}'
        })
    
    return pd.DataFrame(data)

def generate_test_datasets():
    """Generate all test datasets"""
    cdr_df = generate_cdr_data()
    bank_df = generate_bank_data()
    apk_df = generate_apk_data()
    
    # Save to CSV
    cdr_df.to_csv('sample_cdr.csv', index=False)
    bank_df.to_csv('sample_bank.csv', index=False)
    apk_df.to_csv('sample_apk.csv', index=False)
    
    print("✅ Test datasets generated:")
    print(f"   - CDR: {len(cdr_df)} records")
    print(f"   - Bank: {len(bank_df)} records")
    print(f"   - APK: {len(apk_df)} records")
    
    return cdr_df, bank_df, apk_df

if __name__ == '__main__':
    generate_test_datasets()
