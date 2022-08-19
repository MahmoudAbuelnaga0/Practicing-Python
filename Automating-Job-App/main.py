# ---------- MODULES ---------- #
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# ---------- FUNCTIONS ---------- #
# def follow_company():
#     global available_jobs
#     sleep(CLICK_DELAY)
#     try:
#         company_info = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div:last-child.ember-view.jobs-box--generic-occludable-area-large')))
#         driver.execute_script("arguments[0].scrollIntoView();", company_info)
#     except:
#         pass
    
#     # scroll_down_job_details()
#     try:
#         follow_btn = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'follow')))
#         follow_btn.click()
#     except:
#         driver.refresh()
#         follow_company()
#         sleep(7)
#         available_jobs = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")

# def scroll_down_job_details():
#     job_details = driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")
#     container_size = job_details.size
#     x_offset = container_size["width"]/2 - 5
#     y_offset = 20
#     action.move_to_element(job_details).perform()    # Mouse move to container
#     action.move_by_offset(x_offset, 0).perform()    # Teh move to the scroller
#     action.click().perform()    # and click
#     sleep(CLICK_DELAY)    # Waits 2 seconds
#     move_mouse_down(y_offset)
#     sleep(CLICK_DELAY)
#     move_mouse_down(y_offset)

def save_job(*args):
    """A function that save the job on linkedin"""
    
    sleep(CLICK_DELAY)
    try:    # Try to click save button
        save_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-save-button")))
        save_btn.click()   
    except: # If failed print the following
        print("Save button wasn't found.")
    
def follow_company(job_container: WebElement):
    """Follows the company which offer the job

    Args:
        job_container (WebElement): Job container on linkedin (Job rectangle that you click)
    """
    
    try:    # Try to find the company_link
        company = job_container.find_element(By.CLASS_NAME, "job-card-container__company-name")
        company_link = company.get_attribute("href")   
    except: # If wasn't found print the following
        print("Company link wasn't found.")  
    else:   # If company's linkedin link was found
        # Try to open company's page in a new tab
        driver.execute_script(f'''window.open("{company_link}","_blank");''')
        company_window = driver.window_handles[1]
        driver.switch_to.window(company_window)
        
        try:    # Try clicking follow button
            follow_btn = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'follow')))
            follow_btn.click()  
        except: # If failed print the following
            print("Follow button wasn't found")
            
        driver.close()  # Close the company's page
        # Switch to jobs page
        jobs_window = driver.window_handles[0]
        driver.switch_to.window(jobs_window)

def check_jobs(functions_to_apply_on_job:list):
    """Function that clicks on each job on screen.
    
    *args: function arguments to apply on each job you click.
    """
    
    scroll_down_jobs()
    try:    # Try to find jobs list
        available_jobs = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")
    except: # If wasn't found print the following
        print("No jobs found.") 
    else:   # If list was found
        last_job_tile = ""
        last_job_company = ""
        # Do that to each job on the list
        for job in available_jobs:
            sleep(3)
            
            try:    # Try to click on the job
                action.move_to_element(job).click().perform()
            except: # If failed
                sleep(CLICK_DELAY)  # Wait a little bit
                action.move_to_element(job).click().perform()   # Then try to click on the job again
               
            try: # Try to get the jov title and company, then apply functions
                sleep(4)
                current_job_title = job.find_element(By.CLASS_NAME, "job-card-list__title")
                current_job_title = current_job_title.text.strip()
                
                current_job_company = job.find_element(By.CLASS_NAME, "job-card-container__company-name")
                current_job_company = current_job_company.text.strip()
                
                if current_job_title != last_job_tile or last_job_company != current_job_company:
                    for function in functions_to_apply_on_job:   # Do the passed functions on the job I clicked
                        function(job)
                    
                last_job_tile = current_job_title
                last_job_company = current_job_company
            except: # If failed then there was an error loading the page.
                pass
            
page_no = 1
def next_page():
    """Moves to the next page or list of jobs on linkedin

    Returns:
        bool: returns True if there is no othe pages
    """
    global page_no
    page_no += 1
    try:    # Try to find the button with the "page_no" after adding 1
        next_page_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, f"li[data-test-pagination-page-btn='{page_no}']")))
    except: # If failed
        print("There is no other pages")
        return True
    else:   #   If found click it
        next_page_btn.click()
        
def move_mouse_down(delta_y:int = 20, click:bool = True):
    """Move the mouse down

    Args:
        delta_y (int, optional): distance by which to move the mouse down. Defaults to 20.
        click (bool, optional): If true the mouse clicks after moving down. Defaults to True.
    """
    
    action.move_by_offset(0, delta_y).perform()    # Mouse moves down by delta_y
    if click:
        action.click().perform()
        
def scroll_down_jobs():
    """Scrolls down list of jobs."""
    
    try:    # Try to find jobs list and get its width
        jobs_container = driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
        container_size = jobs_container.size
        x_offset = container_size["width"]/2 + 5
        
    except: # If failed print the following
        print("Jobs list wasn't found.")
        
    else:   # If jobs list was found
        action.move_to_element(jobs_container).perform()    # Mouse move to container
        action.move_by_offset(x_offset, 20).perform()    # Mouse move to the scroller
        
        # Keep scrolling down
        move_mouse_down()
        sleep(2)
        move_mouse_down()
        sleep(2)
        move_mouse_down()
        sleep(2)
    
def easy_apply(*args):
    try:    # Try to click on easy apply button
        easy_apply_btn = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))
        easy_apply_btn.click()
    except: # If failed exit the function
        return
    
    # iF easy apply button was clicked
    easy_apply_content = wait.until(ec.presence_of_element_located((By.CLASS_NAME, "jobs-easy-apply-content"))) # Wait until the easy apply form is loaded
    # Loop that tries to apply for the job
    while True: 
        sleep(3)    # Wait 3 seconds
        btn = easy_apply_content.find_element(By.CLASS_NAME, "artdeco-button--primary") # Get the primary button on form (Review, Next, Submit)
        
        # If the button was submit
        if "Submit application" in btn.text.strip():
            # Submit My CV
            try:
                btn.click()
                print("CV was sumbitted")
                sleep(2)
            except:
                print("Couldn't click submit.")
                
            break   # And exit loop
        
        if not("Additional Questions" in easy_apply_content.get_attribute("textContent")) and not("Please enter a valid answer" in easy_apply_content.get_attribute("textContent")) and not("Work experience" in easy_apply_content.get_attribute("textContent")):    # If the form doesn't require additional information just move to next page in form
            btn.click()
        else:   # If the form requires additional information exit the form
            exit_btn = driver.find_element(By.CSS_SELECTOR, "button.artdeco-modal__dismiss") 
            exit_btn.click()
            discard_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='discard_application_confirm_btn']")))
            discard_btn.click()
            break

# ---------- CONSTANTS ---------- #
LINKEDIN_EMAIL = ""
LINKDIN_PASS = ""
ROLE_U_SEARCHING_FOR = ""
JOB_FUNCTIONS = [save_job, follow_company]  # Functions to apply on each job found on jobs list.. Available functionalities (save_job, easy_apply and follow_company)
CLICK_DELAY = 2
        
# ---------- MAIN ---------- #
# Prepare the driver
chrome_driver_path = "D:\programs\chromedriver.exe"
driver = webdriver.Chrome(executable_path= chrome_driver_path)
ignored_exceptions = (TimeoutException ,NoSuchElementException, StaleElementReferenceException)
wait = WebDriverWait(driver, 10, ignored_exceptions= ignored_exceptions)
action = webdriver.ActionChains(driver, 500)

# Open the website
driver.get(url = "https://www.linkedin.com/")
driver.maximize_window()

# Enter the email on linkedin
email_input = driver.find_element(By.NAME, "session_key")
email_input.send_keys(LINKEDIN_EMAIL)

# Enter the password
pass_input = driver.find_element(By.NAME, "session_password")
pass_input.send_keys(LINKDIN_PASS)

# Sign In
sign_in_btn = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
sign_in_btn.click()

# Search for a job
sleep(10)
search_input = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input.always-show-placeholder")))
search_input.send_keys(ROLE_U_SEARCHING_FOR)
search_input.send_keys(Keys.ENTER)

# Show jobs section
jobs_btn = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button')))
jobs_btn.click()

# Click on Easy Apply
easy_apply_select = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[4]/section/div/section/div/div/div/ul/li[8]/div/button')))
easy_apply_select.click()

# Loop that checks jobs on page then move to a new page
while True:
    driver.refresh()    # Refresh page as error might happen while loading the page
    sleep(7)   # Wait 7 seconds to give time to the page to load
    check_jobs(JOB_FUNCTIONS) # Then start checking jobs
    done = next_page()
    if done:
        break
    
driver.quit()