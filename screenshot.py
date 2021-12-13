from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def screen(url):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  driver.get_screenshot_as_file('ss.png')

  