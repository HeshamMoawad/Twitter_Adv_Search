from time import sleep
#from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from typing import List
import re



class Twitter():
    WA_REGEX = r"(https?:\/\/)?chat\.whatsapp\.com\/(?:invite\/)?([a-zA-Z0-9_-]{22})"
    TYPE_TOP = ""
    TYPE_LATEST = "&f=live"
    TYPE_PHOTO = "&f=image"
    TYPE_VEDIO = "&f=video"
    SCROLL_TO_LAST_HIGHT = "window.scrollTo(0,document.body.scrollHeight);return document.body.scrollHeight;"
    SCROLL_TO = f"window.scrollTo(0,hight);return hight"
    SCROLL_TO_BOTTOM = "window.scrollTo(0,0);return 0;"
    CLICK_SHOW_BUTTON = """var btn = document.querySelectorAll("div[class='css-1dbjc4n r-1ndi9ce'] div div span span");btn[1].click();"""
    CLICK_SHOW_BUTTON_0 = """var btn = document.querySelectorAll("div[class='css-1dbjc4n r-1ndi9ce'] div div span span");btn[0].click();"""
    HANDLES_AND_NAMES_CODE = """var handles = document.querySelectorAll("div[class='css-1dbjc4n r-1wbh5a2 r-dnmrzs']");return handles;"""
    GET_CURRENT_LOCATION = """return window.pageYOffset;"""
    MAX_HIGHT = "return document.body.scrollHeight;"
    SHOW_MORE_REPLY = """var btn = document.querySelectorAll('div[role="button"] div[class="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1777fci"]');btn[0].click();"""
    
    
    GET_TWEETS = """tweets = document.querySelectorAll("article[data-testid='tweet']");return tweets;"""
    # GET_TWEETS = """return document.querySelectorAll("article[data-testid='tweet']");"""

    GET_ID = """return tweets[index].querySelector("div > div > div > div div.css-1dbjc4n.r-18u37iz.r-1q142lx > a").getAttribute("href");"""
    GET_HANDLE = """return tweets[index].querySelector("div.css-1dbjc4n.r-1wbh5a2.r-dnmrzs > a > div > span").textContent;"""
    GET_DESC = """return tweets[index].querySelector("div[data-testid='tweetText']").textContent;"""

    def __init__(self,headless) -> None:
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.driver.maximize_window()
        self.driver.get("https://twitter.com/i/flow/login")

    
    def wait_elm(
        self,
        val:str,
        by:str=By.XPATH,
        timeout:int=30 , 
        )->WebElement:
        
        """ waiting element """
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        return self.wait.until(EC.presence_of_element_located((by,val)))



    def wait_elms(
        self,
        val:str,
        by:str=By.XPATH,
        timeout:int=30,
        )->List[WebElement]:
        
        """ waiting elements """
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        return self.wait.until(EC.presence_of_all_elements_located((by,val)))



    def Login(
        self,
        user_:str,
        pwd_:str,
        ):
        self.user_ = user_

        user = self.wait_elm(val="//*[@autocomplete='username']" ,timeout=20)
        user.send_keys(user_)
        self.wait_elm(val="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span",timeout=5).click()      # Next Button 
        try:
            pwd = self.wait_elm(val="//*[@autocomplete='current-password']",timeout=20)
            pwd.send_keys(pwd_)
            sleep(2)
            self.wait_elm(val="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span" , timeout=5).click()    # login Button
        except Exception as e:
            print("error")
            self.wait_elm(val="//*[@aria-label='Tweet']", timeout=3)
            print("user name is not correct ")
        self.wait_elm("/html/body/div[1]/div/div/div[2]/header/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div[4]/div",timeout=5)
    
        

    def move(self,element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def get_acc_info_selen(self)->list:
        username_at = self.wait_elm(val="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/span",timeout=3).text
        username = self.wait_elm(val="/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[1]/span",timeout=5).text
        followers = self.clean_follow(self.wait_elm(val="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span",timeout=5).text)
        bio = self.wait_elm(val="//*[@data-testid='UserDescription']",timeout=5).text
        try:
            self.wait_elm(val="//*[@aria-label='Message']",timeout=5)
            message = True
        except:
            message = False
        following = self.clean_follow(self.wait_elm(val="/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",timeout=5).text)
        return [username,username_at,followers,bio,message,following]



    @staticmethod
    def clean_follow(followers:str)->int:
        print(followers)
        if  "K" in followers or "k" in followers:
            return int(round(float(followers.replace("K","").replace("k","")),2)*1000)
        elif "M" in followers or "m" in followers :
            return int(round(float(followers.replace("M","").replace("m","")),2)*1000000)
        else:
            return int(round(float(followers),2))


    def scrape_replys(self,url:str)->list:
        self.driver.get(f"{url}")
        self.scroll_to_maxhight()
        self.wait_elms("//div[@data-testid='cellInnerDiv']")
        self.jscode(self.CLICK_SHOW_BUTTON)
        print("show button pressed ... ")
        handles_list = []
        current_loc = self.jscode(self.SCROLL_TO_BOTTOM)
        max_loc = self.jscode(self.MAX_HIGHT)
        while current_loc < max_loc:
            print(f"Current location = {current_loc} \t Max hight = {max_loc}")
            handles = self.jscode(self.HANDLES_AND_NAMES_CODE)
            for handle in handles:
                try:
                    print(f"handle is ( {handles[handles.index(handle)-1].text},{handle.text} )")
                    if handle.text != '' and "@" in handle.text :
                        handles_list.append((handles[handles.index(handle)-1].text,handle.text))
                except:
                    print("none ...")
                    pass
            current_loc = self.jscode(self.SCROLL_TO.replace("hight",f"{self.jscode(self.GET_CURRENT_LOCATION) + 2000}"))
            max_loc = self.jscode(self.MAX_HIGHT)
        handles_list = [*set(handles_list)]
        return handles_list



    def scroll_to_maxhight(self):
        while True:
            page_old = self.driver.page_source
            sleep(1)
            self.jscode(self.SCROLL_TO_LAST_HIGHT)
            if page_old == self.driver.page_source :
                break
            print(f"scrolled")
        print("ended")



    def jscode(self,code):
        return self.driver.execute_script(code)



    def scrape_followers(self,url,limit)->list:
        self.driver.get(url)
        handles_list = []
        current_loc = self.jscode(self.SCROLL_TO_BOTTOM)
        max_loc = self.jscode(self.MAX_HIGHT)
        while current_loc < max_loc and len(handles_list) < limit:
            print(f"Current location = {current_loc} \t Max hight = {max_loc}")
            self.wait_elms("//div[@data-testid='cellInnerDiv']")
            handles = self.jscode(self.HANDLES_AND_NAMES_CODE)
            print("before for loop ---")
            for handle in handles:#range(2,len(handles),3)
                try:
                    user_handle = handle.text
                    if user_handle != "" and "@" in user_handle :
                        username = handles[handles.index(handle)-1].text
                        if handles.count((username,user_handle)) == 0: 
                            handles_list.append((username,user_handle))
                            print(f"handle is {user_handle} user is {username}")
                except:
                    print("none")
                    pass
            current_loc = self.jscode(self.SCROLL_TO.replace("hight",f"{self.jscode(self.GET_CURRENT_LOCATION) + 1200}"))
            max_loc = self.jscode(self.MAX_HIGHT)
            handles_list = [*set(handles_list)]
        return handles_list

    def search(self,keyword,type):
        self.driver.get(f"https://twitter.com/search?q=chat.whatsapp.com {keyword}&src=typed_query{type}")

##############################
        current_loc = self.jscode(self.SCROLL_TO_BOTTOM)
        max_loc = self.jscode(self.MAX_HIGHT)
        while current_loc < max_loc:
            print(f"Current location = {current_loc} \t Max hight = {max_loc}")
            self.wait_elms("//div[@data-testid='cellInnerDiv']")
            tweets = self.jscode(self.GET_TWEETS)
            print("before for loop ---")
            print(tweets)
            for index in range(len(tweets)):
                id = self.jscode(self.GET_ID.replace("index",f"{index}")).split("/status/")[-1]
                handle = self.jscode(self.GET_HANDLE.replace("index",f"{index}"))
                desc = self.jscode(self.GET_DESC.replace("index",f"{index}"))
                try:
                    link = re.search(self.WA_REGEX,desc).group()
                    print([id,handle,desc,link])
                except Exception as e :
                    print(e)
                    print([id,handle,desc])
            sleep(5)
            current_loc = self.jscode(self.SCROLL_TO.replace("hight",f"{self.jscode(self.GET_CURRENT_LOCATION) + 1200}"))
            max_loc = self.jscode(self.MAX_HIGHT)


##############################



    def exit(self):
        try:
            self.wait_elm("//*[@id='react-root']/div/div/div[2]/header/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div[4]/div",timeout=5).click()
            self.wait_elm("//*[@id='layers']/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]/div[1]/div/span",timeout=5).click()
            self.wait_elm("//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div",timeout=5).click()
        except:
            pass
        sleep(2)
        self.driver.quit()
        


t = Twitter(False)
t.search("تاسى",t.TYPE_TOP)



# textex = ".\n#شاهد\n\n مقطع قصير\n\n| الحبيب علي الجفري |  صيام عرفة يغفر كل ذنب إلا هذا النوع من الذنوب |\n\n#الحج #يوم_عرفة #مكة_المكرمة #dmc #مساءdmc\n\nhttps://fb.watch/e2Tf8eh5ES/\nوتس\nhttps://chat.whatsapp.com/EgclmZAgmlO9UYAJYI4zI4"
# x = re.search(Twitter.WA_REGEX,textex)
# print(x.group())
# print(Twitter.clean_follow("1M"))


# twitter = Twitter(True)

# twitter.driver.get("https://twitter.com/fahadmutadawul/status/1581291201076297730")


# sleep(5)
# twitter.jscode(twitter.SCROLL_TO_LAST_HIGHT)
# sleep(2)
# twitter.jscode(twitter.SCROLL_TO_LAST_HIGHT)
# print("scrolled")

# twitter.jscode(twitter.CLICK_SHOW_BUTTON)

# print("show button pressed ... \n")

# twitter.jscode(twitter.SCROLL_TO_LAST_HIGHT)
# twitter.jscode(twitter.SCROLL_TO_LAST_HIGHT)


# handles_list = []

# current_loc = twitter.jscode(twitter.SCROLL_TO_BOTTOM)

# max_loc = twitter.jscode(twitter.MAX_HIGHT)

# while current_loc < max_loc:
#     print(f"Current location = {current_loc} \t Max hight = {max_loc}")
#     handles = twitter.jscode(twitter.HANDLES_AND_NAMES_CODE)
#     for handle in handles:
#         try:
#             if handle.text != '' and "@" in handle.text :
#                 print(f"handle is ( {handle.text} )")
#                 handles_list.append(handle.text)
#         except:
#             print("none ...")
#     current_loc = twitter.jscode(twitter.SCROLL_TO.replace("hight",f"{twitter.jscode(twitter.GET_CURRENT_LOCATION) + 1000}"))
#     max_loc = twitter.jscode(twitter.MAX_HIGHT)

# handles_list = [*set(handles_list)]
# print(handles_list)
# twitter.Login("advisorfahd","@hmed23688546")



# handles = twitter.scrape_followers("https://twitter.com/fahadmutadawul/followers",50)

# twitter.exit()
# 
# print("done")
# sleep(50)