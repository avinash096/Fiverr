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

# Review Graph Implementation
- `review_final.py`

# Plotting
- `plot.py`
- `pos_score_plot.py`
- `plot_negative.py`

# LIWC plotting
- After processing with `formatLIWC.py` get the LIWC scores and then running `log_log.py` will give all the *value* vs *frequency* in log-log scale in the same directory where it was run from.

# Word-cloud plotting
- `fiverr_wordcloud.py`
