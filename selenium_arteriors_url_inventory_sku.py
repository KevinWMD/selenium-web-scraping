from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Function to initialize the WebDriver (e.g., Chrome)
def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

# Function to extract URLs from a given page
def extract_urls(driver, page_number, base_url):
    driver.get(f"{base_url}?Page={page_number}")
    div_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.klevuImgWrap"))
    )
    urls = []
    for div_element in div_elements:
        try:
            link_element = div_element.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            if href not in urls:
                urls.append(href)
        except Exception as e:
            print(f"Error processing a div element: {e}")
    return urls

# Function to extract SKU and inventory from a product page
def extract_product_details(driver, product_url):
    driver.get(product_url)
    try:
        sku_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pro-sku"))  # Update the CSS selector based on the actual element
        )
        sku = sku_element.text

        inventory_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#availability_stocks .data"))
        )
        inventory = inventory_element.text
    except Exception as e:
        print(f"Error extracting product details: {e}")
        sku = None
        inventory = None
    
    return sku, inventory

# Main function to run the script
def main():
    base_url = "https://www.arteriorshome.com/shop/outdoor"
    max_pages = 2  # Define the maximum number of pages to crawl
    output = {'url': [], 'sku': [], 'inventory': []}
    output_csv_name = "arteriors_url_outdoor_sku_inventory.csv"
    
    driver = initialize_driver()
    try:
        all_urls = []
        for i in range(1, max_pages + 1):
            print(f"Processing page {i}")
            urls = extract_urls(driver, i, base_url)
            all_urls.extend(urls)
            time.sleep(2)  # Adjust the sleep time as needed

        for url in all_urls:
            sku, inventory = extract_product_details(driver, url)
            output['url'].append(url)
            output['sku'].append(sku)
            output['inventory'].append(inventory)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    output_df = pd.DataFrame(output)
    output_df.to_csv(output_csv_name, index=False)
    print(f'Crawling completed. Product details saved to {output_csv_name}')

if __name__ == "__main__":
    main()
