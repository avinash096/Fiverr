import pymongo
import json
from bson.objectid import ObjectId

try:
	connection = pymongo.MongoClient()
	db = connection["fiverr_data"]
	gigs = db["all_gigs"]
	gigs_multiple = db["gigs_multiple"]
	print("Connection with Mongo DB Succeeded.")
except:
	print("Connection with Mongo DB Failed.")
def multiple():
	total = gigs.count()
	print("Total number of gigs is " + str(total))
	multipleReviewDataList = list()
	gig_count = 0
	gig_iterate = gigs.find()
	for i in gig_iterate:
		s=""
		gig_count = gig_count + 1
		gig_file_name = "Multiple_Reviews/"+str(gig_count)+".txt"
		gig_name = i["Gig_name"]
		s+=("{\n\t\"Gig_name\""+ ": \""+ gig_name + "\",").encode('utf-8')
		s+=("\n\t").encode('utf-8')
		review_array = i["Reviews"]
		buyer_set = set()
		s+=("\"Multiple Review Data\":["). encode('utf-8')
		for reviews in review_array:
			buyer = reviews['User']
			buyer_set.add(buyer)
		for buyer in buyer_set:
			count = 0
			messages = list()
			for reviews in review_array:
				if(buyer == reviews["User"]):
					count = count + 1
					messages.append(reviews["Message"])
			s+=("\n\t\t\t{\n\t\t\t\t\"User_name\":\""+(buyer).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
			s+=("\n\t\t\t\t").encode('utf-8')
			s+=("\"Review_Count\":\""+str(count).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
			s+=("\n\t\t\t\t").encode('utf-8')
			s+=("\"Messages\":["). encode('utf-8')
			for message in messages:
				s+=("\n\t\t\t{\n\t\t\t\t\"Message\":\""+(message).strip("\r\n\t").replace("\"","\\\"")+"\"},").encode('utf-8')
				s+=("\n\t\t\t\t").encode('utf-8')
			s = s[:-6]
			s+=("\n\t]").encode('utf-8')
			s+=("\n},").encode('utf-8')
		s = s[:-1]
		s+=("\n\t]").encode('utf-8')
		s+=("\n}").encode('utf-8')
		s = s.strip(" ")
		s = s.replace("\r","")
		s = s.replace("\n","")
		gig_file = open(gig_file_name,'w')
		gig_file.write(s)
		gig_file.close()
		try:
			gigs_multiple.insert_one(json.loads(s))
			
			print("Storing the above gig Successfull!!")
		except:
			print("Storing the above gig failed!!")
			pass
		print("Stored in the MongoDB. proceeding on the another gig if it exists!!")

multiple()
class multipleReviewData:
	def _init_(gig_name, user_name, count, messages):
		self.gig_name = gig_name
		self.user_name = user_name
		self.count = count
		self.messages = messages
