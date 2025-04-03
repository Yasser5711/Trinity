import json
import logging
import random
from datetime import datetime
from pathlib import Path

import requests

API_URL = "https://world.openfoodfacts.org/cgi/search.pl"
PAGE_SIZE = 10_000
MAX_PRODUCTS = 700_000
COUNTRY_TAG = "france"
OUTPUT_FILE = Path("products_V1.json")


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch_products():
    total_pages = (MAX_PRODUCTS // PAGE_SIZE) + 1
    seen_barcodes = set()
    product_list = []
    product_id = 1

    for page in range(1, total_pages + 1):
        logging.info(f"Fetching page {page} of {total_pages}...")

        params = {
            "action": "process",
            "tagtype_0": "countries",
            "tag_contains_0": "contains",
            "tag_0": COUNTRY_TAG,
            "page_size": PAGE_SIZE,
            "page": page,
            "json": 1,
        }

        try:
            response = requests.get(API_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as err:
            logging.error(f"Failed API request: {err}")
            raise SystemExit(f"Failed API request: {err}") from err
        except json.JSONDecodeError as err:
            logging.error("Invalid JSON response")
            raise SystemExit("Failed to decode JSON response") from err

        products = data.get("products", [])
        if not products:
            logging.info("No more products found. Ending fetch.")
            break

        for product in products:
            try:
                name = product.get("product_name")
                bar_code = product.get("code")
                description = product.get("generic_name")
                picture = product.get("image_small_url")

                if not all([name, bar_code, description, picture]):
                    continue

                if bar_code in seen_barcodes:
                    continue

                try:
                    bar_code_int = int(bar_code)
                except ValueError:
                    continue

                seen_barcodes.add(bar_code)

                product_data = {
                    "product_id": product_id,
                    "name": name,
                    "description": description,
                    "brandId": product.get("brands", "").split(",")[0].strip() or None,
                    "category": product.get("categories", "").split(",")[0].strip()
                    or None,
                    "nutriScore": product.get("nutriscore_grade"),
                    "picture_url": product.get("image_url"),
                    "picture": picture,
                    "barCode": bar_code_int,
                    "quantity": product.get("quantity"),
                    "nutrition": product.get("nutriments", {}),
                    "ingredients": product.get("ingredients_text"),
                    "allergens": product.get("allergens"),
                    "price": round(random.uniform(1.0, 10.0), 2),  # noqa: S311
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }

                product_list.append(product_data)
                product_id += 1

            except KeyError as err:
                logging.warning(f"Missing expected field: {err}")
            except Exception as err:
                logging.warning(f"Unexpected error while parsing product: {err}")

    return product_list


def save_to_file(data: list, output_path: Path):
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Successfully wrote {len(data)} products to {output_path}")
    except OSError as err:
        raise OSError(f"Failed to write output file: {err}") from err


def main():
    logging.info("Starting product fetch...")
    products = fetch_products()
    save_to_file(products, OUTPUT_FILE)


if __name__ == "__main__":
    main()
