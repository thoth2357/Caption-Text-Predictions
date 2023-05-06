from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions as se
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
        driver_ = webdriver.Chrome('chromedriver.exe')
        return driver_

class infine_scroll(object):
  def __init__(self, last):
    self.last = last

  def __call__(self, driver):
    new = driver.execute_script('return document.body.scrollHeight')
    if new > self.last:
        return new
    else:
        return False
    
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
        try:
            save_info = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mount_0_0_NP"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'))).click()
        except Exception:
            print('we faced the same thing')
        # not_now2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    
    def scrape_followers(self):
        'class method to scrape video, captions and alt-text of a user'
        url = f'https://www.instagram.com/{self.account}/'
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        sleep(10)
        height = self.driver.execute_script("return document.body.scrollHeight")
        flag=1
        while flag == 1:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            try:    
                wait = WebDriverWait(self.driver, 4)
                new_height = wait.until(infine_scroll(height))
                height = new_height
            except Exception:
                flag = 0
    
        posts = driver.find_elements(By.CSS_SELECTOR, 'div._aagv > img')
        print(len(posts))
        # Open a CSV file in write mode
        with open('instagram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write column headers
            writer.writerow(['Account', 'Post Alt Text', 'Post Source', 'Post Captions'])
            for post in posts:
                driver.execute_script("arguments[0].click();", post)
                driver.implicitly_wait(5)
                try:
                    post_alt_text = post.get_attribute('alt')
                    post_src = post.get_attribute('src')
                    post_captions = driver.find_element(By.XPATH, '//h1[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')
                    post_captions_text = post_captions.text 
                except se.NoSuchElementException:
                    post_captions_text = ''
                # Write the scraped data to the CSV file
                writer.writerow([self.account, post_alt_text, post_src, post_captions_text])
                # Go back to the account page
                self.driver.back()


config = Config(headless=False)
driver = config.driver()
scraper = Instagram_scrape(driver, 'oyewunmio', 'oyewunmio', 'whatsapp19')
scraper.login()
scraper.scrape_followers()


