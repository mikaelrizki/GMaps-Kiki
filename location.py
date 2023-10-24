from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from env import URL
import time

def data_lokasi():
    print("Function Level : Pencarian Data Lokasi")
    # Informasi terkait lokasi yang ingin didapatkan
    angka_rating = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontDisplayLarge']")
    button = driver.find_element(By.CLASS_NAME, "HHrUdb")
    jumlah_ulasan = button.find_element(By.TAG_NAME, "span")
    # jumlah_ulasan = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontBodySmall']")
    print("\t (i) Berhasil menemukan data lokasi.")
    print("\t (d) Data angka rating pada lokasi  :", angka_rating.text)
    print("\t (d) Data jumlah ulasan pada lokasi :", jumlah_ulasan.text, "\n")

    '''
    Data dalam bentuk list
    [0] -> Angka Rating Bintang dengan range (1,0 - 5,0)
    [1] -> Jumlah Ulasan pada lokasi
    '''
    return [str(angka_rating.text), str(jumlah_ulasan.text)]

if __name__ == "__main__":
    print('Google Maps Scraper oleh Mikael Rizki')
    print('Mulai Program ...')
    
    # Instalasi Chrome Web Driver dan Load Browser 
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Mengarahkan ke URL dari env
    driver.get("https://maps.app.goo.gl/o22SWRD3xqBzic2g7")

    try:
        data_lokasi()
        input()
    except Exception as e:
        print(f"An error occurred: {e}")

    # Menutup Chrome Browser
    driver.quit()