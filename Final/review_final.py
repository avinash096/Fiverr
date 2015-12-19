import pymongo
import json
import math
import numpy as np
from datetime import timedelta
import plotly.plotly as py
from plotly.graph_objs import *

try:
  connection = pymongo.MongoClient()
  #connection1 = pymongo.MongoClient(host='10.109.67.130', port=27017)
  db = connection['fiverr_data']
  #db_ = connection1['fiverr_data']
  gigs_original = db['gigs']
  gigs_senti = db['gigs_senti_sans_pos']
except:
  print('Connection with MongoDB Failed')

#########Global Variables#################

time_threshold = timedelta(days = 3*30)     #3 months
review_agreement_threshold = 0.4   ## Set accordingly
median_score = 0.6   # Median of Effective Score
reviewer_set = set()
gig_set = set()
review_set = set()

########################################

class Reviewer:
  def __init__(self):
    self.trustiness = 1
    self.reviews = []
    self.name = ''
    self.gigs = []

  def __hash__(self):
    return hash(self.name)

class Review:
  def __init__(self):
    self.gig_store = Gig()
    self.reviewer = Reviewer()
    self.honesty = 0
    self.text = ''
    self.pos_score = 0
    self.neg_score = 0
    self.obj_score = 0
    self.eff_score = 0
    self.date = timedelta(days = 0)
    self.agreement = 0

  def __hash__(self):
    return hash((self.text,self.reviewer,self.gig_store))

class Gig:
  def __init__(self):
    self.reliability = 1
    self.reviews = []
    self.users = []
    self.total_number_reviews = 0
    self.rating = 0
    self.name = ''

def calculateHonesty():

  for review in review_set:
    review.honesty = abs(review.gig_store.reliability)*review.agreement

def calculateTrustiness():

  for reviewer in reviewer_set:

    sum_honesty = 0

    for reviewer_review in reviewer.reviews:
      sum_honesty = sum_honesty + reviewer_review.honesty
    
    reviewer.trustiness = ((2*1.0)/(1 + np.exp(-sum_honesty))) - 1

def calculateSentiScore():

  counter = 0
  for review in review_set:
    counter = counter + 1
    #print("Counter is " + str(counter))
    #print("Calculating the Senti Score of " + review.gig_store.name)
    required_gig = gigs_senti.find({'Gig_name':review.gig_store.name})
    for a_gig in required_gig:
      #print("Rquired Gig is " + str(a_gig))
      required_gig_multiple_reviews = a_gig['Multiple Review Data']
      for sect in required_gig_multiple_reviews:
        #print("User name is " + sect['User_name'] )
        #print("Required User name is " + review.reviewer.name)
        if (sect['User_name'] == review.reviewer.name):
          for message in sect['Messages']:
            #print("Message is " + message['Message'])
            if (message['Message'] == review.text):
              review.pos_score = message['Positive_Score']
              review.neg_score = message['Negative_Score']
              review.obj_score = message['Objective_Score']
              review.eff_score = review.pos_score - review.neg_score + (review.obj_score) 

              # if (review.eff_score < 0):
              #   review.eff_score = -1
              # else:
              #   review.eff_score = 1
              #print("Effective Score is " + str(review.eff_score))
              #print("Effective Score is " + str(review.eff_score))

def calculateReliability():

  
  for gig in gig_set:
    sum = 0
    for review in gig.reviews:
      sum = sum + (review.reviewer.trustiness*(review.eff_score - median_score))  
    gig.reliability = ((2*1.0)/(1 + np.exp(-sum))) - 1



def calculateAgreement():

  for gig in gig_set:

    for review in gig.reviews:          #Sv

      sum = 0
      for other_review in gig.reviews:
        if (review == other_review):
          continue
        else:
          if (abs(review.date - other_review.date) < time_threshold):
            if (abs(review.eff_score - other_review.eff_score) < review_agreement_threshold):
              sum = sum + other_review.reviewer.trustiness
              #print("Added: Trustiness is " + str(other_review.reviewer.trustiness))
            else:
              sum = sum - other_review.reviewer.trustiness
              #print("Subtracted: Trustiness is " + str(other_review.reviewer.trustiness))

      review.agreement = ((2*1.0)/(1 + np.exp(-sum))) - 1



def main():

  ################ Initialisation ########################

  print("Starting the Process of Creating Sets for Reviews, Reviewer and Gigs")
  all_gigs = gigs_original.find(no_cursor_timeout=False)
  counter = 0 
  for gig in all_gigs[5000:]:
    try:
      gig
    except:
      continue
    counter = counter + 1
    number_reviews = gig['Number of Reviews']
    number_reviews = int(number_reviews.replace(' Reviews',''))
    if (number_reviews < 10 or number_reviews > 20 or counter > 1000 ):
      continue
    gig_entry = Gig()
    gig_entry.name = gig['Gig_name']
   # print("\nGig name is " + gig_entry.name + "\n")
   # print("\nCounter is " + str(counter-1))
    number_reviews = gig['Number of Reviews']
    number_reviews = int(number_reviews.replace(' Reviews',''))
    gig_entry.total_number_reviews = number_reviews
    gig_entry.rating = float(gig['Rating'])
    gig_set.add(gig_entry)
    reviews_array = gig['Reviews']
    for review in reviews_array:
      
      #print("In reviews array ")
      found = 0
      
      for check_reviewer in reviewer_set:
        if (check_reviewer.name == review['User']):
          reviewer = check_reviewer
          found = 1
      
      if (not found):

        reviewer = Reviewer()
        reviewer.name = review['User']
        reviewer_set.add(reviewer)


      review_entry = Review()
      review_entry.text = review['Message']
      review_entry.gig_store = gig_entry
      review_entry.reviewer = reviewer
      rating_date = review['Rating-Date']
      
      if ('days' in rating_date or 'day' in rating_date):
        for s in rating_date.split(' '):
          if (s.isdigit()):
            review_entry.date = timedelta(days = int(s))

      if ('months' in rating_date or 'month' in rating_date):
        for s in rating_date.split(' '):
          if (s.isdigit()):
            review_entry.date = timedelta(days = int(s)*30)  
        
      if ('years' in rating_date or 'year' in rating_date):
        for s in rating_date.split(' '):
          if (s.isdigit()):
            review_entry.date = timedelta(days = int(s)*365)
      
      if ('hour' in rating_date or 'hours' in rating_date):
        review_entry.date = timedelta(days = 0)
        
      
      if ('today' in rating_date):
          review_entry.date = timedelta(days = 0)

      reviewer.reviews.append(review_entry)
      gig_entry.reviews.append(review_entry)
      review_set.add(review_entry)
      reviewer.gigs.append(gig_entry)
      gig_entry.users.append(reviewer)
  print("Successfully Created Sets")
  calculateSentiScore()

  print("Successfully Calculated the Score")
  calculateAgreement()

  print("Successfully Calculated Agreement Values")
  roundCounter = 1

  reviewer_list = open('initial_sentiments.txt' ,'w')
  for review in review_set:
    reviewer_list.write(((review.text) + ' ' + str(review.eff_score) + "\n\n ").encode('utf-8'))
      
  reviewer_list.close()
  
  while( roundCounter < 20 ):
    calculateHonesty()

    print("Calculated Honesty")
    calculateTrustiness()
    print("Calculated Trustiness")
    calculateReliability()
    print("Calculated Reliabilty")
    calculateAgreement()
    print("Calculated Agreement")
    roundCounter = roundCounter + 1
   
    reviewer_list = open('initial_sentiments' + str(roundCounter) + '.txt' ,'w')
    for review in review_set:
      reviewer_list.write(((review.text) + ' ' + str(review.eff_score) + "\n\n ").encode('utf-8'))
        
    reviewer_list.close()
    
    reviewer_list = open('reviewes_statistics' + str(roundCounter) + '.txt','w')
    for gig in gig_set:
      reviewer_list.write(((gig.name) + ' ' + str(gig.reliability) + "\n\n ").encode('utf-8'))
      
      for user in gig.users:
        reviewer_list.write( '\t'+ ((user.name) + '  ' + str(user.trustiness)+"\n\n\n").encode('utf-8') )

        for review in user.reviews:
          reviewer_list.write( '\t'+ ((review.text) + '  ' + str(review.honesty)+"\n\n\n").encode('utf-8') )        
    reviewer_list.close()
    reviewer_list = open('reviewes_' + str(roundCounter)+ '.txt','w')

    for reviewer in reviewer_set:
      reviewer_list.write(((reviewer.name) + '  ' + str(reviewer.trustiness)+"\n").encode('utf-8') )
      for review in reviewer.reviews:
        reviewer_list.write( '\t'+ ((review.text) + '  ' + str(review.honesty)+"\n").encode('utf-8') )
    for gig in gig_set:
      reviewer_list.write(((gig.name) + ' ' + str(gig.reliability) + "\n ").encode('utf-8'))
    print("Value of roundCounter is " + str(roundCounter) + "\n")
    
  count_trustiness = [0]*100
  number_people_untrustworthy=0
  number_reviews_unhonesty=0
  number_gigs_unreliable=0
    
  for reviewer in reviewer_set:
    count_trustiness[int(reviewer.trustiness*100)] = count_trustiness[int(reviewer.trustiness*100)] + 1
    if (reviewer.trustiness < 0):
      number_people_untrustworthy = number_people_untrustworthy + 1
    #print(reviewer.trustiness)
  for i in range(1,100):
    count_trustiness[i] = (count_trustiness[i]*1.0)
  
  number_people_untrustworthy = (number_people_untrustworthy*1.0)
  print("People is " + str(number_people_untrustworthy))
  review_trustiness = [0]*100
  
  for review in review_set:
    review_trustiness[int(review.honesty*100)] = review_trustiness[int(review.honesty*100)] + 1
    if (review.honesty < 0):
      number_reviews_unhonesty = number_reviews_unhonesty + 1
    #print(review.honesty)
  for i in range(1,100):
    review_trustiness[i] = (review_trustiness[i]*1.0)
  
  number_reviews_unhonesty = (number_reviews_unhonesty*1.0)
  print("Honesty is " + str(number_reviews_unhonesty))
  gig_rel = [0]*100
  
  for gig in gig_set:
    gig_rel[int(gig.reliability*100)] = gig_rel[int(gig.reliability*100)] + 1
    if (gig.reliability < 0):
      number_gigs_unreliable = number_gigs_unreliable + 1
    #print(gig.reliability)
  for i in range(1,100):
    gig_rel[i] = (gig_rel[i]*1.0)
  
  number_gigs_unreliable = (number_gigs_unreliable*1.0)
  print("Unreliable of gigs is "+ str(number_gigs_unreliable))
  print("Number of Gigs are " + str(len(gig_set)))
  print("Number of users ar " + str(len(reviewer_set)))
  print("number of reviews are " + str(len(review_set)))
  #trace1 = Scatter(x = range(1,100), y = count_trustiness)
  #data1 = Data([trace1])
  import matplotlib.pyplot as plt
  plot_url = plt.plot(range(0,100), count_trustiness)
  plt.show()
  plot_url1 = plt.plot(range(0,100), review_trustiness)
  plt.show()
  plot_url2 = plt.plot(range(0,100), gig_rel)
  plt.show()
  ################# Initialisation Done #####################


if __name__ == "__main__":

  main()