import pymongo

client = pymongo.MongoClient("mongodb+srv://flight-time-logger-app:csci6710team5@anthony-test-tfdgg.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = client["flight-time-logger"]

#print(client.list_database_names())

col = db["info"]

#print(db.list_collection_names())

#x = col.insert_one(mydoc)

#print(x.inserted_id)

docs = col.find()

flights = list(docs)

print(flights[0]["id"])
#for each doc, create a row
# for each in docs


# # for that doc, print each field
# print(doc["id"])
# print(doc["departure_date"])
# print(doc["departure_location"])
# print(doc["arrival_date"])
# print(doc["arrival_location"])
# print(doc["flight_time"])
# print(doc["cargo_weight_lbs"])
# print(doc["aircraft_type"])
# print(doc["aircraft_tail_num"])
# for key, value in doc.items():
#     print(key, "=>", value)
# for value in data_for_view.values():
#     print(value)
        