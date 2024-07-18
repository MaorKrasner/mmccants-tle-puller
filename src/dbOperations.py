from pymongo import MongoClient

from config import config

def getNorads():
    client = MongoClient(config["mongo_db_uri"])

    # Access the specific database and collection
    db = client.mmccants
    collection = db.satelliteIds

    # Retrieve all documents and extract NORAD IDs
    norad_ids_cursor = collection.find({}, {"_id": 0, "NORAD ID": 1})

    # Collect all NORAD IDs in a list
    norad_id_list = [document["NORAD ID"] for document in norad_ids_cursor]

    # Print the NORAD IDs
    for norad_id in norad_id_list:
        print(norad_id)

    # Optionally, print the whole list
    print(norad_id_list)