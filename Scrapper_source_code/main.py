from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import os
import klasy_scrapper


BASE_URL = "https://wloczykijki.pl"
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GECKODRIVER_PATH = "C:\\Users\\nozak\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Python 3.12\\Scripts\\geckodriver.exe"

firefox_options = Options()
firefox_options.add_argument("--headless")

def initialize_driver():
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def main():
    Wloczykijki = klasy_scrapper.Wloczykijki(BASE_URL)

    driver = initialize_driver()

    try:
        Wloczykijki.scrapuj_kategorie(driver)
        Wloczykijki.parsuj_liste_kategorii()   #lista kategorii
        for i in range(6):
            Wloczykijki.kategorie[i].scrapuj_podkategorie(driver)
            Wloczykijki.kategorie[i].parsuj_liste_podkategorii()    #listy podkategorii

        #OPASKI
        Wloczykijki.kategorie[5].podkategorie[0].scrapuj_produkty(driver)
        Wloczykijki.kategorie[5].JSON_Podkateogria(0)
        Wloczykijki.kategorie[5].generuj_jpg(0)

        #CZAPKI
        Wloczykijki.kategorie[5].podkategorie[1].scrapuj_produkty(driver)
        Wloczykijki.kategorie[5].JSON_Podkateogria(1)
        Wloczykijki.kategorie[5].generuj_jpg(1)

        #ORGANIZERY
        Wloczykijki.kategorie[3].podkategorie[3].scrapuj_produkty(driver)
        Wloczykijki.kategorie[3].JSON_Podkateogria(3)
        Wloczykijki.kategorie[3].generuj_jpg(3)

        #TORBY
        Wloczykijki.kategorie[3].podkategorie[4].scrapuj_produkty(driver)
        Wloczykijki.kategorie[3].JSON_Podkateogria(4)
        Wloczykijki.kategorie[3].generuj_jpg(4)

        #GUZIKI
        Wloczykijki.kategorie[2].podkategorie[6].scrapuj_produkty(driver)
        Wloczykijki.kategorie[2].JSON_Podkateogria(6)
        Wloczykijki.kategorie[2].generuj_jpg(6)

        #NOZYCZKI
        Wloczykijki.kategorie[2].podkategorie[7].scrapuj_produkty(driver)
        Wloczykijki.kategorie[2].JSON_Podkateogria(7)
        Wloczykijki.kategorie[2].generuj_jpg(7)

        #PROBKI
        Wloczykijki.kategorie[0].podkategorie[1].scrapuj_produkty(driver)
        Wloczykijki.kategorie[0].JSON_Podkateogria(1)
        Wloczykijki.kategorie[0].generuj_jpg(1)

        #WLOCZKI
        Wloczykijki.kategorie[0].podkategorie[2].scrapuj_czesc_produktow(driver,65)
        Wloczykijki.kategorie[0].JSON_Podkateogria(2)
        Wloczykijki.kategorie[0].generuj_jpg(2)


    finally:
        driver.quit()

if __name__ == "__main__":
    main()