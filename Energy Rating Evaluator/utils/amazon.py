from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

def setup_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def get_first_google_result(product_name):
    driver = setup_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{product_name} amazon")
    search_box.send_keys(Keys.RETURN)
    first_result = wait_for_element(driver, By.CSS_SELECTOR, "h3")
    first_link = first_result.find_element(By.XPATH, "..").get_attribute("href")
    return first_link

def scrape_amazon_product(url):
    driver = setup_driver()
    driver.get(url)
    try:
        feature_bullets = wait_for_element(driver, By.ID, "feature-bullets")
        features = [li.text for li in feature_bullets.find_elements(By.TAG_NAME, "li")]
    except (NoSuchElementException, TimeoutException):
        features = []
    return features
