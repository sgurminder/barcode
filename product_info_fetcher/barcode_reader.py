import openfoodfacts
import requests.exceptions
import sys
import argparse

def get_product_info(barcode: str) -> dict | None:
    """
    Fetches product information from OpenFoodFacts API using a barcode.

    Args:
        barcode: The product barcode.

    Returns:
        A dictionary containing product_name, brand, quantity,
        ingredients_text, and categories if the product is found.
        Returns None otherwise.
    """
    try:
        product_data = openfoodfacts.products.get_product(barcode)
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred while fetching product data: {e}", file=sys.stderr)
        return None
    except Exception as e: # Catching other potential errors from the SDK or data processing
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

    if product_data and product_data.get("status") == 1 and product_data.get("product"):
        product = product_data["product"]
        return {
            "product_name": product.get("product_name"),
            "brand": product.get("brands"), # 'brands' is often the key used
            "quantity": product.get("quantity"),
            "ingredients_text": product.get("ingredients_text"),
            "categories": product.get("categories"),
        }
    return None

def main():
    parser = argparse.ArgumentParser(description="Fetch product information using a barcode from OpenFoodFacts.")
    parser.add_argument("barcode", help="The product barcode to look up")
    args = parser.parse_args()

    barcode_from_arg = args.barcode
    print(f"Barcode Reader CLI - Fetching info for barcode: {barcode_from_arg}")

    info = get_product_info(barcode_from_arg)

    if info:
        print(f"Product Name: {info.get('product_name', 'N/A')}")
        print(f"Brand: {info.get('brand', 'N/A')}")
        print(f"Quantity: {info.get('quantity', 'N/A')}")
        print(f"Ingredients: {info.get('ingredients_text', 'N/A')}")
        print(f"Categories: {info.get('categories', 'N/A')}")
    else:
        print(f"Product with barcode {barcode_from_arg} not found or an error occurred while fetching data.")


if __name__ == "__main__":
    main()
