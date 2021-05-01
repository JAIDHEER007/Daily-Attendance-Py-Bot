from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
from os import getcwd
from datetime import date

today = date.today().strftime("%d-%m-%Y")

#Disabling console logging
opt = Options() 
opt.add_experimental_option("excludeSwitches", ["enable-logging"]) 

#Stopping images from Loading 
prefs = {"profile.managed_default_content_settings.images": 2}
opt.add_experimental_option("prefs", prefs)

#Avoiding "Your Connection is not private" error
opt.add_argument('--ignore-ssl-errors=yes')
opt.add_argument('--ignore-certificate-errors')

#Performance boost
opt.add_argument('--no-proxy-server') 
opt.add_argument("--proxy-server='direct://'")
opt.add_argument("--proxy-bypass-list=*")

#opt.add_argument('--headless')

path = getcwd() + '/chromedriver.exe'

driver = webdriver.Chrome(options = opt, executable_path = path) 

driver.get('https://info.aec.edu.in/aec/default.aspx')

driver.find_element_by_id('txtId2').send_keys('---UID---')
driver.find_element_by_id('txtPwd2').send_keys('---PWD---')
log_in = driver.find_element_by_id('imgBtn2')
driver.execute_script("arguments[0].click();", log_in)

driver.find_elements_by_class_name('menuLink')[0].click()

driver.switch_to.frame('capIframeId')
driver.find_element_by_id('radPeriod').click()
driver.find_element_by_id('txtFromDate').send_keys(today)
driver.find_element_by_id('txtToDate').send_keys(today)
driver.find_element_by_id('btnShow').click()

wdw(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"cellBorder")))

soup = BeautifulSoup(driver.page_source, 'html.parser')
tables = soup.find_all('table', class_='cellBorder')
dfs = pd.read_html(str(tables))

dfs[0].drop([0], axis = 0, inplace = True)

headers = ["Sl.No","Subject","Held","Attend","%"]

print(tabulate(dfs[0], headers, tablefmt='pretty', showindex=False))

driver.switch_to.default_content()
driver.find_element_by_id('lnkLogOut').click()

driver.quit() #Used to close the driver