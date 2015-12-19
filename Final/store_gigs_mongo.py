import pymongo
import os
import json

connection = pymongo.MongoClient()
db = connection["fiverr_data"]
gigs = db["gigs_senti_sans_pos"]
gig_not_stored  = open('gigs_not_mongodb_senti.txt','a')
total_gigs = 0


def toMongoDB(filename):
	global total_gigs
	if os.path.exists(filename):
		gig_file_string = open(filename,'r').read().decode('utf-8')
	else:
		return
	s = gig_file_string.replace("\\\\","\\")
	s = s.replace("\"\"Others\"","\"Others\"")
	s = s.replace("[\][\][^\"]","\\\\")
	s = s.replace("\t","")
	s = s.replace("\n","")
	s = s.replace("[\][\][^\\\"]","")
	s = s.replace("\\,",",")
	try:
		json_data = json.loads(s)
		gig_exist = gigs.find({"Gig_name":json_data["Gig_name"]}).count()
		if(gig_exist > 0):
			return
		gigs.insert_one(json_data)
		total_gigs = total_gigs + 1
		# gig_file_string = open('./Others/' + str(i) + '.txt','w')
		# gig_file_string.write(s.encode('utf-8'))
		gig_file_string.close()
	except:
		gig_not_stored.write((filename + "\n").encode('utf-8'))
	print("Loading " + filename + " Successful \t Total: " + str(total_gigs))


def recursive_walk(folder):
    for folderName, subfolders, filenames in os.walk(folder):
        if subfolders:
            for subfolder in subfolders:
                recursive_walk(subfolder)
        print('\nFolder: ' + folderName + '\n')
        for filename in filenames:
            toMongoDB(folderName + '/' + filename)

recursive_walk("./Senti_Review")