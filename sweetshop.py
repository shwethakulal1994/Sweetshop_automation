from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)
driver.get("https://sweetshop.netlify.app/")

wait = WebDriverWait(driver,10)
# //h4[contains(text(),'Bon Bons')]
all_sweets = driver.find_elements(By.XPATH,"//a[@class='btn btn-success btn-block addItem']/parent::div/preceding-sibling::div/child::h4")
# buttons = wait.until(EC.element_to_be_clickable(driver.find_elements(By.XPATH,"//a[@class='btn btn-success btn-block addItem']")))
for sweet in all_sweets:
    if sweet.text == "Bon Bons":
        add_to_cart_buttons= driver.find_element(By.XPATH, "//a[@class='btn btn-success btn-block addItem']")

# buttons = driver.find_elements(By.XPATH,"//a[@class='btn btn-success btn-block addItem']")
# for button in buttons:
#     driver.find_elements(By.XPATH,"//a[@class='btn btn-success btn-block addItem']/parent::div/preceding-sibling::div/child::h4")
#     button_val = button.text
#     print("button_val",button_val)
