from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def tracker(url, alert):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser') 
  title = soup.find(id = "title").get_text();
  price = soup.find(id = "priceblock_ourprice").get_text();

  price = float(((price.strip()).replace(",","")).replace("₹",""))
  if alert == -1.0:
    alert = price
  data = {
        "name": title.strip(),
        "current": price,
        "alert": alert,
        "is_Sale": (price<alert),
        "url": url
  }
  return data