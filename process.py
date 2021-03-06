from selenium import webdriver
from selenium_process import _get_all_product, _create_preview_mockup, _check_store_price, _check_information_product

def get_all_product(): 
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1920, 1080)
    products = _get_all_product(driver)
    driver.quit()
    return products

def preview_mockup(sku, sides):
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1920, 1080)
    images = _create_preview_mockup(driver, sku, sides)
    driver.quit()
    return images

def check_store_price_process(testcase): 
    product_sku = testcase['product']
    prices = testcase['prices']
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1920, 1080)
    result = _check_store_price(driver, product_sku, prices)
    driver.quit()
    return result

def check_information_product_process(testcase):
    product_sku = testcase['product']
    infos = testcase['infos']
    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_size(1920, 1080)
    result = _check_information_product(driver, product_sku, infos)
    driver.quit()
    return result