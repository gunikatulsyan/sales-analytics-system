# 📈 Sales Analytics System  
*A modular data analytics pipeline with API integration and reporting*

---

## 🚀 Project Overview

The **Sales Analytics System** is a Python-based data processing and analytics application designed to transform raw sales transaction data into meaningful business insights.

The system reads unstructured sales data, cleans and validates records, performs multi-dimensional sales analysis, integrates external product metadata via an API, enriches transaction records, and generates structured output files along with a comprehensive sales report.

This project focuses on **clean architecture, defensive programming, and end-to-end execution flow**, rather than isolated scripts.

---

## 🧠 What This Project Demonstrates

- Structured data ingestion and validation  
- Modular analytics pipeline design  
- Defensive handling of incomplete or invalid data  
- API integration and data enrichment  
- Report generation with real business metrics  
- Clear separation of concerns across modules  
- Professional project organization and version control  

---

## 🗂️ Project Structure

sales-analytics-system/
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── __init__.py
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py

⚙️ Core Functionality
1. Data Ingestion

Reads pipe-delimited (|) sales transaction data

Handles encoding issues gracefully

Skips empty and malformed records

2. Data Cleaning & Validation

Cleans numeric and text fields

Removes invalid transactions based on defined business rules

Tracks valid and invalid record counts

3. Optional Filtering

Users can optionally filter transactions by:

Region

Transaction amount range

Filtering is applied before validation to preserve logical flow.

4. Sales Analytics

The system performs multiple analyses, including:

Total revenue calculation

Region-wise sales performance

Top and low-performing products

Customer purchase behavior

Daily sales trends

Peak sales day identification

5. API Integration

Fetches external product data from the DummyJSON API

Maps internal product IDs to API metadata (category, brand)

6. Data Enrichment

Enriches sales transactions with API product information

Adds enrichment flags to indicate match success

Preserves all original transaction records

7. Report Generation

Generates a structured, formatted sales report containing:

Overall summary

Regional performance

Product and customer rankings

Daily trends

API enrichment summary

▶️ How to Run
1. Install Dependencies

Ensure Python 3 is installed, then run:
pip install -r requirements.txt

2. Execute the Program

From the project root directory:
python3 main.py

📄 Output Files

data/enriched_sales_data.txt : 	Enriched transaction data with API metadata

output/sales_report.txt	: Comprehensive formatted analytics report

Output files are generated on every run, even when input data is empty, ensuring deterministic behavior.

🛡️ Error Handling & Reliability

Entire execution wrapped in try-except blocks

API failures handled without crashing the system

Empty or missing data handled safely

No hardcoded absolute file paths (portable execution)

📌 Design Principles Followed

Separation of concerns (I/O, processing, API, reporting)

Modular architecture

Defensive programming

Readable, maintainable code

Predictable outputs

🧪 Edge Case Handling

Empty input files still generate valid output files

Invalid transactions do not affect analytics

API enrichment gracefully degrades when matches are unavailable

📝 Final Note

This project was built to reflect real-world data pipeline behavior, focusing on correctness, clarity, and maintainability rather than overengineering or unnecessary complexity.