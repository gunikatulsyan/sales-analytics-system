def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        try:
            # Clean product name (remove commas)
            product_name = product_name.replace(",", "")

            # Clean numeric fields (remove commas)
            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))

            transaction = {
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with conversion issues
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    # ---- VALIDATION PHASE ----
    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0
                or tx["UnitPrice"] <= 0
                or not tx["TransactionID"].startswith("T")
                or not tx["ProductID"].startswith("P")
                or not tx["CustomerID"].startswith("C")
                or not tx["Region"]
            ):
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1
            continue

    after_validation = len(valid_transactions)

    # ---- FILTERING PHASE ----
    filtered = valid_transactions

    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Region"] == region]
        filtered_by_region = before - len(filtered)

    if min_amount is not None or max_amount is not None:
        before = len(filtered)
        result = []

        for tx in filtered:
            amount = tx["Quantity"] * tx["UnitPrice"]

            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            result.append(tx)

        filtered_by_amount = before - len(result)
        filtered = result

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, filter_summary
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """

    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return round(total_revenue, 2)

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """

    region_stats = {}
    total_revenue = 0.0

    # First pass: accumulate totals
    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        total_revenue += amount

        if region not in region_stats:
            region_stats[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1

    # Second pass: calculate percentages
    for region in region_stats:
        percentage = (region_stats[region]["total_sales"] / total_revenue) * 100
        region_stats[region]["percentage"] = round(percentage, 2)
        region_stats[region]["total_sales"] = round(region_stats[region]["total_sales"], 2)

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """

    product_stats = {}

    # Aggregate by product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = quantity * tx["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_stats[product]["total_quantity"] += quantity
        product_stats[product]["total_revenue"] += revenue

    # Convert to list of tuples
    result = [
        (
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        )
        for product, stats in product_stats.items()
    ]

    # Sort by total quantity descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]
def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        customer_id = tx["CustomerID"].strip()
        if not customer_id:
            continue

        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer_id not in customers:
            customers[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customers[customer_id]["total_spent"] += amount
        customers[customer_id]["purchase_count"] += 1
        customers[customer_id]["products"].add(product)

    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": sorted(list(data["products"]))
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """

    daily_stats = {}

    # Aggregate by date
    for tx in transactions:
        date = tx["Date"]
        customer = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_stats:
            daily_stats[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily_stats[date]["revenue"] += amount
        daily_stats[date]["transaction_count"] += 1
        daily_stats[date]["unique_customers"].add(customer)

    # Finalize counts
    for date, stats in daily_stats.items():
        stats["revenue"] = round(stats["revenue"], 2)
        stats["unique_customers"] = len(stats["unique_customers"])

    # Sort chronologically (ISO dates sort correctly as strings)
    sorted_daily_stats = dict(sorted(daily_stats.items()))

    return sorted_daily_stats
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """

    daily_totals = {}

    # Aggregate revenue and transaction count per date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_totals:
            daily_totals[date] = {
                "revenue": 0.0,
                "count": 0
            }

        daily_totals[date]["revenue"] += amount
        daily_totals[date]["count"] += 1

    # Find peak day
    peak_date = None
    peak_revenue = 0.0
    peak_count = 0

    for date, stats in daily_totals.items():
        if stats["revenue"] > peak_revenue:
            peak_revenue = stats["revenue"]
            peak_count = stats["count"]
            peak_date = date

    return (peak_date, round(peak_revenue, 2), peak_count)
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """

    product_stats = {}

    # Aggregate by product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = quantity * tx["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_stats[product]["total_quantity"] += quantity
        product_stats[product]["total_revenue"] += revenue

    # Filter low-performing products
    low_products = [
        (
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        )
        for product, stats in product_stats.items()
        if stats["total_quantity"] < threshold
    ]

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- BASIC METRICS ----------
    total_transactions = len(transactions)
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = round(total_revenue / total_transactions, 2) if total_transactions else 0

    dates = sorted(tx["Date"] for tx in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # ---------- ANALYTICS ----------
    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customer_stats = customer_analysis(transactions)
    daily_stats = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # ---------- API ENRICHMENT ----------
    enriched_count = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    total_enriched = len(enriched_transactions)
    enrichment_rate = round((enriched_count / total_enriched) * 100, 2) if total_enriched else 0

    unenriched_products = sorted({
        tx["ProductName"]
        for tx in enriched_transactions
        if not tx.get("API_Match")
    })

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:
        # HEADER
        f.write("=" * 44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("=" * 44 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions'}\n")
        for region, stats in region_stats.items():
            f.write(
                f"{region:<10}₹{stats['total_sales']:,.0f}     "
                f"{stats['percentage']:>6.2f}%      "
                f"{stats['transaction_count']}\n"
            )
        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  Product                Quantity   Revenue\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<5} {name:<22} {qty:<10} ₹{rev:,.2f}\n")
        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write("Rank  CustomerID   Total Spent   Orders\n")
        for i, (cust, stats) in enumerate(list(customer_stats.items())[:5], 1):
            f.write(
                f"{i:<5} {cust:<12} ₹{stats['total_spent']:,.2f}   "
                f"{stats['purchase_count']}\n"
            )
        f.write("\n")

        # DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write("Date         Revenue        Transactions  Customers\n")
        for date, stats in daily_stats.items():
            f.write(
                f"{date}   ₹{stats['revenue']:,.2f}      "
                f"{stats['transaction_count']:<13} {stats['unique_customers']}\n"
            )
        f.write("\n")

        # PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {peak_day[0]} "
                f"(₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                f.write(f"- {name}: {qty} units, ₹{rev:,.2f}\n")
        else:
            f.write("No low performing products.\n")
        f.write("\n")

        # API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Records Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {enrichment_rate}%\n")
        f.write("Unmatched Products:\n")
        for p in unenriched_products:
            f.write(f"- {p}\n")

    return output_file
