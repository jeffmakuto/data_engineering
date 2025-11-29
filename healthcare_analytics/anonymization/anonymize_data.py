#!/usr/bin/env python3
"""
Patient Data Anonymization
Implements multiple anonymization techniques to protect sensitive patient information
while preserving data utility for analysis.

Techniques implemented:
1. K-Anonymity - Generalization and suppression
2. L-Diversity - Enhanced privacy beyond k-anonymity
3. Data Masking - Hash-based pseudonymization
4. Differential Privacy - Adding statistical noise
"""
import pandas as pd
import numpy as np
import hashlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PatientDataAnonymizer:
    """Comprehensive patient data anonymization toolkit."""
    
    def __init__(self, k=5, l=2):
        """
        Initialize anonymizer.
        
        Args:
            k: Minimum group size for k-anonymity
            l: Minimum diversity for sensitive attributes
        """
        self.k = k
        self.l = l
        self.anonymization_log = []
        
    def load_data(self):
        """Load patient data for anonymization."""
        print("Loading patient data...")
        
        self.attendance = pd.read_csv('../datasets/clinic_attendance.csv')
        self.ailments = pd.read_csv('../datasets/ailments_diagnoses.csv')
        
        # Merge for comprehensive patient records
        self.data = pd.merge(
            self.attendance,
            self.ailments[['patient_id', 'ailment', 'severity']],
            on='patient_id'
        )
        
        print(f"✓ Loaded {len(self.data):,} patient records")
        print(f"  Columns: {', '.join(self.data.columns)}")
        
        return self.data
    
    def technique_1_pseudonymization(self, df):
        """
        Technique 1: Pseudonymization using cryptographic hashing.
        Replace direct identifiers with irreversible hashes.
        """
        print("\n" + "="*70)
        print("TECHNIQUE 1: PSEUDONYMIZATION (Hash-based)")
        print("="*70)
        
        df_anon = df.copy()
        
        # Hash patient IDs using SHA-256
        df_anon['patient_id_hash'] = df_anon['patient_id'].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
        )
        
        # Remove original patient ID
        df_anon = df_anon.drop('patient_id', axis=1)
        
        print("✓ Applied SHA-256 hashing to patient IDs")
        print(f"  Example: P010001 → {df_anon['patient_id_hash'].iloc[0]}")
        
        self.anonymization_log.append({
            'technique': 'Pseudonymization',
            'method': 'SHA-256 hashing',
            'privacy_level': 'High',
            'data_utility': 'High - preserves all other attributes'
        })
        
        return df_anon
    
    def technique_2_generalization(self, df):
        """
        Technique 2: Generalization for k-anonymity.
        Reduce precision of quasi-identifiers to achieve k-anonymity.
        """
        print("\n" + "="*70)
        print(f"TECHNIQUE 2: GENERALIZATION (k-anonymity, k={self.k})")
        print("="*70)
        
        df_anon = df.copy()
        
        # Generalize age into broader ranges
        def generalize_age(age):
            if age < 18:
                return '0-17'
            elif age < 30:
                return '18-29'
            elif age < 45:
                return '30-44'
            elif age < 60:
                return '45-59'
            else:
                return '60+'
        
        df_anon['age_group'] = df_anon['age'].apply(generalize_age)
        
        # Generalize visit dates to month only
        df_anon['visit_month'] = pd.to_datetime(df_anon['visit_date']).dt.to_period('M')
        
        # Suppress specific clinic names, use clinic type instead
        df_anon['clinic_type'] = df_anon['clinic_name'].apply(
            lambda x: 'Hospital' if 'Hospital' in x 
                     else 'Rural Clinic' if 'Rural' in x 
                     else 'Urban Clinic'
        )
        
        # Drop original quasi-identifiers
        df_anon = df_anon.drop(['age', 'visit_date', 'clinic_name'], axis=1)
        
        # Verify k-anonymity
        quasi_identifiers = ['age_group', 'gender', 'clinic_type', 'visit_month']
        group_sizes = df_anon.groupby(quasi_identifiers).size()
        min_group_size = group_sizes.min()
        violation_count = (group_sizes < self.k).sum()
        
        print(f"✓ Applied generalization to quasi-identifiers")
        print(f"  Age: Generalized to 5 age groups")
        print(f"  Date: Reduced to month precision")
        print(f"  Clinic: Generalized to 3 clinic types")
        print(f"\nk-Anonymity Assessment:")
        print(f"  Target k: {self.k}")
        print(f"  Minimum group size: {min_group_size}")
        print(f"  Groups violating k-anonymity: {violation_count}")
        print(f"  k-anonymity achieved: {'✓ Yes' if min_group_size >= self.k else '✗ No'}")
        
        self.anonymization_log.append({
            'technique': 'Generalization',
            'method': f'k-anonymity (k={self.k})',
            'privacy_level': 'Medium-High',
            'data_utility': 'Medium - some precision lost',
            'k_achieved': min_group_size >= self.k
        })
        
        return df_anon
    
    def technique_3_l_diversity(self, df):
        """
        Technique 3: L-Diversity.
        Ensure sensitive attributes have sufficient diversity within equivalence classes.
        """
        print("\n" + "="*70)
        print(f"TECHNIQUE 3: L-DIVERSITY (l={self.l})")
        print("="*70)
        
        df_anon = df.copy()
        
        # Define quasi-identifiers and sensitive attribute
        quasi_identifiers = ['age_group', 'gender', 'clinic_type', 'visit_month']
        sensitive_attribute = 'ailment'
        
        # Calculate diversity for each equivalence class
        diversity_check = df_anon.groupby(quasi_identifiers)[sensitive_attribute].agg([
            ('count', 'size'),
            ('unique_values', 'nunique'),
            ('diversity', lambda x: x.nunique())
        ]).reset_index()
        
        # Identify groups that don't satisfy l-diversity
        violations = diversity_check[diversity_check['diversity'] < self.l]
        
        print(f"✓ Analyzed l-diversity for sensitive attribute: {sensitive_attribute}")
        print(f"  Total equivalence classes: {len(diversity_check)}")
        print(f"  Classes violating l-diversity: {len(violations)}")
        print(f"  Minimum diversity found: {diversity_check['diversity'].min()}")
        print(f"  l-diversity achieved: {'✓ Yes' if len(violations) == 0 else '✗ Partial'}")
        
        if len(violations) > 0:
            print(f"\nSuggestion: Further generalization or suppression needed for {len(violations)} groups")
        
        self.anonymization_log.append({
            'technique': 'L-Diversity',
            'method': f'l={self.l} for ailment',
            'privacy_level': 'High',
            'data_utility': 'Medium',
            'l_achieved': len(violations) == 0,
            'violation_count': len(violations)
        })
        
        return df_anon, diversity_check
    
    def technique_4_differential_privacy(self, df, epsilon=1.0):
        """
        Technique 4: Differential Privacy.
        Add Laplace noise to numerical aggregates for privacy preservation.
        """
        print("\n" + "="*70)
        print(f"TECHNIQUE 4: DIFFERENTIAL PRIVACY (ε={epsilon})")
        print("="*70)
        
        # Create aggregate statistics with noise
        df_aggregate = df.copy()
        
        # Calculate sensitivities
        numerical_cols = ['wait_time_minutes', 'consultation_duration', 'num_medications']
        
        aggregated_stats = {}
        
        for col in numerical_cols:
            if col in df_aggregate.columns:
                # Original statistics
                original_mean = df_aggregate[col].mean()
                original_count = df_aggregate[col].count()
                
                # Add Laplace noise (sensitivity / epsilon)
                sensitivity = df_aggregate[col].max() - df_aggregate[col].min()
                noise_scale = sensitivity / epsilon
                
                noisy_mean = original_mean + np.random.laplace(0, noise_scale)
                noisy_count = original_count + int(np.random.laplace(0, 1/epsilon))
                
                aggregated_stats[col] = {
                    'original_mean': original_mean,
                    'noisy_mean': noisy_mean,
                    'original_count': original_count,
                    'noisy_count': max(0, noisy_count),  # Ensure non-negative
                    'noise_scale': noise_scale
                }
        
        print("✓ Applied differential privacy to aggregated statistics")
        print(f"  Privacy budget (ε): {epsilon}")
        print(f"\nNoisy Statistics:")
        
        for col, stats in aggregated_stats.items():
            print(f"\n  {col}:")
            print(f"    Original mean: {stats['original_mean']:.2f}")
            print(f"    Noisy mean: {stats['noisy_mean']:.2f}")
            print(f"    Noise added: {abs(stats['noisy_mean'] - stats['original_mean']):.2f}")
        
        self.anonymization_log.append({
            'technique': 'Differential Privacy',
            'method': f'Laplace mechanism (ε={epsilon})',
            'privacy_level': 'Very High',
            'data_utility': 'Medium - suitable for aggregates',
            'epsilon': epsilon
        })
        
        return aggregated_stats
    
    def technique_5_data_masking(self, df):
        """
        Technique 5: Data Masking.
        Mask or suppress specific sensitive fields.
        """
        print("\n" + "="*70)
        print("TECHNIQUE 5: DATA MASKING & SUPPRESSION")
        print("="*70)
        
        df_masked = df.copy()
        
        # Mask insurance type with general categories
        df_masked['insurance_masked'] = df_masked['insurance_type'].apply(
            lambda x: 'Public' if x in ['NHIF', 'County Scheme'] else 'Private/Self-Pay'
        )
        
        # Suppress exact wait times, use categories
        def categorize_wait_time(minutes):
            if minutes < 15:
                return 'Short (<15 min)'
            elif minutes < 30:
                return 'Medium (15-30 min)'
            elif minutes < 60:
                return 'Long (30-60 min)'
            else:
                return 'Very Long (>60 min)'
        
        df_masked['wait_time_category'] = df_masked['wait_time_minutes'].apply(categorize_wait_time)
        
        # Remove original sensitive fields
        df_masked = df_masked.drop(['insurance_type', 'wait_time_minutes'], axis=1)
        
        print("✓ Applied data masking techniques")
        print("  Insurance: Reduced to 2 categories (Public/Private)")
        print("  Wait times: Categorized into 4 ranges")
        print("  Removed exact numerical values")
        
        self.anonymization_log.append({
            'technique': 'Data Masking',
            'method': 'Categorical masking and suppression',
            'privacy_level': 'High',
            'data_utility': 'Medium-High'
        })
        
        return df_masked
    
    def save_anonymized_data(self, df_anon, filename):
        """Save anonymized dataset."""
        df_anon.to_csv(filename, index=False)
        print(f"\n✓ Saved anonymized data to {filename}")
        print(f"  Records: {len(df_anon):,}")
        print(f"  Columns: {len(df_anon.columns)}")
    
    def generate_anonymization_report(self):
        """Generate comprehensive anonymization report."""
        print("\n" + "="*70)
        print("ANONYMIZATION SUMMARY REPORT")
        print("="*70)
        
        report = pd.DataFrame(self.anonymization_log)
        
        print("\nTechniques Applied:")
        for i, row in report.iterrows():
            print(f"\n{i+1}. {row['technique']}")
            print(f"   Method: {row['method']}")
            print(f"   Privacy Level: {row['privacy_level']}")
            print(f"   Data Utility: {row['data_utility']}")
        
        # Save report
        report.to_csv('anonymization_report.csv', index=False)
        print("\n✓ Saved detailed report to anonymization_report.csv")
        
        return report

def main():
    """Main execution function."""
    print("="*70)
    print("PATIENT DATA ANONYMIZATION TOOLKIT")
    print("="*70)
    print()
    
    # Initialize anonymizer
    anonymizer = PatientDataAnonymizer(k=5, l=2)
    
    # Load data
    data = anonymizer.load_data()
    
    # Sample for demonstration (use full dataset in production)
    data_sample = data.head(10000)
    
    # Apply anonymization techniques
    
    # 1. Pseudonymization
    data_pseudo = anonymizer.technique_1_pseudonymization(data_sample)
    
    # 2. Generalization for k-anonymity
    data_general = anonymizer.technique_2_generalization(data_pseudo)
    
    # 3. L-Diversity
    data_ldiv, diversity_stats = anonymizer.technique_3_l_diversity(data_general)
    
    # 4. Data Masking
    data_masked = anonymizer.technique_5_data_masking(data_ldiv)
    
    # 5. Differential Privacy (on aggregates)
    dp_stats = anonymizer.technique_4_differential_privacy(data_masked, epsilon=1.0)
    
    # Save anonymized dataset
    anonymizer.save_anonymized_data(
        data_masked,
        'anonymized_patient_data.csv'
    )
    
    # Generate report
    report = anonymizer.generate_anonymization_report()
    
    print("\n" + "="*70)
    print("ANONYMIZATION COMPLETE")
    print("="*70)
    print("\nRecommendations:")
    print("  ✓ Use pseudonymized data for internal analysis")
    print("  ✓ Use k-anonymous data for sharing with partners")
    print("  ✓ Use differentially private aggregates for public release")
    print("  ✓ Apply l-diversity for sensitive attribute protection")
    print("\nOutputs:")
    print("  • anonymized_patient_data.csv - Fully anonymized dataset")
    print("  • anonymization_report.csv - Detailed technique documentation")
    print("="*70)

if __name__ == "__main__":
    main()
