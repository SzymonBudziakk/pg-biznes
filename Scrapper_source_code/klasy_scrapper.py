from typing import List
import re

import requests
from bs4 import BeautifulSoup
import json
import os
from PIL import Image
from io import BytesIO

BASE_URL = "https://wloczykijki.pl"

class Produkt:
    def __init__(self, nazwa, cena, zdjecie, link, driver):
        self.nazwa = nazwa
        self.cena = cena
        self.opis = ''
        self.zdjecie = BASE_URL+zdjecie
        self.zdjecie2 = ''
        self.link = link
        self.driver = driver
        self.pobierz_szczegolowe_dane()

    def fetch(self):
        self.driver.get(self.link)
        return self.driver.page_source


    def pobierz_szczegolowe_dane(self):
        page_source = self.fetch()
        soup = BeautifulSoup(page_source, "html.parser")

        img_tag = (soup.find('img', class_='photo'))

        if img_tag:
            img_src = img_tag.get('src')
            if img_src:
                self.zdjecie2 = BASE_URL+img_src

        description_div = soup.find('div', class_='resetcss', itemprop='description')
        text = ''

        if description_div:
            paragraphs = [p.text.strip() for p in description_div.find_all('p')]
            text = '\n'.join(paragraphs)

        self.opis = text

    def __call__(self, *args, **kwargs):
        print(self.nazwa + ' ' + self.opis + ' ' + self.cena + ' ' + self.zdjecie + ' ' + self.zdjecie2)

class Podkategoria:
    def __init__(self, nazwa, link):
        self.nazwa = nazwa
        self.link = link
        self.produkty: List[Produkt] = []

    def fetch(self,driver):
        driver.get(self.link)
        return driver.page_source

    def scrapuj_produkty(self,driver):
        page = 1
        main_url = self.link + "/{page}"
        max_page = 1
        page = 1

        while page <= max_page:

            url = main_url.format(page=page)

            driver.get(url)

            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')

            if "404" in driver.title or "Nie znaleziono strony" in html:
                print("404")
                break

            product_divs = soup.find_all('div', class_='product product_view-extended s-grid-3 product-main-wrap product_with-lowest-price')


            if not product_divs:
                print("no product")
                break

            for product_div in product_divs:

                nazwa = product_div.find('span', class_='productname').text.strip() if product_div.find('span', class_='productname') else 'Brak nazwy'
                cena = product_div.find('div', class_='price').find('em').text.strip() if product_div.find('div', class_='price') else 'Brak ceny'
                image_url = product_div.find('img')
                if image_url:
                    src = image_url.get('data-src')
                produkt_link = product_div.find('a', class_='prodimage')['href'] if product_div.find('a',class_='prodimage') else 'Brak linku'
                self.produkty.append(Produkt(nazwa,cena,str(src),BASE_URL+produkt_link,driver))

            if page == 1:
                paginator = soup.find('ul', class_='paginator')
                if paginator:
                    links = paginator.find_all('a')
                    page_numbers = []
                    for link in links:
                        href = link.get('href', '')
                        match = re.search(r'(\d+)$', href)
                        if match:
                            page_numbers.append(int(match.group(1)))
                    if page_numbers:
                        max_page = max(page_numbers)
            page += 1

    def scrapuj_czesc_produktow(self,driver,liczba_stron):
        page = 1
        main_url = self.link + "/{page}"
        max_page = 1
        page = 1

        while page <= max_page:

            url = main_url.format(page=page)

            driver.get(url)

            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')

            if "404" in driver.title or "Nie znaleziono strony" in html:
                print("404")
                break

            product_divs = soup.find_all('div', class_='product product_view-extended s-grid-3 product-main-wrap product_with-lowest-price')


            if not product_divs:
                print("no product")
                break

            for product_div in product_divs:

                nazwa = product_div.find('span', class_='productname').text.strip() if product_div.find('span', class_='productname') else 'Brak nazwy'
                cena = product_div.find('div', class_='price').find('em').text.strip() if product_div.find('div', class_='price') else 'Brak ceny'
                image_url = product_div.find('img')
                if image_url:
                    src = image_url.get('data-src')
                produkt_link = product_div.find('a', class_='prodimage')['href'] if product_div.find('a',class_='prodimage') else 'Brak linku'
                self.produkty.append(Produkt(nazwa,cena,str(src),BASE_URL+produkt_link,driver))

            if page == 1:
                paginator = soup.find('ul', class_='paginator')
                if paginator:
                    links = paginator.find_all('a')
                    page_numbers = []
                    for link in links:
                        href = link.get('href', '')
                        match = re.search(r'(\d+)$', href)
                        if match:
                            page_numbers.append(int(match.group(1)))
                    if page_numbers:
                        max_page = max(page_numbers)
                        if max_page > liczba_stron:
                            max_page = liczba_stron
            page += 1


    def __call__(self, *args, **kwargs):
        print(self.nazwa)
        for k in self.produkty:
           k()

class Kategoria:
    def __init__(self,nazwa, link):
        self.nazwa = nazwa
        self.link = link
        self.podkategorie: List[Podkategoria] = []

    def fetch(self,driver):
        driver.get(self.link)
        return driver.page_source

    def scrapuj_podkategorie(self,driver):
        page_source = self.fetch(driver)
        soup = BeautifulSoup(page_source, "html.parser")

        ul_element = soup.find('ul', class_='level_1')
        li_elements = ul_element.find_all('li')
        for li in li_elements:
            link = li.find('a')
            href = link['href']
            text = link.text
            self.podkategorie.append(Podkategoria(text,BASE_URL+href))

    def __call__(self):
        for k in self.podkategorie:
            print(k.nazwa + 'link: ' + str(k.link))


    def parsuj_liste_podkategorii(self):
        nazwa_pliku = self.nazwa + '_' +'podkategorie.json'
        try:
            nazwy = [pkat.nazwa for pkat in self.podkategorie]

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(nazwy, plik, ensure_ascii=False, indent=4)

        except Exception as e:
            print("Blad zapisu")


    def JSON_Podkateogria(self, numer_podkategorii):
        nazwa_pliku = self.nazwa + '-' + self.podkategorie[numer_podkategorii].nazwa + '.json'
        pola = ["nazwa", "cena", "opis", "zdjecie", "zdjecie2" ]
        try:
            dane = [{pole: getattr(produkt, pole, None) for pole in pola} for produkt in self.podkategorie[numer_podkategorii].produkty]

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)

        except Exception as e:
            print("Blad zapisu")

    def generuj_jpg(self, nr_podkategorii):

        folder = self.nazwa+ '_' + self.podkategorie[nr_podkategorii].nazwa + '-images'
        json_file = self.nazwa + '-' + self.podkategorie[nr_podkategorii].nazwa + '.json'
        os.makedirs(folder, exist_ok=True)
        with open(json_file,'r',encoding='utf-8') as f:
            data = json.load(f)

        for i, pr in enumerate(data):
            try:
                link1 = pr.get('zdjecie')
                link2 = pr.get('zdjecie2')

                if link1:
                    rs = requests.get(link1)
                    rs.raise_for_status()
                    img = Image.open(BytesIO(rs.content))
                    img_jpg_path1 = os.path.join(folder, f"image_{i}_1.jpg")
                    img.convert("RGB").save(img_jpg_path1, "JPEG")
                    pr['zdjecie_jpg'] =  img_jpg_path1

                if link2:
                    rs = requests.get(link2)
                    rs.raise_for_status()
                    img = Image.open(BytesIO(rs.content))
                    img_jpg_path2 = os.path.join(folder, f"image_{i}_2.jpg")
                    img.convert("RGB").save(img_jpg_path2, "JPEG")
                    pr['zdjecie2_jpg'] = img_jpg_path2

            except Exception as e:
                print('blad przy konwersji zdjec')
        with open(json_file,'w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False, indent=4)

class Wloczykijki:
    def __init__(self, link):
        self.link = link
        self.kategorie: List[Kategoria] = []

    def __call__(self):
        for k in self.kategorie:
            print(k.nazwa + 'link: ' + str(k.link))

    def fetch_page_source(self, driver):
        driver.get(BASE_URL)
        return driver.page_source

    def scrapuj_kategorie(self,driver):
        page_source = self.fetch_page_source(driver)
        soup = BeautifulSoup(page_source, "html.parser")

        category_links = soup.find_all("a", class_="spanhover mainlevel")

        for link in category_links:
            category_name = link.find("span").get_text(strip=True)
            self.kategorie.append(Kategoria(category_name, BASE_URL + link['href']))

    def parsuj_liste_kategorii(self):
        nazwa_pliku = 'kategorie.json'
        try:

            nazwy = [kat.nazwa for kat in self.kategorie]

            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(nazwy, plik, ensure_ascii=False, indent=4)

        except Exception as e:
            print("Blad zapisu")
