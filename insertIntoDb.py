import mysql.connector
import csv
from collections import defaultdict
from datetime import datetime
from datetime import date

mydb = mysql.connector.connect(
    host="localhost",
    db="wisata_jogja",
    user="user_wisata",
    password="DGNDH/i33-kJpStS"
)

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







x=0
with open("raw/[FINAL] Taman Hiburan, Shopping, Lainnya - Final.csv", "r") as f:
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

        # make cursor for establish connection
        mycursor = mydb.cursor()

        # proses reviewer
        newReviewer = {}
        newReviewer["google_id"] = reviewer[0]
        newReviewer["google_name"] = reviewer[1].strip()
        newReviewer["reviewer_name"] = encrypt(reviewer[1].strip())
        newReviewer["reviewer_status"] = reviewer[2]
        newReviewer["num_of_reviews"] = reviewer[3].replace('.', '') if reviewer[3].replace('.', '') != '' else 0
        newReviewer["num_of_photos"] = reviewer[4].replace('.', '') if reviewer[4].replace('.', '') != '' else 0
        newReviewer["time_review"] = reviewer[5]

        theReviewerId = None

        # selecting query
        query = "SELECT * FROM reviewers WHERE google_id='"+newReviewer["google_id"]+"'"
        # id, google_id, google_name, reviewer_name, reviewer_status, num_of_reviews, num_of_photos, time_review
        mycursor.execute(query)
        oldReviewer = mycursor.fetchone()
        #if oldReviewer time_review < newReviewer time_review lebih baru then update into DB
        #if oldReviewer = null then insert into DB
        if oldReviewer == None:
            query = "INSERT INTO reviewers (google_id, google_name, reviewer_name, reviewer_status, num_of_reviews, num_of_photos, time_review) VALUES ('"+newReviewer["google_id"]+"',%s,'"+newReviewer["reviewer_name"]+"','"+newReviewer["reviewer_status"]+"','"+str(newReviewer["num_of_reviews"])+"','"+str(newReviewer["num_of_photos"])+"','"+newReviewer["time_review"]+"')"
            values = (newReviewer["google_name"],)
            mycursor.execute(query, values)
            theReviewerId = mycursor.lastrowid
        else: #if time_review lebih baru yang newReviwer
            dt_obj1 = datetime.combine(oldReviewer[7], datetime.min.time())
            dt_obj2 = datetime.strptime(newReviewer['time_review'], "%Y-%m-%d")
            
            if(dt_obj2 > dt_obj1):
                mycursor.execute("UPDATE reviewers SET reviewer_status='"+newReviewer["reviewer_status"]+"', num_of_reviews='"+str(newReviewer["num_of_reviews"])+"', num_of_photos='"+str(newReviewer["num_of_photos"])+"', time_review='"+newReviewer["time_review"]+"' WHERE id='"+str(oldReviewer[0])+"'")
            theReviewerId = oldReviewer[0]
        
        #new reviews
        # selecting query
        query = "SELECT * FROM reviews WHERE location_id=(SELECT id FROM locations WHERE name=%s) AND reviewer_id='"+str(theReviewerId)+"'"
        values = (row['nama_lokasi'],)
        mycursor.execute(query,values)
        oldReview = mycursor.fetchone()
        if oldReview == None:
            newReview = {}
            newReview["time_review"] = row["waktu_ulasan"]
            newReview["rating_value"] = row["rating_ulasan"]
            newReview["review_text"] = row["isi_ulasan"]
            newReview["review_info"] = row["informasi_ulasan"]
            query = "INSERT INTO reviews (location_id, reviewer_id, time_review, rating_value, review_text, review_info) VALUES ((SELECT id FROM locations WHERE name=%s),'"+str(theReviewerId)+"','"+newReview["time_review"]+"','"+newReview["rating_value"]+"',%s,%s)"
            values = (row['nama_lokasi'], newReview["review_text"],newReview["review_info"])
            print(query)
            print(values)
            mycursor.execute(query, values)

        # update location
        query = "SELECT * FROM locations WHERE name=%s"
        values = (row['nama_lokasi'],)
        # id, google_id, google_name, reviewer_name, reviewer_status, num_of_reviews, num_of_photos, time_review
        mycursor.execute(query, values)
        oldLocation = mycursor.fetchone()
        if oldLocation != None:
            row['jumlah_ulasan'] = row['jumlah_ulasan'].replace('.', '')
                    
            if oldLocation[5] == None:
                query = "UPDATE locations SET rating_value='"+row["rating_lokasi"]+"', num_of_review='"+row["jumlah_ulasan"]+"', time_review='"+row['waktu_ulasan']+"' WHERE name=%s"
                values = (row['nama_lokasi'],)
                mycursor.execute(query, values)
            else:  
                dt_obj1 = datetime.combine(oldLocation[5], datetime.min.time())
                dt_obj2 = datetime.strptime(row['waktu_ulasan'], "%Y-%m-%d")
                
                if(dt_obj2 > dt_obj1):
                    query = "UPDATE locations SET rating_value='"+row["rating_lokasi"]+"', num_of_review='"+row["jumlah_ulasan"]+"', time_review='"+row['waktu_ulasan']+"' WHERE name=%s"
                    values = (row['nama_lokasi'],)
                    mycursor.execute(query, values)

        mycursor.execute("Commit")

        #x += 1
        #if x== 10000 :
        #    break

# close connection
mydb.close()