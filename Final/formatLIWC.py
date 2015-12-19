import plotly.plotly as py
from plotly.graph_objs import *
import pymongo
from bson.objectid import ObjectId
import re

try:
  connection = pymongo.MongoClient()
  db = connection["fiverr_data"]
  gigs = db["gigs"]
  print("Connection with Mongo DB Succeeded.")
except:
  print("Connection with Mongo DB Failed.")


def ploted():
  total = gigs.count()
  print("Total number of gigs is " + str(total))
  a = [0.0] * 2000
  b = [0] * 2000
  for i in range(0, 2000):
    s =  str(i) + " Reviews"
    results = gigs.find({"Number of Reviews":s})
    count = results.count()
    a[i] = count/float(total)
    b[i] = i
  trace2 = Scatter(x=b,y=a)
  i = 0
  a = [0.0]*50
  b = [0.0]*50
  while(i<=5):
    s = str(i)
    results = gigs.find({"Rating":s})
    count = results.count()
    a[int(i*10)] = count/float(total)
    b[int(i*10)] = i
    i = i + 0.1
  trace3 = Scatter(x = b, y=a)
  c = [0.0] * 51
  d = [0] * 51

  # for i in xrange(0, 51):
  #   results = gigs.find({"Rating":str(i / 10.0)})
  #   count = results.count()
  #   c[i] = count / float(total)
  #   d[i] = i / 10.0
  # trace2 = Scatter(x=d,y=c)


  data = Data([trace2])
  data2 = Data([trace3])
  plot_url = py.plot(data, filename='Fraction of Gigs vs Reviews')
  plot_url1 = py.plot(data2, filename='Fraction of Gigs vs Rating')
  print plot_url
  print plot_url1

  num_catgories = 11
  category_name = {"Graphics & Design","Online Marketing","Writing & Translation","Video & Animation","Music & Audio","Programming & Tech","Advertising","Business","Lifestyle","Gifts","Fun & Bizarre","Others"}
  for name in category_name:
    data_cat = gigs.find({"Category":name})
    print("category_name: " + name)
    size = data_cat.count()
    sum_rat = 0.0
    sum_rev = 0
    count = 0
    for a in data_cat:
      sum_rat = sum_rat + float(a["Rating"])
      temp_str = str(a["Number of Reviews"])
      temp_int = int(temp_str.replace(" Reviews",""))
      sum_rev = sum_rev + temp_int
      count = count + 1
    if(size != 0):
      print(sum_rev/count)
      print(sum_rat/count)

def convertFormatLIWC():

  reviews_list = open("reviews_list.txt",'w')
  gig_list = open('gig_name_list.txt','w')
  cursor = gigs.find();
  for a_gig in cursor:
    s = ""
    gig_list.write((a_gig['Gig_name']+"\t" + a_gig['Category']+"\n\n\n").encode('utf-8'))
    for a_review in a_gig['Reviews']:
      s +=  re.sub('[^a-zA-Z0-9;,. ]','',a_review['Message']).encode('utf-8')
    s += "\n\n\n"
    s = (re.sub(' +',' ',s)).encode('utf-8')
    print(s)
    reviews_list.write(s)

  reviews_list.close()
  gig_list.close()

convertFormatLIWC()