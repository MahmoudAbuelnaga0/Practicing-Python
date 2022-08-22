# ---------- MODULES ---------- #
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from property import Property

# ---------- CONSTANTS ---------- #
DELAY = 3

# ---------- CLASS DEFINITION ---------- #
class PropertyFinder:
    def __init__(self, url:str) -> None:
        # Preparing the driver
        options = webdriver.ChromeOptions() 
        options.add_argument("user-data-dir=C:/Users/mahmo/AppData/Local/Google/Chrome/User Data") #Path to your chrome profile
        chrome_driver_path = "D:/browsers-driver/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path= chrome_driver_path, chrome_options= options)
        ignored_exceptions = (TimeoutException, NoSuchElementException, StaleElementReferenceException) 
        self.wait = WebDriverWait(self.driver, 10, ignored_exceptions= ignored_exceptions)
        self.action = webdriver.ActionChains(self.driver, 500)
        
        # Open the url user passed
        self.driver.get(url)
        self.driver.maximize_window()
        
    def get_rental_data(self):
        # Get each rental data
        rentals = [None]    # List to store rentals data
        while None in rentals:
            rental_cards = self.driver.find_elements(By.CLASS_NAME, "list-card-info")
            for card in rental_cards[rentals.index(None):]:
                # Scroll to the card
                try:
                    self.action.scroll_to_element(card).perform()
                except StaleElementReferenceException:
                    rentals.append(None)
                    break
                sleep(DELAY)
                
                # Get property price
                try:
                    price = card.find_element(By.CLASS_NAME, "list-card-price").text
                except StaleElementReferenceException:
                    rentals.append(None)
                    break
                if "+" in price:
                    price = price[:price.index("+")]
                elif "/" in price:
                    price = price[:price.index("/")]
                    
                # Get address an link
                address = card.find_element(By.CLASS_NAME, "list-card-addr").text
                link = card.find_element(By.CLASS_NAME, "list-card-link").get_attribute("href")
                
                # Add the property to rentals list
                property = Property(price, address, link)
                card_index = rental_cards.index(card)
                try:
                    rentals[card_index] = property
                except:
                    rentals.append(property)
                    
        return rentals
            
    def next_page(self):
        next_btn = self.driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
        disabled = next_btn.get_attribute('disabled')
        if not(disabled):
            next_btn.click()
        
        return not(disabled)
    
    def quit(self):
        self.driver.quit()    