#!/usr/bin/env python3
"""
Mapper for Kenya County Demographics Analysis
Processes county demographic data and emits key-value pairs for reduction
"""
import sys
from typing import TextIO


def mapper(input_stream: TextIO = sys.stdin) -> None:
    """
    Read county demographics CSV and emit intermediate key-value pairs.
    
    Input format: county_code,county_name,population,area_sq_km,urban_pop,rural_pop,
                  male_pop,female_pop,households,literacy_rate,gdp_per_capita
    
    Emits:
        - total_population\t{population}
        - total_area\t{area_sq_km}
        - total_urban\t{urban_population}
        - total_rural\t{rural_population}
        - total_male\t{male_population}
        - total_female\t{female_population}
        - total_households\t{households}
        - literacy_sum\t{literacy_rate}
        - literacy_count\t1
        - gdp_sum\t{gdp_per_capita}
        - gdp_count\t1
        - county_count\t1
        - high_literacy\t{county_name}:{literacy_rate}  (if literacy > 80%)
        - low_literacy\t{county_name}:{literacy_rate}   (if literacy < 60%)
    """
    # Skip header
    next(input_stream, None)
    
    for line in input_stream:
        line = line.strip()
        if not line:
            continue
            
        try:
            parts = line.split(',')
            if len(parts) != 11:
                continue
                
            county_code = parts[0]
            county_name = parts[1]
            population = int(parts[2])
            area_sq_km = float(parts[3])
            urban_pop = int(parts[4])
            rural_pop = int(parts[5])
            male_pop = int(parts[6])
            female_pop = int(parts[7])
            households = int(parts[8])
            literacy_rate = float(parts[9])
            gdp_per_capita = float(parts[10])
            
            # Emit aggregate statistics
            print(f"total_population\t{population}")
            print(f"total_area\t{area_sq_km}")
            print(f"total_urban\t{urban_pop}")
            print(f"total_rural\t{rural_pop}")
            print(f"total_male\t{male_pop}")
            print(f"total_female\t{female_pop}")
            print(f"total_households\t{households}")
            
            # Emit for average calculations
            print(f"literacy_sum\t{literacy_rate}")
            print(f"literacy_count\t1")
            print(f"gdp_sum\t{gdp_per_capita}")
            print(f"gdp_count\t1")
            print(f"county_count\t1")
            
            # Emit literacy outliers
            if literacy_rate > 80.0:
                print(f"high_literacy\t{county_name}:{literacy_rate:.1f}")
            if literacy_rate < 60.0:
                print(f"low_literacy\t{county_name}:{literacy_rate:.1f}")
                
        except (ValueError, IndexError) as e:
            # Skip malformed lines
            continue


if __name__ == '__main__':
    mapper()
