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
#firefox_options.add_argument("--headless")

def initialize_driver():
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def main():
    Wloczykijki = klasy_scrapper.Wloczykijki(BASE_URL)

    driver = initialize_driver()

    try:
        Wloczykijki.scrapuj_kategorie(driver)
        #Wloczykijki.parsuj_liste_kategorii()   #lista kategorii
        for i in range(6):
            Wloczykijki.kategorie[i].scrapuj_podkategorie(driver)
            #Wloczykijki.kategorie[i].parsuj_liste_podkategorii()    #listy podkategorii

        '''
        #OPASKI
        Wloczykijki.kategorie[5].podkategorie[0].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[5].JSON_Podkateogria(0,True)
        Wloczykijki.kategorie[5].generuj_jpg(0,True)

        #CZAPKI
        Wloczykijki.kategorie[5].podkategorie[1].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[5].JSON_Podkateogria(1,True)
        Wloczykijki.kategorie[5].generuj_jpg(1,True)

        
        #ORGANIZERY
        Wloczykijki.kategorie[3].podkategorie[3].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[3].JSON_Podkateogria(3,True)
        Wloczykijki.kategorie[3].generuj_jpg(3,True)

        #TORBY
        Wloczykijki.kategorie[3].podkategorie[4].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[3].JSON_Podkateogria(4,True)
        Wloczykijki.kategorie[3].generuj_jpg(4,True)
        '''

        #GUZIKI
        Wloczykijki.kategorie[2].podkategorie[6].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[2].JSON_Podkateogria(6,True)
        Wloczykijki.kategorie[2].generuj_jpg(6,True)

        #NOZYCZKI
        Wloczykijki.kategorie[2].podkategorie[7].scrapuj_produkty(driver,True)
        Wloczykijki.kategorie[2].JSON_Podkateogria(7,True)
        Wloczykijki.kategorie[2].generuj_jpg(7,True)

        '''
        #PROBKI
        Wloczykijki.kategorie[0].podkategorie[1].scrapuj_produkty(driver,False)
        Wloczykijki.kategorie[0].JSON_Podkateogria(1,False)
        Wloczykijki.kategorie[0].generuj_jpg(1,False)
        '''

        #WLOCZKI
        Wloczykijki.kategorie[0].podkategorie[2].scrapuj_czesc_produktow(driver,65,True)
        Wloczykijki.kategorie[0].JSON_Podkateogria(2,True)
        Wloczykijki.kategorie[0].generuj_jpg(2,True)




    finally:
        driver.quit()

if __name__ == "__main__":
    main()