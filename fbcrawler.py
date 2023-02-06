#
# Name
#	fbcrawler.py
#
# Description
#   Web crawler that collects users' names and friends' information

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv
def scroll():
    """As the name implies, this function scrolls down the page """
    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
# Open facebook
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
chromedriver = 'C:/Users/mende/Downloads/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(chromedriver, options=options)
driver.get("https://www.facebook.com/")
time.sleep(2)

# Login
with open('login.txt','r') as f:
    logindata = f.readlines()
    
driver.find_element_by_xpath('//*[@id="email"]').send_keys(logindata[0])
time.sleep(1)
driver.find_element_by_xpath('//*[@id="pass"]').send_keys(logindata[1])
time.sleep(5) 
driver.find_element_by_xpath("//button[starts-with(@id,'loginbutton')][@name='login']").click()
time.sleep(5)

# Navigate to Facebook friendlist pages
with open('files.csv', 'r', newline='') as csvfile:
    data = csv.DictReader(csvfile)
# The IDs are pulled and used to obtain each users' friendlist page
    for row in data:
        ID = row['ID']
        driver.get("https://www.facebook.com/" + ID + "/friends")
        time.sleep(5)
        h_name = row['Hypothesis_name']
        f = open(h_name+'.txt','w+',encoding='utf-8')
        
        try:
            # Collect Name
            # xPath is used to find the HTML portion that contains the user's name
            name = driver.find_element_by_xpath('//div[@class="rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw taijpn5t gs1a9yip owycx6da btwxx1t3 ihqw7lf3 cddn0xzi"]/div/div/div/div/div/div/div/div/div/span//h1').text
            #print(name)
            f.writelines(name + "\n")
            # Friendlist Boolean
            # xPath is used to see if "No Friends To Show" is displaying under friends
            try:
                driver.find_element_by_xpath('//div[@class="rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs"]//div//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 ns63r2gh fe6kdd0r mau55g9w c8b282yb iv3no6db o3w64lxj b2s5l15y hnhda86s pipptul6 oqcyycmt"]').text
                #print("False")
                f.writelines("False\n")
            # The absence of this element and its text indicate that the friendlist is displaying
            except NoSuchElementException:
                #print("True")
                f.writelines("True\n")
                # Locate the the HTML portions containing friends' categories
                Xpath_Friends_categories='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]'
                #Fetch it
                Xpath_Friends_categories_fetch=driver.find_element_by_xpath(Xpath_Friends_categories)
                # Find how many categories are available
                Tabs=Xpath_Friends_categories_fetch.find_elements_by_css_selector("a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.pq6dq46d.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.dwo3fsh8.ow4ym5g4.auili1gw.mf7ej076.gmql0nx0.tkr6xdv7.bzsjyuwj.cb02d2ww.j1lvzwm4")
                # Iterover the categories 
                for tab_index, tab in enumerate(Tabs):
                    #Create an Xpath for each category
                    N_Xpath_Friends_categories=Xpath_Friends_categories+"/a["+str(tab_index+1)+"]"
                    category_name=driver.find_element_by_xpath(N_Xpath_Friends_categories)
                    # Print category name
                    #print(category_name.text)
                    f.writelines("\n" + category_name.text + "\n")
                    # Click on it
                    category_name.click()
                    #scroll down to fetch ll the friends
                    scroll()
                    # Finds the HTML portions containing friends' names using xPath
                    friendlist = driver.find_elements_by_xpath('//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]//a[@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"]')
                    # Finds the HTML portions containing friends' displayed info using xPath
                    categories = driver.find_elements_by_xpath('//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]//div[@class="aahdfvyu"]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb mdeji52x e9vueds3 j5wam9gi knj5qynh m9osqain"]')
                    # Finds the HTML portions containing friends' profile URLs using xPath
                    links = driver.find_elements_by_xpath('//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]//a[@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"]')
                    for (tab1, tab2, tab3) in zip(friendlist, categories, links):
                        #print(tab1.text + ", " + tab2.text + ", " + tab3.get_attribute("href"))
                        f.writelines("\n" + tab1.text + ", " + tab2.text + ", " + tab3.get_attribute("href") + "\n")
                    time.sleep(3)
                    #Refresh the page to access to the original elements. 
                    driver.refresh()
                    time.sleep(3)
        # If ID does not load a user's profile
        except NoSuchElementException:
            ##print("NaN")
            f.writelines("NaN")