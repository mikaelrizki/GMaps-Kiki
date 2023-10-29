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
- COLLECTOR_NAME : Sebagai nama collector dari hasil review yang diperoleh
- CREDENTIALS_FILE : Merujuk sebagai nama file kredensial dari API Google
- URL : Berisikan list dari URL POI Google Maps, dapat berisikan 1 atau lebih

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

**5. Cek hasil di Google SpreadSheet**

Periksa hasil yang dari Google SpreadSheet, berikut adalah contoh hasil yang diperoleh :
