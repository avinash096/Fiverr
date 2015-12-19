import requests
import os
import sys
import time
import json
import pymongo
from bson.objectid import ObjectId
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display

#display = Display(visible=0,size=(1024,768))
#display.start()
print("Made a Virtual Display for the browser to run")

myproxy = "10.3.100.207:8080"
proxy = Proxy({
    'proxyType':ProxyType.MANUAL,
    'httpProxy':myproxy,
    'ftpProxy':myproxy,
    'sslProxy':myproxy,
    'noProxy':''
    })
try:
    browser = webdriver.Firefox(proxy=proxy)
    time.sleep(10)
    print("Connection with Firefox Browser Succeeded")
except:
    print("Connection with Firefox Failed")
    sys.exit()

try:
    connection = pymongo.MongoClient()
    db = connection["fiverr_data"]
    gigs = db["new_url"]
    print("Connection with Mongo DB Succeeded")
except:
    print("Connection with Mongo DB Failed. Continuing to store it in a file")

def crawler():
    url = "https://www.fiverr.com/categories/other/"
    browser.get(url)
    time.sleep(10)
    soup = BeautifulSoup(browser.page_source)
    # This is to login into fiverr.com each and every time a new browser opens up

    try:
        a_login = soup('a', text="Sign In")
        url_login = a_login[0]['href']
        print("Connection with Fiverr successfuly made")
    except:
        print("Problem Loading Page. Hence Exiting")
        sys.exit()
    browser.get(url_login)
    time.sleep(10)
    username = browser.find_element_by_class_name("js-form-login")
    username.click()
    username.send_keys("krishna.bagadia2@gmail.com")
    password = browser.find_element_by_class_name("js-form-password")
    password.click()
    password.send_keys("krishna")
    submit = browser.find_element_by_class_name("btn-standard")
    submit.click()
    print("Successfully Logged into Fiverr.com")

    time.sleep(10)
    try:
        soup = BeautifulSoup(browser.page_source)
        new_gig = soup.find('a', {'class':'js-gtm-event-auto', 'data-gtm-label':'new'})
        browser.get("https://www.fiverr.com" + new_gig['href'])
        time.sleep(10)
        print("Connected to New")
    except:
        print("Failed to Connect to New")

    try:
        browser.find_element_by_class_name('btn-standard-lrg').click()
    except:
        pass
    print("Loading all the gigs in the given page")
    for i in range(1, 75):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    print("Loading all the given page succeeded")
            # This count is to count all the gigs
    count = 0
    soup = BeautifulSoup(browser.page_source)
    for link in soup.find_all('a', {'class': 'gig-link-main'}):
        count += 1
        url1 = "https://fiverr.com"+(link.get('href'))
        json_data = {}
        json_data['Category'] = "Other"
        json_data['Sub-Category'] = "Other"
        json_data['url'] = url1
        #json_json_data = json.dumps(json_data)
        #print json_data
        gig_exist = gigs.find(json_data).count()
        if(gig_exist <= 0):
            gigs.insert_one(json_data)
    print count
crawler()
