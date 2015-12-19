import plotly.plotly as py
from plotly.graph_objs import *
import pymongo
from bson.objectid import ObjectId

py.sign_in('djr-jsr','6kj9df5zg6')

try:
	connection1 = pymongo.MongoClient(host='localhost', port=27017)
	# connection2 = pymongo.MongoClient(host='10.105.76.187', port=27017)
	# connection3 = pymongo.MongoClient(host='10.105.76.181', port=27017)
	#connection4 = pymongo.MongoClient(host='localhost', port=27017)
	#connection5 = pymongo.MongoClient(host='localhost', port=27017)
	# connection6 = pymongo.MongoClient(host='10.132.83.78', port=27017)
	db1 = connection1["fiverr_data"]
	# db2 = connection2["fiverr_data"]
	# db3 = connection3["fiverr_data"]
	#db4 = connection4["fiverr_data"]
	#db5 = connection5["fiverr_data"]
	# db6 = connection6["fiverr_data"]
	gigs1 = db1["gigs-negative"]
	# gigs2 = db2["gigs-negative"]
	# gigs3 = db3["gigs-negative"]
	#gigs4 = db4["gigs"]
	#gigs5 = db5["gigs"]
	# gigs6 = db6["gigs-negative"]
	print("Connection with Mongo DB Succeeded.")
except:
	print("Connection with Mongo DB Failed.")


def ploted():
	results = 0
	total = gigs1.find().count()
	# total += gigs2.find().count()
	# total += gigs3.find().count()
	#total += gigs4.find().count()
	#total += gigs5.find().count()
	# total += gigs6.find().count()
	print("Total number of gigs is " + str(total))
	a = [0.0] * 2000
	b = [0] * 2000
	for i in range(0, 9):
		results = db1["gigs-negative"].find({"Negative Reviews":{"$size": i}}).count()
		# s =  str(i) + " Reviews"
		# results = gigs1.find({"Number of Reviews":s}).count()
		# results += gigs2.find({"Number of Reviews":s}).count()
		# results += gigs3.find({"Number of Reviews":s}).count()
		#results += gigs4.find({"Number of Reviews":s}).count()
		#results += gigs5.find({"Number of Reviews":s}).count()
		# results += gigs6.find({"Number of Reviews":s}).count()
		#count = results.count()
		a[i] = results/float(total)
		b[i] = i
	trace2 = Scatter(x=b,y=a)
	# i = 0
	# a = [0.0]*50
	# b = [0.0]*50
	# while(i<=5):
	# 	s = str(i)
	# 	results = gigs1.find({"Rating":s}).count()
	# 	results += gigs2.find({"Rating":s}).count()
	# 	results += gigs3.find({"Rating":s}).count()
	# 	#results += gigs4.find({"Rating":s}).count()
	# 	#results += gigs5.find({"Rating":s}).count()
	# 	results += gigs6.find({"Rating":s}).count()
	# 	#count = results.count()
	# 	a[int(i*10)] = results/float(total)
	# 	b[int(i*10)] = i
	# 	i = i + 0.1
	# trace3 = Scatter(x = b, y=a)
	# c = [0.0] * 51
	# d = [0] * 51

	data = Data([trace2])
	# data1 = Data([trace3])
	layout = Layout(xaxis=XAxis(type='log',autorange=True),yaxis=YAxis(type='log',autorange=True))
	fig = Figure(data=data, layout=layout)
	# fig1 = Figure(data=data1, layout=layout)
	plot_url = py.plot(fig, filename='Fraction of Gigs vs Reviews')
	# plot_url1 = py.plot(data1, filename='Fraction of Gigs vs Rating')
	print plot_url
	# print plot_url1


	# i = 0
	# num_catgories = 11
	# aa = [0]*10
	# bb = [0.0]*10
	# cc = [0]*10
	# dd = [" "]*10
	# category_name = ["Graphics & Design","Online Marketing","Writing & Translation","Video & Animation","Music & Audio","Programming & Tech","Advertising","Business","Lifestyle","Gifts","Fun & Bizarre","Others"]
	# for name in category_name[1:]:
	# 	data_cat1 = gigs1.find({"Category":name})
	# 	data_cat2 = gigs2.find({"Category":name})
	# 	data_cat3 = gigs3.find({"Category":name})
	# 	data_cat6 = gigs6.find({"Category":name})
	# 	print("category_name: " + name)
	# 	size = data_cat1.count()+data_cat2.count()+data_cat3.count()+data_cat6.count()
	# 	sum_rat = 0.0
	# 	sum_rev = 0
	# 	sum_fav = 0
	# 	count = 0
	# 	for a in data_cat1:
	# 		sum_rat = sum_rat + float(a["Rating"])
	# 		temp_str = str(a["Number of Reviews"])
	# 		temp_int = int(temp_str.replace(" Reviews",""))
	# 		sum_rev = sum_rev + temp_int
	# 		sum_fav = sum_fav + int(a["Fourite Count"])
	# 		count = count + 1
	# 	for a in data_cat2:
	# 		sum_rat = sum_rat + float(a["Rating"])
	# 		temp_str = str(a["Number of Reviews"])
	# 		temp_int = int(temp_str.replace(" Reviews",""))
	# 		sum_rev = sum_rev + temp_int
	# 		sum_fav = sum_fav + int(a["Fourite Count"])
	# 		count = count + 1
	# 	for a in data_cat3:
	# 		sum_rat = sum_rat + float(a["Rating"])
	# 		temp_str = str(a["Number of Reviews"])
	# 		temp_int = int(temp_str.replace(" Reviews",""))
	# 		sum_rev = sum_rev + temp_int
	# 		sum_fav = sum_fav + int(a["Fourite Count"])
	# 		count = count + 1
	# 	for a in data_cat6:
	# 		sum_rat = sum_rat + float(a["Rating"])
	# 		temp_str = str(a["Number of Reviews"])
	# 		temp_int = int(temp_str.replace(" Reviews",""))
	# 		sum_rev = sum_rev + temp_int
	# 		sum_fav = sum_fav + int(a["Fourite Count"])
	# 		count = count + 1
	# 	if(size != 0):
	# 		aa[i] = sum_rev/count
	# 		bb[i] = (sum_rat/count - 4.9) * 2000
	# 		cc[i] = sum_fav/count
	# 		dd[i] = name
	# 		print(sum_rev/count)
	# 		print(sum_rat/count)
	# 		print(sum_fav/count)
	# 		i = i + 1

	# trace11 = Bar(x=dd,y=aa,name='Average Reviews')
	# trace22 = Bar(x=dd,y=bb,name='Average Ratings\n(value / 2000 + 4.9)')
	# trace33 = Bar(x=dd,y=cc,name='Average Favorite Count')
	# data = Data([trace11, trace22, trace33])
	# layout = Layout(barmode='group')
	# fig = Figure(data=data, layout=layout)
	# plot_url2 = py.plot(fig, filename='Bar Graph')
	# pint(plot_url2)
ploted()