import unittest
from unittest.mock import patch
import requests.exceptions

# Adjust the import path based on how you will run the tests
from product_info_fetcher.barcode_reader import get_product_info

class TestBarcodeReader(unittest.TestCase):

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_successful_product_lookup(self, mock_api_get):
        sample_barcode = "1234567890123"
        api_response = {
            "code": sample_barcode,
            "product_name": "Delicious Chips",
            "brands": "ChipCo",
            "quantity": "200g",
            "ingredients_text": "Potatoes, Oil, Salt",
            "categories": "Snacks, Salty Snacks"
        }
        mock_api_get.return_value = api_response

        expected_result = {
            "product_name": "Delicious Chips",
            "brand": "ChipCo",  # 'brands' from API becomes 'brand'
            "quantity": "200g",
            "ingredients_text": "Potatoes, Oil, Salt",
            "categories": "Snacks, Salty Snacks"
        }

        result = get_product_info(sample_barcode)
        self.assertEqual(result, expected_result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_product_not_found_api_returns_none(self, mock_api_get):
        sample_barcode = "0000000000000"
        mock_api_get.return_value = None 
        result = get_product_info(sample_barcode)
        self.assertIsNone(result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_product_not_found_barcode_mismatch(self, mock_api_get):
        requested_barcode = "1111111111111"
        returned_barcode = "2222222222222"
        api_response = {
            "code": returned_barcode, # API returns data for a different barcode
            "product_name": "Some Other Product",
            "brands": "OtherBrand"
        }
        mock_api_get.return_value = api_response
        result = get_product_info(requested_barcode)
        self.assertIsNone(result)
        mock_api_get.assert_called_once_with(requested_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_product_not_found_missing_product_name(self, mock_api_get):
        sample_barcode = "3333333333333"
        api_response = {
            "code": sample_barcode,
            # "product_name": "Essential field missing", # product_name is missing
            "brands": "BrandX",
            "quantity": "100g"
        }
        mock_api_get.return_value = api_response
        result = get_product_info(sample_barcode)
        self.assertIsNone(result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_network_error(self, mock_api_get):
        sample_barcode = "4444444444444"
        mock_api_get.side_effect = requests.exceptions.RequestException("Simulated network error")
        result = get_product_info(sample_barcode)
        self.assertIsNone(result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_other_api_error(self, mock_api_get):
        sample_barcode = "5555555555555"
        mock_api_get.side_effect = Exception("Simulated generic API error")
        result = get_product_info(sample_barcode)
        self.assertIsNone(result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])

    @patch('product_info_fetcher.barcode_reader.api.product.get')
    def test_partial_data_from_api(self, mock_api_get):
        sample_barcode = "6666666666666"
        api_response = {
            "code": sample_barcode,
            "product_name": "Partial Product",
            "brands": "BrandY",
            # quantity is missing
            "ingredients_text": "Ingredients Z",
            # categories is missing
        }
        mock_api_get.return_value = api_response

        expected_result = {
            "product_name": "Partial Product",
            "brand": "BrandY",
            "quantity": None, # Expect None for missing fields
            "ingredients_text": "Ingredients Z",
            "categories": None # Expect None for missing fields
        }
        result = get_product_info(sample_barcode)
        self.assertEqual(result, expected_result)
        mock_api_get.assert_called_once_with(sample_barcode, fields=["product_name", "brands", "quantity", "ingredients_text", "categories", "code"])


if __name__ == '__main__':
    unittest.main()
