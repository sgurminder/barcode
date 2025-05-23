import unittest
from unittest.mock import patch
import requests.exceptions

# Adjust the import path based on how you will run the tests
# If running with `python -m unittest discover product_info_fetcher/tests` from project root:
from product_info_fetcher.barcode_reader import get_product_info
# If running the test file directly for debugging and `product_info_fetcher` is in PYTHONPATH:
# from ..barcode_reader import get_product_info


class TestBarcodeReader(unittest.TestCase):

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_successful_product_lookup(self, mock_get_product):
        # Configure the mock to return a sample successful API response
        sample_api_response = {
            "status": 1,
            "product": {
                "product_name": "Test Product",
                "brands": "Test Brand",
                "quantity": "100g",
                "ingredients_text": "Ingredient A, Ingredient B",
                "categories": "Category X, Category Y"
            }
        }
        mock_get_product.return_value = sample_api_response

        expected_result = {
            "product_name": "Test Product",
            "brand": "Test Brand",
            "quantity": "100g",
            "ingredients_text": "Ingredient A, Ingredient B",
            "categories": "Category X, Category Y"
        }

        result = get_product_info("dummy_barcode_success")
        self.assertEqual(result, expected_result)

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_product_not_found_api_returns_none(self, mock_get_product):
        # Configure the mock to return None (simulating API finding no product but not an error)
        # This case is actually handled by the "status" != 1 or no "product" key in current implementation
        # A more accurate simulation for "not found" by the API directly
        mock_get_product.return_value = None 
        result = get_product_info("dummy_barcode_not_found_none")
        self.assertIsNone(result)

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_product_not_found_api_returns_empty_product(self, mock_get_product):
        # Configure the mock for when API returns data but "product" key is missing or status is not 1
        sample_api_response_no_product = {
            "status": 1,
            # "product": {} # Missing 'product' key
        }
        mock_get_product.return_value = sample_api_response_no_product
        result = get_product_info("dummy_barcode_not_found_empty")
        self.assertIsNone(result)

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_product_not_found_api_returns_status_0(self, mock_get_product):
        sample_api_response_status_0 = {
            "status": 0,
            "product": { # Product key might still be there but status 0 means not found
                 "product_name": "Test Product",
            }
        }
        mock_get_product.return_value = sample_api_response_status_0
        result = get_product_info("dummy_barcode_not_found_status_0")
        self.assertIsNone(result)

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_network_error(self, mock_get_product):
        # Configure the mock to raise RequestException
        mock_get_product.side_effect = requests.exceptions.RequestException("Test network error")

        # We can also check if sys.stderr was called, but it's more complex
        # For now, just check the return value
        result = get_product_info("dummy_barcode_network_error")
        self.assertIsNone(result)

    @patch('product_info_fetcher.barcode_reader.openfoodfacts.products.get_product')
    def test_other_api_error(self, mock_get_product):
        # Configure the mock to raise a generic Exception
        mock_get_product.side_effect = Exception("Test generic API error")
        
        result = get_product_info("dummy_barcode_other_error")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
