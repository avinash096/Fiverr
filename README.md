# Data Collection
- `Main2.py`
- `Main_format2.py`
- `others.py`
- `username.py`

# Processing
- `formatLIWC.py`  


# Case Specific Analysis
- `Multiple_review_check.py`  
  This script checks for existence of multiple reviews made by a single user on a particular gig. It runs on the existing    collection of gigs and creates a new collection which gives the gig-wise data on the number of reviews made by each user   that has purchased the gig. It also stores the actual message present in those reviews.
- `Multiple_data_analyse.py`  
  This script works on the collection made by the above file and finds out statistical data like the "Average Number of      reviews given by a single user per gig" and "Average number of users making multiple reviews per gig".

# Sentiment Analysis
- `senti_dict.py`  
Performs sentiment analysis on the reviews of the gigs using Senti Word Net lexicon. Modifies the gig json to add the new positive, negative and objective scores.

# Review Graph Implementation
- `review_final.py`  
Implementation of the heterogenous review graph framework for spammer detection as suggested in [this paper] (https://www.cs.uic.edu/~gwang/papers/ICDM-2011-final.pdf).

# Plotting
- `plot.py`  
Plots of 'fraction of gigs vs reviews'(linear and log-log), 'fraction of gigs vs rating'(linear and log-log), 'category-wise representation of average reviews, ratings and favourite count'
- `pos_score_plot.py`  
Plots of 'fraction of gigs vs positive score'.
- `plot_negative.py`  
Plots of ''fraction of gigs vs negative score'.


# LIWC plotting
- After processing with `formatLIWC.py` get the LIWC scores and then running `log_log.py` will give all the *value* vs *frequency* in log-log scale in the same directory where it was run from.

# Word-cloud plotting
- `fiverr_wordcloud.py`  
Makes a word-cloud of all the words used in the product reviews given in the file specified.
