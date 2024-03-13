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
listLokasi = {"Embung Nglanggeran":"1","Embung Potorono":"2","Embung Langensari":"3","Embung Tambakboyo":"4","Embung Kaliaji":"5","Hutan Pinus Pengger":"6","Hutan Pinus Mangunan":"7","Hutan Pinus Asri":"8","Seribu Batu Songgo Langit":"9","Puncak Pinus Becici Yogyakarta":"10","Puncak Gunung Api Purba - Nglanggeran":"11","Gardu Pandang Merapi":"12","Gunung Ireng":"13","Bukit Bintang":"14","Bukit Paralayang Watugupit":"15","Bunker Kaliadem Merapi":"16","Bukit Klangon":"17","Kalikuning Park":"18","Stonehenge Yogyakarta":"19","Wisata Lava Merapi dan Batu Alien":"20","Ekowisata Kali Talang":"21","Blue Lagoon Jogja":"22","Bukit Wisata Pulepayung":"23","Ekowisata Sungai Mudal":"24","DolanDeso Boro":"25","Kebun Teh Nglinggo":"26","Taman Budaya Kulonprogo":"27","Bukit Panguk Kediwung":"28","Kebun Buah Mangunan":"29","Telaga Jonge":"30","Jomblang Cave":"31","Goa Pindul":"32","Luweng Sampang Waterfalls":"33","Goa Selarong":"34","Plunyon Kalikuning":"35","Candi Sambisari Temple":"36","Candi Gebang":"37","Candi Kalasan":"38","Candi Ijo":"39","Candi Abang":"40","Candi Sari":"41","Candi Sewu":"42","Candi Pawon":"43","Situs Warungboto":"44","Keraton Ngayogyakarta Hadiningrat":"45","Kampung Wisata Taman Sari":"46","Panggung Krapyak":"47","Pura Pakualaman":"48","Gua Maria Sendangsono":"49","Gua Maria Tritis Gunungkidul":"50","Gua Maria Lawangsih":"51","Goa Maria Ratu Perdamaian Sendang Jatiningsih":"52","Klenteng Poncowinatan":"53","Makam Raja-raja Imogiri":"54","Museum Sonobudoyo Unit I":"55","Museum Pendidikan Indonesia":"56","Museum Benteng Vredeburg":"57","Jogja National Museum":"58","Museum Monumen Pangeran Diponegoro Sasana Wiratama":"59","Monggo Chocolate Kingdom Factory Museum Store Kedai & Gelato":"60","Memorial Jenderal Besar HM Soeharto":"61","Museum Sandi":"62","Affandi Museum":"63","Museum Sasmitaloka Panglima Besar Jenderal Sudirman":"64","Ullen Sentalu Museum":"65","Museum TNI AD Dharma Wiratama":"66","Museum Sri Sultan Hamengkubuwono IX":"67","Museum Kars Indonesia":"68","Museum Biologi Fakultas Biologi UGM":"69","Museum Gunungapi Merapi":"70","Museum Pusat TNI AU Dirgantara Mandala":"71","Museum Sejarah Purbakala Pleret":"72","Museum Geoteknologi Mineral":"73","Museum Perjuangan":"74","Museum Gembira Loka Zoo":"75","Diorama Arsip Jogja":"76","Museum Kereta Keraton":"77","Museum Mini Sisa Hartaku":"78","Taman Pintar Yogyakarta":"79","Taman Pelangi":"80","Kids Fun Park":"81","Merapi Park":"82","Sindu Kusuma Edupark":"83","Galaxy Waterpark":"84","Waterboom Jogja":"85","Grand Puri Water Park":"86","HeHa Sky View":"87","HeHa Ocean View":"88","Obelix Hills":"89","Taman Rekreasi Kaliurang":"90","Gembira Loka Zoo":"91","Ekowisata Sungai Mudal":"92","Agro Wisata Bhumi Merapi":"93","The Lost World Castle":"94","Obelix Village":"95","CitraGrand Mutiara Waterpark":"96","Gamplong Studio Alam":"97","La Li Sa Farmer's Village Jogja":"98","Taman Lampion":"99","Mini Zoo Jogja Exotarium (pintu utama)":"100","Desa Wisata Kelor":"101","Gardu Pandang Kaliurang":"102","Suraloka Interactive Zoo":"103","Kaliurang Park - Botanical Garden":"104","Taman Rekreasi Kaliurang":"105","Pasar Legi Kotagede":"106","Ibarbo Park":"107","Pakuwon Mall Jogja":"108","Jogja City Mall":"109","Galeria Mall - Yogyakarta":"110","Malioboro Mall":"111","Plaza Malioboro":"112","LIPPO PLAZA side Lobby":"113","Sleman City Hall":"114","Hamzah Batik - Pusat Oleh-oleh Jogja Batik, Kerajinan dan Camilan":"115","Hamzah Batik Kaliurang":"116","Pasar Lempuyangan":"117","Pasar Beringharjo Yogyakarta":"118","Pasar Kranggan":"119","Pasar Ngasem":"120","Taman Budaya Yogyakarta":"121","Titik Nol Yogyakarta":"122","Malioboro Yogyakarta":"123","Tugu Jogja":"124","Alun-Alun Kidul Yogyakarta":"125","Monumen Serangan Umum 1 Maret 1949":"126","Tugu Pensil":"127","Tlogo Putri Kaliurang":"128","Pantai Baron":"129","Pantai Baru":"130","Pantai Bidara":"131","Pantai Bugel":"132","Pantai Cangkring":"133","Pantai Cemara Sewu":"134","Pantai Congot":"135","Pantai Depok":"136","Pantai Drini":"137","Pantai Gesing":"138","Pantai Glagah Indah":"139","Pantai Goa Cemara":"140","Pantai Indrayanti":"141","Pantai Jogan":"142","Pantai Jungwok":"143","Pantai Kesirat":"144","Pantai Krakal":"145","Pantai Kukup":"146","Pantai Kuwaru":"147","Pantai Midodaren":"148","Pantai Mlarangan Asri":"149","Pantai Ngandong":"150","Pantai Ngedan":"151","Pantai Ngetun":"152","Pantai Nglambor":"153","Pantai Nglolang":"154","Pantai Ngobaran":"155","Pantai Ngrenehan":"156","Pantai Ngrumput":"157","Pantai Nguyahan":"158","Pantai Pandansari":"159","Pantai Pandansimo":"160","Pantai Parang Endog":"161","Pantai Parangkusumo":"162","Pantai Parangtritis":"163","Pantai Pasir Kadilangu":"164","Pantai Pelangi":"165","Pantai Pengklik":"166","Pantai Pok Tunggal":"167","Pantai Pulang Sawal":"168","Pantai Sadeng":"169","Pantai Sadranan":"170","Pantai Samas":"171","Pantai Sarangan Gunungkidul":"172","Pantai Sepanjang":"173","Pantai Seruni":"174","Pantai Siung":"175","Pantai Slili":"176","Pantai Timang":"177","Pantai Trisik":"178","Pantai Watu Kodok":"179","Pantai Watu Lumbung":"180","Pantai Watulawang":"181","Pantai Wediombo":"182","Pantai Wohkudu":"183",}


# Open the CSV file
x = 0
result = [{"reviews":[]} for _ in range(184)]
with open("raw/[FINAL] Alam - Final.csv", "r") as f:
    reader = csv.DictReader(f, delimiter=",")
    # Lewati baris-baris hingga mencapai baris ke-n
    #for _ in range(60000):
    #    next(reader)

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

        #print(row["nama_lokasi"], int(listLokasi[row["nama_lokasi"]]))
        result[int(listLokasi[row["nama_lokasi"]])]["reviews"].append(newReview)
        result[int(listLokasi[row["nama_lokasi"]])]["rating_value"] = row["rating_lokasi"]
        result[int(listLokasi[row["nama_lokasi"]])]["num_of_review"] = row["jumlah_ulasan"]

        x += 1
        if x== 15000 :
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
