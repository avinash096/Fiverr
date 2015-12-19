import pymongo
from bson.objectid import ObjectId


try:
	connection1 = pymongo.MongoClient(host='localhost', port=27017)
	db1 = connection1["fiverr_data"]
	gigs1 = db1["gigs_multiple"]
	print("Connection with Mongo DB Succeeded.")
except:
	print("Connection with Mongo DB Failed.")

def ploted():
	total_gigs = gigs1.find()
	total_gig_count = total_gigs.count()
	sum = 0
	for i in total_gigs:
		size = len(i["Multiple Review Data"])
		sum = sum + size
	average_people = sum *1.0 / total_gig_count
	sum = 0
	total_gigs = gigs1.find()
	for k in total_gigs:
		data = k["Multiple Review Data"]
		count = 0
		for j in data:
			count = count + int(j["Review_Count"])
		sum = sum + count
	average_reviews = sum*1.0 / total_gig_count
	print(str(average_people)+"\n")
	print(str(average_reviews)+"\n")
	print(average_reviews/average_people)
	sum = 0
	total_gigs = gigs1.find()
	for l in total_gigs:
		data = l["Multiple Review Data"]
		count = 0
		count_tot = 0
		for m in data:   # l is a gig
			if(int(m["Review_Count"]) > 1):
				message = m["Messages"]
				message_set = set()
				for messages in message:
					message_set.add(messages["Message"])
				if(len(message_set) > 1):
					count = count + 1   # count denotes the number of users who are giving different reviews
		sum = sum + count*1.0/len(i["Multiple Review Data"])
		#print(count)
	average_people_multiple_reviewing = sum * 1.0 / total_gig_count
	print("\n")
	print(str(average_people_multiple_reviewing)+"\n")
ploted()