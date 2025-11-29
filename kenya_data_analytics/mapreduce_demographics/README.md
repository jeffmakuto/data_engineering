# Kenya County Demographics - MapReduce Analysis

## Overview
This MapReduce job processes Kenya's county-level demographic data to produce aggregate statistics and insights about population distribution, urbanization, literacy, and economic indicators.

## Architecture

### Components
1. **mapper.py** - Processes CSV input and emits intermediate key-value pairs
2. **reducer.py** - Aggregates mapper output and calculates final statistics
3. **driver.py** - Orchestrates the MapReduce job locally (simulates Hadoop)

### Data Flow
```
kenya_county_demographics.csv → Mapper → Shuffle/Sort → Reducer → output.txt
```

## Dataset
**Source**: `datasets/kenya_county_demographics.csv`

**Schema**:
- county_code: Unique county identifier
- county_name: County name
- population: Total population
- area_sq_km: County area in square kilometers
- urban_population: Urban residents
- rural_population: Rural residents
- male_population: Male residents
- female_population: Female residents
- households: Number of households
- literacy_rate: Percentage of literate population
- gdp_per_capita: GDP per capita in KSh

**Coverage**: All 47 Kenyan counties

## Implementation Details

### Mapper Logic
Reads each county record and emits multiple key-value pairs for aggregation:
- Total counts: population, area, urban/rural, male/female, households
- Summation inputs: literacy rates, GDP values, county count
- Outlier detection: High literacy (>80%), low literacy (<60%)

**Output format**: `key\tvalue` (tab-separated)

### Reducer Logic
Aggregates mapper outputs using:
- Summation for totals (population, area, households)
- Division for averages (literacy rate, GDP per capita)
- List collection for outliers (high/low literacy counties)

Calculates derived metrics:
- Population density
- Urbanization rate
- Gender ratio
- Average household size

### Driver Configuration
Simulates Hadoop streaming locally using Python subprocess:
1. Feeds CSV to mapper via stdin
2. Sorts mapper output (shuffle phase)
3. Feeds sorted data to reducer via stdin
4. Writes results to `output.txt`

**Usage**:
```bash
python driver.py [input_csv] [output_file]
```

Default: Reads `../datasets/kenya_county_demographics.csv`, writes to `output.txt`

## Results Summary

### Key Findings
- **Total Population**: 47,897,217 across 47 counties
- **Population Density**: 81.35 persons/km²
- **Urbanization**: 34.85% (16.7M urban, 31.2M rural)
- **Gender Balance**: 100.88 males per 100 females (near parity)
- **Average Literacy**: 74.11%
- **Average GDP per Capita**: KSh 58,574.47
- **Average Household Size**: 4.74 persons

### High-Performance Counties (Literacy >80%)
1. **Nairobi** - 93.8% (capital, highest urbanization)
2. **Kiambu** - 92.1% (metropolitan area)
3. **Nyeri** - 91.2% (central highlands)
4. **Mombasa** - 89.5% (coastal city)

21 counties total achieved >80% literacy, indicating strong education infrastructure in central and urban regions.

### Low Literacy Counties (<60%)
Counties with literacy below 60% are primarily in arid/semi-arid regions:
- **Turkana** - 34.5% (northwestern, pastoralist economy)
- **Wajir** - 38.2% (northeastern, nomadic)
- **Mandera** - 41.5% (northeastern border)
- **Marsabit** - 45.8% (northern, sparse population)

These counties face challenges from remoteness, climate variability, and limited infrastructure.

## Technical Notes

### Performance
- **Local Execution**: Processes 47 records in <1 second
- **Scalability**: Designed for Hadoop streaming (handles millions of records)
- **Memory**: Reducer uses ~O(n) memory for county outlier lists

### Hadoop Deployment
To run on actual Hadoop cluster:
```bash
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -input /data/kenya_county_demographics.csv \
  -output /output/demographics \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py
```

### Error Handling
- Skips malformed CSV lines (catches ValueError, IndexError)
- Validates column count (expects 11 fields)
- Handles division by zero in derived metrics

## Next Steps
1. **Temporal Analysis**: Process multi-year census data to track demographic trends
2. **Geographic Clustering**: Use K-means on literacy/GDP to identify development zones
3. **Join Operations**: Merge with health/education facility data for correlation analysis
4. **Real-time Updates**: Integrate with streaming census updates using Spark Streaming

## Dependencies
- Python 3.8+
- No external packages required (uses stdlib only)
