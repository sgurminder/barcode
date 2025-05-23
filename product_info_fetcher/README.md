# Product Information Fetcher

## Project Overview
Product Information Fetcher is a Python command-line tool that retrieves product details from the Open Food Facts database using a product's barcode. It's designed to quickly provide users with key information about a food product.

## Features
-   **Barcode Lookup:** Fetches product information based on its EAN-13 or UPC barcode.
-   **Specific Information Retrieved:** Gathers essential data such as product name, brand, quantity, ingredients, and categories.
-   **Command-Line Interface (CLI):** Easy-to-use CLI for quick lookups.
-   **Error Handling:** Provides feedback for network issues or if a product is not found.

## Setup Instructions

1.  **Clone the repository (if applicable) or ensure you have the project files.**

2.  **Navigate to the project directory:**
    ```bash
    cd path/to/product_info_fetcher
    ```

3.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv .venv
    ```

4.  **Activate the virtual environment:**
    -   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```
    -   On Windows:
        ```bash
        .\.venv\Scripts\activate
        ```

5.  **Install dependencies:**
    With the virtual environment activated, install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

## Usage Instructions
To use the Product Information Fetcher, run the `barcode_reader.py` script from your terminal, followed by the barcode you wish to look up.

**Command structure:**
```bash
python product_info_fetcher/barcode_reader.py <BARCODE>
```
Replace `<BARCODE>` with the actual product barcode. Ensure you are in the parent directory of `product_info_fetcher` or provide the correct path to `barcode_reader.py`. If you are in the `product_info_fetcher` directory itself, the command would be:
```bash
python barcode_reader.py <BARCODE>
```

## Example Usage
Here's an example of how to look up a product with the barcode `3017620422003`:

**Command:**
```bash
python product_info_fetcher/barcode_reader.py 3017620422003
```
Or, if you are inside the `product_info_fetcher` directory:
```bash
python barcode_reader.py 3017620422003
```

**Example Output (will vary based on product data and availability):**
```
Barcode Reader CLI - Fetching info for barcode: 3017620422003
Product Name: Pépito Pockitos - Chocolat au Lait
Brand: Lu
Quantity: 295 g
Ingredients: Farine de BLÉ 51 %, chocolat au LAIT 27 % [sucre, pâte de cacao, beurre de cacao, LAIT écrémé en poudre, lactosérum en poudre (de LAIT), graisses végétales (palme et karité en proportions variables), BEURRE pâtissier, émulsifiants (lécithines de SOJA, E476), arôme vanille], huile de palme, sucre, sirop de glucose-fructose, LAIT écrémé en poudre 0,7 % (équivalent LAIT écrémé 7,3 %), noix de coco, LAIT entier en poudre 0,3 % (équivalent LAIT entier 2,6 %), poudres à lever (carbonates d'ammonium, carbonates de sodium), sel, arômes.
Categories: Snacks, Snacks sucrés, Biscuits et gâteaux, Biscuits, Biscuits au chocolat, Biscuits au chocolat au lait
```
*(Note: The actual output details like ingredients might be very long or differ. The above is a representative example.)*

If a product is not found or a network error occurs, you will see a message like:
```
Product with barcode <BARCODE> not found or an error occurred while fetching data.
```
Or specific error messages printed to `stderr` in case of network issues.

## Running Tests
To run the unit tests for this project, navigate to the root directory of the project (the one containing the `product_info_fetcher` directory and `setup.py` if it existed) and use the following command:

```bash
python -m unittest discover product_info_fetcher/tests
```
This command will automatically discover and run all tests within the `product_info_fetcher/tests` directory. Make sure you have activated your virtual environment and installed dependencies first.
