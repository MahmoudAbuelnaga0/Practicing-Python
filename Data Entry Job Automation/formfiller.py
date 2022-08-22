# ---------- MODULES ---------- #
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# ---------- CONSTANTS ---------- #
DELAY = 3

# ---------- CLASS DEFINITION ---------- #
class FormFiller:
    def __init__(self, url:str) -> None:
        # Preparing the driver
        chrome_driver_path = "D:/browsers-driver/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path= chrome_driver_path)
        ignored_exceptions = (TimeoutException, NoSuchElementException, StaleElementReferenceException) 
        self.wait = WebDriverWait(self.driver, 10, ignored_exceptions= ignored_exceptions)
        self.action = webdriver.ActionChains(self.driver, 500)
        
        # Open the url user passed
        self.url = url
        self.driver.get(self.url)
        self.driver.maximize_window()
        
    def submit(self):
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, '.NPEfkd.RveJvd.snByac')
        self.action.move_to_element(submit_btn).click().perform()
        
    def fill_form(self, *args):
        text_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        for entry, input_area in zip(args, text_inputs):
            input_area.send_keys(entry)
            
        sleep(DELAY)
        self.submit()
        sleep(DELAY)
        self.driver.get(self.url)
        
    def quit(self):
        self.driver.quit()