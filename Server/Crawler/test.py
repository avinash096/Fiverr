import requests
import time
import json
import pymongo
from bson.objectid import ObjectId
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
display = Display(visible=0,size(1024,768))
display.start()
myproxy = "10.3.100.207:8080"
proxy = Proxy({
    'proxyType':ProxyType.MANUAL,
    'httpProxy':myproxy,
    'ftpProxy':myproxy,
    'sslProxy':myproxy,
    'noProxy':''
    })

browser = webdriver.Firefox(proxy=proxy)
connection = pymongo.MongoClient()

db = connection["fiverr_data"]
gigs = db["gigs"]

def crawler():
    url = "https://www.fiverr.com"
    browser.get(url)
    time.sleep(10)
    soup = BeautifulSoup(browser.page_source)
    # This is to login into fiverr.com each and every time a new browser opens up
    a_login = soup('a', text="Sign In")
    url_login = a_login[0]['href']
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
    # This sleep is to make the page load
    time.sleep(20)
    file_gigs = open('gig_sample.txt', 'w')
    s="";
    # Find all the names of the categories of fiverr.com
    gig_category = soup.find_all('a', attrs={'data-gtm-event': 'Category Navigation'})
    gig_couno=0
    for cat in gig_category:
        # All the sub categories are listed in a div having class attribute menu-cont
        gig_couno +=1
        if (gig_couno <= 1):
            data = soup.find_all('div', attrs={'class': 'menu-cont'})
            fg = 0
            for div in data:
                # each menu-cont div contains ul which in turns contains various links for the subcategories
                # U can look at tree if you right click and click on inspect element
                fg += 1
                if (fg <=1):
                    data1 = div.find_all('ul')
                    div_data = 0
                    gig_category = (div.parent).parent
                    for ul in data1:
                        div_data +=1
                        print("cat_count"+str(div_data))
                        if (div_data <= 1):
                            links = ul.find_all('a')
                            link_count=0
                            for a in links[1:]:
                                link_count+=1
                                if (link_count<=1):
                                    print a['href']
                                    url = "https://www.fiverr.com" + a['href']+"#layout=auto&page=1"
                                    browser.get(url)
                                    time.sleep(20)
                                    # This load more is to load all the gigs
                                    # try:
                                    #     browser.find_element_by_class_name('gig-load-more').click()
                                    # except:
                                    #     pass
                                    # for i in range(1, 8000):
                                    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                                    # This count is to count all the gigs
                                    count = 0
                                    soup = BeautifulSoup(browser.page_source)
                                    for link in soup.find_all('a', {'class': 'gig-link-main'}):
                                        count += 1
                                        print("Count is "+str(count))
                                        if(count <= 1):
                                            url1 = "https://fiverr.com"+(link.get('href'))
                                            browser.get(url1)

                                            time.sleep(5)
                                            i = 2
                                            # while(i > 0):
                                            #     try:
                                            #         browser.find_element_by_link_text("Show More").click()
                                            #     except:
                                            #         break
                                            # for i in range(1, 1000):
                                            #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                                            soup = BeautifulSoup(browser.page_source)
                                            favourite= soup.find_all('div',{'class':'gig-collect-count'})
                                            for d1 in soup.find_all('span', {'class': 'gig-title'}):
                                                # Here the storing of data starts
                                                print("Description text "+((d1.text).strip("\r\n\t")))
                                                s+=("{\n\t\"Gig_name\""+": \""+(d1.text).strip("\r\n\t")+"\",").encode('utf-8')
                                            s+=("\n\t").encode('utf-8')
                                            # I have continously opened and closed file in order to see the data at regular
                                            #file_gigs.close()
                                            #file_gigs = open('gig_sample.txt', 'a')
                                            s+=("\"Category\":\"" + (cat.text).strip("\r\n\t") + "\",").encode('utf-8')
                                            s+=("\n\t").encode('utf-8')
                                            # file_gigs.close()
                                            # file_gigs = open('gig_sample.txt', 'a')
                                            s+=("\"Sub Category\":\"" + (a.text).strip("\r\n\t") + "\",").encode('utf-8')
                                            s+=("\n\t").encode('utf-8')
                                            # file_gigs.close()
                                            # file_gigs = open('gig_sample.txt', 'a')
                                            for span in soup.find_all('span', {'class': 'numeric-rating'}):
                                                s+=("\"Rating\": \"" + (span.text).strip("\r\n\t") + "\",\n\t").encode('utf-8')
                                            for div in soup.find_all('div', {'class': 'gig-main-desc'}):
                                                s+=("\"Description\":\"" + (div.text).strip("\r\n\t") + "\"\t,").encode('utf-8')
                                            sum = 0
                                            for fav in favourite:
                                                s += ("\"Fourite Count\":\""+(fav.text).strip("\r\n\t")+"\",\n\t").encode('utf-8')
                                            for review_count in soup.find_all('h4',{'itemprop':'reviewCount'}):
                                                s += ("\"Number of Reviews\":\""+(review_count.text).strip("\r\n\t")+"\",\n\t").encode('utf-8')
                                            data2 = soup.find_all('ul', {'class': 'reviews-list'})
                                            #file_gigs = open('gig_sample.txt', 'a')
                                            count_review = 1
                                            for ul2 in data2:
                                                s+=("\"Reviews\":["). encode('utf-8')
                                                # file_gigs.close()
                                                # file_gigs = open('gig_sample.txt', 'a')
                                                for li2 in ul2.find_all('li'):
                                                    linkss = li2.find_all('a')
                                                    divi = li2.find_all('div', {'class': 'msg-body'})
                                                    spann = li2.find_all('span', {'class': 'rating-date'})
                                                    count_r = 0
                                                    for a2 in linkss:
                                                        # s+=("\n\t\t\"Review"+str(count_review)+"\":").encode('utf-8')
                                                        s+=("\n\t\t\t{\n\t\t\t\t\"User\":\""+(a2.text).strip("\r\n\t")+"\",").encode('utf-8')
                                                        s+=("\n\t\t\t\t").encode('utf-8')

                                                        # file_gigs.close()
                                                        # file_gigs = open('gig_sample.txt', 'a')
                                                        s+=("\"Message\":\""+(divi[count_r].text).strip("\r\n\t")+"\",").encode('utf-8')
                                                        s+=("\n\t\t\t\t").encode('utf-8')

                                                        # file_gigs.close()
                                                        # file_gigs = open('gig_sample.txt', 'a')
                                                        s+=("\"Rating-Date\":\""+(spann[count_r].text).strip("\r\n\t")+"\"\n\t\t\t},").encode('utf-8')
                                                        count_review += 1
                                                        count_r += 1
                                                    sum += 1
                                                    time.sleep(1)
                                            s = s[:-1]
                                            s+=("\n\t]").encode('utf-8')
                                            print(sum)
                                        else:
                                            break
                                        s+=("\n}").encode('utf-8')
                        # file_gigs.close()
    print(type(s))
    s = s.strip(" ")
    s = s.replace("\r","")
    s = s.replace("\n","")
    print(s)
    print(s[246])
    file_gigs.write(s)
    file_gigs.close()
    gigs.insert=json.loads(s)

crawler()
