import time, re, csv, glob
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from lib.stopwatch import Timer
from pyexcel.cookbook import merge_all_to_a_book
import pyexcel.ext.xlsx # needed to support xlsx format, pip install pyexcel-xlsx


##################### Web scrape website #####################

timer = Timer()
timer.start()
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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'IDToken1')))
username = 'pdrean4'
password = 'Lnephite44'


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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pf-signin')))

# Navigate to directory
account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
account_button.click()

directory_button = driver.find_element_by_xpath("//*[contains(text(), 'Directory')]")
directory_button.click()

## Grab information and put into dictionary
households = {}
counter1 = 0
household_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
    By.ID, 'listItem0')))

while(household_link):
    # Grab next household link based on counter
    household_id = 'listItem' + str(counter1)
    try:
        # Grab link and household name
        household_link = driver.find_element_by_id(household_id) \
            .find_element_by_tag_name('a')
        household_name = household_link.text

        # Click into household
        household_link.click()

        # Wait for ajox to load then assign to element
        element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.ID, 'householdAddress'))
            )

        # Grab household address
        household_address_spans = element.find_elements_by_tag_name('span')

        # Change final_pos if household is the logged in user
        # TODO
        try:
             driver.find_element_by_id("show_profile_edit")
             final_pos = (len(household_address_spans) - 3)

         # Assign for all other households
        except NoSuchElementException:
            final_pos = (len(household_address_spans) - 1)

        i = 0
        household_street_address = ''
        household_city = ''
        household_zip = ''

        # Loop to grab the street address
        while(i < final_pos):
            household_street_address += ' {}'.format(household_address_spans[i].text)
            i += 1

        # Grab city
        household_city = household_address_spans[final_pos].text.split(',')[0]

        # Grab zip
        household_zip = re.search(
            r'(\d{5})',
            household_address_spans[final_pos].text
            )
        if household_zip:
            household_zip = household_zip.group(0)
        else:
            household_zip = '84606'

        # Add to dictionary
        households[household_name] = (
            household_street_address.strip(),
            household_city,
            household_zip)

        # Show progress of homes
        print()
        print(household_name)
        print(household_street_address.strip())
        print(household_city)
        print(household_zip)

    # Output when finished
    except NoSuchElementException:
        print("\nFinished compiling each household.")
        household_link = None
        print(timer.stop(message = 'Time Elapsed: '))

    # Increment
    counter1 += 1

## Write to csv file
with open('data/map_data_backup.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'Street', 'City', 'State', 'Country', 'Zipcode']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for key, value in households.items():
        writer.writerow({
            'Name': key,
            'Street': value[0],
            'City': value[1],
            'State': 'UT',
            'Country': 'United States',
            'Zipcode': value[2]
            })

merge_all_to_a_book(glob.glob("data/map_data.csv"), "data/map_data.xlsx")

##################### Compare map excel file #####################


##################### Upload to Zeemaps #####################

# Quit process
input()
driver.quit()
