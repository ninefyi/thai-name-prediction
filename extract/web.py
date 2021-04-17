from selenium import webdriver
import time

def extract_meaning(browser, url):
    browser.get(url)
    box = browser.find_element_by_xpath('/html/body/div/section[6]/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]')
    print(f"{box.text}")
    print("")
    
options = webdriver.FirefoxOptions()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
# options.add_argument('window-size=1200x600') # optional
driver = webdriver.Firefox(options=options)
driver.get('https://dekgenius.com/name/index.php')
results = driver.find_elements_by_class_name('a1')

meaning_list = []
url_list = []

for a in results:
    text = a.text
    href = a.get_property('href')
    str = {
            'text': text,
            'href': href
        }
    if text == "ความหมาย":
        t = a.find_element_by_xpath("../..")
        x = t.text.split()
        str['name'] = x[1]
        str['sex'] = x[2]
        meaning_list.append(str)
    else:
        url_list.append(str)

for m in meaning_list:
    extract_meaning(driver, m['href'])