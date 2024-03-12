import json
from collections import defaultdict
from pathlib import Path

listLokasi = {'Embung Nglanggeran':'1','Embung Potorono':'2','Embung Langensari':'3','Embung Tambakboyo':'4','Embung Kaliaji':'5','Hutan Pinus Pengger':'6','Hutan Pinus Mangunan':'7','Hutan Pinus Asri':'8','Seribu Batu Songgo Langit':'9','Puncak Pinus Becici Yogyakarta':'10','Embung Nglanggeran':'11','Puncak Gunung Api Purba - Nglanggeran':'12','Gardu Pandang Merapi':'13','Gunung Ireng':'14','Bukit Bintang':'15','Bukit Paralayang Watugupit':'16','Bunker Kaliadem Merapi':'17','Bukit Klangon':'18','Kalikuning Park':'19','Stonehenge Yogyakarta':'20','Wisata Lava Merapi dan Batu Alien':'21','Ekowisata Kali Talang':'22','Blue Lagoon Jogja':'23','Bukit Wisata Pulepayung':'24','Ekowisata Sungai Mudal':'25','DolanDeso Boro':'26','Kebun Teh Nglinggo':'27','Taman Budaya Kulonprogo':'28','Bukit Panguk Kediwung':'29','Kebun Buah Mangunan':'30','Telaga Jonge':'31','Jomblang Cave':'32','Goa Pindul':'33','Luweng Sampang Waterfalls':'34','Goa Selarong':'35','Plunyon Kalikuning':'36'}

for key in range (1,37):
    with open("results/"+str(key)+".json", 'r') as f:
        tempData = json.load(f)
        for eachRev in tempData["reviews"]
