from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium
import time
import json
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
# from scrapy.selector import Selector

# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False
driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', options=chrome_options)
driver.get("https://www.limeroad.com/search/nike%20shoes")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'ENGLISH')]")))

# assert "Python" in driver.title
# driver.execute_script("alert('Hello World');")

# elem = driver.find_element_by_css_selector("div.bgL:nth-child(2)")
# elem.clear()
# elem.send_keys("pycon")

element.click()

jsScript = """
        function move_down(element) {
            element.scrollTop = element.scrollTop + 2000;
        }
        move_down(arguments[0]);
    """
centerPanel = driver.find_element_by_css_selector("main#views > div.hscr")

def get_products():
    products = driver.find_elements_by_css_selector('#views > div.hscr > div.conW > .prdC')

    # print(str(products))
    data = []
    for product in products:
        try:
            url = product.find_element_by_css_selector('a.dB').get_attribute('href')
            title_driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', options=chrome_options)
            title_driver.get(url)
            title = title_driver.find_element_by_css_selector('#views > .conn > .fs0 > .w560 > .bs > h1').text
            title_driver.close()
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            url = "None"
            print('Exception Raised')

        try:
            image = product.find_element_by_css_selector('a.dB > img.dB').get_attribute('src')
        except selenium.common.exceptions.NoSuchElementException:
            image = "None"
            print('Exception Raised')
        
        try:
            price = product.find_element_by_css_selector('div.dT > div.dTc div.taL div:nth-child(1)').text
        except selenium.common.exceptions.NoSuchElementException:
            price = "None"
            print('Exception Raised')

        try:
            mrp = product.find_element_by_css_selector('div.dT > div.dTc div.taL div:nth-child(2)').text
        except selenium.common.exceptions.NoSuchElementException:
            mrp = "None"
            print('Exception Raised')
        
        try:
            discount = product.find_element_by_css_selector('div.dT > div.dTc div.taL div:nth-child(3)').text
        except selenium.common.exceptions.NoSuchElementException:
            discount = "None"
            print('Exception Raised')        
        

        print(str(title)+"\n"+str(url)+"\n"+str(image)+"\n"+str(price)+"\n"+str(mrp)+"\n"+str(discount)+"\n\n")
        data.append(
            {
                'title': str(title),
                'url': str(url),
                'image': str(image),
                'price': str(price),
                'mrp': str(mrp),
                'discount': str(discount)
            }
        )

    with open('products_limeroad.json', 'w') as file:
        for d in data:
            json.dump({'title': d['title'], 'url': d['url'], 'price': d['price'], 'image': d['image'], 'mrp': d['mrp'], 'discount': d['discount']}, file)
            file.write(',\n')

while True:
    prev_scroll_pos = driver.execute_script('return arguments[0].scrollTop', centerPanel)
    driver.execute_script(jsScript, centerPanel)
    time.sleep(2)
    curr_scroll_pos = driver.execute_script('return arguments[0].scrollTop', centerPanel)

    if curr_scroll_pos == prev_scroll_pos:
        time.sleep(5)
        get_products()
        break

# assert "No results found." not in driver.page_source
# driver.close()

# main = driver.find_element_by_id('main')
# print(str(main))

# i = 0
# data = list()
# for products in driver.find_elements_by_css_selector("div.hCUpcT > div._35HD7C > div.bhgxx2"):
#     # i+=1
#     for product in products.find_elements_by_css_selector("div._3O0U0u > div"):
#         url = product.find_element(By.CSS_SELECTOR, "._3O0U0u > div:nth-child(1) > .IIdQZO > ._3dqZjq").getAttribute('href')
#         print(url)
    #     info = product.text.split("\n")

    #     if info[len(info)-1].find('% off') != -1:
    #         discount = info[len(info)-1][info[len(info)-1].find('% off')-2:len(info[len(info)-1])]
    #         price = info[len(info)-1].split('₹')[1]
    #         cost = info[len(info)-1].split('₹')[3][0:info[len(info)-1].find('% off')-2]
    #     else:
    #         discount = None
    #         price = info[len(info)-1]
    #         cost = None
        
    #     if info[0] == 'Trending':
    #         status = 'Trending'
    #         title = info[2]
    #     else:
    #         status = None
    #         title = info[1]

    #     print(str(title)+"\n"+str(price)+"\n"+str(discount)+"\n"+str(status)+"\n"+str(cost)+"\n\n")

    # title = product.find_element_by_xpath('').text
    # image = product.find_element_by_xpath('').getAttribute('src')
    # price = product.find_element_by_xpath('').text
    # discount = product.find_element_by_xpath('').text
    # cost = product.find_element_by_xpath('').text
    # print(str(i))

# print(str(data))
