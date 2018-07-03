from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

# Navigate to the application home page
driver.get("https://pubs.acs.org/")

# get the search textbox
search_field = driver.find_element_by_id("searchText")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("plant breeding spain")
search_field.submit()


temp = True
while(temp):
    try:
        next = driver.find_element_by_class_name("nextPage")
        next.click()
    except Exception as e:
        print("Exception : " + str(e))
        temp = False
