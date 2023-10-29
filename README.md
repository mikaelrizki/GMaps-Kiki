# Google Maps Review Scraper

Scrapper Review Google Maps menggunakan Selenium Python
```
Dibuat oleh : Mikael Rizki Pandu Ekanto
Kolaborasi dengan : Danny Sebastian, S.Kom., M.M., M.T.
```
Kamu dapat menggunakan repositori ini untuk berbagai project, silahkan lakukan kostumisasi sesuai dengan keperluanmu!

## Fitur

- Support untuk segala desktop device
- Ekstraksi review dari berbagai POI di Google Mpas
- Kustomisasi filter ulasan berdasarkan preferensi
- Pemantauan terhadap jalannya program melalui Chrome Web Driver
- Dapat digunakan untuk ekstraksi lebih dari 1 POI
- Mendapatkan maksimal 1090 data review selama satu cycle (Tested on Windows 11) 
- Hasil ekstraksi dimuat ke dalam Google SpreadSheet

## Cara Penggunaan

**1. Clone repositori ini**
```
git clone https://github.com/mikaelrizki/GMaps-Scrapper.git
gh repo clone mikaelrizki/GMaps-Scrapper
```
**2. Set-Up file .env**
   
Berikut adalah struktur file .env yang akan digunakan :

```
COLLECTOR_NAME = "Mikael Rizki"
CREDENTIALS_FILE = "credentials-mikael.json"
URL = [
  "https://maps.app.goo.gl/RQQBBfd4aBtsMYH57",
  ... add more URL ...
]
```
*Penjelasan :*
- **COLLECTOR_NAME** : Sebagai nama collector dari hasil review yang diperoleh
- **CREDENTIALS_FILE** : Merujuk sebagai nama file kredensial dari API Google
- **URL** : Berisikan list dari URL POI Google Maps, dapat berisikan 1 atau lebih

**3. Install library yang diperlukan**

Pada program utama "reviewer.py" lalu run terminal baru dan tuliskan perintah berikut :
```
pip install -r requirements.txt
```

**4. Jalankan program**

Jalankan program utama "reviewer.py" dengan cara :
```
python reviewer.py
```

**5. Panduan program**

Program akan berjalan secara maximized-window dan tanpa load image di browser, kode tersebut dapat ditemukan pada option di :
```
options.add_argument("start-maximized")
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
```
*Penjelasan Program:*
- Tahap 1 : Program akan melakukan instalasi Chrome Web Driver menggunakan webdriver_manager, kemudian option akan diterapkan saat eksekusi program.
- Tahap 2 : Program akan collect data lokasi, kemudian program akan berpindah ke menu ulasan secara otomatis, terakhir program akan collect data rating lokasi dan jumlah ulasan pada lokasi.

  *Note : Pastikan link lokasi yang digunakan didapatkan dari menu share pada lokasi.*

  ![Share](https://github.com/mikaelrizki/GMaps-Scrapper/assets/103487218/53517804-9b91-4507-8a85-38d2334bb583)

- Tahap 3 : Filter ulasan dapat dilakukan menggunakan 2 cara :
  ```
  filter_ulasan()  ->  Untuk filter secara otomatis menggunakan filter ulasan "Terbaru"
  custom_filter_ulasan()  ->  Untuk filter sesuai dengan keperluan (Manual)
  ```
- Tahap 4 : Scroll ulasan dilakukan secara manual, untuk mempermudah silahkan *Inspect Element (F11)* kemudian cari element *lXJj5c Hk4XGb*.

  *Note : Pastikan jumlah ulasan yang diambil kurang dari 1090 ulasan, dapat di periksa melalui pencarian element d4r55*

  ![image](https://github.com/mikaelrizki/GMaps-Scrapper/assets/103487218/35d3b6c6-d717-47b3-9925-7c13564b4a32)

- Tahap 5 : Expand ulasan secara otomatis, silahkan tunggu hingga informasi expand ulasan berhasil dilakukan.
  
  ![image](https://github.com/mikaelrizki/GMaps-Scrapper/assets/103487218/dbf76be0-2070-46a0-a6b7-2f462b980f4f)

- Tahap 6 : Collect data ulasan dilakukan secara otomatis, silahkan tunggu hingga informasi expand ulasan berhasil dilakukan.

  ![image](https://github.com/mikaelrizki/GMaps-Scrapper/assets/103487218/9794084f-a821-4e32-a181-30816c46132a)

- Tahap 7 : Upload data ke Google SpreadSheet akan dilakukan secara otomatis, silahkan lakukan penyesuaian lokasi file pada :
  ```
  spreadsheet = gc.open("[Result] Data Ulasan Google Maps")  ->  Nama file Google SpreadSheet 
  worksheet = spreadsheet.worksheet("Pantai")  ->  Nama halaman / work sheet yang akan digunakan 
  ```
**6. Cek hasil di Google SpreadSheet**

Periksa hasil yang dari Google SpreadSheet, berikut adalah contoh hasil yang diperoleh :

![Hasil](https://github.com/mikaelrizki/GMaps-Scrapper/assets/103487218/5f1ea252-12f6-42d0-831f-602da1357e19)
