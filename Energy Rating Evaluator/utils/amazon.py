import urllib.parse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def setup_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def get_relevant_amazon_result(product_name):
    driver = setup_driver()
    search_url = f"https://www.amazon.in/s?{urllib.parse.urlencode({'k': product_name})}"
    driver.get(search_url)
    wait = WebDriverWait(driver, 10)
    search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-component-type="s-search-result"]')))
    for result in search_results:
        sponsored_element = result.find_elements(By.CSS_SELECTOR, '[data-component-type="sp-sponsored-result"]')
        if not sponsored_element:
            product_link = result.find_element(By.CSS_SELECTOR, 'h2 a')
            product_url = product_link.get_attribute('href')
            driver.quit()
            return product_url
    driver.quit()
    raise("Couldn't find the link to a non-sponsored Amazon product")

def scrape_amazon_product(url):
    driver = setup_driver()
    driver.get(url)
    try:
        feature_bullets = wait_for_element(driver, By.ID, "feature-bullets")
        name = wait_for_element(driver, By.ID, "productTitle").text.strip()
        features = [li.text for li in feature_bullets.find_elements(By.TAG_NAME, "li")]
    except (NoSuchElementException, TimeoutException):
        features = []
        name = ''
    return name, features
