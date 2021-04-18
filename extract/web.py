from selenium import webdriver
import pandas as pd

def extract_meaning(browser, obj):
    url = obj['href']
    meaning_box = '/html/body/div/section[6]/div/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'
    browser.get(url)
    box = browser.find_element_by_xpath(meaning_box)
    o = box.text.splitlines()
    spelling = o[2].split(':')[1].strip()
    meaning = o[3].split(':')[1].strip()
    obj['spelling'] = spelling
    obj['meaning'] = meaning
    return obj 
    
def generate_url_list():
    generated_list = []
    url = "https://dekgenius.com/name/index.php?page={0}&p={1}"
    for i in range(11):
        start = (i*20)+1
        stop = ((i+1)*20)+1
        for j in range(start, stop):
            new_url = url.format(j, i+1)
            generated_list.append(new_url)
    return generated_list

options = webdriver.FirefoxOptions()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
# options.add_argument('window-size=1200x600') # optional
driver = webdriver.Firefox(options=options)

meaning_list = []
url_list = []

url_list = generate_url_list()

print(f"EXTRACT URL LIST .....")

for url in url_list:
    print(f"Url:{url}")
    driver.get(url)
    links = driver.find_elements_by_class_name('a1')
    for link in links:
        text = link.text
        href = link.get_property('href')
        str = {
                'href': href
            }
        if text == "ความหมาย":
            t = link.find_element_by_xpath("../..")
            x = t.text.split()
            str['name'] = x[1]
            str['sex'] = x[2]
            meaning_list.append(str)
        
print(f"EXTRACT MEANING.... ")
for m in meaning_list:
    m = extract_meaning(driver, m)
    print(f"{m}")

df = pd.DataFrame(meaning_list)
df.to_csv(u'meaning.csv', index=False)

driver.close()