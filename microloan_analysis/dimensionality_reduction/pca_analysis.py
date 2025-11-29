#!/usr/bin/env python3
"""
Dimensionality Reduction for Microloan Data using PCA
Compresses 500 features into principal components
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import time
import warnings
warnings.filterwarnings('ignore')

class DimensionalityReducer:
    """Apply PCA to compress microloan dataset."""
    
    def __init__(self, n_components=10):
        self.n_components = n_components
        self.pca = None
        self.scaler = None
        self.results = {}
        
    def load_data(self, filepath):
        """Load microloan dataset."""
        print(f"Loading data from: {filepath}")
        start = time.time()
        df = pd.read_csv(filepath)
        elapsed = time.time() - start
        print(f"✅ Loaded {df.shape[0]:,} rows × {df.shape[1]} columns in {elapsed:.2f}s")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
        return df
    
    def preprocess_data(self, df):
        """Prepare data for PCA."""
        print("Preprocessing data...")
        
        # Separate features and target
        X = df.drop('loan_default', axis=1)
        y = df['loan_default']
        
        # Encode categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"Encoding {len(categorical_cols)} categorical columns...")
            le = LabelEncoder()
            for col in categorical_cols:
                X[col] = le.fit_transform(X[col].astype(str))
        
        # Handle missing values
        if X.isnull().any().any():
            print("Filling missing values with median...")
            X = X.fillna(X.median())
        
        print(f"✅ Preprocessed: {X.shape[0]:,} samples, {X.shape[1]} features\n")
        return X, y
    
    def apply_pca(self, X, variance_threshold=0.95):
        """Apply PCA to reduce dimensionality."""
        print("="*70)
        print("PRINCIPAL COMPONENT ANALYSIS (PCA)")
        print("="*70)
        
        # Standardize features
        print("Standardizing features...")
        start = time.time()
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        elapsed = time.time() - start
        print(f"✅ Standardization completed in {elapsed:.2f}s\n")
        
        # Apply PCA to determine number of components for variance threshold
        print(f"Determining components needed for {variance_threshold*100:.0f}% variance...")
        pca_full = PCA()
        pca_full.fit(X_scaled)
        
        cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)
        n_components_95 = np.argmax(cumulative_variance >= variance_threshold) + 1
        
        print(f"Components needed for {variance_threshold*100:.0f}% variance: {n_components_95}")
        print(f"Components for analysis: {self.n_components}\n")
        
        # Apply PCA with specified components
        print(f"Applying PCA with {self.n_components} components...")
        start = time.time()
        self.pca = PCA(n_components=self.n_components)
        X_pca = self.pca.fit_transform(X_scaled)
        elapsed = time.time() - start
        
        # Calculate metrics
        variance_explained = self.pca.explained_variance_ratio_
        cumulative_variance_n = np.sum(variance_explained)
        
        print(f"✅ PCA completed in {elapsed:.2f}s")
        print(f"\nVariance explained by {self.n_components} components: {cumulative_variance_n*100:.2f}%")
        print(f"Original dimensions: {X.shape[1]}")
        print(f"Reduced dimensions: {X_pca.shape[1]}")
        print(f"Compression ratio: {(1 - X_pca.shape[1]/X.shape[1])*100:.1f}%\n")
        
        # Display variance per component
        print(f"Variance explained by each component:")
        print("-" * 70)
        for i, var in enumerate(variance_explained, 1):
            cum_var = np.sum(variance_explained[:i])
            print(f"PC{i:2d}: {var*100:6.2f}% (Cumulative: {cum_var*100:6.2f}%)")
        
        # Store results
        self.results['original_features'] = X.shape[1]
        self.results['pca_components'] = self.n_components
        self.results['variance_explained'] = cumulative_variance_n
        self.results['compression_ratio'] = (1 - X_pca.shape[1]/X.shape[1])
        self.results['components_for_95pct'] = n_components_95
        
        return X_pca, X_scaled, pca_full
    
    def compare_model_performance(self, X_original, X_pca, y):
        """Compare model performance on original vs PCA-transformed data."""
        print("\n" + "="*70)
        print("MODEL PERFORMANCE COMPARISON")
        print("="*70)
        
        # Split data
        print("Splitting data (80% train, 20% test)...")
        X_orig_train, X_orig_test, y_train, y_test = train_test_split(
            X_original, y, test_size=0.2, random_state=42, stratify=y
        )
        X_pca_train, X_pca_test, _, _ = train_test_split(
            X_pca, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training samples: {X_orig_train.shape[0]:,}")
        print(f"Test samples: {X_orig_test.shape[0]:,}\n")
        
        # Train on original data
        print("Training Random Forest on ORIGINAL data...")
        print("(This may take several minutes for large datasets...)")
        start_orig = time.time()
        rf_orig = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        rf_orig.fit(X_orig_train, y_train)
        train_time_orig = time.time() - start_orig
        
        print("Predicting on test set...")
        start_pred_orig = time.time()
        y_pred_orig = rf_orig.predict(X_orig_test)
        y_pred_proba_orig = rf_orig.predict_proba(X_orig_test)[:, 1]
        pred_time_orig = time.time() - start_pred_orig
        
        acc_orig = accuracy_score(y_test, y_pred_orig)
        auc_orig = roc_auc_score(y_test, y_pred_proba_orig)
        
        print(f"✅ Original data - Training: {train_time_orig:.2f}s, Prediction: {pred_time_orig:.2f}s")
        print(f"   Accuracy: {acc_orig:.4f}, AUC-ROC: {auc_orig:.4f}\n")
        
        # Train on PCA data
        print(f"Training Random Forest on PCA data ({self.n_components} components)...")
        start_pca = time.time()
        rf_pca = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        rf_pca.fit(X_pca_train, y_train)
        train_time_pca = time.time() - start_pca
        
        print("Predicting on test set...")
        start_pred_pca = time.time()
        y_pred_pca = rf_pca.predict(X_pca_test)
        y_pred_proba_pca = rf_pca.predict_proba(X_pca_test)[:, 1]
        pred_time_pca = time.time() - start_pred_pca
        
        acc_pca = accuracy_score(y_test, y_pred_pca)
        auc_pca = roc_auc_score(y_test, y_pred_proba_pca)
        
        print(f"✅ PCA data - Training: {train_time_pca:.2f}s, Prediction: {pred_time_pca:.2f}s")
        print(f"   Accuracy: {acc_pca:.4f}, AUC-ROC: {auc_pca:.4f}\n")
        
        # Calculate improvements
        speed_improvement_train = ((train_time_orig - train_time_pca) / train_time_orig) * 100
        speed_improvement_pred = ((pred_time_orig - pred_time_pca) / pred_time_orig) * 100
        accuracy_change = ((acc_pca - acc_orig) / acc_orig) * 100
        
        # Display comparison table
        print("="*70)
        print("PERFORMANCE COMPARISON SUMMARY")
        print("="*70)
        print(f"{'Metric':<30} {'Original':<15} {'PCA':<15} {'Change':<15}")
        print("-" * 70)
        print(f"{'Features':<30} {X_original.shape[1]:<15} {X_pca.shape[1]:<15} {'-'}")
        print(f"{'Training Time (s)':<30} {train_time_orig:<15.2f} {train_time_pca:<15.2f} {speed_improvement_train:+.1f}%")
        print(f"{'Prediction Time (s)':<30} {pred_time_orig:<15.2f} {pred_time_pca:<15.2f} {speed_improvement_pred:+.1f}%")
        print(f"{'Accuracy':<30} {acc_orig:<15.4f} {acc_pca:<15.4f} {accuracy_change:+.2f}%")
        print(f"{'AUC-ROC':<30} {auc_orig:<15.4f} {auc_pca:<15.4f} {'-'}")
        print("="*70)
        
        # Store results
        self.results['original_accuracy'] = acc_orig
        self.results['pca_accuracy'] = acc_pca
        self.results['original_auc'] = auc_orig
        self.results['pca_auc'] = auc_pca
        self.results['train_time_orig'] = train_time_orig
        self.results['train_time_pca'] = train_time_pca
        self.results['speed_improvement'] = speed_improvement_train
        self.results['accuracy_change'] = accuracy_change
        
        return {
            'original': {'accuracy': acc_orig, 'auc': auc_orig, 'train_time': train_time_orig},
            'pca': {'accuracy': acc_pca, 'auc': auc_pca, 'train_time': train_time_pca}
        }
    
    def visualize_pca_results(self, pca_full, output_file='pca_analysis.png'):
        """Create visualizations of PCA results."""
        print("\nCreating PCA visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('PCA Dimensionality Reduction Analysis', fontsize=16, fontweight='bold')
        
        # 1. Scree plot
        ax1 = axes[0, 0]
        variance_ratios = pca_full.explained_variance_ratio_[:50]
        ax1.plot(range(1, len(variance_ratios)+1), variance_ratios, 'bo-', linewidth=2, markersize=6)
        ax1.axvline(x=self.n_components, color='r', linestyle='--', linewidth=2, label=f'{self.n_components} components selected')
        ax1.set_xlabel('Principal Component', fontsize=11)
        ax1.set_ylabel('Variance Explained Ratio', fontsize=11)
        ax1.set_title('Scree Plot (First 50 Components)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 2. Cumulative variance
        ax2 = axes[0, 1]
        cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)
        ax2.plot(range(1, len(cumulative_variance[:100])+1), cumulative_variance[:100], 'go-', linewidth=2, markersize=4)
        ax2.axhline(y=0.95, color='r', linestyle='--', linewidth=2, label='95% variance threshold')
        ax2.axvline(x=self.n_components, color='orange', linestyle='--', linewidth=2, label=f'{self.n_components} components')
        ax2.set_xlabel('Number of Components', fontsize=11)
        ax2.set_ylabel('Cumulative Variance Explained', fontsize=11)
        ax2.set_title('Cumulative Variance Explained (First 100 Components)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 3. Variance bar chart for selected components
        ax3 = axes[1, 0]
        variance_selected = pca_full.explained_variance_ratio_[:self.n_components]
        bars = ax3.bar(range(1, self.n_components+1), variance_selected, 
                      color=plt.cm.viridis(np.linspace(0.3, 0.9, self.n_components)))
        ax3.set_xlabel('Principal Component', fontsize=11)
        ax3.set_ylabel('Variance Explained', fontsize=11)
        ax3.set_title(f'Variance Explained by Top {self.n_components} Components', fontsize=12, fontweight='bold')
        ax3.set_xticks(range(1, self.n_components+1))
        ax3.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{variance_selected[i]*100:.1f}%',
                    ha='center', va='bottom', fontsize=8)
        
        # 4. Component comparison
        ax4 = axes[1, 1]
        n_components_95 = self.results.get('components_for_95pct', 0)
        categories = ['Original\nFeatures', f'{self.n_components}\nComponents\n(Selected)', 
                     f'{n_components_95}\nComponents\n(95% var)']
        values = [self.results['original_features'], self.n_components, n_components_95]
        colors_bar = ['#e74c3c', '#3498db', '#2ecc71']
        
        bars = ax4.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
        ax4.set_ylabel('Number of Features/Components', fontsize=11)
        ax4.set_title('Dimensionality Comparison', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_file}")
        plt.close()
    
    def save_pca_dataset(self, X_pca, y, output_file='microloan_pca_components.csv'):
        """Save PCA-transformed dataset."""
        print(f"\nSaving PCA-transformed dataset...")
        
        # Create DataFrame
        columns = [f'PC{i+1}' for i in range(X_pca.shape[1])]
        df_pca = pd.DataFrame(X_pca, columns=columns)
        df_pca['loan_default'] = y.values
        
        # Save
        df_pca.to_csv(output_file, index=False)
        
        file_size = df_pca.memory_usage(deep=True).sum() / 1024**2
        print(f"✅ Saved: {output_file}")
        print(f"   Shape: {df_pca.shape[0]:,} rows × {df_pca.shape[1]} columns")
        print(f"   Size: {file_size:.2f} MB")
        
        return df_pca

def main():
    """Main dimensionality reduction pipeline."""
    print("="*70)
    print("MICROLOAN DATA - PCA DIMENSIONALITY REDUCTION")
    print("="*70)
    print()
    
    # Initialize
    reducer = DimensionalityReducer(n_components=10)
    
    # Load data
    df = reducer.load_data('../data/microloan_transactions.csv')
    
    # Preprocess
    X, y = reducer.preprocess_data(df)
    
    # Apply PCA
    X_pca, X_scaled, pca_full = reducer.apply_pca(X)
    
    # Compare model performance
    performance = reducer.compare_model_performance(X_scaled, X_pca, y)
    
    # Visualize
    reducer.visualize_pca_results(pca_full)
    
    # Save PCA dataset
    df_pca = reducer.save_pca_dataset(X_pca, y)
    
    # Final summary
    print("\n" + "="*70)
    print("✅ DIMENSIONALITY REDUCTION COMPLETE")
    print("="*70)
    print(f"\nKey Findings:")
    print(f"  - Original features: {reducer.results['original_features']}")
    print(f"  - PCA components: {reducer.results['pca_components']}")
    print(f"  - Variance retained: {reducer.results['variance_explained']*100:.2f}%")
    print(f"  - Compression ratio: {reducer.results['compression_ratio']*100:.1f}%")
    print(f"  - Speed improvement: {reducer.results['speed_improvement']:.1f}%")
    print(f"  - Accuracy change: {reducer.results['accuracy_change']:+.2f}%")
    print(f"\nOutput files:")
    print(f"  - pca_analysis.png (visualizations)")
    print(f"  - microloan_pca_components.csv (PCA dataset)")
    print("="*70)

if __name__ == "__main__":
    main()
