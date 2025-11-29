#!/usr/bin/env python3
"""
Feature Selection for Microloan Default Prediction
Selects top 10 features most strongly correlated with loan default
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.preprocessing import LabelEncoder
import time
import warnings
warnings.filterwarnings('ignore')

class FeatureSelector:
    """Select top features for loan default prediction."""
    
    def __init__(self, n_features=10):
        self.n_features = n_features
        self.selected_features = None
        self.feature_scores = None
        
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
        """Prepare data for feature selection."""
        print("Preprocessing data...")
        
        # Separate features and target
        if 'loan_default' not in df.columns:
            raise ValueError("Target variable 'loan_default' not found")
        
        X = df.drop('loan_default', axis=1)
        y = df['loan_default']
        
        # Encode categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        print(f"Encoding {len(categorical_cols)} categorical columns...")
        
        le = LabelEncoder()
        for col in categorical_cols:
            X[col] = le.fit_transform(X[col].astype(str))
        
        # Handle any missing values
        if X.isnull().any().any():
            print("Filling missing values with median...")
            X = X.fillna(X.median())
        
        print(f"✅ Preprocessed: {X.shape[0]:,} samples, {X.shape[1]} features\n")
        return X, y
    
    def correlation_analysis(self, X, y):
        """Analyze correlation between features and target."""
        print("="*70)
        print("METHOD 1: CORRELATION ANALYSIS")
        print("="*70)
        
        # Combine X and y for correlation
        df_corr = X.copy()
        df_corr['loan_default'] = y
        
        # Calculate correlation with target
        print("Calculating correlations...")
        correlations = df_corr.corr()['loan_default'].drop('loan_default')
        correlations_abs = correlations.abs().sort_values(ascending=False)
        
        top_features = correlations_abs.head(self.n_features)
        
        print(f"\nTop {self.n_features} features by absolute correlation:")
        print("-" * 70)
        for i, (feature, score) in enumerate(top_features.items(), 1):
            corr_value = correlations[feature]
            print(f"{i:2d}. {feature:40s} {corr_value:+.4f} (|r| = {score:.4f})")
        
        return top_features.index.tolist(), top_features.to_dict()
    
    def mutual_information_analysis(self, X, y):
        """Analyze mutual information between features and target."""
        print("\n" + "="*70)
        print("METHOD 2: MUTUAL INFORMATION")
        print("="*70)
        
        print("Calculating mutual information scores...")
        start = time.time()
        
        # Calculate mutual information
        mi_scores = mutual_info_classif(X, y, random_state=42)
        elapsed = time.time() - start
        
        # Create series with feature names
        mi_series = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
        top_features = mi_series.head(self.n_features)
        
        print(f"✅ Completed in {elapsed:.2f}s\n")
        print(f"Top {self.n_features} features by mutual information:")
        print("-" * 70)
        for i, (feature, score) in enumerate(top_features.items(), 1):
            print(f"{i:2d}. {feature:40s} {score:.6f}")
        
        return top_features.index.tolist(), top_features.to_dict()
    
    def random_forest_importance(self, X, y):
        """Use Random Forest feature importance."""
        print("\n" + "="*70)
        print("METHOD 3: RANDOM FOREST FEATURE IMPORTANCE")
        print("="*70)
        
        print("Training Random Forest classifier...")
        print("(This may take a few minutes for large datasets...)")
        start = time.time()
        
        # Train Random Forest
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        rf.fit(X, y)
        elapsed = time.time() - start
        
        # Get feature importances
        importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
        top_features = importances.head(self.n_features)
        
        print(f"✅ Training completed in {elapsed:.2f}s\n")
        print(f"Top {self.n_features} features by Random Forest importance:")
        print("-" * 70)
        for i, (feature, score) in enumerate(top_features.items(), 1):
            print(f"{i:2d}. {feature:40s} {score:.6f}")
        
        return top_features.index.tolist(), top_features.to_dict()
    
    def anova_f_test(self, X, y):
        """Use ANOVA F-test for feature selection."""
        print("\n" + "="*70)
        print("METHOD 4: ANOVA F-TEST")
        print("="*70)
        
        print("Calculating ANOVA F-scores...")
        start = time.time()
        
        # Calculate F-scores
        f_scores, p_values = f_classif(X, y)
        elapsed = time.time() - start
        
        # Create series with feature names
        f_series = pd.Series(f_scores, index=X.columns).sort_values(ascending=False)
        top_features = f_series.head(self.n_features)
        
        print(f"✅ Completed in {elapsed:.2f}s\n")
        print(f"Top {self.n_features} features by F-score:")
        print("-" * 70)
        for i, (feature, score) in enumerate(top_features.items(), 1):
            p_val = p_values[X.columns.get_loc(feature)]
            print(f"{i:2d}. {feature:40s} F={score:.2f} (p={p_val:.2e})")
        
        return top_features.index.tolist(), top_features.to_dict()
    
    def consensus_selection(self, methods_results):
        """Select features appearing most frequently across methods."""
        print("\n" + "="*70)
        print("CONSENSUS FEATURE SELECTION")
        print("="*70)
        
        # Count feature appearances
        feature_counts = {}
        for method_name, (features, scores) in methods_results.items():
            for feature in features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        # Sort by frequency
        sorted_features = sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nFeature selection frequency across {len(methods_results)} methods:")
        print("-" * 70)
        print(f"{'Feature':<45} {'Appears in N methods':<20}")
        print("-" * 70)
        
        final_features = []
        for feature, count in sorted_features[:self.n_features]:
            print(f"{feature:<45} {count}/{len(methods_results)}")
            final_features.append(feature)
        
        # If we don't have enough features, add from first method
        if len(final_features) < self.n_features:
            first_method_features = list(methods_results.values())[0][0]
            for feature in first_method_features:
                if feature not in final_features:
                    final_features.append(feature)
                    if len(final_features) >= self.n_features:
                        break
        
        self.selected_features = final_features[:self.n_features]
        return self.selected_features
    
    def visualize_feature_importance(self, methods_results, output_file='feature_importance.png'):
        """Create visualization of feature importance across methods."""
        print(f"\nCreating feature importance visualization...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Feature Importance Analysis - Multiple Methods', fontsize=16, fontweight='bold')
        
        methods = list(methods_results.keys())
        axes_flat = axes.flatten()
        
        for idx, (method_name, (features, scores)) in enumerate(methods_results.items()):
            ax = axes_flat[idx]
            
            # Create bar plot
            features_list = features[:self.n_features]
            scores_list = [scores[f] for f in features_list]
            
            y_pos = np.arange(len(features_list))
            bars = ax.barh(y_pos, scores_list, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(features_list))))
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(features_list, fontsize=8)
            ax.invert_yaxis()
            ax.set_xlabel('Score', fontsize=10)
            ax.set_title(method_name, fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, (bar, score) in enumerate(zip(bars, scores_list)):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f'{score:.4f}', ha='left', va='center', fontsize=7, 
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_file}")
        plt.close()
    
    def save_selected_features(self, output_file='selected_features.txt'):
        """Save selected features to file."""
        if self.selected_features is None:
            print("No features selected yet!")
            return
        
        with open(output_file, 'w') as f:
            f.write("TOP 10 SELECTED FEATURES FOR LOAN DEFAULT PREDICTION\n")
            f.write("="*70 + "\n\n")
            for i, feature in enumerate(self.selected_features, 1):
                f.write(f"{i:2d}. {feature}\n")
        
        print(f"✅ Selected features saved: {output_file}")
    
    def create_reduced_dataset(self, df, output_file='microloan_top10_features.csv'):
        """Create dataset with only selected features."""
        if self.selected_features is None:
            print("No features selected yet!")
            return
        
        print(f"\nCreating reduced dataset with top {self.n_features} features...")
        
        # Include selected features + target
        columns_to_keep = self.selected_features + ['loan_default']
        df_reduced = df[columns_to_keep]
        
        # Save
        df_reduced.to_csv(output_file, index=False)
        
        original_size = df.memory_usage(deep=True).sum() / 1024**2
        reduced_size = df_reduced.memory_usage(deep=True).sum() / 1024**2
        reduction_pct = (1 - reduced_size/original_size) * 100
        
        print(f"Original dataset: {df.shape[1]} features, {original_size:.2f} MB")
        print(f"Reduced dataset:  {df_reduced.shape[1]} features, {reduced_size:.2f} MB")
        print(f"Size reduction:   {reduction_pct:.1f}%")
        print(f"✅ Saved: {output_file}")
        
        return df_reduced

def main():
    """Main feature selection pipeline."""
    print("="*70)
    print("MICROLOAN FEATURE SELECTION - TOP 10 FEATURES")
    print("="*70)
    print()
    
    # Initialize
    selector = FeatureSelector(n_features=10)
    
    # Load data
    df = selector.load_data('../data/microloan_transactions.csv')
    
    # Preprocess
    X, y = selector.preprocess_data(df)
    
    # Apply multiple feature selection methods
    methods_results = {}
    
    # Method 1: Correlation
    features_corr, scores_corr = selector.correlation_analysis(X, y)
    methods_results['Correlation Analysis'] = (features_corr, scores_corr)
    
    # Method 2: Mutual Information
    features_mi, scores_mi = selector.mutual_information_analysis(X, y)
    methods_results['Mutual Information'] = (features_mi, scores_mi)
    
    # Method 3: Random Forest
    features_rf, scores_rf = selector.random_forest_importance(X, y)
    methods_results['Random Forest Importance'] = (features_rf, scores_rf)
    
    # Method 4: ANOVA F-test
    features_anova, scores_anova = selector.anova_f_test(X, y)
    methods_results['ANOVA F-Test'] = (features_anova, scores_anova)
    
    # Consensus selection
    final_features = selector.consensus_selection(methods_results)
    
    # Visualize
    selector.visualize_feature_importance(methods_results)
    
    # Save results
    selector.save_selected_features()
    df_reduced = selector.create_reduced_dataset(df)
    
    # Final summary
    print("\n" + "="*70)
    print("✅ FEATURE SELECTION COMPLETE")
    print("="*70)
    print(f"\nFinal selected features ({len(final_features)}):")
    for i, feature in enumerate(final_features, 1):
        print(f"  {i:2d}. {feature}")
    print("\nOutput files:")
    print("  - feature_importance.png (visualization)")
    print("  - selected_features.txt (feature list)")
    print("  - microloan_top10_features.csv (reduced dataset)")
    print("="*70)

if __name__ == "__main__":
    main()
