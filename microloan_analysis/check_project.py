#!/usr/bin/env python3
"""
Check if all required files are present in the microloan_analysis project.
This script verifies that all implementation files have been created correctly.
"""

import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    size = ""
    if exists and os.path.isfile(filepath):
        size_bytes = os.path.getsize(filepath)
        if size_bytes < 1024:
            size = f" ({size_bytes} B)"
        elif size_bytes < 1024 * 1024:
            size = f" ({size_bytes / 1024:.1f} KB)"
        else:
            size = f" ({size_bytes / (1024 * 1024):.1f} MB)"
    
    print(f"{status} {description}: {filepath}{size}")
    return exists

def main():
    print("=" * 70)
    print("MICROLOAN ANALYSIS PROJECT - FILE VERIFICATION")
    print("=" * 70)
    print()
    
    # Check implementation files
    print("📝 Implementation Files:")
    impl_files = [
        ("data/generate_microloan_data.py", "Data Generator"),
        ("feature_selection/feature_selection.py", "Feature Selection"),
        ("dimensionality_reduction/pca_analysis.py", "PCA Analysis"),
        ("reports/generate_reflection_report.py", "PDF Report Generator"),
        ("run_analysis.py", "Master Execution Script"),
    ]
    
    impl_count = sum(check_file_exists(f, d) for f, d in impl_files)
    print()
    
    # Check documentation files
    print("📚 Documentation Files:")
    doc_files = [
        ("README.md", "Main Documentation"),
        ("QUICK_START.md", "Quick Start Guide"),
        ("PROJECT_STATUS.md", "Project Status Report"),
    ]
    
    doc_count = sum(check_file_exists(f, d) for f, d in doc_files)
    print()
    
    # Check output files (may not exist yet)
    print("📊 Output Files (generated after running analysis):")
    output_files = [
        ("data/microloan_transactions.csv", "Dataset (1M rows × 500 features)"),
        ("feature_selection/feature_importance.png", "Feature Importance Visualization"),
        ("feature_selection/selected_features.txt", "Top 10 Features List"),
        ("feature_selection/microloan_top10_features.csv", "Reduced Dataset (10 features)"),
        ("dimensionality_reduction/pca_analysis.png", "PCA Variance Visualization"),
        ("dimensionality_reduction/microloan_pca_components.csv", "PCA Dataset (10 components)"),
        ("reports/Microloan_Analysis_Reflection_Report.pdf", "Comprehensive PDF Report"),
    ]
    
    output_count = sum(check_file_exists(f, d) for f, d in output_files)
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Implementation Files: {impl_count}/{len(impl_files)} ✅")
    print(f"Documentation Files: {doc_count}/{len(doc_files)} ✅")
    print(f"Output Files: {output_count}/{len(output_files)}")
    
    if output_count < len(output_files):
        print()
        print("⚠️  Output files not yet generated. Run: python run_analysis.py")
    else:
        print()
        print("✅ All files present! Project is complete.")
    
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    
    if output_count == 0:
        print("1. Run the full analysis: python run_analysis.py")
        print("2. Wait 15-25 minutes for completion")
        print("3. Review the PDF report in reports/")
        print("4. Submit Microloan_Analysis_Reflection_Report.pdf")
    elif output_count < len(output_files):
        print("⚠️  Some output files missing. Consider re-running: python run_analysis.py")
    else:
        print("✅ All files generated successfully!")
        print("✅ Review: reports/Microloan_Analysis_Reflection_Report.pdf")
        print("✅ Ready for submission!")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
