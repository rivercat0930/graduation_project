from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

url = "https://www.facebook.com/"

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

acc = "0979196823"
password = "duprys-Jyjwam-xaxky7"


WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
)
elem = driver.find_elements(By.CLASS_NAME, "inputtext._55r1._6luy")

elem[0].send_keys(acc)
time.sleep(1)
elem[1].send_keys(password)
time.sleep(1)

enter_button = driver.find_element(
    By.CLASS_NAME, "_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy".replace(" ", ".")
)
enter_button.click()
time.sleep(5)

search = driver.find_element(
    By.CLASS_NAME,
    "x1i10hfl xggy1nq x1s07b3s x1kdt53j x1yc453h xhb22t3 xb5gni xcj1dhv x2s2ed0 xq33zhf xjyslct xjbqb8w xnwf7zb x40j3uw x1s7lred x15gyhx8 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u xdl72j9 x1iyjqo2 xs83m0k xjb2p0i x6prxxf xeuugli x1a2a7pz x1n2onr6 x15h3p50 xm7lytj x1sxyh0 xdvlbce xurb0ha x1vqgdyp x1xtgk1k x17hph69 xo6swyp x1ad04t7 x1glnyev x1ix68h3 x19gujb8".replace(
        " ", "."
    ),
)
search.send_keys("麥如芳")
time.sleep(2)
search.send_keys(Keys.RETURN)
time.sleep(5)

username = driver.find_elements(
    By.CLASS_NAME,
    "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(
        " ", "."
    ),
)
time.sleep(2)
for i in username:
    # print(i.get_attribute("href"))
    herf_name = i.get_attribute("href")
    if "[0]=" in str(herf_name) or herf_name is None:
        print("no")
    else:
        print(herf_name)
        driver.get(herf_name)
        break
# driver.get(username.get_attribute("href"))

time.sleep(7)

driver.execute_script("window.scrollTo(0, 500);")
SCROLL_PAUSE_TIME = 1

for i in range(15):
    driver.execute_script("window.scrollTo(0, 1000000000, 'smooth');")
    time.sleep(10)
    driver.execute_script("window.scrollTo(0,document.body);")
    # time.sleep(SCROLL_PAUSE_TIME)

time.sleep(7)


blank_of_name = driver.find_elements(
    By.CLASS_NAME,
    "x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a".replace(" ", "."),
)
for i in blank_of_name:
    if "，在" in str(i.get_attribute("textContent")):
        print(i.get_attribute("textContent"))
# print(blank_of_name.find_element(By.CLASS_NAME,"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(" ",".")).find_element(By.CLASS_NAME,"xt0psk2").text)
# text_content = driver.find_elements(By.CLASS_NAME,"xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a".replace(" ","."))
#
# local_name = driver.find_elements(By.CLASS_NAME,"xt0psk2")
time.sleep(3)


driver.close()
