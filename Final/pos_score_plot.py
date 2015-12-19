import plotly.plotly as py
from plotly.graph_objs import *
import pymongo
from bson.objectid import ObjectId
import sys
import numpy

try:
  connection = pymongo.MongoClient()
  #connection1 = pymongo.MongoClient(host='10.136.205.46', port=27017)
  db = connection["fiverr_data"]
  gigs = db["gigs"]
  #db_ = connection1['fiverr_data']
  gigs_score = db['gigs_senti_sans_pos']

except:
  print("Connection to MongoDB Failed")

def effPlot():

  total_gigs = gigs_score.find(no_cursor_timeout=True)
  total_gigs_count = gigs_score.count()
  gig_eff_score = {}
  eff_score_list = []
  count_gigs = [0] * 1000
  for i in total_gigs:

    #print("Gig is ")
    eff_sum = 0
    total_number_reviews = 0
    reviews = i['Multiple Review Data']
    for user in reviews:
      total_number_reviews = total_number_reviews + int(user['Review_Count'])
      for message in user['Messages']:
        eff_sum = eff_sum +  message['Positive_Score'] - message['Negative_Score']
    eff_sum_average = (eff_sum*1000.0)/total_number_reviews
    eff_score_list.append(eff_sum_average)

  for i in range(0,1000):
    sum_score = 0
    for j in eff_score_list:
      if (int(j) == i):
        sum_score = sum_score + 1 
    count_gigs[i] = (sum_score*1.0 / total_gigs_count)

  trace1 = Scatter( x = range(1,1000), y = count_gigs)
  data = Data([trace1])
  layout = Layout(xaxis=XAxis(type='log',autorange=True),yaxis=YAxis(type='log',autorange=True))
  fig = Figure(data=data)
  plot_url = py.plot(fig, filename='Fraction of Gigs vs Effective Score')

def posPlot():

  total_gigs = gigs_score.find(no_cursor_timeout=True)
  total_gigs_count = gigs_score.count()
  gig_eff_score = {}
  eff_score_list = []
  count_gigs = [0] * 1000
  for i in total_gigs:

    eff_sum = 0
    total_number_reviews = 0
    reviews = i['Multiple Review Data']
    for user in reviews:
      total_number_reviews = total_number_reviews + int(user['Review_Count'])
      for message in user['Messages']:
        eff_sum = eff_sum +  message['Positive_Score']
    eff_sum_average = (eff_sum*1000.0)/total_number_reviews
    eff_score_list.append(eff_sum_average)

  for i in range(0,1000):
    sum_score = 0
    for j in eff_score_list:
      if (int(j) == i):
        sum_score = sum_score + 1 
    count_gigs[i] = (sum_score*1.0 / total_gigs_count)

  trace2 = Scatter( x = range(1,1000), y = count_gigs)
  data = Data([trace2])
  layout = Layout(xaxis=XAxis(type='log',autorange=True),yaxis=YAxis(type='log',autorange=True))
  fig = Figure(data=data)
  plot_url2 = py.plot(fig, filename='Fraction of Gigs vs Positive Score')

def negPlot():

  total_gigs = gigs_score.find(no_cursor_timeout=True)
  total_gigs_count = gigs_score.count()
  gig_eff_score = {}
  eff_score_list = []
  count_gigs = [0] * 1000
  for i in total_gigs:

    eff_sum = 0
    total_number_reviews = 0
    reviews = i['Multiple Review Data']
    for user in reviews:
      total_number_reviews = total_number_reviews + int(user['Review_Count'])
      for message in user['Messages']:
        eff_sum = eff_sum +  message['Negative_Score']
    eff_sum_average = (eff_sum*1000.0)/total_number_reviews
    eff_score_list.append(eff_sum_average)

  for i in range(0,1000):
    sum_score = 0
    for j in eff_score_list:
      if (int(j) == i):
        sum_score = sum_score + 1 
    count_gigs[i] = (sum_score*1.0 / total_gigs_count)


  trace3 = Scatter( x = range(1,1000), y = count_gigs)
  data = Data([trace3])
  layout = Layout(xaxis=XAxis(type='log',autorange=True),yaxis=YAxis(type='log',autorange=True))
  fig = Figure(data=data)
  plot_url3 = py.plot(fig, filename='Fraction of Gigs vs Positive Score')

def avgScore():

  total_review = 0
  total_eff = list()
  total_pos = list()
  total_neg = list()
  total_gigs = gigs_score.find(no_cursor_timeout=True)
  total_gigs_count = gigs_score.count()
  gig_eff_score = {}
  eff_score_list = []
  count_gigs = [0] * 1000
  for i in total_gigs:

    eff_sum = 0
    total_number_reviews = 0
    reviews = i['Multiple Review Data']
    for user in reviews:
      total_number_reviews = total_number_reviews + int(user['Review_Count'])
      for message in user['Messages']:
        eff_sum = eff_sum +  message['Negative_Score']
        total_neg.append(message['Negative_Score'])
        total_pos.append(message['Positive_Score'])
        total_eff.append(message['Positive_Score'] - message['Negative_Score'] + message['Objective_Score'])
        total_review += 1
    eff_sum_average = (eff_sum*1000.0)/total_number_reviews
    eff_score_list.append(eff_sum_average)
    sys.stdout.write("Review progress:\t %d reviews   \r" % (total_review) )
    sys.stdout.flush()

  for i in range(0,1000):
    sum_score = 0
    for j in eff_score_list:
      if (int(j) == i):
        sum_score = sum_score + 1 
    count_gigs[i] = (sum_score*1.0 / total_gigs_count)

  print "\n"
  print "Positive SD :\t\t ", numpy.std(total_pos, axis=0)
  print "Negative SD :\t\t ", numpy.std(total_neg, axis=0)
  print "Effective SD :\t\t ", numpy.std(total_eff, axis=0)
  print "Effective Median :\t\t ", numpy.median(total_eff)
  print "Effective Average :\t\t ", numpy.average(total_eff)
  trace3 = Scatter( x = range(1,1000), y = count_gigs)
  data = Data([trace3])
  layout = Layout(xaxis=XAxis(type='log',autorange=True),yaxis=YAxis(type='log',autorange=True))
  fig = Figure(data=data)
  plot_url3 = py.plot(fig, filename='Fraction of Gigs vs Positive Score')


avgScore()
effPlot()
posPlot()
negPlot()