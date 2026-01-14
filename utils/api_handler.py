import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """

    url = "https://dummyjson.com/products"

    try:
        response = requests.get(url, params={"limit": 100}, timeout=5)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        cleaned_products = []

        for p in products:
            cleaned_products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price")
            })

        print("Successfully fetched products from DummyJSON API")
        return cleaned_products

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products from DummyJSON API:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand")
        }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions using API product data
    """

    enriched = []

    for tx in transactions:
        enriched_tx = tx.copy()

        product_id = tx.get("ProductID", "")
        numeric_id = None

        try:
            numeric_id = int("".join(filter(str.isdigit, product_id)))
        except ValueError:
            pass

        api_product = product_mapping.get(numeric_id)

        # Optional fallback by product name
        if not api_product:
            for p in product_mapping.values():
                if (
                    p["title"].lower() in tx["ProductName"].lower()
                    or tx["ProductName"].lower() in p["title"].lower()
                ):
                    api_product = p
                    break

        if api_product:
            enriched_tx["API_Category"] = api_product.get("category")
            enriched_tx["API_Brand"] = api_product.get("brand")
            enriched_tx["API_Match"] = True
        else:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Match"] = False

        enriched.append(enriched_tx)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to file
    """

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = [str(tx.get(h, "")) for h in headers]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
