from selenium import webdriver
from datetime import date, timedelta, datetime
import os
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

country_path = "/Users/Doris/Downloads/Electri/Chile/" #Path for Holding the Initial Zip and Final Output
os.mkdir(country_path)
os.chdir(country_path)

url = 'https://www.cenace.gob.mx/SIM/VISTA/REPORTES/DemandaRealSist.aspx'


# Configuration

chrome_options = Options()
chrome_options.headless = True #Not Launching Browser
chrome_options.add_experimental_option("prefs",{
    "download.default_directory":country_path,
    "download.prompt_for_download": False}) # Setting Download Preference
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options = chrome_options)

# HTML XPaths
datepath1 = '//*[@id="ctl00_ContentPlaceHolder1_RadDatePickerVisualizarPorBalance_dateInput"]'
buttonpath = "//input[@name='ctl00$ContentPlaceHolder1$GridRadPorBalance$ctl00$ctl04$gbccolumn' and @id ='ctl00_ContentPlaceHolder1_GridRadPorBalance_ctl00_ctl04_gbccolumn']"

# Load URL
driver.get(url)

time.sleep(np.random.randint(20,40))


# Dates
d1 = date(2016,1,27)
d2 = date(2020,6,5)

dates = []

delta = d2 - d1

for i in range(delta.days + 1):
    day = d1 + timedelta(days = i)
    dates.append(day)

# Additional Configuration
wait = WebDriverWait(driver,60)
element = wait.until(EC.presence_of_element_located((By.XPATH,datepath1)))
click_button = driver.find_elements_by_xpath("//input[@name='ctl00$ContentPlaceHolder1$GridRadPorBalance$ctl00$ctl04$gbccolumn' and @id ='ctl00_ContentPlaceHolder1_GridRadPorBalance_ctl00_ctl04_gbccolumn']")[0]

# Every Date Download
download = 0
for day in dates:
    element.clear()
    daystring = day.strftime("%d/%m/%Y")
    number = np.random.randint(0,5)
    element.send_keys(daystring[0:number])
    time.sleep(np.random.randint(10,20))
    element.send_keys(daystring[number:])
    time.sleep(np.random.randint(10,20))
    click_button.click()
    download += 1

