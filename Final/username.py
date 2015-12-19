import urllib2
from bs4 import BeautifulSoup
import json

username = raw_input('Enter username: ')
url = 'http://fiverr.com/'+username
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(url, headers=hdr)
page = urllib2.urlopen(req)

soup = BeautifulSoup(page)
div = soup.find_all('div', 'gig-carousel loading cf ')
json_path = div[0].attrs['data-json-path']

r = urllib2.Request('http://fiverr.com'+json_path, headers=hdr)
json_list = urllib2.urlopen(r)

json_source = json.load(json_list)
total_gigs = len(json_source['gigs'])
print 'Total Gigs:' + str(total_gigs)
i = 0
while i < total_gigs:
    gig_url = json_source['gigs'][i]['gig_url']
    gig_name = json_source['gigs'][i]['title']
    print 'Gig Name: %s, Gig URL: http://fiverr.com%s' % (gig_name, gig_url)
    i += 1

