import re
import urllib.parse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
            return driver
        except WebDriverException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2)

def get_top_non_sponsored_products(product_name, num_products=1, max_retries=3):
    driver = None
    for attempt in range(max_retries):
        try:
            driver = setup_driver()
            search_url = f"https://www.amazon.in/s?{urllib.parse.urlencode({'k': product_name})}"
            driver.get(search_url)
            
            # Wait for either products or captcha
            wait = WebDriverWait(driver, 20)
            try:
                wait.until(lambda d: 
                    len(d.find_elements(By.CSS_SELECTOR, "div.s-result-item")) > 0 or
                    len(d.find_elements(By.ID, "captchacharacters")) > 0
                )
            except TimeoutException:
                if attempt < max_retries - 1:
                    continue
                else:
                    raise

            # Check for captcha
            if len(driver.find_elements(By.ID, "captchacharacters")) > 0:
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait before retry
                    continue
                else:
                    raise Exception("Captcha detected after maximum retries")

            product_urls = []
            products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
            
            for product in products:
                if len(product_urls) >= num_products:
                    break
                    
                try:
                    # Skip sponsored products
                    sponsored_selectors = [
                        "span.s-label-popover-default",
                        "span.puis-label-popover-default",
                        "span[data-component-type='s-sponsored-label-info-icon']"
                    ]
                    
                    sponsored = any(
                        bool(product.find_elements(By.CSS_SELECTOR, selector)) 
                        for selector in sponsored_selectors
                    )
                    
                    if sponsored:
                        continue

                    # Get product URL
                    url_elements = product.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")
                    if not url_elements:
                        continue
                        
                    url = url_elements[0].get_attribute("href")
                    if url and url.startswith("https://www.amazon.in") and ("/dp/" in url or "/gp/product/" in url):
                        product_urls.append(url)
                        
                except (NoSuchElementException, StaleElementReferenceException):
                    continue

            if product_urls:
                return product_urls
                
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
                continue
            else:
                raise Exception("No valid products found after maximum retries")
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2)
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    return []

def scrape_amazon_product(url, max_retries=3):
    driver = None
    for attempt in range(max_retries):
        try:
            driver = setup_driver()
            driver.get(url)
            
            wait = WebDriverWait(driver, 20)
            
            # Check for captcha
            if len(driver.find_elements(By.ID, "captchacharacters")) > 0:
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                raise Exception("Captcha detected")
            
            # Get product name
            name = wait.until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            ).text.strip()
            
            # Get features
            try:
                feature_bullets = wait.until(
                    EC.presence_of_element_located((By.ID, "feature-bullets"))
                )
                features = [li.text.strip() for li in feature_bullets.find_elements(By.TAG_NAME, "li")
                          if li.text.strip() and not li.get_attribute("class")]
            except (TimeoutException, NoSuchElementException):
                features = []
            
            return name, features
            
        except Exception as e:
            if attempt == max_retries - 1:
                return '', []
            time.sleep(2)
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    return '', []