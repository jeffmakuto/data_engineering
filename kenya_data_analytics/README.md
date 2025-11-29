# Kenya Data Analytics - Big Data Engineering Project

[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.x-orange)](https://spark.apache.org/)
[![Hadoop](https://img.shields.io/badge/Hadoop-MapReduce-yellow)](https://hadoop.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive data engineering project demonstrating **Hadoop MapReduce**, **Spark Batch Analytics**, **Spark Streaming**, and **Spark SQL** applied to Kenyan datasets covering demographics, agriculture, and traffic.

## 🎯 Project Overview

This project analyzes three critical datasets from Kenya:

1. **County Demographics** (47 counties) - Population, literacy, GDP analysis
2. **Agricultural Production** (2020-2023) - Crop yields, regional patterns, climate impact
3. **Nairobi Traffic** (5 major junctions) - Real-time congestion monitoring

## 📁 Project Structure

```
kenya_data_analytics/
├── datasets/                              # Raw datasets (3 CSV files)
├── mapreduce_demographics/                # Hadoop MapReduce implementation
│   ├── mapper.py
│   ├── reducer.py
│   ├── driver.py
│   └── output.txt
├── spark_batch_analytics/                 # Comprehensive Spark analysis
│   └── kenya_comprehensive_analysis.ipynb
├── spark_streaming_traffic/               # Real-time traffic monitoring
│   └── nairobi_traffic_stream.py
├── spark_sql_agriculture/                 # SQL-based crop analysis
│   └── agricultural_analysis.py
├── COMPREHENSIVE_REPORT.md                # Full project report
└── README.md                              # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python 3.8+
python --version

# Install required packages
pip install pyspark pandas matplotlib seaborn jupyter
```

### Run MapReduce Job

```bash
cd mapreduce_demographics
python driver.py
```

**Output**: National statistics, literacy outliers, urbanization analysis

### Run Spark Batch Analytics

```bash
cd spark_batch_analytics
jupyter notebook kenya_comprehensive_analysis.ipynb
```

**Features**: Interactive analysis, visualizations, correlations

### Run Spark Streaming

```bash
cd spark_streaming_traffic
python nairobi_traffic_stream.py
```

**Output**: Real-time congestion alerts, peak hour identification

### Run Spark SQL Analysis

```bash
cd spark_sql_agriculture
python agricultural_analysis.py
```

**Output**: 8 SQL queries analyzing crop production, regional patterns, climate impact

## 📊 Key Findings

### Demographics
- **Total Population**: 47.9 million across 47 counties
- **Urbanization**: 34.85% (strong urban-rural divide)
- **Literacy-GDP Correlation**: r = 0.95+ (very strong)
- **Top Counties**: Nairobi (93.8% literacy), Kiambu, Nyeri

### Agriculture
- **Maize Production**: 2.8M tonnes (dominant staple)
- **Tea Yield**: 5.5 tonnes/ha (highest productivity)
- **Growth**: 9.3% increase from 2020-2023
- **Top Region**: Rift Valley (Uasin Gishu, Trans Nzoia, Kericho)

### Traffic
- **Peak Hours**: 7-9 AM, 5-7 PM (critical congestion)
- **Busiest Junction**: Thika Road (687 vehicles at 8 AM)
- **Speed Impact**: Drops to 15-20 km/h during rush hour

## 🛠️ Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Batch Processing** | Hadoop MapReduce | County demographics aggregation |
| **Batch Analytics** | Apache Spark (PySpark) | Interactive data exploration |
| **Stream Processing** | Spark Streaming | Real-time traffic monitoring |
| **SQL Analytics** | Spark SQL | Agricultural production queries |
| **Visualization** | matplotlib, seaborn | Charts and graphs |
| **Development** | Jupyter Notebooks | Interactive analysis |

## 📈 Sample Visualizations

The project generates 10+ visualizations including:
- Population distribution charts
- Literacy vs GDP scatter plots
- Crop production trends (year-over-year)
- Traffic pattern heatmaps
- Congestion level pie charts

## 🎓 Learning Outcomes

This project demonstrates:
- **MapReduce Programming**: Mapper, Reducer, Driver patterns
- **Spark DataFrames**: Transformations, actions, aggregations
- **Spark SQL**: Complex queries, joins, window functions
- **Spark Streaming**: Real-time processing, alerts, windows
- **Data Engineering**: ETL, data quality, feature engineering
- **Big Data Best Practices**: Partitioning, optimization, deployment

## 📋 Requirements

### Python Packages
```
pyspark>=3.0.0
pandas>=1.5.0
matplotlib>=3.5.0
seaborn>=0.12.0
jupyter>=1.0.0
```

### System Requirements
- Python 3.8+
- 4GB RAM (minimum for local Spark)
- Java 8 or 11 (for Spark)

## 🚀 Production Deployment

For production use:

1. **Hadoop Cluster**: Deploy on AWS EMR, Azure HDInsight, or Google Dataproc
2. **Spark Cluster**: Use Databricks, EMR, or standalone cluster
3. **Streaming**: Connect to Kafka for real-time data ingestion
4. **Monitoring**: Integrate with Grafana, Prometheus
5. **Dashboards**: Use Tableau, Power BI, or Apache Superset

See `COMPREHENSIVE_REPORT.md` for detailed deployment guidelines.

## 📝 Documentation

- **Comprehensive Report**: [COMPREHENSIVE_REPORT.md](COMPREHENSIVE_REPORT.md) - Full analysis, findings, recommendations
- **MapReduce README**: `mapreduce_demographics/README.md` - Component documentation
- **Jupyter Notebook**: Self-documenting with markdown cells and comments

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Machine learning models (traffic prediction, yield forecasting)
- Additional datasets (health, education, infrastructure)
- Geospatial analysis with GeoSpark
- Real-time dashboard with Streamlit/Dash

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Data Engineering Team - 2024

## 📧 Contact

For questions or collaboration opportunities, please open an issue.

## 🙏 Acknowledgments

- Kenya National Bureau of Statistics (KNBS) for data inspiration
- Apache Spark and Hadoop communities
- Open data initiatives in Kenya

---

**Status**: ✅ Production-ready  
**Last Updated**: 2024  
**Version**: 1.0
