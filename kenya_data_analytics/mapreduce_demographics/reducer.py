#!/usr/bin/env python3
"""
Reducer for Kenya County Demographics Analysis
Aggregates intermediate key-value pairs from mapper
"""
import sys
from typing import TextIO, Dict, List
from collections import defaultdict


def reducer(input_stream: TextIO = sys.stdin) -> None:
    """
    Aggregate mapper outputs to produce final statistics.
    
    Input: sorted key-value pairs from mapper (key\tvalue)
    
    Outputs:
        - Total population across all counties
        - Total area (sq km)
        - Urban vs Rural population breakdown
        - Male vs Female population breakdown
        - Total households
        - Average literacy rate
        - Average GDP per capita
        - Number of counties processed
        - High literacy counties (>80%)
        - Low literacy counties (<60%)
    """
    current_key: str | None = None
    values: List[float] = []
    
    # Track aggregated results
    results: Dict[str, float] = defaultdict(float)
    high_literacy_counties: List[str] = []
    low_literacy_counties: List[str] = []
    
    def process_key(key: str, vals: List[float]) -> None:
        """Process accumulated values for a key."""
        if key == 'total_population':
            results['total_population'] = sum(vals)
        elif key == 'total_area':
            results['total_area'] = sum(vals)
        elif key == 'total_urban':
            results['total_urban'] = sum(vals)
        elif key == 'total_rural':
            results['total_rural'] = sum(vals)
        elif key == 'total_male':
            results['total_male'] = sum(vals)
        elif key == 'total_female':
            results['total_female'] = sum(vals)
        elif key == 'total_households':
            results['total_households'] = sum(vals)
        elif key == 'literacy_sum':
            results['literacy_sum'] = sum(vals)
        elif key == 'literacy_count':
            results['literacy_count'] = sum(vals)
        elif key == 'gdp_sum':
            results['gdp_sum'] = sum(vals)
        elif key == 'gdp_count':
            results['gdp_count'] = sum(vals)
        elif key == 'county_count':
            results['county_count'] = sum(vals)
        elif key == 'high_literacy':
            high_literacy_counties.extend([str(v) for v in vals])
        elif key == 'low_literacy':
            low_literacy_counties.extend([str(v) for v in vals])
    
    # Process input
    for line in input_stream:
        line = line.strip()
        if not line:
            continue
            
        try:
            key, value = line.split('\t', 1)
            
            # New key encountered
            if key != current_key:
                if current_key is not None:
                    process_key(current_key, values)
                current_key = key
                values = []
            
            # Accumulate values (special handling for county lists)
            if key in ['high_literacy', 'low_literacy']:
                values.append(value)
            else:
                values.append(float(value))
                
        except ValueError:
            continue
    
    # Process last key
    if current_key is not None:
        process_key(current_key, values)
    
    # Calculate derived statistics
    avg_literacy = (results['literacy_sum'] / results['literacy_count'] 
                   if results['literacy_count'] > 0 else 0)
    avg_gdp = (results['gdp_sum'] / results['gdp_count']
              if results['gdp_count'] > 0 else 0)
    population_density = (results['total_population'] / results['total_area']
                         if results['total_area'] > 0 else 0)
    urbanization_rate = ((results['total_urban'] / results['total_population'] * 100)
                        if results['total_population'] > 0 else 0)
    gender_ratio = ((results['total_male'] / results['total_female'] * 100)
                   if results['total_female'] > 0 else 0)
    avg_household_size = (results['total_population'] / results['total_households']
                         if results['total_households'] > 0 else 0)
    
    # Output results
    print("=" * 70)
    print("KENYA COUNTY DEMOGRAPHICS - MAPREDUCE ANALYSIS")
    print("=" * 70)
    print(f"\nSUMMARY STATISTICS")
    print(f"{'Counties Processed:':<35} {int(results['county_count']):,}")
    print(f"{'Total Population:':<35} {int(results['total_population']):,}")
    print(f"{'Total Area (sq km):':<35} {results['total_area']:,.2f}")
    print(f"{'Population Density (per sq km):':<35} {population_density:.2f}")
    
    print(f"\nURBAN VS RURAL")
    print(f"{'Urban Population:':<35} {int(results['total_urban']):,}")
    print(f"{'Rural Population:':<35} {int(results['total_rural']):,}")
    print(f"{'Urbanization Rate:':<35} {urbanization_rate:.2f}%")
    
    print(f"\nGENDER DISTRIBUTION")
    print(f"{'Male Population:':<35} {int(results['total_male']):,}")
    print(f"{'Female Population:':<35} {int(results['total_female']):,}")
    print(f"{'Gender Ratio (M per 100 F):':<35} {gender_ratio:.2f}")
    
    print(f"\nHOUSEHOLDS")
    print(f"{'Total Households:':<35} {int(results['total_households']):,}")
    print(f"{'Average Household Size:':<35} {avg_household_size:.2f}")
    
    print(f"\nEDUCATION & ECONOMY")
    print(f"{'Average Literacy Rate:':<35} {avg_literacy:.2f}%")
    print(f"{'Average GDP per Capita (KSh):':<35} {avg_gdp:,.2f}")
    
    if high_literacy_counties:
        print(f"\nHIGH LITERACY COUNTIES (>80%)")
        for county_info in sorted(high_literacy_counties, 
                                 key=lambda x: float(x.split(':')[1]), 
                                 reverse=True):
            county_name, rate = county_info.split(':')
            print(f"  - {county_name:<30} {rate}%")
    
    if low_literacy_counties:
        print(f"\nLOW LITERACY COUNTIES (<60%)")
        for county_info in sorted(low_literacy_counties, 
                                 key=lambda x: float(x.split(':')[1])):
            county_name, rate = county_info.split(':')
            print(f"  - {county_name:<30} {rate}%")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    reducer()
