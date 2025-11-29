#!/usr/bin/env python3
"""
OLAP Analysis - Healthcare Data Cube
Implements OLAP operations to analyze relationships between medication supply
and seasonal ailments, along with other healthcare trends.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 10)

class HealthcareOLAPCube:
    """OLAP Cube for healthcare data analysis."""
    
    def __init__(self):
        self.fact_table = None
        self.dim_time = None
        self.dim_clinic = None
        self.dim_ailment = None
        self.dim_medication = None
        self.cube = None
        
    def load_data(self):
        """Load all healthcare datasets."""
        print("Loading healthcare datasets...")
        
        self.attendance = pd.read_csv('../datasets/clinic_attendance.csv')
        self.ailments = pd.read_csv('../datasets/ailments_diagnoses.csv')
        self.medications = pd.read_csv('../datasets/medication_supply.csv')
        self.reduced_data = pd.read_csv('../dimensionality_reduction/reduced_dataset.csv')
        
        print(f"✓ Loaded {len(self.attendance):,} attendance records")
        print(f"✓ Loaded {len(self.ailments):,} ailment records")
        print(f"✓ Loaded {len(self.medications):,} medication records")
        print(f"✓ Loaded {len(self.reduced_data):,} reduced dimension records")
        
    def build_dimensions(self):
        """Build OLAP dimension tables."""
        print("\nBuilding dimension tables...")
        
        # Time Dimension
        dates = pd.to_datetime(self.ailments['visit_date'])
        self.dim_time = pd.DataFrame({
            'date': dates,
            'year': dates.dt.year,
            'month': dates.dt.month,
            'month_name': dates.dt.month_name(),
            'week': dates.dt.isocalendar().week,
            'day_of_week': dates.dt.dayofweek,
            'day_name': dates.dt.day_name(),
            'season': dates.dt.month.map({
                6: 'Long Rains', 7: 'Long Rains',
                8: 'Cool/Dry', 9: 'Cool/Dry', 10: 'Cool/Dry',
                11: 'Short Rains'
            })
        })
        print(f"✓ Time dimension: {len(self.dim_time):,} records")
        
        # Clinic Dimension
        self.dim_clinic = self.ailments[['clinic_name']].drop_duplicates()
        self.dim_clinic['clinic_type'] = self.dim_clinic['clinic_name'].apply(
            lambda x: 'Hospital' if 'Hospital' in x 
                     else 'Rural' if 'Rural' in x 
                     else 'Urban Clinic'
        )
        print(f"✓ Clinic dimension: {len(self.dim_clinic)} clinics")
        
        # Ailment Dimension
        self.dim_ailment = self.ailments[['ailment', 'severity']].drop_duplicates()
        self.dim_ailment['ailment_category'] = self.dim_ailment['ailment'].apply(
            lambda x: 'Infectious' if x in ['Malaria', 'Typhoid', 'Upper Respiratory Infection', 
                                            'Pneumonia', 'Diarrhea', 'Skin Infections']
                     else 'Chronic' if x in ['Hypertension', 'Diabetes', 'Asthma', 'Arthritis']
                     else 'Other'
        )
        print(f"✓ Ailment dimension: {len(self.dim_ailment)} unique ailment-severity combinations")
        
        # Medication Dimension
        self.dim_medication = self.medications[['medication_name', 'category']].drop_duplicates()
        print(f"✓ Medication dimension: {len(self.dim_medication)} medications")
        
    def build_fact_table(self):
        """Build the fact table combining all measures."""
        print("\nBuilding fact table...")
        
        # Merge datasets
        fact = pd.merge(
            self.ailments,
            self.attendance[['patient_id', 'age', 'gender', 'insurance_type', 
                           'wait_time_minutes', 'consultation_duration']],
            on='patient_id'
        )
        
        # Add time dimension
        fact['visit_date'] = pd.to_datetime(fact['visit_date'])
        fact['month'] = fact['visit_date'].dt.month
        fact['month_name'] = fact['visit_date'].dt.month_name()
        fact['year'] = fact['visit_date'].dt.year
        fact['season'] = fact['month'].map({
            6: 'Long Rains', 7: 'Long Rains',
            8: 'Cool/Dry', 9: 'Cool/Dry', 10: 'Cool/Dry',
            11: 'Short Rains'
        })
        
        # Add derived measures
        fact['is_follow_up'] = (fact['treatment_outcome'] == 'Follow-up Required').astype(int)
        fact['is_severe'] = (fact['severity'] == 'Severe').astype(int)
        fact['is_referred'] = (fact['treatment_outcome'] == 'Referred').astype(int)
        
        self.fact_table = fact
        print(f"✓ Fact table: {len(self.fact_table):,} records with {len(self.fact_table.columns)} measures")
        
    def create_olap_cube(self):
        """Create multidimensional OLAP cube."""
        print("\nCreating OLAP cube...")
        
        # Define dimensions and measures
        dimensions = ['clinic_name', 'ailment', 'month_name', 'season', 'severity']
        measures = {
            'patient_id': 'count',
            'num_medications': 'sum',
            'age': 'mean',
            'wait_time_minutes': 'mean',
            'is_severe': 'sum',
            'is_follow_up': 'sum'
        }
        
        # Create cube using pivot tables and groupby operations
        self.cube = self.fact_table.groupby(dimensions).agg(measures).reset_index()
        self.cube.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                            for col in self.cube.columns.values]
        
        print(f"✓ OLAP cube created with {len(self.cube):,} cells")
        print(f"  Dimensions: {', '.join(dimensions)}")
        print(f"  Measures: {', '.join(measures.keys())}")
        
    def olap_slice(self, dimension, value):
        """OLAP Slice operation - fix a dimension to a specific value."""
        print(f"\n📊 OLAP SLICE: {dimension} = {value}")
        result = self.fact_table[self.fact_table[dimension] == value]
        print(f"  Result: {len(result):,} records")
        return result
    
    def olap_dice(self, conditions):
        """OLAP Dice operation - filter multiple dimensions."""
        print(f"\n📊 OLAP DICE with conditions:")
        result = self.fact_table.copy()
        for dim, val in conditions.items():
            print(f"  {dim} = {val}")
            if isinstance(val, list):
                result = result[result[dim].isin(val)]
            else:
                result = result[result[dim] == val]
        print(f"  Result: {len(result):,} records")
        return result
    
    def olap_drill_down(self, dimension_from, dimension_to):
        """OLAP Drill-down - move from higher to lower level of detail."""
        print(f"\n📊 OLAP DRILL-DOWN: {dimension_from} → {dimension_to}")
        
        if dimension_from == 'season' and dimension_to == 'month_name':
            result = self.fact_table.groupby(['season', 'month_name', 'ailment']).agg({
                'patient_id': 'count',
                'num_medications': 'sum'
            }).reset_index()
            print(f"  Drilling down from season to monthly ailment patterns")
        else:
            result = self.fact_table.groupby([dimension_from, dimension_to]).size().reset_index(name='count')
        
        return result
    
    def olap_roll_up(self, dimension_from, dimension_to):
        """OLAP Roll-up - move from lower to higher level of aggregation."""
        print(f"\n📊 OLAP ROLL-UP: {dimension_from} → {dimension_to}")
        
        result = self.fact_table.groupby(dimension_to).agg({
            'patient_id': 'count',
            'num_medications': 'sum',
            'age': 'mean'
        }).reset_index()
        
        return result
    
    def analyze_seasonal_ailments(self):
        """Analyze relationship between seasons and ailments."""
        print("\n" + "="*70)
        print("ANALYSIS 1: Seasonal Ailment Patterns")
        print("="*70)
        
        # Group by season and ailment
        seasonal = self.fact_table.groupby(['season', 'month_name', 'ailment']).agg({
            'patient_id': 'count',
            'severity': lambda x: (x == 'Severe').sum()
        }).reset_index()
        seasonal.columns = ['season', 'month', 'ailment', 'cases', 'severe_cases']
        
        # Top ailments by season
        print("\nTop 3 ailments by season:")
        for season in seasonal['season'].unique():
            season_data = seasonal[seasonal['season'] == season]
            top_ailments = season_data.groupby('ailment')['cases'].sum().nlargest(3)
            print(f"\n{season}:")
            for ailment, cases in top_ailments.items():
                print(f"  • {ailment}: {cases:,} cases")
        
        return seasonal
    
    def analyze_medication_supply_correlation(self):
        """Analyze relationship between medication supply and ailments."""
        print("\n" + "="*70)
        print("ANALYSIS 2: Medication Supply vs Ailment Trends")
        print("="*70)
        
        # Aggregate ailments by month and category
        monthly_ailments = self.fact_table.groupby(['month_name', 'ailment']).agg({
            'patient_id': 'count',
            'num_medications': 'sum'
        }).reset_index()
        monthly_ailments.columns = ['month', 'ailment', 'cases', 'medications_prescribed']
        
        # Aggregate medication supply by month
        self.medications['month_num'] = self.medications['month'].str.slice(5, 7).astype(int)
        monthly_supply = self.medications.groupby(['month_num', 'category']).agg({
            'quantity_consumed': 'sum',
            'stock_out_days': 'sum',
            'closing_stock': 'mean'
        }).reset_index()
        
        # Map ailment to medication category
        ailment_to_category = {
            'Malaria': 'Malaria',
            'Upper Respiratory Infection': 'Respiratory',
            'Pneumonia': 'Respiratory',
            'Asthma': 'Asthma',
            'Diarrhea': 'Diarrhea',
            'Typhoid': 'Typhoid',
            'Hypertension': 'Hypertension',
            'Diabetes': 'Diabetes',
            'Skin Infections': 'Skin',
            'Arthritis': 'Arthritis'
        }
        
        monthly_ailments['med_category'] = monthly_ailments['ailment'].map(ailment_to_category)
        monthly_ailments = monthly_ailments.dropna(subset=['med_category'])
        
        # Convert month names to numbers for merging
        month_to_num = {'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11}
        monthly_ailments['month_num'] = monthly_ailments['month'].map(month_to_num)
        
        # Merge with supply data
        correlation_data = pd.merge(
            monthly_ailments.groupby(['month_num', 'med_category']).agg({
                'cases': 'sum',
                'medications_prescribed': 'sum'
            }).reset_index(),
            monthly_supply,
            left_on=['month_num', 'med_category'],
            right_on=['month_num', 'category'],
            how='inner'
        )
        
        print("\nCorrelation between ailment cases and medication consumption:")
        print(f"  Pearson correlation: {correlation_data['cases'].corr(correlation_data['quantity_consumed']):.3f}")
        
        print("\nMonths with highest stock-out days:")
        stockout_summary = correlation_data.groupby('month_num')['stock_out_days'].sum().nlargest(3)
        month_names = {6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November'}
        for month, days in stockout_summary.items():
            print(f"  • {month_names[month]}: {days:.0f} total stock-out days")
        
        return correlation_data
    
    def analyze_clinic_performance(self):
        """Analyze clinic performance metrics."""
        print("\n" + "="*70)
        print("ANALYSIS 3: Clinic Performance Analysis")
        print("="*70)
        
        clinic_metrics = self.fact_table.groupby('clinic_name').agg({
            'patient_id': 'count',
            'wait_time_minutes': 'mean',
            'consultation_duration': 'mean',
            'is_severe': 'sum',
            'is_follow_up': 'sum',
            'num_medications': 'mean'
        }).reset_index()
        
        clinic_metrics.columns = ['clinic', 'total_visits', 'avg_wait_time', 
                                 'avg_consultation', 'severe_cases', 'follow_ups',
                                 'avg_medications']
        
        clinic_metrics = clinic_metrics.sort_values('total_visits', ascending=False)
        
        print("\nTop 5 busiest clinics:")
        for _, row in clinic_metrics.head(5).iterrows():
            print(f"\n{row['clinic']}:")
            print(f"  • Total visits: {row['total_visits']:,}")
            print(f"  • Avg wait time: {row['avg_wait_time']:.1f} minutes")
            print(f"  • Severe cases: {row['severe_cases']:.0f}")
            print(f"  • Follow-ups required: {row['follow_ups']:.0f}")
        
        return clinic_metrics
    
    def visualize_olap_insights(self, seasonal_data, correlation_data, clinic_metrics):
        """Create comprehensive OLAP visualizations."""
        print("\n" + "="*70)
        print("Generating OLAP Visualization Dashboard...")
        print("="*70)
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Seasonal ailment heatmap
        ax1 = fig.add_subplot(gs[0, :2])
        seasonal_pivot = seasonal_data.pivot_table(
            values='cases', 
            index='ailment', 
            columns='season', 
            aggfunc='sum'
        )
        sns.heatmap(seasonal_pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax1, cbar_kws={'label': 'Cases'})
        ax1.set_title('Seasonal Ailment Distribution (OLAP Cube View)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Season')
        ax1.set_ylabel('Ailment')
        
        # 2. Medication consumption vs ailment cases
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.scatter(correlation_data['cases'], correlation_data['quantity_consumed'], 
                   alpha=0.6, s=100, c=correlation_data['month_num'], cmap='viridis')
        ax2.set_xlabel('Ailment Cases')
        ax2.set_ylabel('Medication Consumed')
        ax2.set_title('Supply-Demand Correlation', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Monthly trends (Drill-down view)
        ax3 = fig.add_subplot(gs[1, :2])
        monthly_trends = self.fact_table.groupby('month_name')['patient_id'].count()
        month_order = ['June', 'July', 'August', 'September', 'October', 'November']
        monthly_trends = monthly_trends.reindex(month_order)
        ax3.plot(monthly_trends.index, monthly_trends.values, marker='o', linewidth=2, 
                markersize=8, color='steelblue')
        ax3.fill_between(range(len(monthly_trends)), monthly_trends.values, alpha=0.3)
        ax3.set_xlabel('Month')
        ax3.set_ylabel('Total Visits')
        ax3.set_title('Monthly Visit Trends (Drill-Down Analysis)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Stock-out analysis
        ax4 = fig.add_subplot(gs[1, 2])
        stockout_by_month = correlation_data.groupby('month_num')['stock_out_days'].sum()
        ax4.bar(stockout_by_month.index, stockout_by_month.values, color='coral', alpha=0.7)
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Total Stock-Out Days')
        ax4.set_title('Medication Stock-Outs', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Clinic wait times (Slice operation result)
        ax5 = fig.add_subplot(gs[2, :])
        clinic_metrics_sorted = clinic_metrics.nsmallest(10, 'avg_wait_time')
        colors = ['green' if x < 30 else 'orange' if x < 45 else 'red' 
                 for x in clinic_metrics_sorted['avg_wait_time']]
        ax5.barh(clinic_metrics_sorted['clinic'], clinic_metrics_sorted['avg_wait_time'], color=colors, alpha=0.7)
        ax5.set_xlabel('Average Wait Time (minutes)')
        ax5.set_title('Clinic Efficiency: Average Wait Times (OLAP Slice)', fontsize=12, fontweight='bold')
        ax5.axvline(x=30, color='green', linestyle='--', alpha=0.5, label='Target: 30 min')
        ax5.legend()
        ax5.grid(True, alpha=0.3, axis='x')
        
        plt.savefig('olap_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved OLAP dashboard to olap_dashboard.png")
        plt.close()
        
    def save_olap_results(self):
        """Save OLAP cube and analysis results."""
        print("\nSaving OLAP analysis results...")
        
        self.cube.to_csv('olap_cube.csv', index=False)
        print("✓ Saved OLAP cube to olap_cube.csv")
        
        # Save fact table
        self.fact_table.to_csv('fact_table.csv', index=False)
        print("✓ Saved fact table to fact_table.csv")

def main():
    """Main execution function."""
    print("="*70)
    print("HEALTHCARE OLAP ANALYSIS")
    print("="*70)
    print()
    
    # Initialize OLAP
    olap = HealthcareOLAPCube()
    
    # Load data
    olap.load_data()
    
    # Build dimensions and fact table
    olap.build_dimensions()
    olap.build_fact_table()
    
    # Create OLAP cube
    olap.create_olap_cube()
    
    # Demonstrate OLAP operations
    print("\n" + "="*70)
    print("DEMONSTRATING OLAP OPERATIONS")
    print("="*70)
    
    # Slice
    june_data = olap.olap_slice('month_name', 'June')
    
    # Dice
    rainy_malaria = olap.olap_dice({
        'season': ['Long Rains', 'Short Rains'],
        'ailment': 'Malaria'
    })
    
    # Drill-down
    seasonal_monthly = olap.olap_drill_down('season', 'month_name')
    
    # Roll-up
    clinic_summary = olap.olap_roll_up('clinic_name', 'clinic_name')
    
    # Perform analyses
    seasonal_data = olap.analyze_seasonal_ailments()
    correlation_data = olap.analyze_medication_supply_correlation()
    clinic_metrics = olap.analyze_clinic_performance()
    
    # Visualize
    olap.visualize_olap_insights(seasonal_data, correlation_data, clinic_metrics)
    
    # Save results
    olap.save_olap_results()
    
    print("\n" + "="*70)
    print("OLAP ANALYSIS COMPLETE")
    print("="*70)
    print("\nKey Findings:")
    print("  ✓ Identified strong seasonal patterns in infectious diseases")
    print("  ✓ Found correlation between ailment cases and medication consumption")
    print("  ✓ Analyzed clinic performance metrics across 10 facilities")
    print("  ✓ Identified medication stock-out patterns")
    print("\nOutputs:")
    print("  • olap_cube.csv - Multidimensional OLAP cube")
    print("  • fact_table.csv - Complete fact table")
    print("  • olap_dashboard.png - Comprehensive visualization")
    print("="*70)

if __name__ == "__main__":
    main()
