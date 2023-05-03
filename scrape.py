from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from fake_useragent import UserAgent
from typing import Optional
from bs4 import BeautifulSoup
import csv
from time import sleep

class Config():
    def __init__(self, headless:bool=False, experimental_features:Optional[dict]={}) -> None:
        # web driver configuration
        # self.ua = UserAgent()
        # self.userAgent = self.ua.random
        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.headless = headless
        self.chrome_options.add_experimental_option("prefs", experimental_features)
        # self.chrome_options.add_argument(f'user-agent={self.userAgent}')

    def driver(self):
        driver_ = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        return driver_

    
class Instagram_scrape():
    'class to login and scrape instagram account for captions and alt-text'
    def __init__(self, driver, account:str, username:str, password:str) -> None:
        self.driver = driver
        self.account = account
        self.username = username
        self.password = password
        
    def login(self):
        'class method to login to user account'
        self.driver.get('http://instagram.com')
        #target username
        username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))

        # accept_all = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All")]'))).click()
       
        #enter username and password
        username_field.clear()
        username_field.send_keys(self.username)
        password_field.clear()
        password_field.send_keys(self.password)

        #target the login button and click it
        button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mount_0_0_l1"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'))).click()
        # not_now2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    
    def scrape_followers(self):
        'class method to scrape video, captions and alt-text of a user'
        url = f'https://www.instagram.com/{self.account}/'
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        sleep(30)
        # post_links = []
        # for link in driver.find_elements_by_tag_name('a'):
        #     if "/p/" in link.get_attribute('href'):
        #         post_links.append(link.get_attribute('href'))

        # with open(f'{account}_captions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['Caption', 'Post URL'])

        #     for post_link in post_links:
        #         driver.get(post_link)
        #         soup = BeautifulSoup(driver.page_source, 'html.parser')

        #         caption = soup.find('div', {'class': 'C4VMK'}).span.text
        #         writer.writerow([caption, post_link])

        # driver.quit()
        
config = Config(headless=False)
driver = config.driver()
scraper = Instagram_scrape(driver, 'oyewunmio', 'oyewunmio', 'whatsapp19')
scraper.login()
scraper.scrape_followers()

