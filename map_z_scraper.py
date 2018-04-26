from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Open firefox browser
driver = webdriver.Firefox()

# Navigate to URL
driver.get("https://lds.org")

# Navigate to login
account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
account_button.click()

signin_button = driver.find_element_by_xpath("//*[contains(text(), 'Sign In')]")
signin_button.click()


# Prompt for login info
# username = input('Enter username:')
# password = input('Enter password:')
time.sleep(4)
username = 'pdrean4'
password = 'Lnephite44'

time.sleep(1)

# Grab inputs
username_input = driver.find_element_by_name("IDToken1")
password_input = driver.find_element_by_name("IDToken2")

# Enter values
username_input.clear()
username_input.send_keys(username)

password_input.clear()
password_input.send_keys(password)

# Submit form
username_input.submit()

# Wait for browser to refresh
WebDriverWait(driver, 10).until(EC.title_contains("The Church"))
time.sleep(5)

# Navigate to directory
account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
account_button.click()

directory_button = driver.find_element_by_xpath("//*[contains(text(), 'Directory')]")
directory_button.click()

## Grab information and put into list
time.sleep(3)
people = []
counter1 = 0
household_link = not None

while(household_link):
    # Grab next household link based on counter
    household_id = 'listItem' + str(counter1)
    try:
        household_link = driver.find_element_by_id(household_id)
        print(household_link)
    except NoSuchElementException:
        print("Finished compiling each household.")
        household_link = None

    # Increment
    counter1 += 1

# Quite process
input()
driver.quit()



# content = request.urlopen(url).read()
#
# soup = BeautifulSoup(content)
#
# print (soup)
