from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import os
import time
import configparser
import pandas as pd
import random


class InstagramBot:

    def __init__(self, username, password):
        """
        Initializes an instance of the InstagramBot class.

        Args:
            username (str): Instagram username for a user
            password (str): Instagram password for a user

        Attributes:
            base_url (str): Instagram's base url
            driver (Selenium.webdriver.Chrome): Chromedriver used to automate browser actions

        """

        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com/'


        self.driver = webdriver.Chrome('./chromedriver.exe')


    def login(self):
        """
        Log into the Instagram account using the username and password provided.

        """
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

        # wait for the not now button (turn on notification)
        self.driver.implicitly_wait(5)

        not_now_button = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        not_now_button.click()


    def nav_user(self, user):
        """
        Navigate to the provided user's page.

        Args:
            user (str): The username of the user to be navigated to

        """
        self.driver.get(self.base_url + user)
        self.driver.implicitly_wait(5)


    def follow_user_action(self, user=None, unfollow=False):
        """
        Follows or unfollow user.
        If user is not provided, will try to follow the first person available on the current page

        Args:
            user (str): The username of the user to be followed/unfollowed
            unfollow (bool): Boolean whether to unfollow or not
        """

        if user is not None:
            self.nav_user(user)

        # self.driver.implicitly_wait(5)
        # time.sleep(5)

        # 3 buttons in user page
        # 1. Follow button
        # 2. Arrow down button
        # 3. 3 dots button
        button_list = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
        button_list[0].click()

        # 2 buttons
        # 1. Unfollow button
        # 2. Cancel button
        # if length is 0, not followed before
        unfollow_button_list = self.driver.find_elements_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW')

        if len(unfollow_button_list) != 0:
            if unfollow:
                unfollow_button_list[0].click()
            else:
                unfollow_button_list[1].click()


    def click_like(self):
        """
        Clicks the like button on the current page/post.
        Returns True if post already liked before, False otherwise.

        """

        like_button = self.driver.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > svg[aria-label="Like"]')
        url = self.driver.current_url
        if len(like_button) != 0:
            like_button[0].click()
            print(url + ' liked!')
            return False
        else:
            print(url + ' already liked!')
            return True



    def is_private(self, user):
        """
        Returns True if the user provided is a private account, False otherwise.

        Args:
            user (str): The username of the user to check if private account or not

        """
        self.nav_user(user)
        private_h2 = self.driver.find_elements_by_css_selector('#react-root > section > main > div > div.Nd_Rl._2z6nI > article > div._4Kbb_ > div > h2[class="rkEop"]')
        if len(private_h2) == 0:
            print(user + " not private")
            return False
        print(user + " is private!")
        return True


    def creepy_like(self, user):
        """
        Likes the oldest post of a user.

        Args:
            user (str): The username of the user to have their oldest post liked
        """
        self.nav_user(user)
        self.driver.implicitly_wait(5)

        self.scroll_to_bottom()
        img_list = self.driver.find_elements_by_class_name('_9AhH0')

        if len(img_list) != 0:
            img_list[-1].click()

        self.click_like()


    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of a page.

        """
        SCROLL_PAUSE_TIME = 1.75

        # Get scroll height
        last_height = self.driver.execute_script('return document.body.scrollHeight')

        while True:

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height


    def nav_tag(self, tag):
        """
        Navigates to the given tag.

        Args:
            tag (str): The tag to be navigated to

        """
        self.driver.get(self.base_url + 'explore/tags/' + str(tag) + '/')

        # self.like_and_comment(5)

        
    def follow_like_and_comment(self, num=10):
        """
        Follow the poster, likes and comments a number of posts on the current page starting from the first post.
        Saves the url of the posts liked and commented. And also the username of the poster.
        Used in a hashtag page. (Use nav_tag first before this function)

        Args:
            num (int): The number of posts to like and comment

        """
        old_df = pd.DataFrame(columns=['url', 'username'])

        try:
            old_df = pd.read_csv('data.csv', delimiter=',').iloc[:, 1:3]
        except:
            print('csv file is empty')

        url_list = list(old_df['url'])
        username_list = list(old_df['username'])

        img_list = self.driver.find_elements_by_class_name('_9AhH0')

        # click first picture
        if len(img_list) != 0:
            img_list[0].click()

        self.driver.implicitly_wait(5)

        for i in range(num):
            current_url = self.driver.current_url

            if current_url not in url_list:
                print('NEVER BEFORE')
                url_list.append(self.driver.current_url)

                time.sleep(random.randint(3,7))

                self.driver.implicitly_wait(5)

                current_user = self.driver.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > a')[0].text
                username_list.append(current_user)

                follow_button = self.driver.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > header > div.o-MQd.z8cbW > div.PQo_0.RqtMr > div.bY2yH > button')[0]
                print(follow_button.text)
                if follow_button.text != 'Following':
                    follow_button.click()
                    print(current_user + ' followed!')
                else:
                    print(current_user + ' already followed!')

                time.sleep(random.randint(5, 10))

                # if already liked, no need to comment (assumes post has been commented before)
                liked_before = self.click_like()
                if not liked_before:
                    time.sleep(random.randint(8, 15))
                    self.comment_photo()
            else:
                print('FOUND BEFORE')

            next_button = self.driver.find_elements_by_xpath('//a[contains(text(), "Next")]')
            if len(next_button) != 0:
                time.sleep(3)
                next_button[0].click()

        new_df = pd.DataFrame(list(zip(url_list, username_list)), columns=['url', 'username'])
        new_df.to_csv('data.csv')


    def like_photos(self, user=None, num=10):
        """
        Likes a number of photos on a user's page or a hashtag's page.

        Args:
            user (str): The user to be given the likes to
            num (int): The number of posts to be liked
        """

        # like button class name = wpO6b
        # image button class name = _9AhH0
        if user is not None:
            self.nav_user(user)
        self.driver.implicitly_wait(5)

        # post_span = self.driver.find_elements_by_css_selector('#react-root > section > main > div > header > section > ul > li:nth-child(1) > span > span')
        # post_num = int(post_span[0].text)
        # post_num = 10
        
        img_list = self.driver.find_elements_by_class_name('_9AhH0')

        # click first picture
        if len(img_list) != 0:
            img_list[0].click()

        self.driver.implicitly_wait(5)

        for i in range(num):
            time.sleep(3)

            self.click_like()

            next_button = self.driver.find_elements_by_xpath('//a[contains(text(), "Next")]')
            if len(next_button) != 0:
                next_button[0].click()


    def comment_photo(self):
        """
        Posts a comment under a post.
        Has to be on the post's page already.

        """
        comment_num = random.randint(0, 10)
        self.driver.implicitly_wait(5)
        comment_button = self.driver.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button > svg')
        if len(comment_button) != 0:
            comment_button[0].click()
            time.sleep(random.randint(1, 3))
        comment_box = self.driver.find_elements_by_css_selector('body > div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea[class="Ypffh focus-visible"]')
        if len(comment_box) != 0: 
            comment_list = [
                'Really cool!', 
                'Nice work :)', 
                'Good shot!', 
                'Very amazing!', 
                'Definitely one of the best!',
                'I love it!',
                'It\'s so good!',
                'Great shot!']
            comment = random.choice(comment_list)
            comment_box[0].send_keys(comment)
            time.sleep(random.randint(1, 3))
            comment_box[0].send_keys(Keys.ENTER)
            print('Commented with: ' + comment)


# Main
if __name__ == '__main__':
    

    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)

    username = cparser.get('AUTH', 'USERNAME')
    password = cparser.get('AUTH', 'PASSWORD')

    hashtags = ['pcgaming', 'gaming', 'travelgram', 'cool', 'awesome']

    ig_bot = InstagramBot(username, password)

    ig_bot.login()

    for hashtag in hashtags:
        ig_bot.nav_tag(hashtag)
        ig_bot.follow_like_and_comment(10)


    print('done!')







