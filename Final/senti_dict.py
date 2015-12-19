from nltk.corpus import sentiwordnet as swn
from nltk import tokenize
import nltk
import re
import pymongo
import json
from bson.objectid import ObjectId

try:
	connection = pymongo.MongoClient()
	db = connection["fiverr_data"]
	gigs = db["all_gigs"]
	gigs_multiple = db["gigs_senti_dict"]
	print("Connection with Mongo DB Succeeded.")
except:
	print("Connection with Mongo DB Failed.")
dick = {}

def review_score(review):
	review = re.sub('([.,!?()])', r' \1 ', review)
	sents = tokenize.sent_tokenize(review)
	score = [0.0, 0.0, 0.0]
	no_of_sents = 0
	for sentences in sents:
		if len(sentences.strip()) <= 0:
			continue
		temp_score = sentence_score(sentences.strip())
		if(temp_score[0] == 0 and temp_score[1] == 0 and temp_score[2] == 0):
			continue
		score[:] = [sum(i) for i in zip(score,temp_score)]
		no_of_sents = no_of_sents + 1
	if(no_of_sents > 0):
		score[:] = [x/no_of_sents for x in score]
	return score

def sentence_score(sentence):
	text = nltk.word_tokenize(sentence)
	score = [0.0, 0.0, 0.0]
	no_of_words = 0
	for words in nltk.pos_tag(text):
		temp_pos = words[1]
		if temp_pos in ["JJ","JJR","JJS"]:
			pos = "a"
		elif temp_pos in ["NN","NNS","NNP","NNPS"]:
			pos = "n"
		elif temp_pos in ["RB","RBR","RBS"]:
			pos = "r"
		elif temp_pos in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
			pos = "v"
		elif temp_pos in [".",",",";",":"]:
			continue
		else:
			pos = "k"
		temp_score = word_score(words[0],pos)
		if(temp_score[0] == 0 and temp_score[1] == 0 and temp_score[2] == 0):
			continue
		score[:] = [sum(i) for i in zip(score,temp_score)]
		no_of_words = no_of_words + 1
	if(no_of_words > 0):
		score[:] = [x/no_of_words for x in score]
	#print (sentence , ":", score)
	return score

def word_score(word,tag):
	if(dick.has_key(word)):
		score = dick[word]
	else:
		if tag == "k":
			all_words = swn.senti_synsets(word)
		else:
			all_words = swn.senti_synsets(word,tag)
		score = [0.0, 0.0, 0.0]
		for words in all_words:
			score[0] = score[0] + words.pos_score()
			score[1] = score[1] + words.neg_score()
			score[2] = score[2] + words.obj_score()
		if(len(all_words) > 0):
			score[0] = score[0] / len(all_words)
			score[1] = score[1] / len(all_words)
			score[2] = score[2] / len(all_words)
		dick[word] = score
	#print (word, " : ", score)
	return score

def multiple():
	countt = 0
	total = gigs.count()
	print("Total number of gigs is " + str(total))
	multipleReviewDataList = list()
	gig_count = 0
	gig_iterate = gigs.find(no_cursor_timeout=True)
	for i in gig_iterate:
		try:
			s=""
			gig_count = gig_count + 1
			if(gig_count <= 40):
				continue
			gig_file_name = "Senti_Review/"+str(gig_count)+".txt"
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
				messagesDate = list()
				for reviews in review_array:
					if(buyer == reviews["User"]):
						count = count + 1
						messagesDate.append((reviews["Message"],reviews["Rating-Date"]))
				s+=("\n\t\t\t{\n\t\t\t\t\"User_name\":\""+(buyer).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
				s+=("\n\t\t\t\t").encode('utf-8')
				s+=("\"Review_Count\":\""+str(count).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
				s+=("\n\t\t\t\t").encode('utf-8')
				s+=("\"Messages\":["). encode('utf-8')
				for message in messagesDate:
					score = review_score(message[0].lower())
					s+=("\n\t\t\t{\n\t\t\t\t\"Message\":\""+(message[0]).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
					s+=("\n\t\t\t\t").encode('utf-8')
					s+=("\"Review-Date\":\""+(message[1]).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
					s+=("\n\t\t\t\t").encode('utf-8')
					s+=("\"Positive_Score\":"+ str(score[0]) + ",").encode('utf-8')
					s+=("\n\t\t\t\t").encode('utf-8')
					s+=("\"Negative_Score\":"+ str(score[1]) + ",").encode('utf-8')
					s+=("\n\t\t\t\t").encode('utf-8')
					s+=("\"Objective_Score\":"+ str(score[2]) + "\n\t\t\t\t},").encode('utf-8')
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
			dick_butt = open("dick.txt",'w')
			for yyy in dick:
				aaaa = [round(float(i), 4) for i in dick[yyy]]
				dick_butt.write((yyy + ":\t\t" + str(aaaa) + "\n").encode('utf-8'))
			dick_butt.close()
		except:
			continue

#print review_score(raw_input("Enter Paragraph:\n").lower())
multiple()
gigs.close()