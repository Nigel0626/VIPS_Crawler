# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 15:22:38 2021

@author: nigel
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
from Vips import Vips
import time
import re
from difflib import SequenceMatcher

homapage_link =  "http://eatwhateatwhere.blogspot.com/"

# CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # chrome path
# CHROMEDRIVER_PATH = r"C:\Program Files (x86)\chromedriver4.exe" # driver path  
# chrome_options = Options()
# chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# chrome_options.add_argument('--disable-gpu')
# chrome_options.binary_location = CHROME_PATH        
# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

# #For blogspot
# def getArchivedLinks(archiveList):
#     linkStack = []
#     linkNameStack = []
#     posts = archiveList.find_elements_by_class_name("posts")
#     for post in posts:
#         links=post.find_elements(By.TAG_NAME,"a")
#         for link in links:
#             linkStack.append(link.get_attribute("href"))
#             linkNameStack.append(link.text)
#     return linkStack, linkNameStack

# def expandList(date):
#     try:
#         time.sleep(0.2)
#         checkExpand = WebDriverWait(date, 3).until(EC.presence_of_element_located((By.XPATH, "./li")))
#         if checkExpand.get_attribute("class") != "archivedate expanded":
#             try:
#                 WebDriverWait(checkExpand, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "toggle"))).click()
#             except TimeoutException:
#                 pass
#     except TimeoutException:
#             pass  
        
# driver.get(homapage_link)           
# archiveList = driver.find_element_by_id("BlogArchive1_ArchiveList")
# yearToggles = archiveList.find_elements_by_xpath("./ul")         

# for year in yearToggles:
#   expandList(year)
#   checkExpand = year.find_element_by_xpath("./li")
#   monthToggles =  checkExpand.find_elements_by_xpath("ul")
#   for month in monthToggles:
#         expandList(month)
# URL_Link,name = getArchivedLinks(archiveList)
# time.sleep(2)
# driver.quit()

# for a in range(10):
#     print(URL_Link[a])


# for i in range(10):
#     print(URL_Link[i])
#     print(name[i])
#     Crawl = None
#     Crawl = Vips(URL_Link[i],name[i])
#     Crawl.start()
#     time.sleep(2)
Crawl = Vips("http://www.vkeong.com/eat/buffet/iketeru-japanse-buffet-the-hungry-deal-hilton-kl/","Iketeru Japanse Buffet (The Hungry Deal) @ Hilton KL")
Crawl.start()

        
## For other website   
# driver.get(homapage_link)        
# links=driver.find_elements_by_tag_name("a")

# def filter(homepage_link, links):
#     link_list = []
#     for link in links:
#         urllink = link.get_attribute("href")
#         if re.search(homepage_link, str(urllink)) and len(str(urllink))>80 and len(str(urllink))<=105:
#             link_list.append(urllink)
#     return link_list

# def removeDuplicate(links):
#     tempList = []
#     for link in links:
#         repeat = False
#         for tempLink in tempList:
#             #print(2)
#             if re.search(link, tempLink) or similar(link, tempLink):
#                 #print("triggered")
#                 repeat = True
#         if(repeat == False):
#             tempList.append(link)
#             print(link)

#     return tempList



# def similar(a, b):
#     if SequenceMatcher(None, a, b).ratio()>0.8:
#         return True
#     else:
#         return False


# URL_Link = filter(homapage_link, links)  
# URL_Link = removeDuplicate(URL_Link)    
# time.sleep(2)
# driver.quit()

# URL_Link = ["https://foodeverywhere.wordpress.com/2019/01/14/namelaka-patisserie-bangsar/"
#          ,"https://foodeverywhere.wordpress.com/2019/01/13/bar-patua-mgm-cotai-macao-macau/"
# 	,"https://foodeverywhere.wordpress.com/2019/01/07/legit-burger-joint-at-jalan-imbi-burger-on-16/"
# 	,"https://foodeverywhere.wordpress.com/2019/01/03/macao-sweet-treats-portuguese-tart-which-is-the-best/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/26/margarets-cafe-e-nata-macao-authentic-portuguese-egg-tart/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/25/kara-conceptual-french-cuisine-kota-damansara-sunway-giza-mall/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/23/lei-ka-choi-hot-pot-at-broadway-macaos-hot-pot-sensation/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/21/infused-with-love-at-hard-rock-cafe/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/19/burgers-and-lobsters-sky-avenue-genting-highland-still-a-hype-in-2019/"
# 	,"https://foodeverywhere.wordpress.com/2018/12/17/mong-seng-kopitiam-for-some-authentic-hee-kiaw-noodle-melaka/"]

# for i in range(10):
#     print(URL_Link[i])
#     Crawl = None
#     Crawl = Vips(URL_Link[i],"Blog")
#     Crawl.start()
#     time.sleep(2)
    

    

    
