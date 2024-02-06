from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from env import COLLECTOR_NAME, CREDENTIALS_FILE, GSHEETS_NAME, WORKSHEET_NAME, URL
import time
from datetime import datetime, timedelta


def data_lokasi(url):
    print("Function Level : Pencarian Data Lokasi")
    # Informasi terkait lokasi yang ingin didapatkan
    time.sleep(1)
    nama_lokasi = driver.find_element(By.CLASS_NAME, "DUwDvf")
    nama_lokasi = nama_lokasi.text
    print("\t (i) Berhasil menemukan data lokasi.")
    print("\t (d) Nama lokasi  :", nama_lokasi)
    print("\t (d) Link lokasi  :", url)
    time.sleep(1)
    buttons = driver.find_elements(By.XPATH, "//div[@class='RWPxGd']//button")

    # Melakukan aksi penekanan pada tombol "Ulasan"
    ulasan_button = buttons[1]
    ulasan_button.click()
    print("\t (a) Menekan tombol Ulasan!")

    angka_rating = driver.find_element(
        By.XPATH, "//div[@class='jANrlb ']/div[@class='fontDisplayLarge']"
    )
    angka_rating = angka_rating.text
    angka_rating = angka_rating.replace(",", ".")
    jumlah_ulasan = driver.find_element(
        By.XPATH, "//div[@class='jANrlb ']/div[@class='fontBodySmall']"
    )
    jumlah_ulasan = jumlah_ulasan.text
    jumlah_ulasan = jumlah_ulasan.replace(" ulasan", "")

    print("\t (d) Data angka rating pada lokasi  :", angka_rating)
    print("\t (d) Data jumlah ulasan pada lokasi :", jumlah_ulasan, "\n")

    dict_data_lokasi = dict(
        nama_lokasi=nama_lokasi,
        link_lokasi=url,
        angka_rating=angka_rating,
        jumlah_ulasan=jumlah_ulasan,
    )
    """
    Data dalam bentuk list
    [0] -> Angka Rating Bintang dengan range (1,0 - 5,0)
    [1] -> Jumlah Ulasan pada lokasi
    """

    return dict_data_lokasi


def filter_ulasan():
    print("Function Level : Filter Ulasan Terbaru")
    # Mencari tombol Urutkan
    btn_urutkan = driver.find_element(
        By.CSS_SELECTOR,
        "button.g88MCb.S9kvJb[aria-label='Urutkan ulasan'][data-value='Urutkan']",
    )
    print("\t (i) Berhasil menemukan tombol urutkan.")
    # Menambahkan aksi untuk menekan button urutkan
    btn_urutkan.click()
    print("\t (a) Menekan tombol urutkan!")
    print("\t (i) Menu drop-down untuk filter ulasan terbuka.")

    # Mencari option menu 'terbaru' pada drop-down menu filter ulasan
    # Memberi waktu tunggu selama 10 detik hingga element berhasil ter-load
    menu_terbaru = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "div[aria-checked='false'][data-index='1'][role='menuitemradio'][tabindex='0'].fxNQSd",
            )
        )
    )
    # Menambahkan aksi untuk menekan option menu 'terbaru'
    menu_terbaru.click()

    if menu_terbaru:
        print("\t (i) Berhasil menemukan option menu terbaru pada filter ulasan.")
        print("\t (a) Menekan option menu 'terbaru'!\n")
        return True
    else:
        return False


def custom_filter_ulasan():
    print("Function Level : Filter Ulasan")
    print("\t (i) Lakukan pemilihan filter secara manual pada Browser yang terbuka.")
    print()


def scroll_ulasan():
    print("Function Level : Scroll Ulasan")
    print("\t (w) Fitur scrolling ulasan gagal dilakukan.")
    print("\t (i) Lakukan scrolling manual pada Browser yang terbuka.")
    input("\t (a) Tekan key apa saja untuk melanjutkan program!")
    print()
    # Element Scroll : lXJj5c Hk4XGb
    # Cek Jumlah Review : d4r55


def expand_ulasan():
    print("Function Level : Expand Ulasan")
    print("\t (i) Berhasil menemukan seluruh tombol 'Read More'.")
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.w8nwRe.kyuRq")

    print("\t (a) Menekan", len(buttons), "option menu 'Read More'!\n")
    for button in buttons:
        button.click()


def ambil_ulasan(data_lokasi, collector_name):
    """
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
    """
    data_ulasan = list()

    print("Function Level : Ambil Data Ulasan")
    print("\t (i) Waktu tunggu element diatur selama tiga detik.")
    time.sleep(3)

    semua_data_reviewer = driver.find_elements(
        By.CSS_SELECTOR, "button.al6Kxe[data-review-id][data-href][jslog]"
    )
    for data_reviewer in semua_data_reviewer:
        text = data_reviewer.text
        temp = text.split("\n")

        meta_id_reviewer = data_reviewer.get_attribute("data-href")
        id_reviewer = meta_id_reviewer.split("/contrib/")[1].split("/")[0]

        if len(temp) == 1:
            dict_data_reviewer = dict(
                id_reviewer=id_reviewer,
                nama_reviewer=temp[0],
                informasi_reviewer="null",
            )
        else:
            dict_data_reviewer = dict(
                id_reviewer=id_reviewer,
                nama_reviewer=temp[0],
                informasi_reviewer=temp[1],
            )

        data_ulasan.append(dict_data_reviewer)

    print(
        "\t (i) Berhasil mendapatkan data reviewer sebanyak "
        + str(len(data_ulasan))
        + "."
    )
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
                informasi_ulasan = driver.execute_script(
                    "return arguments[0].innerText;", data2
                )
                informasi_ulasan = informasi_ulasan.replace("\n", " - ")
            except:
                informasi_ulasan = "null"

            data3 = i.find_element(By.CSS_SELECTOR, "span.kvMYJc")
            rating_ulasan = data3.get_attribute("aria-label")
            rating_ulasan = rating_ulasan.replace(" bintang", "")

            data4 = i.find_element(By.CSS_SELECTOR, "span.rsqaWe")
            raw_waktu = data4.text
            current_date = datetime.now()

            time_mapping = dict()

            for i in range(1, 60):
                time_mapping[f"{i} menit lalu"] = timedelta(minutes=i)

            for i in range(1, 24):
                time_mapping[f"{i} jam lalu"] = timedelta(hours=i)

            for i in range(1, 32):
                time_mapping[f"{i} hari lalu"] = timedelta(days=i)

            time_mapping["seminggu lalu"] = timedelta(weeks=1)
            for i in range(1, 5):
                time_mapping[f"{i} minggu lalu"] = timedelta(weeks=i)

            time_mapping["sebulan lalu"] = timedelta(days=30)
            for i in range(1, 13):
                time_mapping[f"{i} bulan lalu"] = timedelta(days=i * 30)

            time_mapping["setahun lalu"] = timedelta(days=365)
            for i in range(1, 13):
                time_mapping[f"{i} tahun lalu"] = timedelta(days=i * 365)

            try:
                waktu_ulasan = current_date - time_mapping[raw_waktu]
                waktu_ulasan = waktu_ulasan.strftime("%Y-%m-%d")
            except:
                waktu_ulasan = raw_waktu

            dict_data_ulasan = dict(
                isi_ulasan=isi_ulasan,
                informasi_ulasan=informasi_ulasan,
                waktu_ulasan=waktu_ulasan,
                rating_ulasan=rating_ulasan,
                collector=collector_name,
            )
            data_ulasan2.append(dict_data_ulasan)
        counter += 1

    print(
        "\t (i) Berhasil mendapatkan data ulasan sebanyak "
        + str(len(data_ulasan2))
        + "."
    )
    # for i in data_ulasan2:
    #     print("Isi Ulasan : ", i["isi_ulasan"], "\tInformasi Ulasan : ", i["informasi_ulasan"], "\tRating : ", i["rating_ulasan"], )

    data = list()
    for dict1, dict2 in zip(data_ulasan, data_ulasan2):
        merged_dict = {**dict1, **dict2}
        data.append(merged_dict)
    print(
        "\t (i) Berhasil menggabungkan data ulasan reviewer sebanyak "
        + str(len(data))
        + ".\n"
    )

    new_data = []
    for data_dict in data:
        new_dict = {**data_lokasi, **data_dict}
        new_data.append(new_dict)

    return new_data


def upload(data, credentials_file, gsheets_name, worksheet_name):
    cond = False
    while cond != True:
        try:
            print("Function Level: Upload Data ke SpreadSheet")
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_file, scope
            )
            gc = gspread.authorize(credentials)
            spreadsheet = gc.open(gsheets_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            print("\t (a) Opening Spreadsheet:", spreadsheet.title)
            print("\t (a) Opening Worksheet:", worksheet.title)

            data_values = [list(d.values()) for d in data]
            try:
                worksheet.insert_rows(data_values, 2)
                print("\t (i) Data rows inserted successfully.")
            except Exception as e:
                print("\t (e) Error inserting data rows:", str(e))
            print("\t (i) Data uploaded successfully.")
            cond = True
        except:
            print(f"\t An error occurred: {e}")


if __name__ == "__main__":
    print("Google Maps Scraper oleh Mikael Rizki")
    print("Mulai Program ...")

    # Instalasi Chrome Web Driver dan Load Browser
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    for url in URL:
        # Mengarahkan ke URL dari env
        driver.get(url)

        try:
            data_lokasi = data_lokasi(url)
            # filter_ulasan()
            custom_filter_ulasan()
            scroll_ulasan()
            expand_ulasan()
            repeat = ""
            data = ambil_ulasan(data_lokasi, COLLECTOR_NAME)
            upload(data, CREDENTIALS_FILE, GSHEETS_NAME, WORKSHEET_NAME)
            print("\t (i) Melakukan penghapusan cache pada browser.")
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            driver.execute_script("window.location.reload(true);")
            print("\t (a) Masukkan 'stop' untuk berhenti ambil data!")
            repeat = input("\t (inp) Masukkan kamu : ")
            print()
            while repeat != "stop":
                expand_ulasan()
                data = ambil_ulasan(data_lokasi, COLLECTOR_NAME)
                upload(data, CREDENTIALS_FILE, GSHEETS_NAME, WORKSHEET_NAME)
                print("\t (i) Melakukan penghapusan cache pada browser.")
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.execute_script("window.location.reload(true);")
                print("\t (a) Masukkan 'stop' untuk berhenti ambil data!")
                repeat = input("\t (inp) Masukkan kamu : ")
                print()
        except Exception as e:
            print(f"An error occurred: {e}")

    # Menutup Chrome Browser
    driver.quit()
    print("Program selesai!\n")
