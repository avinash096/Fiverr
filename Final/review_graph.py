import pymongo
import json
import math
#import numpy as np
from datetime import timedelta

try:
  connection = pymongo.MongoClient()
  #connection1 = pymongo.MongoClient(host='10.109.67.130', port=27017)
  db = connection['fiverr_data']
  #db_ = connection1['fiverr_data']
  gigs_original = db['gigs']
  gigs_senti = db['gigs_senti_dict']
except:
  print('Connection with MongoDB Failed')

#########Global Variables#################

time_threshold = timedelta(days = 3*30)     #3 months
review_agreement_threshold = 0.03   ## Set accordingly
median_score = 0.5   # Median of Effective Score
reviewer_set = set()
gig_set = set()
review_set = set()
########################################

class Reviewer:
  def __init__(self):
    self.trustiness = 1
    self.reviews = []
    self.name = ''

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

  for review in review_set:

    required_gig = gigs_senti.find({'Gig_name':review.gig_store.name})
    required_gig_multiple_reviews = required_gig['Multiple Review Data']
    for sect in required_gig_multiple_reviews:
      if (sect['User_name'] == review.reviewer.name):
        for message in sect['Messages']:
          if (message['Message'] == review.text):
            review.pos_score = message['Positive_Score']
            review.neg_score = message['Negative_Score']
            review.eff_score = review.pos_score - review.neg_score
    

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
      for other_reivew in gig.reviews:
        if (review == other_reivew):
          continue
        else:
          if (abs(review.date - other_review.date) < time_threshold):
            if (abs(review.eff_score - other_reivew.eff_score) < review_agreement_threshold):
              sum = sum + other_reivew.reviewer.trustiness
              print("Added: Trustiness is " + str(other_reivew.reviewer.trustiness))
            else:
              sum = sum - other_reivew.reviewer.trustiness
              print("Subtracted: Trustiness is " + str(other_reivew.reviewer.trustiness))

      review.agreement = ((2*1.0)/(1 + np.exp(sum))) - 1



def main():

  ################ Initialisation ########################

  print("Starting the Process of Creating Sets for Reviews, Reviewer and Gigs")
  all_gigs = gigs_original.find()
  counter = 0 
  for gig in all_gigs:
    counter = counter + 1
    gig_entry = Gig()
    gig_entry.name = gig['Gig_name']
    print("\nGig name is " + gig_entry.name + "\n")
    print("\nCounter is " + str(counter-1))
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

  print("Successfully Created Sets")
  calculateSentiScore()

  print("Successfully Calculated the Score")
  calculateAgreement()

  print("Successfully Calculated Agreement Values")
  roundCounter = 0

  while( roundCounter < 4 ):

    print("Value of roundCounter is " + str(roundCounter) + "\n")
    calculateHonesty()

    print("Calculated Honesty")
    calculateTrustiness()
    print("Calculated Trustiness")
    calculateReliability()
    print("Calculated Reliabilty")
    calculateAgreement()
    print("Calculated Agreement")
    roundCounter = roundCounter + 1
  ################# Initialisation Done #####################


if __name__ == "__main__":

  main()