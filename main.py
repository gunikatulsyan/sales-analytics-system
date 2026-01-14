from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1] Read data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2] Parse
        print("\n[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed)} records")

        # [3] Filter options
        regions = sorted({tx["Region"] for tx in parsed if tx.get("Region")})
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in parsed]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{int(min(amounts))} - ₹{int(max(amounts))}")

        use_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if use_filter == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            region_filter = region_filter if region_filter else None

            min_val = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_val = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_val) if min_val else None
            max_amount = float(max_val) if max_val else None

        # [4] Validate
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            parsed,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # [5] Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # [6] API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # [7] Enrich
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for tx in enriched_transactions if tx["API_Match"])
        rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({rate:.1f}%)")

        # [8] Save enriched file
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9] Generate report
        print("\n[9/10] Generating report...")
        report_path = generate_sales_report(valid_transactions, enriched_transactions)
        print(f"✓ Report saved to: {report_path}")

        # [10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n An error occurred:")
        print(str(e))
        print("Please check input files and try again.")


if __name__ == "__main__":
    main()
