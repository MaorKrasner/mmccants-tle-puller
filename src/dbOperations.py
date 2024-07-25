from pymongo import MongoClient
from config import config

def getNorads() -> list:
    try:
        client = MongoClient(config["mongo_db_uri"])

        db = client.get_database('mmccants')
        collection = db.satelliteIds

        norad_ids_cursor = collection.find({}, {"_id": 0, "NORAD ID": 1})

        norad_id_list = [document["NORAD ID"] for document in norad_ids_cursor]

        for norad_id in norad_id_list:
            print(norad_id)

        print(norad_id_list)

        return norad_id_list

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()