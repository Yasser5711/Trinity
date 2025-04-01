import json
import random
from datetime import datetime

import requests


def main():
    api_url = "https://world.openfoodfacts.org/cgi/search.pl"

    total_products_to_fetch = 700000
    page_size = 10000
    total_pages = (total_products_to_fetch // page_size) + 1

    product_list = []
    seen_barcodes = set()  # Ensemble pour vérifier les doublons
    product_id = 1

    for page in range(1, total_pages + 1):
        params = {
            "action": "process",
            "tagtype_0": "countries",
            "tag_contains_0": "contains",
            "tag_0": "france",
            "page_size": page_size,
            "page": page,
            "json": 1,
        }
        print(f"Récupération de la page {page}...")

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête HTTP : {e}")
            break
        except json.JSONDecodeError:
            print("Erreur lors du décodage JSON.")
            break

        if "products" in data:
            products = data["products"]
            print(f"Nombre de produits récupérés sur la page {page} : {len(products)}")

            if not products:
                print(
                    f"Aucun produit trouvé sur la page {page}. Arrêt de la pagination."
                )
                break

            for product in products:
                try:
                    brand = product.get("brands", "").split(",")[0].strip() or None
                    nutri_score = product.get("nutriscore_grade", None)
                    category = (
                        product.get("categories", "").split(",")[0].strip() or None
                    )
                    picture_url = product.get("image_url", None)
                    name = product.get("product_name", None)
                    bar_code = product.get("code", None)
                    description = product.get("generic_name", None)
                    picture = product.get("image_small_url", None)

                    # Champs supplémentaires
                    quantity = product.get("quantity", None)
                    nutrition = product.get("nutriments", {})
                    ingredients = product.get("ingredients_text", None)
                    allergens = product.get("allergens", None)

                    price = random.uniform(1.0, 10.0)

                    # Ignorer les produits sans informations essentielles
                    if not all([name, bar_code, description, picture]):
                        continue

                    # Vérification des doublons avec le code-barres
                    if bar_code in seen_barcodes:
                        print(f"Doublon ignoré pour le produit avec le code-barres {bar_code}.")
                        continue

                    seen_barcodes.add(bar_code)  # Ajouter le code-barres vu
                    current_datetime = datetime.now().isoformat()

                    product_data = {
                        "brandId": brand,
                        "nutriScore": nutri_score,
                        "category": category,
                        "updated_at": current_datetime,
                        "picture_url": picture_url,
                        "price": round(price, 2),
                        "description": description,
                        "name": name,
                        "barCode": int(bar_code),
                        "product_id": product_id,
                        "picture": picture,
                        "quantity": quantity,
                        "nutrition": nutrition,
                        "ingredients": ingredients,
                        "allergens": allergens,
                        "created_at": current_datetime,
                    }

                    product_list.append(product_data)
                    product_id += 1

                    print(
                        f"Produit ajouté : {name} avec un prix de {round(price, 2)} €"
                    )

                except Exception as e:
                    print(f"Erreur lors du traitement du produit {name}: {e}")

        else:
            print(f"Aucun produit trouvé sur la page {page}. Arrêt de la pagination.")
            break

    output_file = "products_V1.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(product_list, f, ensure_ascii=False, indent=4)
        print(
            f"Les données de {len(product_list)} produits ont été écrites dans {output_file}."
        )
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")


if __name__ == "__main__":
    main()
