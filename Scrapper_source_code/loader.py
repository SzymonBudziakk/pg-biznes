import os
import base64
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "http://localhost:8080/api"

def upload_product_image(product_id, image_path):
    endpoint = f"{API_URL}/images/products/{product_id}"
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{API_KEY}:".encode()).decode()}'
    }
    try:
        with open(image_path, 'rb') as image_file:
            files = {
                'image': (image_path.split('/')[-1], image_file, 'image/jpeg')
            }
            response = requests.post(endpoint, headers=headers, files=files, verify=False)

        # Check for success
        if response.status_code < 300 or response.status_code == 500:
            print("Image uploaded successfully.")
        else:
            print(f"Failed to upload image: {response.status_code} - {response.text}")

        return response

    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_product(category_id, name, price, description, vat_category="1", lang="1"):
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
    meta_description_lang.text = description

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
    ET.SubElement(product, "id_tax_rules_group").text = vat_category
    ET.SubElement(product, "indexed").text = "1"

    product_data = ET.tostring(prestashop, encoding="utf-8", method="xml").decode("utf-8")

    encoded_key = base64.b64encode(f"{API_KEY}:".encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_key}',
        'Content-Type': 'application/xml'
    }
    response = requests.post(API_URL + "/products", headers=headers, data=product_data, verify=False)

    if response.status_code == 201:
        print("Sukces: Produkt dodany.")
    else:
        print(f"Błąd: {response.status_code} - {response.text}")
        print("Nagłówki żądania:", response.request.headers)
        print("Dane wysłane:", product_data)

data = {
    "nazwa": "Torba Hobby Bag - abstrakcja",
    "cena": "89,00 zł",
    "opis": "Materiał: płótno, gramatura 220 g/m2; wypełnienie: izolonKolor: zewnętrzny - wzór, wewnętrzny - jednolity (beżowy) z elementami wzoruWymiary: szer. 30 cm, wys. 26 cm,  głęb. 13 cmUchwyt: podwójny, 44 cmWnętrze: 9 funkcjonalnych kieszeni, 1 metalowy pierścień na przypinki\nMasa: 0,2 kg\nPranie: prać ręcznie. Suszyć rozłożone na płasko.\nTolerancja wymiarów +/- 2 cm\n",
    "zdjecie": "https://wloczykijki.pl/environment/cache/images/300_300_productGfx_4436/abstrakcja1.webp",
    "zdjecie2": "https://wloczykijki.pl/environment/cache/images/500_500_productGfx_4436/abstrakcja1.webp",
    "zdjecie_jpg": "Gadżety_Torby na hobby-images\\image_0_1.jpg",
    "zdjecie2_jpg": "Gadżety_Torby na hobby-images\\image_0_2.jpg"
}

# convert price

# def add_p(category_id, name, price, description, vat_category="1", lang="1"):
# add_product(20, 'NOWY PRODUKT', 22, 'OPIS PRODUKTU')

image_path = 'Scrapper_data/Gadżety_Torby na hobby-images/image_0_2.jpg'
api_image_path = '../' + image_path

#def upload_product_image(product_id, image_path):
upload_product_image(33, api_image_path)


