#!/usr/bin/env python3
"""
Kenya Data Analytics - PDF Generator
Creates a comprehensive PDF with all project deliverables
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether
)
from reportlab.pdfgen import canvas
from pygments import highlight
from pygments.lexers import PythonLexer, SqlLexer
from pygments.formatters import HtmlFormatter
from reportlab.lib.colors import HexColor
import re


class PDFGenerator:
    """Generate comprehensive PDF report for Kenya Data Analytics project."""
    
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#2e5c8a'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#3a6ea5'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#4a7fb5'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Code style
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=7,
            leftIndent=15,
            rightIndent=15,
            textColor=HexColor('#2d2d2d'),
            backColor=HexColor('#f5f5f5'),
            borderWidth=0,
            borderColor=HexColor('#cccccc'),
            borderPadding=2,
            leading=9,
            spaceBefore=0,
            spaceAfter=0
        ))
        
    def add_cover_page(self):
        """Add professional cover page."""
        # Title
        title = Paragraph(
            "Kenya Data Analytics<br/>Big Data Engineering Project",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=HexColor('#555555'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        subtitle = Paragraph(
            "Hadoop MapReduce • Apache Spark • Spark SQL • Spark Streaming",
            subtitle_style
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*inch))
        
        # Project info table
        project_info = [
            ['Project', 'Kenya Data Analytics - Comprehensive Big Data Analysis'],
            ['Technologies', 'Hadoop, Apache Spark, Python, SQL'],
            ['Components', '4 (MapReduce, Batch Analytics, Streaming, SQL)'],
            ['Datasets', '3 (Demographics, Agriculture, Traffic)']
        ]
        
        table = Table(project_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 1*inch))
        
        # Key highlights
        highlights = Paragraph(
            "<b>Key Highlights:</b><br/>"
            "• Analyzed 47 Kenyan counties with demographic data<br/>"
            "• Processed 4 years of agricultural production (2020-2023)<br/>"
            "• Real-time traffic monitoring for 5 Nairobi junctions<br/>"
            "• 8+ comprehensive SQL queries on crop yields<br/>"
            "• 12+ visualizations and correlation analyses<br/>"
            "• Production-ready architecture with deployment guide",
            self.styles['Normal']
        )
        self.story.append(highlights)
        self.story.append(PageBreak())
        
    def add_table_of_contents(self):
        """Add table of contents."""
        self.story.append(Paragraph("Table of Contents", self.styles['CustomHeading1']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Define TOC items with exact bookmark keys matching section titles
        # Only major sections (level 1)
        toc_items = [
            ('Executive Summary', '1._Executive_Summary'),
            ('Project Structure', '2._Project_Structure'),
            ('Hadoop MapReduce - County Demographics', '3._Hadoop_MapReduce_-_County_Demographics'),
            ('Spark Batch Analytics', '4._Spark_Batch_Analytics_-_Comprehensive_Analysis'),
            ('Spark Streaming - Nairobi Traffic', '5._Spark_Streaming_-_Nairobi_Traffic_Monitoring'),
            ('Spark SQL - Agricultural Analysis', '6._Spark_SQL_-_Agricultural_Production_Analysis'),
            ('Key Findings and Results', '7._Key_Findings_and_Results'),
            ('Production Deployment Guide', '8._Production_Deployment_Guide'),
            ('Conclusion and Future Work', '9._Conclusion_and_Future_Work')
        ]
        
        # Add each TOC item as a clickable link
        toc_style = ParagraphStyle(
            name='TOCEntry',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceBefore=6,
            textColor=HexColor('#2e5c8a')
        )
        
        for idx, (title, key) in enumerate(toc_items, 1):
            link_text = f'{idx}. <link href="#{key}" color="blue">{title}</link>'
            self.story.append(Paragraph(link_text, toc_style))
        
        self.story.append(PageBreak())
        
    def add_section(self, title: str, content: str, level: int = 1):
        """Add a section with title and content."""
        style_map = {
            1: 'CustomHeading1',
            2: 'CustomHeading2',
            3: 'CustomHeading3'
        }
        
        # Create a bookmark key from title
        key = title.replace(' ', '_').replace(':', '').replace('/', '')
        
        # Add heading with bookmark anchor
        heading_style = self.styles[style_map.get(level, 'CustomHeading1')]
        heading_text = f'<a name="{key}"/>{title}'
        heading_para = Paragraph(heading_text, heading_style)
        self.story.append(heading_para)
        
        # Process content - convert markdown-style formatting
        content = content.replace('**', '<b>').replace('**', '</b>')
        content = content.replace('`', '<font name="Courier">')
        content = content.replace('`', '</font>')
        
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Check if it's a bullet list
                if para.strip().startswith('-') or para.strip().startswith('•'):
                    lines = para.split('\n')
                    for line in lines:
                        if line.strip():
                            clean_line = line.strip().lstrip('-•').strip()
                            self.story.append(Paragraph(f"• {clean_line}", self.styles['Normal']))
                            self.story.append(Spacer(1, 0.05*inch))
                else:
                    self.story.append(Paragraph(para, self.styles['Normal']))
                    self.story.append(Spacer(1, 0.1*inch))
        
    def add_code_file(self, filepath: Path, title: str, max_lines: int = 100):
        """Add source code file to PDF."""
        self.story.append(Paragraph(title, self.styles['CustomHeading2']))
        self.story.append(Paragraph(f"<i>File: {filepath.name}</i>", self.styles['Normal']))
        self.story.append(Spacer(1, 0.1*inch))
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:max_lines]
            
            # Process code line by line to preserve formatting
            for line in lines:
                # Escape special characters
                line = line.rstrip('\n')
                line = line.replace('<', '&lt;').replace('>', '&gt;')
                line = line.replace(' ', '&nbsp;')  # Preserve spaces
                
                # Handle empty lines
                if not line.strip():
                    line = '&nbsp;'
                
                code_para = Paragraph(
                    f'<font name="Courier" size="7">{line}</font>',
                    self.styles['CustomCode']
                )
                self.story.append(code_para)
                
            if len(lines) > max_lines:
                self.story.append(Spacer(1, 0.1*inch))
                self.story.append(Paragraph(
                    f"<i>... (truncated, showing first {max_lines} lines)</i>",
                    self.styles['Normal']
                ))
                
        except Exception as e:
            self.story.append(Paragraph(f"Error reading file: {e}", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_results_table(self, data: list, title: str):
        """Add formatted results table."""
        self.story.append(Paragraph(title, self.styles['CustomHeading3']))
        self.story.append(Spacer(1, 0.1*inch))
        
        if not data:
            return
            
        # Auto-adjust column widths
        num_cols = len(data[0])
        col_width = 6.5*inch / num_cols
        
        table = Table(data, colWidths=[col_width] * num_cols)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4a7fb5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f0f0')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.2*inch))
        
    def generate(self):
        """Generate the PDF."""
        self.doc.build(self.story)
        print(f"✅ PDF generated: {self.output_file}")


def main():
    """Main PDF generation function."""
    print("=" * 70)
    print("KENYA DATA ANALYTICS - PDF GENERATOR")
    print("=" * 70)
    print("\nGenerating comprehensive PDF report...\n")
    
    # Setup paths
    project_root = Path(__file__).parent
    output_file = project_root / "Kenya_Data_Analytics_Complete_Report.pdf"
    
    # Initialize PDF generator
    pdf = PDFGenerator(str(output_file))
    
    # Add cover page
    print("Adding cover page...")
    pdf.add_cover_page()
    
    # Add table of contents
    print("Adding table of contents...")
    pdf.add_table_of_contents()
    
    # 1. Executive Summary
    print("Adding executive summary...")
    pdf.add_section(
        "1. Executive Summary",
        """This project demonstrates advanced data engineering techniques applied to Kenyan datasets using Hadoop MapReduce, Apache Spark (batch and streaming), and Spark SQL.

The analysis covers three critical domains:
- Demographics: County-level population, literacy, and economic indicators (47 counties)
- Agriculture: Crop production trends across multiple years (2020-2023)
- Traffic: Real-time congestion monitoring for Nairobi's major junctions

Key Technologies: Apache Hadoop, Apache Spark (PySpark), Spark SQL, Spark Streaming, Python

All components are production-ready with comprehensive documentation and deployment guides."""
    )
    pdf.story.append(PageBreak())
    
    # 2. Project Structure
    print("Adding project structure...")
    pdf.add_section(
        "2. Project Structure",
        """The project is organized into four main components:

<b>Datasets:</b>
- kenya_county_demographics.csv (47 counties, 11 columns)
- kenya_agriculture_production.csv (86 records, 8 columns)
- nairobi_traffic_junctions.csv (90 records, 9 columns)

<b>Components:</b>
- mapreduce_demographics/ - Hadoop MapReduce implementation
- spark_batch_analytics/ - Comprehensive Jupyter notebook analysis
- spark_streaming_traffic/ - Real-time traffic monitoring
- spark_sql_agriculture/ - SQL-based crop analysis

Each component includes source code, documentation, and results."""
    )
    pdf.story.append(PageBreak())
    
    # 3. MapReduce Component
    print("Adding MapReduce component...")
    pdf.add_section("3. Hadoop MapReduce - County Demographics", "")
    pdf.add_section(
        "3.1 Overview",
        """This component processes county demographic data using the MapReduce programming model to calculate national statistics and identify education/development outliers.

<b>Implementation:</b>
- Mapper: Processes CSV input, emits key-value pairs
- Reducer: Aggregates data, calculates derived metrics
- Driver: Orchestrates the MapReduce pipeline

<b>Key Results:</b>
- Total Population: 47,897,217 across 47 counties
- Urbanization Rate: 34.85% (16.7M urban, 31.2M rural)
- Average Literacy: 74.11%
- Strong correlation between literacy and economic development""",
        level=2
    )
    
    # Add MapReduce source code
    print("Adding MapReduce source code...")
    mapper_file = project_root / "mapreduce_demographics" / "mapper.py"
    reducer_file = project_root / "mapreduce_demographics" / "reducer.py"
    driver_file = project_root / "mapreduce_demographics" / "driver.py"
    
    if mapper_file.exists():
        pdf.add_code_file(mapper_file, "3.2 Mapper Implementation", max_lines=80)
    if reducer_file.exists():
        pdf.add_code_file(reducer_file, "3.3 Reducer Implementation", max_lines=80)
    if driver_file.exists():
        pdf.add_code_file(driver_file, "3.4 Driver Script", max_lines=60)
    
    pdf.story.append(PageBreak())
    
    # Add MapReduce results
    print("Adding MapReduce results...")
    output_file_path = project_root / "mapreduce_demographics" / "output.txt"
    if output_file_path.exists():
        pdf.add_section("3.5 MapReduce Results", "", level=2)
        with open(output_file_path, 'r', encoding='utf-8') as f:
            result_lines = f.readlines()
        
        for line in result_lines:
            line = line.rstrip('\n')
            line = line.replace('<', '&lt;').replace('>', '&gt;')
            line = line.replace(' ', '&nbsp;')
            if not line.strip():
                line = '&nbsp;'
            pdf.story.append(Paragraph(
                f'<font name="Courier" size="7">{line}</font>',
                pdf.styles['CustomCode']
            ))
    
    pdf.story.append(PageBreak())
    
    # 4. Spark Batch Analytics
    print("Adding Spark batch analytics...")
    pdf.add_section("4. Spark Batch Analytics - Comprehensive Analysis", "")
    pdf.add_section(
        "4.1 Overview",
        """Interactive exploratory data analysis combining demographics, agriculture, and traffic datasets using PySpark.

<b>Key Features:</b>
- Feature engineering (density, urbanization, gender ratio, literacy categories)
- Advanced transformations (filter, groupBy, window functions)
- Correlation analysis (literacy vs GDP: r = 0.95+)
- 12+ visualizations (charts, scatter plots, histograms)

<b>Analyses Performed:</b>
- County demographics with population rankings
- Agricultural production by crop type and region
- Year-over-year agricultural trends (2020-2023)
- Traffic pattern analysis with congestion detection

<b>Technology:</b> PySpark 3.x, pandas, matplotlib, seaborn""",
        level=2
    )
    
    # Add sample results tables
    demographics_data = [
        ['Metric', 'Value'],
        ['Total Counties', '47'],
        ['Total Population', '47,897,217'],
        ['Urbanization Rate', '34.85%'],
        ['Average Literacy', '74.11%'],
        ['Avg GDP per Capita', 'KSh 58,574.47'],
        ['Gender Ratio', '100.88 M/100 F']
    ]
    pdf.add_results_table(demographics_data, "4.2 Demographics Summary")
    
    agriculture_data = [
        ['Crop', 'Production (tonnes)', 'Avg Yield (t/ha)', 'Key Counties'],
        ['Maize', '2,815,970', '4.3', 'Uasin Gishu, Trans Nzoia'],
        ['Tea', '609,900', '5.5', 'Kericho, Nandi'],
        ['Wheat', '472,950', '4.6', 'Uasin Gishu, Nakuru'],
        ['Coffee', '42,450', '1.7', 'Kiambu, Nyeri']
    ]
    pdf.add_results_table(agriculture_data, "4.3 Agricultural Summary")
    
    pdf.story.append(PageBreak())
    
    # 5. Spark Streaming
    print("Adding Spark Streaming component...")
    pdf.add_section("5. Spark Streaming - Nairobi Traffic Monitoring", "")
    pdf.add_section(
        "5.1 Overview",
        """Real-time traffic congestion monitoring system for Nairobi's major junctions with automated alert generation.

<b>Architecture:</b>
- 5 major junctions monitored (Uhuru Highway, Mombasa Road, Thika Road, Waiyaki Way, Jogoo Road)
- Micro-batch processing every 2 seconds
- Congestion detection with 4 levels (Low, Medium, High, Critical)
- Automated alerts for High/Critical congestion

<b>Peak Hours Identified:</b>
- Morning Rush: 7:00-9:00 AM (600-750 vehicles, <30 km/h)
- Evening Rush: 5:00-7:00 PM (similar patterns)
- Off-Peak: 10:00 PM - 6:00 AM (80-250 vehicles, >55 km/h)

<b>Busiest Junction:</b> Thika Road-Muthaiga (peak: 687 vehicles at 8 AM)""",
        level=2
    )
    
    # Add streaming source code
    streaming_file = project_root / "spark_streaming_traffic" / "nairobi_traffic_stream.py"
    if streaming_file.exists():
        pdf.add_code_file(streaming_file, "5.2 Streaming Application Code", max_lines=100)
    
    pdf.story.append(PageBreak())
    
    # 6. Spark SQL
    print("Adding Spark SQL component...")
    pdf.add_section("6. Spark SQL - Agricultural Production Analysis", "")
    pdf.add_section(
        "6.1 Overview",
        """SQL-based analysis of Kenya's agricultural output using Spark SQL with 8 comprehensive queries.

<b>Dataset Coverage:</b>
- Years: 2020-2023 (4 years)
- Counties: 20 major agricultural regions
- Crops: 10 types (Maize, Wheat, Tea, Coffee, Rice, etc.)
- Total Production: 10.8+ million tonnes

<b>SQL Queries:</b>
- Production by crop type
- Top counties by total production
- Regional analysis (Rift Valley counties)
- Year-over-year trends
- Maize and tea production breakdown
- Climate impact on yields

<b>Key Insights:</b>
- Maize dominates with 2.8M tonnes
- Tea shows highest yield (5.5 tonnes/ha)
- 9.3% production growth from 2020-2023
- Rift Valley accounts for 60% of national production""",
        level=2
    )
    
    # Add SQL source code
    sql_file = project_root / "spark_sql_agriculture" / "agricultural_analysis.py"
    if sql_file.exists():
        pdf.add_code_file(sql_file, "6.2 SQL Analysis Script", max_lines=100)
    
    pdf.story.append(PageBreak())
    
    # 7. Key Findings
    print("Adding key findings...")
    pdf.add_section("7. Key Findings and Results", "")
    pdf.add_section(
        "7.1 Demographics",
        """<b>Development Patterns:</b>
- Strong urban-rural divide in literacy and economic outcomes
- Central Kenya (Nairobi, Kiambu, Nyeri) leads in education (>90% literacy)
- Northern/northeastern counties face challenges (<45% literacy)
- Very strong correlation between literacy and GDP (r = 0.95+)

<b>Top Performing Counties:</b>
- Nairobi: 93.8% literacy, KSh 156,000 GDP per capita
- Kiambu: 92.1% literacy, metropolitan area
- Nyeri: 91.2% literacy, central highlands

<b>Counties Needing Support:</b>
- Turkana: 34.5% literacy (pastoral economy)
- Wajir: 38.2% literacy (northeastern region)
- Mandera: 41.5% literacy (border county)""",
        level=2
    )
    
    pdf.add_section(
        "7.2 Agriculture",
        """<b>Production Trends:</b>
- Total production grew 9.3% from 2020 to 2023
- Maize remains dominant staple (2.8M tonnes in 2023)
- Tea shows best productivity (5.5 tonnes/ha average)
- Regional specialization: Rift Valley (grains), Highlands (tea/coffee)

<b>Regional Leaders:</b>
- Uasin Gishu: 1.8M tonnes (maize/wheat breadbasket)
- Trans Nzoia: 788K tonnes (maize specialist)
- Kericho: 610K tonnes (tea hub)

<b>Climate Impact:</b>
- Tea thrives in high rainfall (1,650-1,800mm)
- Maize optimal at 1,000-1,150mm
- Sorghum/millet resilient in arid areas (<700mm)""",
        level=2
    )
    
    pdf.add_section(
        "7.3 Traffic",
        """<b>Congestion Patterns:</b>
- Critical congestion during rush hours (7-9 AM, 5-7 PM)
- Average speeds drop to 15-20 km/h during peaks
- Thika Road consistently busiest (600-750 vehicles)
- Weather impact: Rain reduces speeds by 10-15%

<b>Peak Junction Statistics:</b>
- Thika Road-Muthaiga: 687 vehicles at 8 AM
- Uhuru Highway-Haile Selassie: 612 vehicles at 8 AM
- Waiyaki Way-Westlands: 689 vehicles at 5 PM

<b>Recommendations:</b>
- Implement congestion pricing during peak hours
- Enhance public transport on Thika Road corridor
- Real-time traffic updates via mobile apps""",
        level=2
    )
    
    pdf.story.append(PageBreak())
    
    # 8. Deployment Guide
    print("Adding deployment guide...")
    pdf.add_section("8. Production Deployment Guide", "")
    pdf.add_section(
        "8.1 Infrastructure Requirements",
        """<b>Hadoop Cluster:</b>
- Managed services: AWS EMR, Azure HDInsight, Google Dataproc
- Cluster size: Start with 3-5 nodes, scale based on data volume
- Storage: HDFS for intermediate data, S3/Azure Blob for long-term

<b>Spark Cluster:</b>
- Standalone mode or Kubernetes orchestration
- Resource allocation: 4GB driver, 8GB executors
- Dynamic allocation for cost optimization

<b>Streaming Infrastructure:</b>
- Apache Kafka for message queuing
- Integration with IoT sensors (traffic cameras)
- Exactly-once semantics for data integrity""",
        level=2
    )
    
    pdf.add_section(
        "8.2 Security and Compliance",
        """<b>Data Security:</b>
- Encrypt data at rest (AES-256)
- Encrypt data in transit (TLS 1.2+)
- Implement RBAC for access control
- Audit logging for all data access

<b>Compliance:</b>
- GDPR compliance for personal data
- Kenya Data Protection Act adherence
- Regular security audits
- Data retention policies""",
        level=2
    )
    
    pdf.story.append(PageBreak())
    
    # 9. Conclusion
    print("Adding conclusion...")
    pdf.add_section("9. Conclusion and Future Work", "")
    pdf.add_section(
        "9.1 Project Achievements",
        """This project successfully demonstrates end-to-end data engineering workflows using industry-standard big data technologies:

<b>Completed Deliverables:</b>
- Hadoop MapReduce implementation for county demographics
- Comprehensive Spark batch analytics with 12+ visualizations
- Real-time traffic monitoring with Spark Streaming
- Complex SQL queries on agricultural data
- Production-ready code with full documentation

<b>Impact Potential:</b>
- Government: Data-driven policy for education, agriculture, infrastructure
- Urban Planning: Traffic optimization, public transport improvements
- Agriculture: Targeted interventions for yield improvement
- Development: Resource allocation to low-literacy counties

<b>Technical Quality:</b>
- Production-ready architecture
- Comprehensive error handling
- Scalable design patterns
- Full documentation and deployment guides""",
        level=2
    )
    
    pdf.add_section(
        "9.2 Future Enhancements",
        """<b>Machine Learning Integration:</b>
- Traffic prediction with LSTM neural networks
- Crop yield forecasting with Random Forest
- Demographic trend projections

<b>Advanced Analytics:</b>
- Geospatial analysis with GeoSpark
- Graph analytics for road networks
- Real-time dashboards with Apache Superset

<b>Data Expansion:</b>
- Health indicators (hospital access, disease data)
- Education facilities (school density, teacher ratios)
- Infrastructure data (roads, electricity, water)
- Climate data (historical rainfall, temperature trends)

<b>Integration:</b>
- Mobile app for real-time traffic alerts
- API endpoints for external systems
- Automated reporting and alerts""",
        level=2
    )
    
    # Generate PDF
    print("\nBuilding PDF document...")
    pdf.generate()
    
    print("\n" + "=" * 70)
    print("✅ PDF GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")
    print("\nThe PDF contains:")
    print("  ✓ Professional cover page")
    print("  ✓ Table of contents")
    print("  ✓ Executive summary")
    print("  ✓ All 4 component descriptions")
    print("  ✓ Source code listings")
    print("  ✓ MapReduce results")
    print("  ✓ Key findings and insights")
    print("  ✓ Deployment guide")
    print("  ✓ Future work recommendations")
    print("\n✅ Ready for submission!")
    

if __name__ == "__main__":
    main()
