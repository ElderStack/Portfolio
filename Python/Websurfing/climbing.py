from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
USERNAME = ''
PASSWORD = ''

driver.get("https://mason360.gmu.edu/home_login")

try:
    driver.maximize_window()

    sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "topbar__menu--row")))
    webdriver.ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME,"topbar__menu--row")).click().perform()

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn--school")))
    webdriver.ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, "btn--school")).click().perform()

    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email.clear()
    email.send_keys(USERNAME)

    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password.clear()
    password.send_keys(PASSWORD)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "form-button")))
    webdriver.ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, "form-button")).click().perform()

    #print("waiting")
    groups_button = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header__group-icon"]')))
    webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="header__group-icon"]')).click().perform()

    #print('looking for crux')
    crux_climbing_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[2]/nav/ul/li[2]/ul/li/div[2]/ul/li[1]/ul/li[1]/a[1]/div/div[2]/h3/span')))
    webdriver.ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/nav/ul/li[2]/ul/li/div[2]/ul/li[1]/ul/li[1]/a[1]/div/div[2]/h3/span')).click().perform()
finally:
    pass