import requests
import xml.etree.ElementTree as ET
from config import API_URL, HEADERS, API_KEY
import random
import re
import os

def get_products():
    endpoint = f"{API_URL}/products"

    try:
        response = requests.get(endpoint, headers=HEADERS, verify=False)

        if response.status_code == 200:
            print("Products fetched successfully!")
            root = ET.fromstring(response.text)
            for product in root.findall(".//product"):
                product_id = product.get("id")
                if product_id:
                    print(f"Product ID: {product_id}")
                else:
                    print("Product ID: Not found")
        else:
            print(f"Failed to fetch products: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def upload_image(product_id, image_path):
    if not os.path.isfile(image_path):
        print(f"File not found: {image_path}")
        return None

    endpoint = f"{API_URL}/images/products/{product_id}"

    try:
        with open(image_path, 'rb') as image_file:
            files = {
                'image': (os.path.basename(image_path), image_file, 'image/jpeg')
            }
            response = requests.post(endpoint, headers=HEADERS, files=files, verify=False)

        if response.status_code in [200, 201]:
            print("Image uploaded successfully.")
            return response
        else:
            print(f"Failed to upload image: {response.status_code} - {response.text}")
            return response

    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_quantity(product_id, new_quantity):
    stock_url = f"{API_URL}/stock_availables"
    params = {
        "filter[id_product]": product_id,
        "display": "full"
    }

    response = requests.get(stock_url, params=params, auth=(API_KEY, ''), verify=False)
    if response.status_code != 200:
        raise Exception(f"Error getting stock availables: {response.status_code}, {response.text}")

    root = ET.fromstring(response.content)
    stock_id = root.find(".//stock_available/id").text
    id_shop = root.find(".//stock_available/id_shop").text
    id_product_attribute = root.find(".//stock_available/id_product_attribute").text
    id_shop_group = root.find(".//stock_available/id_shop_group").text
    depends_on_stock = root.find(".//stock_available/depends_on_stock").text
    location = root.find(".//stock_available/location").text

    if not stock_id:
        raise Exception(f"Stock available not found for product: {product_id}")

    update_url = f"{API_URL}/stock_availables/{stock_id}"
    prestashop = ET.Element("prestashop", {"xmlns:xlink": "http://www.w3.org/1999/xlink"})
    stock_available = ET.SubElement(prestashop, "stock_available")
    ET.SubElement(stock_available, "id").text = str(stock_id)
    ET.SubElement(stock_available, "id_product").text = str(product_id)
    ET.SubElement(stock_available, "id_product_attribute").text = str(id_product_attribute)
    ET.SubElement(stock_available, "id_shop").text = str(id_shop)
    ET.SubElement(stock_available, "quantity").text = str(new_quantity)
    ET.SubElement(stock_available, "id_shop_group").text = str(id_shop_group)
    ET.SubElement(stock_available, "depends_on_stock").text = str(depends_on_stock)
    ET.SubElement(stock_available, "out_of_stock").text = "0"
    ET.SubElement(stock_available, "location").text = str(location)

    update_data = ET.tostring(prestashop, encoding="utf-8", method="xml").decode("utf-8")
    requests.put(update_url, headers=HEADERS, data=update_data, auth=(API_KEY, ''), verify=False)

def create_product(category_id, name, price, description, lang="1"):
    prestashop = ET.Element("prestashop", {"xmlns:xlink": "http://www.w3.org/1999/xlink"})
    product = ET.SubElement(prestashop, "product")

    name_elem = ET.SubElement(product, "name")
    name_lang = ET.SubElement(name_elem, "language", {"id": lang})
    name_lang.text = name
    ET.SubElement(product, "price").text = str(price)

    description_elem = ET.SubElement(product, "description")
    description_lang = ET.SubElement(description_elem, "language", {"id": lang})
    description_lang.text = description

    meta_description_elem = ET.SubElement(product, "meta_description")
    meta_description_lang = ET.SubElement(meta_description_elem, "language", {"id": lang})
    meta_description = re.sub(r'[^A-Za-z0-9\s]', '', description[:255])
    meta_description_lang.text = meta_description

    meta_keywords_elem = ET.SubElement(product, "meta_keywords")
    meta_keywords_lang = ET.SubElement(meta_keywords_elem, "language", {"id": lang})
    meta_keywords_lang.text = "tag"

    meta_title_elem = ET.SubElement(product, "meta_title")
    meta_title_lang = ET.SubElement(meta_title_elem, "language", {"id": lang})
    meta_title_lang.text = "title"

    ET.SubElement(product, "id_category_default").text = str(category_id)
    associations = ET.SubElement(product, "associations")
    categoriess = ET.SubElement(associations, "categories")
    category = ET.SubElement(categoriess, "category")
    ET.SubElement(category, "id").text = str(category_id)

    ET.SubElement(product, "active").text = "1"
    ET.SubElement(product, "visibility").text = "both"
    ET.SubElement(product, "state").text = "1"
    ET.SubElement(product, "available_for_order").text = "1"
    ET.SubElement(product, "minimal_quantity").text = "1"
    ET.SubElement(product, "reference").text = name.replace(" ", "_")
    ET.SubElement(product, "id_tax_rules_group").text = '1'
    ET.SubElement(product, "indexed").text = "1"

    product_data = ET.tostring(prestashop, encoding="utf-8", method="xml").decode("utf-8")
    response = requests.post(API_URL + "/products", headers=HEADERS, data=product_data, verify=False)

    if response.status_code == 201:
        try:
            root = ET.fromstring(response.text)
            product_id = root.find("./product/id").text
            print(f"New Product ID: {product_id}")
        
            # set product quantity
            if random.random() < 0.75:
                quantity = random.randint(3, 100)
                update_quantity(product_id, quantity)
            else:
                print(f"Skipping stock update for product ID {product_id}.")
        
            return product_id
        
        except Exception as e:
            print("Unable to parse the product ID:", e)
            return None
    else:
        print(f"An error occured: {response.status_code} {response.text}")
        return None