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
from datetime import datetime, timedelta

def data_lokasi():
    print("Function Level : Pencarian Data Lokasi")
    # Informasi terkait lokasi yang ingin didapatkan
    angka_rating = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontDisplayLarge']")
    jumlah_ulasan = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontBodySmall']")
    print("\t (i) Berhasil menemukan data lokasi.")
    print("\t (d) Data angka rating pada lokasi  :", angka_rating.text)
    print("\t (d) Data jumlah ulasan pada lokasi :", jumlah_ulasan.text)
    nama_lokasi = input("\t (a) Masukkan Nama Lokasi : ")
    link_lokasi = input("\t (a) Masukkan Link Lokasi : ")
    print()
    dict_data_lokasi = dict(nama_lokasi = nama_lokasi, link_lokasi = link_lokasi, angka_rating = angka_rating.text, jumlah_ulasan = jumlah_ulasan.text)

    '''
    Data dalam bentuk list
    [0] -> Angka Rating Bintang dengan range (1,0 - 5,0)
    [1] -> Jumlah Ulasan pada lokasi
    '''
    return dict_data_lokasi

def filter_ulasan():
    print("Function Level : Filter Ulasan Terbaru")
    # Mencari tombol Urutkan
    btn_urutkan = driver.find_element(By.CSS_SELECTOR, "button.g88MCb.S9kvJb[aria-label='Urutkan ulasan'][data-value='Urutkan']")
    print("\t (i) Berhasil menemukan tombol urutkan.")
    # Menambahkan aksi untuk menekan button urutkan
    btn_urutkan.click()
    print("\t (a) Menekan tombol urutkan!")
    print("\t (i) Menu drop-down untuk filter ulasan terbuka.")

    # Mencari option menu 'terbaru' pada drop-down menu filter ulasan
    # Memberi waktu tunggu selama 10 detik hingga element berhasil ter-load
    menu_terbaru = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-checked='false'][data-index='1'][role='menuitemradio'][tabindex='0'].fxNQSd")))
    # Menambahkan aksi untuk menekan option menu 'terbaru'
    menu_terbaru.click()

    if menu_terbaru:
        print("\t (i) Berhasil menemukan option menu terbaru pada filter ulasan.")
        print("\t (a) Menekan option menu 'terbaru'!\n")
        return True
    else:
        return False


def scroll_ulasan():
    print("Function Level : Scroll Ulasan")
    print("\t (w) Fitur scrolling ulasan gagal dilakukan.")
    print("\t (i) Lakukan scrolling manual pada Browser yang terbuka.")
    input("\t (a) Tekan key apa saja untuk melanjutkan program!")
    print()
    # lXJj5c Hk4XGb
    # scrollable_div = driver.find_element(By.XPATH, '//div[@class="qjESne"]')
    # for _ in range(12):
    #     driver.execute_script(
    #         'arguments[0].scrollTop = arguments[0].scrollHeight',
    #         scrollable_div
    #     )
    #     time.sleep(3)
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    # driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top);", driver.find_elements(By.CSS_SELECTOR, "div.qjESne"))

def expand_ulasan():
    print("Function Level : Expand Ulasan")
    print("\t (i) Waktu tunggu element diatur selama lima detik.")
    time.sleep(5)
    
    print("\t (i) Berhasil menemukan seluruh tombol 'Read More'.")
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.w8nwRe.kyuRq")
    
    print("\t (a) Menekan", len(buttons), "option menu 'Read More'!\n")
    for button in buttons:
        button.click()
    
def ambil_ulasan(data_lokasi):
    '''
    Data Ulasan Google Maps
    Dalam bentuk list yang setiap itemnya berisikan satu buah data dictionary
    {
        "id_reviewer" : <button class="WEBjve" data-href="https://www.google.com/maps/contrib/114379365424296008124/reviews?hl=id">
        "nama_reviewer" : <div class='d4r55'>
        "informasi_reviewer" : <div class="RfnDt">
        "icon_reviewer" : <img class="NBa7we" alt="" src="">
        "isi_ulasan" : <span class='wiI7pd'>
        "informasi_ulasan" : <span class='wiI7pd'>
        "rating_ulasan" : <span class="kvMYJc" role="img" aria-label="4 bintang">
    }
    '''
    data_ulasan = list()
    
    print("Function Level : Ambil Data Ulasan")
    print("\t (i) Waktu tunggu element diatur selama lima detik.")
    time.sleep(5)
    
    semua_data_reviewer = driver.find_elements(By.CSS_SELECTOR, "button.al6Kxe[data-review-id][data-href][jslog]")
    for data_reviewer in semua_data_reviewer:
        text = data_reviewer.text
        temp = text.split("\n")
        
        meta_id_reviewer = data_reviewer.get_attribute("data-href")
        id_reviewer = meta_id_reviewer.split("/contrib/")[1].split("/")[0]
        
        if(len(temp) == 1):
            dict_data_reviewer = dict(id_reviewer = id_reviewer, nama_reviewer = temp[0], informasi_reviewer = "null")
        else:
            dict_data_reviewer = dict(id_reviewer = id_reviewer, nama_reviewer = temp[0], informasi_reviewer = temp[1])
        
        data_ulasan.append(dict_data_reviewer)
    
    print("\t (i) Berhasil mendapatkan data reviewer sebanyak " +  str(len(data_ulasan)) + ".")
    # for i in data_ulasan:
    #     print("ID : ", i["id_reviewer"], "\tNama : ", i["nama_reviewer"], "\tInformasi :", i["informasi_reviewer"])
    
    data_ulasan2 = list()
    semua_data_isi_ulasan = driver.find_elements(By.CSS_SELECTOR, "div.GHT2ce")
    counter = 1
    for i in semua_data_isi_ulasan:
        if counter % 2 == 0:            
            try:
                data1 = i.find_element(By.CSS_SELECTOR, "div div.MyEned span.wiI7pd")
                isi_ulasan = data1.text
            except:
                isi_ulasan = "null"
            
            try:
                data2 = i.find_element(By.CSS_SELECTOR, "div[jslog='127691']")
                informasi_ulasan = driver.execute_script("return arguments[0].innerText;", data2)
                informasi_ulasan = informasi_ulasan.replace("\n", " - ")
            except:
                informasi_ulasan = "null"
            
            data3 = i.find_element(By.CSS_SELECTOR, "span.kvMYJc")
            rating_ulasan = data3.get_attribute("aria-label")
            
            data4 = i.find_element(By.CSS_SELECTOR, "span.rsqaWe")
            raw_waktu = data4.text
            current_date = datetime.now()
            
            time_mapping = {
                "seminggu lalu": timedelta(weeks=1),
                "2 minggu lalu": timedelta(weeks=2),
                "3 minggu lalu": timedelta(weeks=3),
                "4 minggu lalu": timedelta(weeks=4),
                "sebulan lalu": timedelta(days=30),
                "2 bulan lalu": timedelta(days=60),
                "3 bulan lalu": timedelta(days=90),
                "4 bulan lalu": timedelta(days=120),
                "5 bulan lalu": timedelta(days=150),
                "6 bulan lalu": timedelta(days=180),
                "7 bulan lalu": timedelta(days=210),
                "8 bulan lalu": timedelta(days=240),
                "9 bulan lalu": timedelta(days=270),
                "10 bulan lalu": timedelta(days=300),
                "11 bulan lalu": timedelta(days=330),
                "setahun lalu": timedelta(days=365),
                "2 tahun lalu": timedelta(days=730)
            }
            
            waktu_ulasan = current_date - time_mapping[raw_waktu]
            
            dict_data_ulasan = dict(isi_ulasan = isi_ulasan, informasi_ulasan = informasi_ulasan, waktu_ulasan = waktu_ulasan.strftime("%Y-%m-%d"), rating_ulasan = rating_ulasan)
            data_ulasan2.append(dict_data_ulasan)
        counter += 1
    
    print("\t (i) Berhasil mendapatkan data ulasan sebanyak " + str(len(data_ulasan2)) + ".")
    # for i in data_ulasan2:
    #     print("Isi Ulasan : ", i["isi_ulasan"], "\tInformasi Ulasan : ", i["informasi_ulasan"], "\tRating : ", i["rating_ulasan"], )
    
    data = list()
    for dict1, dict2 in zip(data_ulasan, data_ulasan2):
        merged_dict = {**dict1, **dict2}
        data.append(merged_dict)
    print("\t (i) Berhasil menggabungkan data ulasan reviewer sebanyak " + str(len(data)) + ".\n")
    
    new_data = []
    for data_dict in data:
        new_dict = {**data_lokasi, **data_dict}
        new_data.append(new_dict)
    
    return new_data

def upload(data):
    print("Function Level: Upload Data ke SpreadSheet")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open("[Result] Data Ulasan Google Maps")
    worksheet = spreadsheet.worksheet("Sheet2")
    print("\t (a) Opening Spreadsheet:", spreadsheet.title)
    print("\t (a) Opening Worksheet:", worksheet.title)

    data_values = [list(d.values()) for d in data]
    try:
        worksheet.insert_rows(data_values, 2)
        print("\t (i) Data rows inserted successfully.")
    except Exception as e:
        print("\t (e) Error inserting data rows:", str(e))
    print("\t (i) Data uploaded successfully.")
    

if __name__ == "__main__":
    print('Google Maps Scraper oleh Mikael Rizki')
    print('Mulai Program ...')
    
    # Instalasi Chrome Web Driver dan Load Browser 
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Mengarahkan ke URL dari env
    driver.get(URL)

    try:
        data_lokasi = data_lokasi()
        filter_ulasan()
        scroll_ulasan()
        expand_ulasan()
        data = ambil_ulasan(data_lokasi)
        upload(data)
        input("\t (a) Tekan key apapun untuk keluar! ")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Menutup Chrome Browser
    driver.quit()