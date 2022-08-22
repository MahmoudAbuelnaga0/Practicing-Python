# ---------- MODULES ---------- #
import os
from formfiller import FormFiller
from propertyfinder import PropertyFinder
from property import Property
from time import sleep

# ---------- CONSTANTS ---------- #
try:
    FORM_LINK = os.environ["FORM_LINK"]   # Link of the form we're going to fill
except:
    FORM_LINK = ""
    
ZILLOW_RENTALS_PAGE = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64762520478779%2C%22east%22%3A-122.24593758271747%2C%22south%22%3A37.63637941330653%2C%22north%22%3A37.85193675606984%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%5D%7D" # Link of zillow website with search specification already done
DELAY = 5

# ---------- MAIN ---------- #
form_filler = FormFiller(FORM_LINK)
finder = PropertyFinder(ZILLOW_RENTALS_PAGE)
more_pages = True
while more_pages:
    sleep(DELAY)
    rentals = finder.get_rental_data()
    for property in rentals:
        sleep(DELAY)
        property:Property;
        address, price, link = property.get_attributes()
        form_filler.fill_form(address, price, link)
        
    more_pages = finder.next_page()
    
form_filler.quit()
finder.quit()