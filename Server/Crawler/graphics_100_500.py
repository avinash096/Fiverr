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
#print("Made a Virtual Display for the browser to run")

myproxy = "10.3.100.207:8080"
proxy = Proxy({
    'proxyType':ProxyType.MANUAL,
    'httpProxy':myproxy,
    'ftpProxy':myproxy,
    'sslProxy':myproxy,
    'noProxy':''
    })
try:
    browser = webdriver.Firefox()
    time.sleep(20)
    print("Connection with Firefox Browser Succeeded")
except:
    print("Connection with Firefox Failed")
    sys.exit()

try:
    connection = pymongo.MongoClient()
    db = connection["fiverr_data"]
    gigs = db["gigs"]
    print("Connection with Mongo DB Succeeded")
except:
    print("Connection with Mongo DB Failed. Continuing to store it in a file")

def crawler():
    url = "https://www.fiverr.com/categories"
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
    print("Successfully Logined into Fiverr.com")
    
    gig_category = soup.find_all('h5')
    gig_category = gig_category[0:]
    

    for cat in gig_category[0:1]:
        # All the sub categories are listed in a div having class attribute menu-cont
        print("Entering Category: "+(cat.text).strip("\n\t"))
        link_category = cat.find('a')
        link_ = "http://www.fiverr.com" + link_category['href']
        print("Link to the Category is " + link_)
        try:
            browser.get(link_)
            time.sleep(10)
            soup = BeautifulSoup(browser.page_source)
            data = soup.find_all('a', attrs={'class': 'category-card'})
            data[0]
            print(data)
        except:
            continue
        for a in data[0:]:
            # each menu-cont div contains ul which in turns contains various links for the subcategories
            # U can look at tree if you right click and click on inspect element
            print("Entering Sub Category: "+(a.text).strip("\n\t"))
            url = "https://www.fiverr.com" + a['href']+"#layout=auto&page=1"
            try:
                browser.get(url)
                time.sleep(20)
                print("Successfully connected to the above Sub Category")
            except:
                print("Failed to Connect to the above Sub Category")
                continue
            
            filename = (cat.text).strip("\n\t ") + "/" +(a.text).strip("\n\t ")
            print("Filename is "+filename)
            filename = filename.strip(" ")
            if not os.path.exists(filename):
                os.makedirs(filename)
                                
            # This load more is to load all the gigs
            try:
                browser.find_element_by_class_name('btn-standard-lrg').click()
            except:
                pass
            print("Loading all the gigs in the given page")
            for i in range(1, 8000):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Loading all the given page succeeded")
            # This count is to count all the gigs
            count = 0
            soup = BeautifulSoup(browser.page_source)
            for link in (soup.find_all('a', {'class': 'gig-link-main'})):
                count += 1
                gig_file_name = filename+"/"+str(count)+".txt"
                print(gig_file_name)
                if os.path.isfile(gig_file_name):
                    print("Gig " + gig_file_name + "Already exist")
                    continue

                    
                print("Directory Creation for Storing the file successfull!!")
                url1 = "https://fiverr.com"+(link.get('href'))
                browser.get(url1)
                time.sleep(5)
                soup = BeautifulSoup(browser.page_source)
                revCountInit=""
                try:
                    for review_count in soup.find_all('h4',{'itemprop':'reviewCount'}):
                        revCountInit += review_count.text;
                    print("revCount is:"+revCountInit)
                    temp_int = int(revCountInit.replace(" Reviews",""))
                except:
                    continue
                if(temp_int<=100 or temp_int>500):
                    continue
                for d1 in soup.find_all('span', {'class': 'gig-title'}):
                    print("Connecting to Gig "+(d1.text).strip("\n\t\r"))
               
                i = 1
                print("Entering a loop to load all the comments and reviews")
                error_conn = 0
                while(i > 0):
                    try:
                        soup = BeautifulSoup(browser.page_source)
                        load_reviews_tag = soup.find('a',text="Show More")
                        if load_reviews_tag:
                            if "disabled in-progress" in str(load_reviews_tag):
                                print("Connection Error in Loading Reviews")
                                error_conn = 1
                                break
                        browser.find_element_by_link_text("Show More").click()
                        time.sleep(2)
                    except:
                        break
                if (error_conn==1):
                    count = count -1
                    continue;
                for i in range(1, 1000):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                soup = BeautifulSoup(browser.page_source)
                s=""
                favourite= soup.find_all('div',{'class':'gig-collect-count'})
                for d1 in soup.find_all('span', {'class': 'gig-title'}):
                    print("Connected to Gig "+(d1.text).strip("\n\t\r"))
                    print("Storing the data of this gig in string")
                    s+=("{\n\t\"Gig_name\""+": \""+(d1.text).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
                s+=("\n\t").encode('utf-8')
                
                s+=("\"Category\":\"" + (cat.text).strip("\r\n\t").replace("\"","\\\"") + "\",").encode('utf-8')
                s+=("\n\t").encode('utf-8')
                
                s+=("\"Sub Category\":\"" + (a.text).strip("\r\n\t").replace("\"","\\\"") + "\",").encode('utf-8')
                s+=("\n\t").encode('utf-8')
                
                for span in soup.find_all('span', {'class': 'numeric-rating'}):
                    s+=("\"Rating\": \"" + (span.text).strip("\r\n\t").replace("\"","\\\"") + "\",\n\t").encode('utf-8')
                
                for div in soup.find_all('div', {'class': 'gig-main-desc'}):
                    s+=("\"Description\":\"" + (div.text).strip("\r\n\t").replace("\"","\\\"") + "\"\t,").encode('utf-8')
                
                for fav in favourite:
                    s += ("\"Fourite Count\":\""+(fav.text).strip("\r\n\t")+"\",\n\t").encode('utf-8')
                
                for review_count in soup.find_all('h4',{'itemprop':'reviewCount'}):
                    s += ("\"Number of Reviews\":\""+(review_count.text).strip("\r\n\t").replace("\"","\\\"")+"\",\n\t").encode('utf-8')
                data2 = soup.find_all('ul', {'class': 'reviews-list'})
                
                count_review = 1
                for ul2 in data2:
                    s+=("\"Reviews\":["). encode('utf-8')
                
                    for li2 in ul2.find_all('li'):
                        linkss = li2.find_all('a')
                        divi = li2.find_all('div', {'class':'msg-body'})
                        spann = li2.find_all('span', {'class': 'rating-date'})
                        count_r = 0
                        for a2 in linkss:
                            try: 
                                s+=("\n\t\t\t{\n\t\t\t\t\"User\":\""+(a2.text).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
                                s+=("\n\t\t\t\t").encode('utf-8')
                            except:
                                pass
                            try:
                                s+=("\"Message\":\""+(divi[count_r].text).strip("\r\n\t").replace("\"","\\\"")+"\",").encode('utf-8')
                                s+=("\n\t\t\t\t").encode('utf-8')
                            except:
                                pass
                            try:
                                s+=("\"Rating-Date\":\""+(spann[count_r].text).strip("\r\n\t").replace("\"","\\\"")+"\"\n\t\t\t},").encode('utf-8')
                                count_r += 1
                            except:
                                pass
                        time.sleep(1)
                s = s[:-1]
                s+=("\n\t]").encode('utf-8')
                s+=("\n}").encode('utf-8')
                print("Formatting the data to be stored into database")
                s = s.strip(" ")
                s = s.replace("\r","")
                s = s.replace("\n","")
                print("Formatting the data done")
                try:
                    gigs.insert_one(json.loads(s))
                    gig_file = open(gig_file_name,'w')
                    gig_file.write(s)
                    gig_file.close()
                    print("Storing the above gig Successfull!!")
                except:
                    print("Storing the above gig failed!!")
                    pass
                print("Stored in the MongoDB. proceeding on the another gig if it exists!!")
    browser.close()
crawler()
