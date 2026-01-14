* Sales Analytics System
Description

This project implements a Python-based Sales Analytics System that processes raw sales transaction data, cleans and validates records, performs multiple analytical computations, integrates external product data via an API, enriches transactions, and generates structured output files and a formatted sales report.


* Architecture at a Glance

Raw Sales Data (TXT)
        ↓
File Handling & Cleaning
        ↓
Validated Transactions
        ↓
Business Analytics
        ↓
API Enrichment
        ↓
Enriched Dataset
        ↓
Automated Sales Report



* Repository Structure:

sales-analytics-system/
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── utils/
│   ├── _init_.py
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report_generator.py
│
├── output/
│   └── sales_report.txt
│
├── main.py
├── requirements.txt
└── README.md\


* Part 1: File Handling & Preprocessing
    Key Features

•⁠  ⁠Reads raw sales data with proper UTF-8 encoding handling  
•⁠  ⁠Parses pipe-separated (⁠ | ⁠) transaction records  
•⁠  ⁠Cleans messy data by handling:
  - Commas in numeric fields  
  - Invalid or inconsistent data types  
  - Missing or malformed fields  
•⁠  ⁠Applies strict validation rules for:
  - Transaction IDs  
  - Product IDs  
  - Customer IDs  
  - Quantity and price values  
•⁠  ⁠Supports optional filtering by:
  - Region  
  - Transaction amount range  




* Part 2: Data Processing & Analytics

Analytics Implemented

•⁠  ⁠Total revenue calculation across all valid transactions  
•⁠  ⁠Region-wise sales performance with percentage contribution  
•⁠  ⁠Identification of top-selling products by quantity and revenue  
•⁠  ⁠Detection of low-performing products for business insights  
•⁠  ⁠Customer purchase behavior analysis including:
  - Total spend
  - Purchase count
  - Average order value  
•⁠  ⁠Date-based analysis:
  - Daily sales trend
  - Peak sales day identification  

These analytics simulate *real-world business KPIs* used for strategic decision-making.

* Part 3: API Integration

API Enrichment:

•⁠  ⁠Integrates a simulated external product API  
•⁠  ⁠Fetches additional product metadata such as:
  - Product category
  - Brand
  - Rating  
•⁠  ⁠Uses structured mappings to efficiently enrich transactions  
•⁠  ⁠Tracks:
  - Successful API enrichments  
  - Failed or unmatched products  
•⁠  ⁠Saves enriched transaction data to a separate output file  

Demonstrates real-world API integration concepts and fault tolerance.


* Part 4: Automated Report Generation

The system automatically generates a *professional sales analytics report* containing structured business insights.

Report Sections:

The report includes the following sections:

1.⁠ ⁠Report header and metadata  
2.⁠ ⁠Overall sales summary  
3.⁠ ⁠Region-wise performance analysis  
4.⁠ ⁠Top 5 products by sales  
5.⁠ ⁠Top 5 customers by spending  
6.⁠ ⁠Daily sales trend analysis  
7.⁠ ⁠Product performance evaluation  
8.⁠ ⁠API enrichment summary  

Generated report location:
output/sales_report.txt


* Functionality:

    Reads and parses pipe-delimited sales data
    Cleans and validates transaction records
    Supports optional filtering by region and amount
    Performs sales analysis:
        Revenue calculation
        Region-wise performance
        Product and customer analysis
        Daily sales trends
    Fetches product data from an external API
    Enriches transactions with API product metadata
    Generates enriched data file and comprehensive sales report
    Handles errors gracefully without program termination

* How to Run

Install dependencies:
    pip install -r requirements.txt

Execute the program:
    python3 main.py

Output Files

Enriched Transactions: data/enriched_sales_data.txt
Sales Report: output/sales_report.txt

Files are generated on every execution, even if input data is empty
