from pymongo import MongoClient
import os

# from crud import Operations

class DatabaseConnection():
    def main(self):
        client = MongoClient(os.getenv('MONGO_URI'))
        print(client)
        db = client.omnius
        return db

    def RawModel(self):
        db = DatabaseConnection().main()
        cursor = db.raw.find()
        # print(cursor)
        for document in cursor:
            print(document)