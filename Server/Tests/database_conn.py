#This is just a test file to check the database connection for MongoDB
#Can be referred in future for working with the database
import pymongo
import json
from bson.objectid import ObjectId


connection = pymongo.MongoClient()

db = connection["tutorial"]
employees = db["employees"]

employees.insert(json.loads("{\"name\": \"Lucas Hightower\", \"gender\":\"m\", \"phone\":\"520-555-1212\", \"age\":8}"))

cursor = db.employees.find()
for employee in db.employees.find():
    print employee


print employees.find({"name":"Lucas Hightower"})[0]


cursor = employees.find({"age": {"$lt": 35}})
for employee in cursor:
     print "under 35: %s" % employee


diana = employees.find_one({"_id":ObjectId("55eb5643f31ef94041b7f087")})
print "Diana %s" % diana
