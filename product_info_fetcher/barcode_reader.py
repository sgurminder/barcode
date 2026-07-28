from openfoodfacts import API # Changed import
import requests.exceptions
import sys
import argparse

# Global API instance
api = API(user_agent="ProductInfoFetcherApp/1.0")

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
        # Use the api.product.get method with specified fields
        product_data = api.product.get(barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

        # Check if product_data is valid and contains essential information
        if product_data and product_data.get('code') == barcode and product_data.get('product_name'):
            return {
                "product_name": product_data.get("product_name"),
                "brand": product_data.get("brands"),  # API returns 'brands'
                "quantity": product_data.get("quantity"),
                "ingredients_text": product_data.get("ingredients_text"),
                "categories": product_data.get("categories")
            }
        else:
            # Product not found or essential data missing
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}", file=sys.stderr)
        return None
    except Exception as e: # Catching other potential errors from the SDK or data processing
        print(f"An unexpected error occurred in get_product_info: {e}", file=sys.stderr)
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
        # Main expects 'brand', get_product_info now returns 'brand' (mapped from 'brands')
        print(f"Brand: {info.get('brand', 'N/A')}")
        print(f"Quantity: {info.get('quantity', 'N/A')}")
        # Main expects 'ingredients', but uses info.get('ingredients_text', 'N/A')
        # get_product_info returns 'ingredients_text', which is fine.
        print(f"Ingredients: {info.get('ingredients_text', 'N/A')}")
        print(f"Categories: {info.get('categories', 'N/A')}")
    else:
        print(f"Product with barcode {barcode_from_arg} not found or an error occurred while fetching data.")


if __name__ == "__main__":
    main()
