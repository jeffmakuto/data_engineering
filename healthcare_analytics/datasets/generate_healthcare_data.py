#!/usr/bin/env python3
"""
Healthcare Data Generator
Creates realistic clinic attendance, ailments, and medication supply datasets
for a 6-month period across multiple clinics in a county.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_clinic_attendance():
    """Generate clinic attendance data for 6 months."""
    print("Generating clinic attendance data...")
    
    clinics = [
        'Central County Hospital',
        'Eastside Health Center',
        'Westgate Clinic',
        'Northview Medical Center',
        'Southside Community Clinic',
        'Rural Health Post A',
        'Rural Health Post B',
        'Urban Primary Care',
        'Community Wellness Center',
        'District Referral Hospital'
    ]
    
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 11, 30)
    
    records = []
    patient_id = 10000
    
    for single_date in pd.date_range(start_date, end_date):
        day_of_week = single_date.weekday()
        month = single_date.month
        
        for clinic in clinics:
            # Base attendance varies by clinic size
            if 'Hospital' in clinic or 'District' in clinic:
                base_attendance = 80
            elif 'Rural' in clinic:
                base_attendance = 25
            else:
                base_attendance = 50
            
            # Weekday variation (lower on weekends)
            weekday_factor = 0.6 if day_of_week >= 5 else 1.0
            
            # Seasonal variation (higher in rainy seasons: June-July, Nov)
            seasonal_factor = 1.3 if month in [6, 7, 11] else 1.0
            
            # Calculate daily attendance
            daily_attendance = int(base_attendance * weekday_factor * seasonal_factor * 
                                 random.uniform(0.8, 1.2))
            
            for _ in range(daily_attendance):
                patient_id += 1
                
                # Patient demographics
                age = int(np.random.choice(
                    [5, 15, 25, 35, 45, 55, 65, 75],
                    p=[0.15, 0.12, 0.18, 0.20, 0.15, 0.10, 0.07, 0.03]
                ))
                
                gender = random.choice(['M', 'F'])
                
                # Insurance status
                insurance = np.random.choice(
                    ['NHIF', 'Private', 'Self-Pay', 'County Scheme'],
                    p=[0.45, 0.15, 0.30, 0.10]
                )
                
                # Visit type
                visit_type = np.random.choice(
                    ['Outpatient', 'Emergency', 'Follow-up', 'Vaccination'],
                    p=[0.60, 0.15, 0.20, 0.05]
                )
                
                records.append({
                    'patient_id': f'P{patient_id:06d}',
                    'clinic_name': clinic,
                    'visit_date': single_date.strftime('%Y-%m-%d'),
                    'age': age,
                    'gender': gender,
                    'insurance_type': insurance,
                    'visit_type': visit_type,
                    'wait_time_minutes': int(np.random.gamma(3, 10)),
                    'consultation_duration': int(np.random.gamma(2, 5))
                })
    
    df = pd.DataFrame(records)
    df.to_csv('clinic_attendance.csv', index=False)
    print(f"✓ Generated {len(df)} attendance records")
    return df

def generate_ailments_data(attendance_df):
    """Generate ailments/diagnosis data based on attendance."""
    print("Generating ailments data...")
    
    # Common ailments with seasonal patterns
    ailments = {
        'Malaria': {'base': 0.15, 'seasonal_months': [6, 7, 11], 'seasonal_boost': 2.0},
        'Upper Respiratory Infection': {'base': 0.20, 'seasonal_months': [6, 7, 8], 'seasonal_boost': 1.5},
        'Diarrhea': {'base': 0.12, 'seasonal_months': [6, 7], 'seasonal_boost': 1.8},
        'Hypertension': {'base': 0.08, 'seasonal_months': [], 'seasonal_boost': 1.0},
        'Diabetes': {'base': 0.06, 'seasonal_months': [], 'seasonal_boost': 1.0},
        'Typhoid': {'base': 0.05, 'seasonal_months': [6, 11], 'seasonal_boost': 2.2},
        'Pneumonia': {'base': 0.07, 'seasonal_months': [6, 7], 'seasonal_boost': 1.6},
        'Skin Infections': {'base': 0.08, 'seasonal_months': [8, 9], 'seasonal_boost': 1.4},
        'Arthritis': {'base': 0.04, 'seasonal_months': [], 'seasonal_boost': 1.0},
        'Asthma': {'base': 0.06, 'seasonal_months': [6, 7], 'seasonal_boost': 1.3},
        'Minor Injuries': {'base': 0.09, 'seasonal_months': [], 'seasonal_boost': 1.0}
    }
    
    records = []
    
    for _, row in attendance_df.iterrows():
        month = int(row['visit_date'].split('-')[1])
        
        # Calculate probabilities for this visit
        probs = []
        ailment_names = []
        
        for ailment, config in ailments.items():
            prob = config['base']
            if month in config['seasonal_months']:
                prob *= config['seasonal_boost']
            probs.append(prob)
            ailment_names.append(ailment)
        
        # Normalize probabilities
        total = sum(probs)
        probs = [p/total for p in probs]
        
        # Select ailment
        ailment = np.random.choice(ailment_names, p=probs)
        
        # Severity
        severity = np.random.choice(['Mild', 'Moderate', 'Severe'], p=[0.50, 0.35, 0.15])
        
        # Treatment outcome
        outcome = np.random.choice(
            ['Recovered', 'Improving', 'Referred', 'Follow-up Required'],
            p=[0.60, 0.25, 0.10, 0.05]
        )
        
        # Number of medications prescribed
        num_medications = random.randint(1, 4)
        
        records.append({
            'patient_id': row['patient_id'],
            'clinic_name': row['clinic_name'],
            'visit_date': row['visit_date'],
            'ailment': ailment,
            'severity': severity,
            'num_medications': num_medications,
            'treatment_outcome': outcome,
            'follow_up_required': 'Yes' if outcome == 'Follow-up Required' else 'No'
        })
    
    df = pd.DataFrame(records)
    df.to_csv('ailments_diagnoses.csv', index=False)
    print(f"✓ Generated {len(df)} ailment records")
    return df

def generate_medication_supply():
    """Generate medication supply/inventory data."""
    print("Generating medication supply data...")
    
    medications = [
        ('Artemether-Lumefantrine', 'Malaria', 5000, 800),
        ('Quinine', 'Malaria', 2000, 300),
        ('Amoxicillin', 'Infections', 8000, 1200),
        ('Paracetamol', 'General', 15000, 2500),
        ('Ibuprofen', 'General', 10000, 1500),
        ('ORS Sachets', 'Diarrhea', 5000, 900),
        ('Metronidazole', 'Infections', 3000, 500),
        ('Amlodipine', 'Hypertension', 4000, 600),
        ('Metformin', 'Diabetes', 3500, 550),
        ('Ciprofloxacin', 'Typhoid', 2500, 400),
        ('Azithromycin', 'Respiratory', 3000, 450),
        ('Salbutamol Inhaler', 'Asthma', 1500, 250),
        ('Hydrocortisone Cream', 'Skin', 2000, 350),
        ('Diclofenac', 'Arthritis', 2500, 400),
        ('Ambroxol Syrup', 'Respiratory', 3000, 500)
    ]
    
    clinics = [
        'Central County Hospital',
        'Eastside Health Center',
        'Westgate Clinic',
        'Northview Medical Center',
        'Southside Community Clinic',
        'Rural Health Post A',
        'Rural Health Post B',
        'Urban Primary Care',
        'Community Wellness Center',
        'District Referral Hospital'
    ]
    
    start_date = datetime(2024, 6, 1)
    months = pd.date_range(start_date, periods=6, freq='MS')
    
    records = []
    
    for month_date in months:
        month = month_date.month
        
        for clinic in clinics:
            # Clinic size factor
            if 'Hospital' in clinic or 'District' in clinic:
                size_factor = 1.5
            elif 'Rural' in clinic:
                size_factor = 0.6
            else:
                size_factor = 1.0
            
            for med_name, category, base_stock, base_consumption in medications:
                # Seasonal variation
                seasonal_factor = 1.0
                if category == 'Malaria' and month in [6, 7, 11]:
                    seasonal_factor = 2.0
                elif category == 'Respiratory' and month in [6, 7, 8]:
                    seasonal_factor = 1.5
                elif category == 'Diarrhea' and month in [6, 7]:
                    seasonal_factor = 1.8
                
                opening_stock = int(base_stock * size_factor)
                consumption = int(base_consumption * size_factor * seasonal_factor * 
                                random.uniform(0.8, 1.2))
                received = int(base_consumption * size_factor * 1.2)
                
                closing_stock = opening_stock + received - consumption
                stock_out_days = max(0, int(random.uniform(0, 5))) if closing_stock < 500 else 0
                
                records.append({
                    'clinic_name': clinic,
                    'month': month_date.strftime('%Y-%m'),
                    'medication_name': med_name,
                    'category': category,
                    'opening_stock': opening_stock,
                    'quantity_received': received,
                    'quantity_consumed': consumption,
                    'closing_stock': closing_stock,
                    'stock_out_days': stock_out_days,
                    'expiry_soon': 'Yes' if random.random() < 0.05 else 'No'
                })
    
    df = pd.DataFrame(records)
    df.to_csv('medication_supply.csv', index=False)
    print(f"✓ Generated {len(df)} medication supply records")
    return df

def main():
    """Generate all healthcare datasets."""
    print("="*70)
    print("HEALTHCARE DATA GENERATOR")
    print("="*70)
    print()
    
    # Generate datasets
    attendance_df = generate_clinic_attendance()
    ailments_df = generate_ailments_data(attendance_df)
    medication_df = generate_medication_supply()
    
    print()
    print("="*70)
    print("DATASET SUMMARY")
    print("="*70)
    print(f"Clinic Attendance Records: {len(attendance_df):,}")
    print(f"Ailment/Diagnosis Records: {len(ailments_df):,}")
    print(f"Medication Supply Records: {len(medication_df):,}")
    print()
    print(f"Date Range: 2024-06-01 to 2024-11-30 (6 months)")
    print(f"Number of Clinics: 10")
    print(f"Number of Medications Tracked: 15")
    print()
    print("✓ All datasets generated successfully!")
    print("="*70)

if __name__ == "__main__":
    main()
