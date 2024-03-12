import csv
import copy
import json
from collections import defaultdict
from datetime import datetime

def encrypt(text):
    key = "157890236"
    encrypted_text = ""
    key_index = len(text) % 9

    for char in text:
        if not char.isalpha():
            key_index += 1
            continue

        if key_index >= len(key):
            key_index = 0

        char_unicode = ord(char)
        if not(char.islower() | char.isupper()):
            char_unicode = char_unicode%26
            if char_unicode%2 == 0:
                char = chr(ord('a') + char_unicode)
            else:
                char = chr(ord('Z') - char_unicode)
            char_unicode = ord(char)
        
        key_digit = int(key[key_index])

        if char.islower():
            encrypted_char_unicode = char_unicode + key_digit
            if encrypted_char_unicode > ord('z'):
                encrypted_char_unicode = ord('a') + (encrypted_char_unicode - ord('z') - 1)
        elif char.isupper() :
            encrypted_char_unicode = char_unicode - key_digit
            if encrypted_char_unicode < ord('A'):
                encrypted_char_unicode = ord('Z') + (encrypted_char_unicode - ord('A') + 1)
        
        encrypted_char = chr(encrypted_char_unicode)
        if key_index %2 == 0 | key_digit%2 != 0:
            encrypted_char = encrypted_char.upper()
        else:
            encrypted_char = encrypted_char.lower()
        
        encrypted_text += encrypted_char
        key_index += 1

    return encrypted_text

def extract_info(input_string):
	list = input_string.split("\u00b7")
	status = ""
	num_of_reviews = ""
	num_of_photos = ""
	for each in list:
		if each.find("Local Guide") >=0 :
			status = "Local Guide"
		if each.find("ulasan") >=0 :
			num_of_reviews = each.rstrip(" ulasan")
		if each.find("foto") >=0 :
			num_of_photos = each.rstrip(" foto")	
	return status, num_of_reviews, num_of_photos

def generate_reviewer_id(data):
    if len(data["reviewers"]) == 0:
         return 1
    max_reviewer_id = max(int(reviewer["reviewer_id"]) for reviewer in data["reviewers"])
    new_reviewer_id = str(max_reviewer_id + 1)
    return new_reviewer_id

def update_or_insert_reviewer(tempList, newReviewer):
    # Jika google_id sudah ada, cari index untuk pembaruan
    index_to_update = None
    index_to_insert = -1
    #print("start update or insert")
    returnReviewer = newReviewer.copy()
    
    if len(tempList["reviewers"])==0 or newReviewer["google_id"] < tempList["reviewers"][0]["google_id"]:
        index_to_insert = 0
    elif len(tempList["reviewers"])>0 and newReviewer["google_id"] > tempList["reviewers"][len(tempList["reviewers"])-1]["google_id"]:
        index_to_insert = len(tempList["reviewers"])
    else:
        #for i, eachReviewer in enumerate(tempList["reviewers"]):
        #    print(newReviewer["google_id"], eachReviewer["google_id"])
        #    if newReviewer["google_id"] == eachReviewer["google_id"]:
        #        index_to_update = i
        #        break
        #    if newReviewer["google_id"] < eachReviewer["google_id"]:
        #        index_to_insert = i
        #        break
        low, high = 0, len(tempList["reviewers"]) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_value = tempList["reviewers"][mid]["google_id"]

            if newReviewer["google_id"] == tempList["reviewers"][mid]["google_id"]:
                index_to_update = mid
                break
            if newReviewer["google_id"] < tempList["reviewers"][mid]["google_id"]:
                index_to_insert = mid
                break

            if mid_value == newReviewer["google_id"]:
                return mid  # Nilai ditemukan, kembalikan index
            elif mid_value < newReviewer["google_id"]:
                low = mid + 1  # Cari di setengah kanan
            else:
                high = mid - 1  # Cari di setengah kiri

    #print(index_to_insert)
    #print(index_to_update)
    if index_to_update is not None:
        dt_obj1 = datetime.strptime(tempList["reviewers"][index_to_update]['time_review'], "%Y-%m-%d")
        dt_obj2 = datetime.strptime(newReviewer['time_review'], "%Y-%m-%d")
        #print(tempList["reviewers"][index_to_update]['time_review'])
        #print(newReviewer['time_review'])
        if(dt_obj2 > dt_obj1):
            tempList["reviewers"][index_to_update]["reviewer_status"] = newReviewer["reviewer_status"]
            tempList["reviewers"][index_to_update]["num_of_reviews"] = newReviewer["num_of_reviews"]
            tempList["reviewers"][index_to_update]["num_of_photos"] = newReviewer["num_of_photos"]
            tempList["reviewers"][index_to_update]["time_review"] = newReviewer["time_review"]
            #tempList["reviewers"][index_to_update]["review_count"] = tempList["reviewers"][index_to_update]["review_count"]+1
            #print("update")
        else:
            returnReviewer = tempList["reviewers"][index_to_update].copy()
            #tempList["reviewers"][index_to_update]["review_count"] = tempList["reviewers"][index_to_update]["review_count"]+1
    elif index_to_insert != -1:
        #newReviewer["review_count"] = 0
        tempList["reviewers"].insert(index_to_insert, newReviewer)
        #print("insert")
    #print(tempList)
    
    del returnReviewer["google_id"]
    del returnReviewer["google_name"]
    return tempList, returnReviewer
    
# Open the reviewer.json file in write mode
with open("reviewer_private.json", "r") as f:
    listReviewer = json.load(f)

# list key value pair location
listLokasi = {'Embung Nglanggeran':'1','Embung Potorono':'2','Embung Langensari':'3','Embung Tambakboyo':'4','Embung Kaliaji':'5','Hutan Pinus Pengger':'6','Hutan Pinus Mangunan':'7','Hutan Pinus Asri':'8','Seribu Batu Songgo Langit':'9','Puncak Pinus Becici Yogyakarta':'10','Embung Nglanggeran':'11','Puncak Gunung Api Purba - Nglanggeran':'12','Gardu Pandang Merapi':'13','Gunung Ireng':'14','Bukit Bintang':'15','Bukit Paralayang Watugupit':'16','Bunker Kaliadem Merapi':'17','Bukit Klangon':'18','Kalikuning Park':'19','Stonehenge Yogyakarta':'20','Wisata Lava Merapi dan Batu Alien':'21','Ekowisata Kali Talang':'22','Blue Lagoon Jogja':'23','Bukit Wisata Pulepayung':'24','Ekowisata Sungai Mudal':'25','DolanDeso Boro':'26','Kebun Teh Nglinggo':'27','Taman Budaya Kulonprogo':'28','Bukit Panguk Kediwung':'29','Kebun Buah Mangunan':'30','Telaga Jonge':'31','Jomblang Cave':'32','Goa Pindul':'33','Luweng Sampang Waterfalls':'34','Goa Selarong':'35','Plunyon Kalikuning':'36',"Candi Sambisari Temple":"67","Candi Gebang":"68","Candi Kalasan":"69","Candi Ijo":"70","Candi Abang":"71","Candi Sari":"72","Candi Sewu":"73","Candi Pawon":"74","Situs Warungboto":"75","Keraton Ngayogyakarta Hadiningrat":"76","Kampung Wisata Taman Sari":"77","Panggung Krapyak":"78","Pura Pakualaman":"79","Gua Maria Sendangsono":"","Gua Maria Tritis Gunungkidul":"","Gua Maria Lawangsih":"","Goa Maria Ratu Perdamaian Sendang Jatiningsih":"","Klenteng Poncowinatan":"","Makam Raja-raja Imogiri":"","Museum Sonobudoyo Unit I":"","Museum Pendidikan Indonesia":"","Museum Benteng Vredeburg":"","Jogja National Museum":"","Museum Monumen Pangeran Diponegoro Sasana Wiratama":"","Monggo Chocolate Kingdom Factory Museum Store Kedai & Gelato":"","Memorial Jenderal Besar HM Soeharto":"","Museum Sandi":"","Affandi Museum":"","Museum Sasmitaloka Panglima Besar Jenderal Sudirman":"","Ullen Sentalu Museum":"","Museum TNI AD Dharma Wiratama":"","Museum Sri Sultan Hamengkubuwono IX":"","Museum Kars Indonesia":"","Museum Biologi Fakultas Biologi UGM":"","Museum Gunungapi Merapi":"","Museum Pusat TNI AU Dirgantara Mandala":"","Museum Sejarah Purbakala Pleret":"","Museum Geoteknologi Mineral":"","Museum Perjuangan":"","Museum Gembira Loka Zoo":"","Diorama Arsip Jogja":"","Museum Kereta Keraton":"","Museum Mini Sisa Hartaku":"","Taman Pintar Yogyakarta":"110","Taman Pelangi":"111","Kids Fun Park":"112","Merapi Park":"113","Sindu Kusuma Edupark":"114","Galaxy Waterpark":"115","Waterboom Jogja":"116","Grand Puri Water Park":"117","HeHa Sky View":"118","HeHa Ocean View":"119","Obelix Hills":"120","Taman Rekreasi Kaliurang":"121","Gembira Loka Zoo":"122","Ekowisata Sungai Mudal":"123","Agro Wisata Bhumi Merapi":"124","The Lost World Castle":"125","Obelix Village":"126","CitraGrand Mutiara Waterpark":"127","Gamplong Studio Alam":"128","La Li Sa Farmer's Village Jogja":"129","Taman Lampion":"","Mini Zoo Jogja Exotarium (pintu utama)":"","Desa Wisata Kelor":"","Gardu Pandang Kaliurang":"","Suraloka Interactive Zoo":"","Kaliurang Park - Botanical Garden":"","Taman Rekreasi Kaliurang":"","Pasar Legi Kotagede":"","Ibarbo Park":"","Pakuwon Mall Jogja":"","Jogja City Mall":"","Galeria Mall - Yogyakarta":"","Malioboro Mall":"","Plaza Malioboro":"","LIPPO PLAZA side Lobby":"","Sleman City Hall":"","Hamzah Batik - Pusat Oleh-oleh Jogja Batik, Kerajinan dan Camilan":"","Hamzah Batik Kaliurang":"","Pasar Lempuyangan":"","Pasar Beringharjo Yogyakarta":"","Pasar Kranggan":"","Pasar Ngasem":"","Taman Budaya Yogyakarta":"","Titik Nol Yogyakarta":"","Malioboro Yogyakarta":"","Tugu Jogja":"","Alun-Alun Kidul Yogyakarta":"","Monumen Serangan Umum 1 Maret 1949":"","Tugu Pensil":"","Tlogo Putri Kaliurang":"","Pantai Baron":"160","Pantai Baru":"161","Pantai Bidara":"162","Pantai Bugel":"163","Pantai Cangkring":"164","Pantai Cemara Sewu":"165","Pantai Congot":"166","Pantai Depok":"167","Pantai Drini":"168","Pantai Gesing":"169","Pantai Glagah Indah":"170","Pantai Goa Cemara":"171","Pantai Indrayanti":"172","Pantai Jogan":"173","Pantai Jungwok":"174","Pantai Kesirat":"175","Pantai Krakal":"176","Pantai Kukup":"177","Pantai Kuwaru":"178","Pantai Midodaren":"179","Pantai Mlarangan Asri":"180","Pantai Ngandong":"181","Pantai Ngedan":"182","Pantai Ngetun":"183","Pantai Nglambor":"184","Pantai Nglolang":"","Pantai Ngobaran":"","Pantai Ngrenehan":"","Pantai Ngrumput":"","Pantai Nguyahan":"","Pantai Pandansari":"","Pantai Pandansimo":"","Pantai Parang Endog":"","Pantai Parangkusumo":"","Pantai Parangtritis":"","Pantai Pasir Kadilangu":"","Pantai Pelangi":"","Pantai Pengklik":"","Pantai Pok Tunggal":"","Pantai Pulang Sawal":"","Pantai Sadeng":"","Pantai Sadranan":"","Pantai Samas":"","Pantai Sarangan Gunungkidul":"","Pantai Sepanjang":"","Pantai Seruni":"","Pantai Siung":"","Pantai Slili":"","Pantai Timang":"","Pantai Trisik":"","Pantai Watu Kodok":"","Pantai Watu Lumbung":"","Pantai Watulawang":"","Pantai Wediombo":"","Pantai Wohkudu":""}


# Open the CSV file
x = 0
result = [{"reviews":[]} for _ in range(37)]
with open("raw/[FINAL] Alam - Final.csv", "r") as f:
    reader = csv.DictReader(f, delimiter=",")
    # Lewati baris-baris hingga mencapai baris ke-n
    for _ in range(60000):
        next(reader)

    # Group reviews by location
    reviews_by_location = defaultdict(list)
    for row in reader:
        info_reviewer = extract_info(row["informasi_reviewer"])
        row["status"] = info_reviewer[0].strip()
        row["num_of_reviews"] = info_reviewer[1].replace('.', '').strip()
        row["num_of_photos"] = info_reviewer[2].replace('.', '').strip()

        reviewer = (
            row["id_reviewer"],
            row["nama_reviewer"],
            row["status"],
            row["num_of_reviews"],
            row["num_of_photos"],
            row["waktu_ulasan"]
        )

        # proses reviewer
        newReviewer = {}
        newReviewer["google_id"] = reviewer[0]
        newReviewer["google_name"] = reviewer[1].strip()
        newReviewer["reviewer_id"] = generate_reviewer_id(listReviewer)
        newReviewer["reviewer_name"] = encrypt(reviewer[1].strip())
        newReviewer["reviewer_status"] = reviewer[2]
        newReviewer["num_of_reviews"] = reviewer[3]
        newReviewer["num_of_photos"] = reviewer[4]
        newReviewer["time_review"] = reviewer[5]
        listReviewer, newReviewer = update_or_insert_reviewer(listReviewer, newReviewer)
        
        #new reviews
        newReview = {}
        newReview["reviewer"] = newReviewer
        newReview["time_review"] = row["waktu_ulasan"]
        newReview["rating_value"] = row["rating_ulasan"]
        newReview["review_text"] = row["isi_ulasan"]
        newReview["review_info"] = row["informasi_ulasan"]

        print(row["nama_lokasi"], int(listLokasi[row["nama_lokasi"]]))
        result[int(listLokasi[row["nama_lokasi"]])]["reviews"].append(newReview)
        result[int(listLokasi[row["nama_lokasi"]])]["rating_value"] = row["rating_lokasi"]
        result[int(listLokasi[row["nama_lokasi"]])]["num_of_review"] = row["jumlah_ulasan"]

        x += 1
        if x== 80000 :
            break

with open("reviewer_private.json", 'w') as file:
    json.dump(listReviewer, file, indent=2)

# write to masing-masing file
# buka file index.json
# cek review nya sudah ada belum, kalau sudah ada skip. based on review_text
# kalau bvelum ada append urut waktu ulasan
key = 1
for eachResult in result:
    if len(eachResult["reviews"]) > 0:
        print("results/"+str(key-1)+".json")
        with open("results/"+str(key-1)+".json", 'r') as f:
            tempRewriteData = json.load(f)
            #print(tempRewriteData)
            #print(eachResult["rating_value"],eachResult["num_of_review"])
            eachResult["num_of_review"]=eachResult["num_of_review"].replace('.', '')
            if tempRewriteData["rating_value"] != eachResult["rating_value"]: 
                tempRewriteData["rating_value"] = eachResult["rating_value"]
            if tempRewriteData["num_of_review"] < eachResult["num_of_review"]: 
                tempRewriteData["num_of_review"] = eachResult["num_of_review"]
            for eachNewReview in eachResult["reviews"]:
                #print(eachNewReview["review_text"],tempRewriteData["reviews"]["review_text"].values())
                #print(eachNewReview["review_text"],[review["review_text"] for review in tempRewriteData.get("reviews", [])], )
                if not (eachNewReview["review_text"] in [review["review_text"] for review in tempRewriteData.get("reviews", [])]):
                    tempRewriteData["reviews"].append(eachNewReview)
        with open("results/"+str(key-1)+".json", 'w') as file:
            json.dump(tempRewriteData, file, indent=2)
    key+=1
