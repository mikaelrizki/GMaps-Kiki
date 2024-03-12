import json
from collections import defaultdict
from pathlib import Path

with open("raw/temp.json", "r") as f:
    listLocation = json.load(f)
    for location in listLocation:
        print(location)
        with open("results/"+location["id"]+".json", 'w') as file:
            # Menulis data ke file JSON
            location["num_of_review"]=location["num_of_review"].replace('.', '')
            json.dump(location, file, indent=2)
