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

    print(f'Search url : {search_url}')

    wait = WebDriverWait(driver, 10)
    search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-component-type="s-search-result"]')))
    for result in search_results:
        sponsored_element = result.find_elements(By.CSS_SELECTOR, '[data-component-type="sp-sponsored-result"]')
        if not sponsored_element:
            product_link = result.find_element(By.CSS_SELECTOR, 'h2 a')
            product_url = product_link.get_attribute('href')

            print(f'Product url: {product_url}')

            driver.quit()
            return product_url
    driver.quit()
    raise("Couldn't find the link to a non-sponsored Amazon product")

def get_top_non_sponsored_products(product_name, num_products=1):
    driver = setup_driver()
    search_url = f"https://www.amazon.in/s?{urllib.parse.urlencode({'k': product_name})}"
    
    driver.get(search_url)
    
    product_urls = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item"))
        )
        
        products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
        
        for product in products:
            if len(product_urls) >= num_products:
                break
            
            # Check for sponsored label in multiple possible locations
            sponsored = False
            sponsored_selectors = [
                "span.s-label-popover-default",
                "span.puis-label-popover-default",
                "span[data-component-type='s-sponsored-label-info-icon']"
            ]
            
            for selector in sponsored_selectors:
                try:
                    sponsored_element = product.find_element(By.CSS_SELECTOR, selector)
                    if sponsored_element.is_displayed() and re.search(r'sponsor', sponsored_element.get_attribute('innerHTML'), re.IGNORECASE):
                        sponsored = True
                        break
                except:
                    pass
            
            if sponsored:
                continue
            
            try:
                url_element = product.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")
                url = url_element.get_attribute("href")
                if url and url.startswith("https://www.amazon.in"):
                    # Additional check to filter out non-product pages
                    if "/dp/" in url or "/gp/product/" in url:
                        product_urls.append(url)
            except:
                continue
    
    finally:
        driver.quit()
    
    return product_urls


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
