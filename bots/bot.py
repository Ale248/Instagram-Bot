from selenium import webdriver
import os
import time
import configparser

class InstagramBot:

    def __init__(self, username, password):
        """
        Initializes an instance of the InstagramBot class.
        Calls the login method to log into Instagram.

        Args:
            username:str: Instagram username for a user
            password:str: Instagram password for a user

        Attributes:
            driver:Selenium.webdriver.Chrome: Chromedriver used to automate browser actions

        """

        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com/'


        self.driver = webdriver.Chrome('./chromedriver.exe')


        self.login()


    def login(self):
        self.driver.get(self.base_url + 'accounts/login/')

        # has to wait because if no wait, it search first before load and wont found
        self.driver.implicitly_wait(2)

        # find the text-boxes and login button
        username_box = self.driver.find_element_by_name('username')
        password_box = self.driver.find_element_by_name('password')
        login_button = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button')

        # fill the text-boxes
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)

        # click login
        login_button.click()

        # wait for the not now button
        self.driver.implicitly_wait(2)

        not_now_button = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        not_now_button.click()

    def nav_user(self, user):
        self.driver.get(self.base_url + user)

    def follow_user_action(self, user, unfollow=False):
        
        self.nav_user(user)

        # self.driver.implicitly_wait(5)
        # time.sleep(5)

        # 3 buttons in user page
        # 1. Follow button
        # 2. Arrow down button
        # 3. 3 dots button
        # button_list = self.driver.find_elements_by_tag_name('button')

        button_list = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
        button_list[0].click()

        # 2 buttons
        # 1. Unfollow button
        # 2. Cancel button
        # if length is 0, not followed before
        unfollow_button_list = self.driver.find_elements_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW')
        # print(len(unfollow_button_list))

        if len(unfollow_button_list) != 0:
            if unfollow:
                unfollow_button_list[0].click()
            else:
                unfollow_button_list[1].click()

        
        
        
        # if unfollow:
        #     button_list[0].click()
        #     unfollow_button = self.driver.find_element_by_xpath


        # cancel_button = self.driver.find_elements_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        # if len(cancel_button) != 0:
        #     cancel_button[0].click()

        # print(len(cancel_button))


    def like_photos(self, user):

        self.nav_user(user)

        
    
if __name__ == '__main__':
    

    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)

    username = cparser.get('AUTH', 'USERNAME')
    password = cparser.get('AUTH', 'PASSWORD')
    # print(cparser.get('AUTH', 'USERNAME'))

    ig_bot = InstagramBot(username, password)


    ig_bot.follow_user_action('xqcow1')

