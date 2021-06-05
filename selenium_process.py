from utils import get_url, get_auth
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import COLORS
import urllib.request 
import re 

def login(driver):
    login_link = get_url('/login')
    driver.get(login_link)
    elem = driver.find_element_by_id("PolarisTextField1")
    email, password = get_auth()
    elem.send_keys(email)
    elem1 = driver.find_element_by_id("PolarisTextField2")
    elem1.send_keys(password)
    elem1 = driver.find_element_by_class_name("Polaris-Button__Text")
    elem1.click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn-create-product"))
    )

def parse_product_element(element):
    sku = element.find_element_by_class_name('product-sku').text
    name = element.find_element_by_class_name("card-meta-product-name").text 
    image = element.find_element_by_class_name('product-image-container').find_element_by_tag_name("img").get_attribute("src")
    return {"name": name, "sku": sku, "image": image}

def append_side_product(driver, product):
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "btn-create-{}".format(product['sku'].lower())))
    )
    element.click()
    time.sleep(2)
    side_elements = driver.find_elements_by_class_name('choose-side-btn')
    side_elements = side_elements[:int((len(side_elements)/2))]
    sides = []
    for side_element in side_elements: 
       side_text = side_element.text
       sides.append(side_text)
    product['sides'] = sides
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/button').click()

def _get_all_product(driver, pass_skus=None):
    login(driver)
    products = []
    new_product_link = get_url('/u/products/new')
    driver.get(new_product_link)
    product_elements = driver.find_elements_by_class_name('ant-list-item')
    for product_element in product_elements:
        product = parse_product_element(product_element)
        products.append(product)
    if pass_skus:
        products = [x for x in products if x.sku not in pass_skus]    
    for product in products:
        append_side_product(driver, product)
    return products

def _create_preview_mockup(driver, sku, sides):
    preview_mockup_urls = []
    #TODO: dung selenium de tao preview mockup tu sku va sides
    login(driver)
    new_product_link = get_url('/u/products/new')
    driver.get(new_product_link)
    element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "btn-create-{}".format(sku.lower())))
        )
    ele1 = driver.find_element_by_id("btn-create-{}".format(sku.lower())).click()
    time.sleep(1)
    for key in sides: 
        id= "tab-side-{}".format(key.lower().replace(" ", "-"))
        ele = driver.find_element_by_id(id).click()
        color = COLORS[sides[key]['color']]
        element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'btn-color-{}'.format(color.lower())))
        ).click()
        if sides[key]['artwork']:
            ele = driver.find_element_by_id("btn-new-artwork").click()
            time.sleep(1)
            # driver.find_element_by_xpath("//div[@class='image-container']//img[@src='https://printholo.storage.googleapis.com/default_artworks/thumbnails/Front_1604031195402_Afd622cb55.png']").click()
            eles = driver.find_elements_by_class_name("image-container")
            for ele in eles:  
                    src = ele.find_element_by_tag_name('img').get_attribute("src")
                    if src == sides[key]['artwork']:
                        ele.click()
                        break 
            driver.find_element_by_id("btn-done-select").click()
             
    ele2 = driver.find_element_by_id("btn-preview").click()
    # get element  after explicitly waiting for 60 seconds
    try:
        element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CLASS_NAME, "image-mockup-preview"))
            )
    except Exception as e: 
        return ["error"]
    imgs = driver.find_elements_by_class_name('image-mockup-preview')
    for img in imgs:
        src = img.get_attribute('src')
        if not src in preview_mockup_urls:
            preview_mockup_urls.append(src)
            nameImage= getNameImage(src)
            urllib.request.urlretrieve(src, 'Image_mockup/{}'.format(nameImage))  
    return preview_mockup_urls

def getNameImage(src):
    return src.split('/')[-1]

def _check_store_price(driver, product_sku, prices): 
    login(driver)
    new_product_link = get_url('/u/products/new')
    driver.get(new_product_link)
    element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "btn-create-{}".format(product_sku.lower())))
        )
    ele1 = driver.find_element_by_id("btn-create-{}".format(product_sku.lower())).click()
    time.sleep(1)
    ele2 = driver.find_element_by_id("checkbox-notice-legal").click()
    ele3 = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/button").click()
    time.sleep(1)
    ele4 = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div[2]/button").click()
    time.sleep(1)
    eles = driver.find_element_by_class_name("shopifilize-table").find_elements_by_class_name("ant-table-row")
    for ele in eles:
        size = ele.find_elements_by_tag_name('td')[0].text
        input_size = ele.find_element_by_tag_name('input')
        for price in prices:
            if price['attribute'] == size:
                input_size.clear()
                input_size.send_keys(price['value'])
    
    ele = driver.find_element_by_id("shopList").find_elements_by_class_name("flex-middle")[0]
    ele.find_element_by_tag_name('input').click()
    time.sleep(1)
    ele = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button").click()
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'home')]")))

    element = driver.find_element_by_class_name("title-list-uploading").click()
    ele = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Preview')]")))
    link = ele.get_attribute("href")
    driver.get(link)
    ele = driver.find_element_by_id("password").send_keys('1')
    ele = driver.find_element_by_xpath("//button[contains(., 'Enter')]").click()
    driver.get(link)
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, "SingleOptionSelector-0")))
    
    for price in prices:
        size = price['attribute']
        ele = driver.find_element_by_xpath("//select[@id='SingleOptionSelector-0']/option[text()='{}']".format(size)).click()
        time.sleep(2)
        ele = driver.find_element_by_class_name("price").text
        if float(re.findall(r'\d+\.\d+', ele)[0]) != float(price['value']): 
            return False
    return True

def _check_information_product(driver, product_sku, infos):
    login(driver)
    new_product_link = get_url('/u/products/new')
    driver.get(new_product_link)
    element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "btn-create-{}".format(product_sku.lower())))
        )
    ele = driver.find_element_by_xpath("//button[contains(., 'Info')]").click()
    time.sleep(1)
    for info in infos:
        size = info['attribute']
        ele = driver.find_element_by_xpath("//class[contains(., '{}'".fomat(size))])
        base_cost = info['base_cost']
        US_ship = info['US_ship']
        US_ship_add = info['US_ship_add']
        EU_ship = info['EU_ship']
        EU_ship_add = info['EU_ship_add'] 
        ROW_ship = info['ROW_ship']
        ROW_ship_add = info['ROW_ship_add']







   