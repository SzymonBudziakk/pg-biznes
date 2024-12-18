from read_json import read_json
from category import create_category
from product import create_product, upload_image

def load_data():
    categories = read_json(path='../Scrapper_data/kategorie.json')
    load_categories(categories=categories)


def load_categories(categories, parent_category_id=2): # parent_category_id=2 = Home
    for category_name in categories:
        # TODO:-----------------------------
        # if category_name != 'Druty i ...':
        #     continue

        category_id = create_category(
            name=category_name,
            parent_category_id=parent_category_id
        )

        subcategories_path = f'../Scrapper_data/{category_name}_podkategorie.json'
        subcategories = read_json(path=subcategories_path)

        if not subcategories:
            continue

        load_subcategories(
            subcategories=subcategories,
            category_id=category_id,
            category_name=category_name
        )


def load_subcategories(subcategories, category_id, category_name):
    for subcategory_name in subcategories:
        # TODO:-----------------------------
        # if subcategory_name != 'Nożyczki':
        #     continue
            
        subcategory_id = create_category(
            name=subcategory_name,
            parent_category_id=category_id
        )

        products_path = f'../Scrapper_data/{category_name}-{subcategory_name}.json'
        products = read_json(path=products_path)

        if not products:
            continue
        # print(category_name, subcategory_name)

        load_products(
            products=products,
            subcategory_id=subcategory_id
        )

        
def load_products(products, subcategory_id):
    for product in products:
        product_id = create_product(
            category_id=subcategory_id,
            name=product['nazwa'][:64],
            price=product['cena'][:-3].replace(',', '.'),
            description=product['opis'][:512]
        )

        image_paths = [f'Scrapper_data\\{product['zdjecie2_jpg']}']
        if 'zdjecie3_jpg' in product:
            image_paths.append(f'Scrapper_data\\{product['zdjecie3_jpg']}')

        load_images(
            product_id=product_id,
            image_paths=image_paths
        )


def load_images(product_id, image_paths):
    for image_path in image_paths:
        upload_image(
            product_id=product_id,
            image_path=image_path
        )

load_data()


