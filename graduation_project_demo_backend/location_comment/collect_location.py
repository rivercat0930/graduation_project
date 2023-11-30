from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import os

print("==================" + os.getcwd())

url = "https://www.google.com/maps/"

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
time.sleep(3)

# search box
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.clear()
search_box.send_keys("台中景點")

search_button = driver.find_element(By.CLASS_NAME, "mL3xi")
search_button.click()
time.sleep(3)


spot_div_list = []

search_result_pane = driver.find_element(
    By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
)


for i in range(35):
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight", search_result_pane
    )
    time.sleep(4)


spot_div_list = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK.THOPZb.CpccDe")

# location_file = open("../src/main/resources/location.txt", "w+")
location_file = open("./src/main/resources/location.txt", "w+")

for i in spot_div_list:
    href = i.find_element(By.CLASS_NAME, "hfpxzc")
    print("writing:", href.get_attribute("aria-label"))
    location_file.write(href.get_attribute("aria-label") + "\n")

driver.close()
location_file.close()
