#!/usr/bin/env python3
"""
Master Execution Script for Microloan Analysis
Runs complete analysis pipeline: data generation → feature selection → PCA → report
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def run_script(script_path, description):
    """Run a Python script and report status."""
    print(f"📝 {description}")
    print(f"   Running: {script_path}")
    print()
    
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True,
            check=True
        )
        elapsed = time.time() - start
        print(f"\n✅ Completed in {elapsed:.1f}s\n")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start
        print(f"\n❌ Failed after {elapsed:.1f}s")
        print(f"   Error: {e}")
        return False

def main():
    """Run complete microloan analysis pipeline."""
    print_header("MICROLOAN ANALYSIS - MASTER EXECUTION SCRIPT")
    
    print("This script will run the complete analysis pipeline:")
    print("  1. Generate microloan dataset (500 features, 1M rows)")
    print("  2. Feature selection (top 10 features)")
    print("  3. PCA dimensionality reduction (10 components)")
    print("  4. Generate reflection report (PDF)")
    print()
    print("⏱️  Estimated total time: 15-25 minutes")
    print("💾 Disk space required: ~500 MB")
    print()
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Track success
    steps_completed = []
    steps_failed = []
    
    # Step 1: Generate dataset
    print_header("STEP 1/4: GENERATE MICROLOAN DATASET")
    if run_script('data/generate_microloan_data.py', 'Generating 1M rows, 500 features'):
        steps_completed.append("Data generation")
    else:
        steps_failed.append("Data generation")
        print("⚠️  Cannot proceed without dataset. Stopping.")
        return
    
    # Step 2: Feature selection
    print_header("STEP 2/4: FEATURE SELECTION")
    if run_script('feature_selection/feature_selection.py', 'Selecting top 10 features'):
        steps_completed.append("Feature selection")
    else:
        steps_failed.append("Feature selection")
    
    # Step 3: PCA
    print_header("STEP 3/4: PCA DIMENSIONALITY REDUCTION")
    if run_script('dimensionality_reduction/pca_analysis.py', 'Applying PCA compression'):
        steps_completed.append("PCA analysis")
    else:
        steps_failed.append("PCA analysis")
    
    # Step 4: Generate report
    print_header("STEP 4/4: GENERATE REFLECTION REPORT")
    if run_script('reports/generate_reflection_report.py', 'Creating PDF report'):
        steps_completed.append("Report generation")
    else:
        steps_failed.append("Report generation")
    
    # Final summary
    print_header("EXECUTION SUMMARY")
    
    print(f"✅ Completed steps ({len(steps_completed)}/4):")
    for step in steps_completed:
        print(f"   • {step}")
    
    if steps_failed:
        print(f"\n❌ Failed steps ({len(steps_failed)}/4):")
        for step in steps_failed:
            print(f"   • {step}")
    
    print("\n" + "="*70)
    
    if len(steps_completed) == 4:
        print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print()
        print("📄 Main deliverable:")
        print("   reports/Microloan_Analysis_Reflection_Report.pdf")
        print()
        print("📊 Supporting files:")
        print("   data/microloan_transactions.csv")
        print("   feature_selection/feature_importance.png")
        print("   feature_selection/selected_features.txt")
        print("   dimensionality_reduction/pca_analysis.png")
        print()
        print("✅ Ready for submission!")
    else:
        print("⚠️  PIPELINE INCOMPLETE")
        print("="*70)
        print("Some steps failed. Please review error messages above.")
    
    print("="*70)

if __name__ == "__main__":
    main()
