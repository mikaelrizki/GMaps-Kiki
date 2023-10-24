def data_lokasi():
    print("Function Level : Pencarian Data Lokasi")
    # Informasi terkait lokasi yang ingin didapatkan
    angka_rating = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontDisplayLarge']")
    jumlah_ulasan = driver.find_element(By.XPATH, "//div[@class='jANrlb']/div[@class='fontBodySmall']")
    print("\t (i) Berhasil menemukan data lokasi.")
    print("\t (d) Data angka rating pada lokasi  :", angka_rating.text)
    print("\t (d) Data jumlah ulasan pada lokasi :", jumlah_ulasan.text, "\n")

    '''
    Data dalam bentuk list
    [0] -> Angka Rating Bintang dengan range (1,0 - 5,0)
    [1] -> Jumlah Ulasan pada lokasi
    '''
    return [str(angka_rating.text), str(jumlah_ulasan.text)]