#!/usr/bin/env python3
"""
Microloan Transaction Data Generator
Generates realistic microloan transaction dataset with 500 features and millions of rows
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MicroloanDataGenerator:
    """Generate realistic microloan transaction data for Kenya."""
    
    def __init__(self, n_samples=1_000_000, n_features=500, random_state=42):
        self.n_samples = n_samples
        self.n_features = n_features
        self.random_state = random_state
        np.random.seed(random_state)
        
    def generate_dataset(self):
        """Generate complete microloan dataset."""
        print(f"Generating {self.n_samples:,} loan records with {self.n_features} features...")
        print("This may take a few minutes...\n")
        
        # Initialize feature dictionary
        features = {}
        
        # 1. CUSTOMER DEMOGRAPHICS (50 features)
        print("1/10 Generating customer demographics...")
        features.update(self._generate_demographics())
        
        # 2. LOAN CHARACTERISTICS (50 features)
        print("2/10 Generating loan characteristics...")
        features.update(self._generate_loan_characteristics())
        
        # 3. TRANSACTION HISTORY (100 features)
        print("3/10 Generating transaction history...")
        features.update(self._generate_transaction_history())
        
        # 4. PAYMENT BEHAVIOR (100 features)
        print("4/10 Generating payment behavior...")
        features.update(self._generate_payment_behavior())
        
        # 5. MOBILE MONEY PATTERNS (50 features)
        print("5/10 Generating mobile money patterns...")
        features.update(self._generate_mobile_money_patterns())
        
        # 6. CREDIT HISTORY (50 features)
        print("6/10 Generating credit history...")
        features.update(self._generate_credit_history())
        
        # 7. TEMPORAL FEATURES (30 features)
        print("7/10 Generating temporal features...")
        features.update(self._generate_temporal_features())
        
        # 8. BEHAVIORAL FEATURES (30 features)
        print("8/10 Generating behavioral features...")
        features.update(self._generate_behavioral_features())
        
        # 9. DERIVED/INTERACTION FEATURES (40 features)
        print("9/10 Generating derived features...")
        features.update(self._generate_derived_features(features))
        
        # Create DataFrame
        print("10/10 Creating DataFrame...")
        df = pd.DataFrame(features)
        
        # Generate target variable (loan default)
        print("Generating target variable (loan_default)...")
        df['loan_default'] = self._generate_target_variable(df)
        
        print(f"\n✅ Dataset generated: {df.shape[0]:,} rows × {df.shape[1]} columns")
        return df
    
    def _generate_demographics(self):
        """Generate customer demographic features."""
        return {
            'age': np.random.normal(35, 10, self.n_samples).clip(18, 70),
            'gender': np.random.choice(['M', 'F'], self.n_samples, p=[0.55, 0.45]),
            'marital_status': np.random.choice(['Single', 'Married', 'Divorced', 'Widowed'], 
                                              self.n_samples, p=[0.35, 0.50, 0.10, 0.05]),
            'education_level': np.random.choice(['Primary', 'Secondary', 'Tertiary', 'University'], 
                                               self.n_samples, p=[0.20, 0.40, 0.25, 0.15]),
            'employment_status': np.random.choice(['Employed', 'Self-employed', 'Unemployed'], 
                                                  self.n_samples, p=[0.45, 0.40, 0.15]),
            'monthly_income': np.random.lognormal(10, 0.8, self.n_samples).clip(5000, 200000),
            'dependents': np.random.poisson(2, self.n_samples).clip(0, 10),
            'home_ownership': np.random.choice(['Own', 'Rent', 'Family'], 
                                              self.n_samples, p=[0.30, 0.50, 0.20]),
            'years_at_residence': np.random.exponential(3, self.n_samples).clip(0, 30),
            'county': np.random.choice(['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
                                       'Machakos', 'Meru', 'Nyeri', 'Kakamega', 'Kiambu'],
                                      self.n_samples),
            **{f'demo_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 41)}  # Additional demographic noise features
        }
    
    def _generate_loan_characteristics(self):
        """Generate loan-specific features."""
        loan_amount = np.random.lognormal(9, 0.7, self.n_samples).clip(1000, 500000)
        interest_rate = np.random.normal(15, 3, self.n_samples).clip(8, 25)
        loan_term = np.random.choice([1, 3, 6, 12, 24, 36], self.n_samples, 
                                    p=[0.20, 0.25, 0.25, 0.15, 0.10, 0.05])
        
        return {
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_term_months': loan_term,
            'loan_purpose': np.random.choice(['Business', 'Education', 'Emergency', 'Agriculture',
                                             'Home Improvement', 'Medical', 'Other'],
                                            self.n_samples),
            'collateral_type': np.random.choice(['None', 'Property', 'Vehicle', 'Guarantor'],
                                               self.n_samples, p=[0.60, 0.15, 0.10, 0.15]),
            'loan_to_income_ratio': loan_amount / (np.random.lognormal(10, 0.8, self.n_samples).clip(5000, 200000)),
            'number_of_installments': loan_term,
            'installment_amount': loan_amount * (1 + interest_rate/100) / loan_term,
            'processing_fee': loan_amount * 0.02,
            'insurance_fee': loan_amount * 0.01,
            **{f'loan_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 41)}  # Additional loan noise features
        }
    
    def _generate_transaction_history(self):
        """Generate transaction history features."""
        return {
            'total_transactions_3m': np.random.poisson(25, self.n_samples).clip(0, 200),
            'total_transactions_6m': np.random.poisson(50, self.n_samples).clip(0, 400),
            'total_transactions_12m': np.random.poisson(100, self.n_samples).clip(0, 800),
            'avg_transaction_amount': np.random.lognormal(7, 1.2, self.n_samples).clip(100, 50000),
            'max_transaction_amount': np.random.lognormal(8.5, 1.5, self.n_samples).clip(500, 200000),
            'min_transaction_amount': np.random.lognormal(5, 1, self.n_samples).clip(10, 5000),
            'transaction_velocity_7d': np.random.poisson(3, self.n_samples),
            'transaction_velocity_30d': np.random.poisson(12, self.n_samples),
            'unique_merchants_3m': np.random.poisson(8, self.n_samples).clip(0, 50),
            'unique_merchants_6m': np.random.poisson(15, self.n_samples).clip(0, 100),
            'deposit_count_3m': np.random.poisson(15, self.n_samples),
            'withdrawal_count_3m': np.random.poisson(20, self.n_samples),
            'deposit_to_withdrawal_ratio': np.random.gamma(1, 1, self.n_samples).clip(0.1, 5),
            'weekend_transaction_pct': np.random.beta(2, 5, self.n_samples),
            'night_transaction_pct': np.random.beta(1, 10, self.n_samples),
            **{f'trans_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 86)}  # Additional transaction noise features
        }
    
    def _generate_payment_behavior(self):
        """Generate payment behavior features."""
        return {
            'payment_history_score': np.random.beta(8, 2, self.n_samples) * 100,
            'on_time_payment_rate': np.random.beta(7, 2, self.n_samples),
            'late_payment_count_12m': np.random.poisson(1.5, self.n_samples).clip(0, 20),
            'missed_payment_count_12m': np.random.poisson(0.5, self.n_samples).clip(0, 10),
            'avg_days_overdue': np.random.gamma(2, 3, self.n_samples).clip(0, 90),
            'max_days_overdue': np.random.gamma(3, 5, self.n_samples).clip(0, 180),
            'payment_amount_variance': np.random.gamma(2, 1000, self.n_samples),
            'early_payment_count': np.random.poisson(3, self.n_samples),
            'partial_payment_count': np.random.poisson(1, self.n_samples),
            'payment_method_diversity': np.random.poisson(2, self.n_samples).clip(1, 5),
            'autopay_enabled': np.random.choice([0, 1], self.n_samples, p=[0.70, 0.30]),
            'payment_reminder_response_rate': np.random.beta(5, 3, self.n_samples),
            'restructure_request_count': np.random.poisson(0.3, self.n_samples).clip(0, 5),
            'grace_period_usage_count': np.random.poisson(0.5, self.n_samples),
            'payment_channel_mpesa_pct': np.random.beta(6, 2, self.n_samples),
            **{f'payment_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 86)}  # Additional payment noise features
        }
    
    def _generate_mobile_money_patterns(self):
        """Generate mobile money usage features."""
        return {
            'mpesa_account_age_months': np.random.exponential(24, self.n_samples).clip(1, 120),
            'mpesa_transaction_count_3m': np.random.poisson(40, self.n_samples),
            'mpesa_avg_balance': np.random.lognormal(8, 1.5, self.n_samples).clip(100, 100000),
            'mpesa_min_balance_3m': np.random.lognormal(6, 1.8, self.n_samples).clip(0, 50000),
            'mpesa_max_balance_3m': np.random.lognormal(9, 1.5, self.n_samples).clip(1000, 200000),
            'airtime_purchase_frequency': np.random.poisson(8, self.n_samples),
            'bill_payment_frequency': np.random.poisson(5, self.n_samples),
            'p2p_transfer_count_3m': np.random.poisson(15, self.n_samples),
            'merchant_payment_count_3m': np.random.poisson(10, self.n_samples),
            'paybill_usage_count': np.random.poisson(6, self.n_samples),
            'till_number_usage_count': np.random.poisson(8, self.n_samples),
            'mobile_data_purchase_freq': np.random.poisson(4, self.n_samples),
            'international_transfer_count': np.random.poisson(0.5, self.n_samples),
            'savings_account_linked': np.random.choice([0, 1], self.n_samples, p=[0.60, 0.40]),
            'mobile_loan_history_count': np.random.poisson(2, self.n_samples).clip(0, 20),
            **{f'mobile_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 36)}  # Additional mobile money noise features
        }
    
    def _generate_credit_history(self):
        """Generate credit history features."""
        return {
            'credit_score': np.random.normal(600, 100, self.n_samples).clip(300, 850),
            'credit_history_length_months': np.random.exponential(30, self.n_samples).clip(0, 240),
            'total_credit_accounts': np.random.poisson(3, self.n_samples).clip(0, 15),
            'active_credit_accounts': np.random.poisson(2, self.n_samples).clip(0, 10),
            'closed_credit_accounts': np.random.poisson(1, self.n_samples).clip(0, 10),
            'total_credit_limit': np.random.lognormal(11, 1, self.n_samples).clip(10000, 1000000),
            'credit_utilization_ratio': np.random.beta(3, 5, self.n_samples),
            'hard_inquiries_6m': np.random.poisson(1.5, self.n_samples).clip(0, 10),
            'soft_inquiries_6m': np.random.poisson(3, self.n_samples).clip(0, 20),
            'delinquency_count_24m': np.random.poisson(0.8, self.n_samples).clip(0, 15),
            'public_records_count': np.random.poisson(0.1, self.n_samples).clip(0, 5),
            'collection_count': np.random.poisson(0.3, self.n_samples).clip(0, 8),
            'bankruptcy_flag': np.random.choice([0, 1], self.n_samples, p=[0.98, 0.02]),
            'previous_default_count': np.random.poisson(0.2, self.n_samples).clip(0, 5),
            'debt_to_income_ratio': np.random.gamma(2, 0.15, self.n_samples).clip(0, 1.5),
            **{f'credit_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 36)}  # Additional credit noise features
        }
    
    def _generate_temporal_features(self):
        """Generate time-based features."""
        month = np.random.randint(1, 13, self.n_samples)
        day_of_week = np.random.randint(0, 7, self.n_samples)
        
        return {
            'application_month': month,
            'application_day_of_week': day_of_week,
            'application_hour': np.random.randint(0, 24, self.n_samples),
            'is_weekend': (day_of_week >= 5).astype(int),
            'is_month_end': np.random.choice([0, 1], self.n_samples, p=[0.85, 0.15]),
            'is_holiday_season': np.random.choice([0, 1], self.n_samples, p=[0.90, 0.10]),
            'days_since_last_loan': np.random.exponential(180, self.n_samples).clip(0, 1825),
            'season': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], self.n_samples),
            'time_to_first_payment_days': np.random.normal(30, 5, self.n_samples).clip(7, 60),
            'account_age_days': np.random.exponential(365, self.n_samples).clip(1, 3650),
            **{f'temporal_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 21)}  # Additional temporal noise features
        }
    
    def _generate_behavioral_features(self):
        """Generate customer behavioral features."""
        return {
            'app_login_frequency_7d': np.random.poisson(5, self.n_samples),
            'app_login_frequency_30d': np.random.poisson(20, self.n_samples),
            'customer_service_contacts_3m': np.random.poisson(2, self.n_samples),
            'complaint_count_12m': np.random.poisson(0.5, self.n_samples),
            'promotional_email_open_rate': np.random.beta(3, 7, self.n_samples),
            'sms_response_rate': np.random.beta(4, 6, self.n_samples),
            'referral_count': np.random.poisson(1, self.n_samples).clip(0, 20),
            'loyalty_program_member': np.random.choice([0, 1], self.n_samples, p=[0.70, 0.30]),
            'app_rating_given': np.random.choice([0, 1], self.n_samples, p=[0.80, 0.20]),
            'feature_usage_diversity': np.random.poisson(5, self.n_samples).clip(1, 15),
            'session_duration_avg_minutes': np.random.gamma(3, 2, self.n_samples).clip(1, 60),
            'verification_completion_time_minutes': np.random.gamma(5, 3, self.n_samples).clip(1, 120),
            'document_upload_attempts': np.random.poisson(2, self.n_samples).clip(1, 10),
            'social_media_linked': np.random.choice([0, 1], self.n_samples, p=[0.65, 0.35]),
            'consent_to_data_sharing': np.random.choice([0, 1], self.n_samples, p=[0.40, 0.60]),
            **{f'behavior_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 16)}  # Additional behavioral noise features
        }
    
    def _generate_derived_features(self, features):
        """Generate derived and interaction features."""
        age = features['age']
        income = features['monthly_income']
        loan_amount = features['loan_amount']
        
        return {
            'income_to_age_ratio': income / age,
            'loan_burden': loan_amount / income,
            'age_group': (age // 10).astype(int),
            'income_quartile': np.random.randint(1, 5, self.n_samples),
            'risk_score_composite': np.random.beta(5, 3, self.n_samples) * 100,
            **{f'derived_feature_{i}': np.random.randn(self.n_samples) 
               for i in range(1, 36)}  # Additional derived noise features
        }
    
    def _generate_target_variable(self, df):
        """Generate loan default target variable based on realistic patterns."""
        # Base default probability
        default_prob = np.full(self.n_samples, 0.15)
        
        # Adjust based on key risk factors
        default_prob += (df['late_payment_count_12m'] > 3).values * 0.20
        default_prob += (df['credit_score'] < 500).values * 0.15
        default_prob += (df['debt_to_income_ratio'] > 0.5).values * 0.10
        default_prob += (df['loan_to_income_ratio'] > 3).values * 0.12
        default_prob += (df['missed_payment_count_12m'] > 2).values * 0.18
        default_prob += (df['employment_status'] == 'Unemployed').values * 0.25
        default_prob += (df['previous_default_count'] > 0).values * 0.20
        default_prob -= (df['payment_history_score'] > 80).values * 0.15
        default_prob -= (df['on_time_payment_rate'] > 0.9).values * 0.10
        default_prob -= (df['credit_score'] > 700).values * 0.12
        
        # Clip to valid probability range
        default_prob = default_prob.clip(0.01, 0.95)
        
        # Generate binary default outcome
        return (np.random.random(self.n_samples) < default_prob).astype(int)

def main():
    """Generate and save microloan dataset."""
    print("="*70)
    print("KENYAN MICROLOAN TRANSACTION DATA GENERATOR")
    print("="*70)
    print()
    
    # Generate dataset
    generator = MicroloanDataGenerator(n_samples=1_000_000, n_features=500)
    df = generator.generate_dataset()
    
    # Display info
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    print(f"Shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nDefault rate: {df['loan_default'].mean():.2%}")
    print(f"Non-default: {(df['loan_default']==0).sum():,} ({(df['loan_default']==0).mean():.2%})")
    print(f"Default: {(df['loan_default']==1).sum():,} ({(df['loan_default']==1).mean():.2%})")
    
    # Save dataset
    print("\n" + "="*70)
    print("SAVING DATASET")
    print("="*70)
    output_file = 'microloan_transactions.csv'
    print(f"Saving to: {output_file}")
    print("This may take several minutes for large datasets...")
    df.to_csv(output_file, index=False)
    
    file_size = pd.io.common.file_exists(output_file)
    import os
    file_size_mb = os.path.getsize(output_file) / 1024**2
    print(f"✅ Saved successfully: {file_size_mb:.2f} MB")
    
    # Display sample
    print("\n" + "="*70)
    print("SAMPLE DATA (First 5 rows, first 10 columns)")
    print("="*70)
    print(df.iloc[:5, :10])
    
    print("\n" + "="*70)
    print("✅ DATA GENERATION COMPLETE")
    print("="*70)
    print(f"\nOutput file: {output_file}")
    print(f"Ready for feature selection and dimensionality reduction analysis!")
    print("="*70)

if __name__ == "__main__":
    main()
