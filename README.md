Sales Analytics System
Description

This project implements a Python-based Sales Analytics System that processes raw sales transaction data, cleans and validates records, performs multiple analytical computations, integrates external product data via an API, enriches transactions, and generates structured output files and a formatted sales report.

Architecture at a Glance

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


Functionality:

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

How to Run

Install dependencies:
    pip install -r requirements.txt

Execute the program:
    python3 main.py

Output Files

Enriched Transactions: data/enriched_sales_data.txt
Sales Report: output/sales_report.txt

Files are generated on every execution, even if input data is empty
```
