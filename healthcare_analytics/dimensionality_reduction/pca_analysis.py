#!/usr/bin/env python3
"""
Dimensionality Reduction using PCA and t-SNE
Reduces the healthcare dataset dimensions for easier analysis and visualization
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

class HealthcareDimensionalityReduction:
    """Perform dimensionality reduction on healthcare data."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = None
        self.tsne = None
        self.label_encoders = {}
        
    def load_and_prepare_data(self):
        """Load and prepare healthcare data for dimensionality reduction."""
        print("Loading healthcare datasets...")
        
        # Load datasets
        attendance = pd.read_csv('../datasets/clinic_attendance.csv')
        ailments = pd.read_csv('../datasets/ailments_diagnoses.csv')
        medications = pd.read_csv('../datasets/medication_supply.csv')
        
        print(f"Loaded {len(attendance):,} attendance records")
        print(f"Loaded {len(ailments):,} ailment records")
        print(f"Loaded {len(medications):,} medication records")
        
        # Merge datasets
        print("\nMerging datasets...")
        merged_data = pd.merge(attendance, ailments, on=['patient_id', 'clinic_name', 'visit_date'])
        
        print(f"Merged dataset size: {len(merged_data):,} records")
        
        return merged_data, medications
    
    def create_feature_matrix(self, df):
        """Create numerical feature matrix from healthcare data."""
        print("\nCreating feature matrix...")
        
        # Encode categorical variables
        categorical_cols = ['clinic_name', 'gender', 'insurance_type', 'visit_type', 
                           'ailment', 'severity', 'treatment_outcome']
        
        df_encoded = df.copy()
        
        for col in categorical_cols:
            if col in df_encoded.columns:
                le = LabelEncoder()
                df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col])
                self.label_encoders[col] = le
        
        # Select numerical features
        numerical_features = [
            'age',
            'wait_time_minutes',
            'consultation_duration',
            'num_medications',
            'clinic_name_encoded',
            'gender_encoded',
            'insurance_type_encoded',
            'visit_type_encoded',
            'ailment_encoded',
            'severity_encoded',
            'treatment_outcome_encoded'
        ]
        
        # Create aggregated monthly features
        df_encoded['month'] = pd.to_datetime(df_encoded['visit_date']).dt.month
        df_encoded['day_of_week'] = pd.to_datetime(df_encoded['visit_date']).dt.dayofweek
        
        numerical_features.extend(['month', 'day_of_week'])
        
        X = df_encoded[numerical_features].values
        
        print(f"Feature matrix shape: {X.shape}")
        print(f"Number of features: {len(numerical_features)}")
        
        return X, numerical_features, df_encoded
    
    def apply_pca(self, X, n_components=5):
        """Apply PCA for dimensionality reduction."""
        print(f"\nApplying PCA (reducing to {n_components} components)...")
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA
        self.pca = PCA(n_components=n_components)
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Explained variance
        explained_var = self.pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        print(f"\nPCA Results:")
        print(f"Total variance explained: {cumulative_var[-1]:.2%}")
        print(f"\nVariance explained by each component:")
        for i, var in enumerate(explained_var, 1):
            print(f"  PC{i}: {var:.2%}")
        
        return X_pca, explained_var
    
    def apply_tsne(self, X, n_components=2, sample_size=5000):
        """Apply t-SNE for visualization (on sample for performance)."""
        print(f"\nApplying t-SNE (reducing to {n_components} components)...")
        print(f"Using sample of {sample_size} records for performance...")
        
        # Sample data for t-SNE (computationally expensive)
        if len(X) > sample_size:
            indices = np.random.choice(len(X), sample_size, replace=False)
            X_sample = X[indices]
        else:
            X_sample = X
            indices = np.arange(len(X))
        
        # Standardize
        X_scaled = self.scaler.transform(X_sample)
        
        # Apply t-SNE
        self.tsne = TSNE(n_components=n_components, random_state=42, 
                         perplexity=30, max_iter=1000, verbose=1)
        X_tsne = self.tsne.fit_transform(X_scaled)
        
        print("t-SNE completed")
        
        return X_tsne, indices
    
    def visualize_pca(self, X_pca, explained_var, df_encoded, save_path='pca_analysis.png'):
        """Visualize PCA results."""
        print("\nGenerating PCA visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Scree plot
        axes[0, 0].bar(range(1, len(explained_var) + 1), explained_var, 
                       alpha=0.7, color='steelblue')
        axes[0, 0].plot(range(1, len(explained_var) + 1), np.cumsum(explained_var), 
                        'ro-', linewidth=2, label='Cumulative')
        axes[0, 0].set_xlabel('Principal Component')
        axes[0, 0].set_ylabel('Variance Explained')
        axes[0, 0].set_title('PCA Scree Plot')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. PC1 vs PC2 colored by ailment
        scatter = axes[0, 1].scatter(X_pca[:, 0], X_pca[:, 1], 
                                     c=df_encoded['ailment_encoded'], 
                                     cmap='tab10', alpha=0.5, s=10)
        axes[0, 1].set_xlabel('First Principal Component')
        axes[0, 1].set_ylabel('Second Principal Component')
        axes[0, 1].set_title('PCA: PC1 vs PC2 (Colored by Ailment)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. PC1 vs PC2 colored by severity
        severity_map = {'Mild': 0, 'Moderate': 1, 'Severe': 2}
        severity_numeric = df_encoded['severity'].map(severity_map)
        scatter2 = axes[1, 0].scatter(X_pca[:, 0], X_pca[:, 1], 
                                      c=severity_numeric, 
                                      cmap='RdYlGn_r', alpha=0.5, s=10)
        axes[1, 0].set_xlabel('First Principal Component')
        axes[1, 0].set_ylabel('Second Principal Component')
        axes[1, 0].set_title('PCA: PC1 vs PC2 (Colored by Severity)')
        axes[1, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=axes[1, 0], label='Severity')
        
        # 4. Feature importance (loadings)
        loadings = self.pca.components_[0]
        feature_names = ['age', 'wait_time', 'consult_dur', 'num_meds', 
                        'clinic', 'gender', 'insurance', 'visit_type',
                        'ailment', 'severity', 'outcome', 'month', 'day']
        
        # Top 10 most important features
        importance_indices = np.argsort(np.abs(loadings))[-10:]
        axes[1, 1].barh([feature_names[i] for i in importance_indices],
                        loadings[importance_indices], color='coral')
        axes[1, 1].set_xlabel('PC1 Loading')
        axes[1, 1].set_title('Top 10 Feature Loadings (PC1)')
        axes[1, 1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved PCA visualization to {save_path}")
        plt.close()
    
    def visualize_tsne(self, X_tsne, df_encoded, indices, save_path='tsne_analysis.png'):
        """Visualize t-SNE results."""
        print("\nGenerating t-SNE visualizations...")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Sample the corresponding encoded data
        df_sample = df_encoded.iloc[indices]
        
        # 1. t-SNE colored by ailment
        scatter1 = axes[0].scatter(X_tsne[:, 0], X_tsne[:, 1], 
                                   c=df_sample['ailment_encoded'], 
                                   cmap='tab10', alpha=0.6, s=20)
        axes[0].set_xlabel('t-SNE Component 1')
        axes[0].set_ylabel('t-SNE Component 2')
        axes[0].set_title('t-SNE Visualization (Colored by Ailment)')
        axes[0].grid(True, alpha=0.3)
        
        # 2. t-SNE colored by month (seasonal patterns)
        scatter2 = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1], 
                                   c=df_sample['month'], 
                                   cmap='coolwarm', alpha=0.6, s=20)
        axes[1].set_xlabel('t-SNE Component 1')
        axes[1].set_ylabel('t-SNE Component 2')
        axes[1].set_title('t-SNE Visualization (Colored by Month)')
        axes[1].grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=axes[1], label='Month')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved t-SNE visualization to {save_path}")
        plt.close()
    
    def save_reduced_data(self, X_pca, df_encoded, save_path='reduced_dataset.csv'):
        """Save the reduced dataset for OLAP analysis."""
        print("\nSaving reduced dataset for OLAP analysis...")
        
        # Create DataFrame with PCA components
        pca_df = pd.DataFrame(
            X_pca,
            columns=[f'PC{i+1}' for i in range(X_pca.shape[1])]
        )
        
        # Add original categorical columns
        pca_df['patient_id'] = df_encoded['patient_id'].values
        pca_df['clinic_name'] = df_encoded['clinic_name'].values
        pca_df['visit_date'] = df_encoded['visit_date'].values
        pca_df['ailment'] = df_encoded['ailment'].values
        pca_df['severity'] = df_encoded['severity'].values
        pca_df['age'] = df_encoded['age'].values
        pca_df['num_medications'] = df_encoded['num_medications'].values
        pca_df['treatment_outcome'] = df_encoded['treatment_outcome'].values
        
        pca_df.to_csv(save_path, index=False)
        print(f"✓ Saved reduced dataset to {save_path}")
        print(f"  Original dimensions: {len(df_encoded.columns)} columns")
        print(f"  Reduced dimensions: {X_pca.shape[1]} principal components + key categorical variables")

def main():
    """Main execution function."""
    print("="*70)
    print("HEALTHCARE DATA - DIMENSIONALITY REDUCTION ANALYSIS")
    print("="*70)
    print()
    
    # Initialize
    dr = HealthcareDimensionalityReduction()
    
    # Load data
    merged_data, medications = dr.load_and_prepare_data()
    
    # Create feature matrix
    X, feature_names, df_encoded = dr.create_feature_matrix(merged_data)
    
    # Apply PCA
    X_pca, explained_var = dr.apply_pca(X, n_components=5)
    
    # Apply t-SNE
    X_tsne, indices = dr.apply_tsne(X, n_components=2, sample_size=5000)
    
    # Visualize results
    dr.visualize_pca(X_pca, explained_var, df_encoded, save_path='pca_analysis.png')
    dr.visualize_tsne(X_tsne, df_encoded, indices, save_path='tsne_analysis.png')
    
    # Save reduced dataset
    dr.save_reduced_data(X_pca, df_encoded, save_path='reduced_dataset.csv')
    
    print()
    print("="*70)
    print("DIMENSIONALITY REDUCTION COMPLETE")
    print("="*70)
    print()
    print("Summary:")
    print(f"  • Original features: {len(feature_names)}")
    print(f"  • PCA components: {X_pca.shape[1]}")
    print(f"  • Variance explained: {np.sum(explained_var):.2%}")
    print(f"  • Visualizations saved: pca_analysis.png, tsne_analysis.png")
    print(f"  • Reduced dataset saved: reduced_dataset.csv")
    print()
    print("Next Step: Use reduced_dataset.csv for OLAP analysis")
    print("="*70)

if __name__ == "__main__":
    main()
