import time, re, csv, glob
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from lib.stopwatch import Timer
from pyexcel.cookbook import merge_all_to_a_book
from openpyxl import load_workbook


# ##################### Web scrape website #####################
#
# timer = Timer()
# timer.start()
# # Open firefox browser
# driver = webdriver.Firefox()
#
# # Navigate to URL
# driver.get("https://lds.org")
#
# # Navigate to login
# account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
# account_button.click()
#
# signin_button = driver.find_element_by_xpath("//*[contains(text(), 'Sign In')]")
# signin_button.click()
#
#
# # Prompt for login info
# # username = input('Enter username:')
# # password = input('Enter password:')
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'IDToken1')))
# username = 'pdrean4'
# password = 'Lnephite44'
#
#
# # Grab inputs
# username_input = driver.find_element_by_name("IDToken1")
# password_input = driver.find_element_by_name("IDToken2")
#
# # Enter values
# username_input.clear()
# username_input.send_keys(username)
#
# password_input.clear()
# password_input.send_keys(password)
#
# # Submit form
# username_input.submit()
#
# # Wait for browser to refresh
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pf-signin')))
#
# # Navigate to directory
# account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
# account_button.click()
#
# directory_button = driver.find_element_by_xpath("//*[contains(text(), 'Directory')]")
# directory_button.click()
#
# ## Grab information and put into dictionary
# households = {}
# counter1 = 0
# household_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
#     By.ID, 'listItem0')))
#
# while(household_link):
#     # Grab next household link based on counter
#     household_id = 'listItem' + str(counter1)
#     try:
#         # Grab link and household name
#         household_link = driver.find_element_by_id(household_id) \
#             .find_element_by_tag_name('a')
#         household_name = household_link.text
#
#         # Click into household
#         household_link.click()
#
#         # Wait for ajox to load then assign to element
#         element = WebDriverWait(driver, 40).until(
#             EC.presence_of_element_located((By.ID, 'householdAddress'))
#             )
#
#         # Grab household address
#         household_address_spans = element.find_elements_by_tag_name('span')
#
#         # Change final_pos if household is the logged in user
#         # TODO
#         try:
#             driver.find_element_by_id("show_profile_edit")
#             final_pos = (len(household_address_spans) - 2)
#
#          # Assign for all other households
#         except NoSuchElementException:
#             final_pos = (len(household_address_spans) - 1)
#
#         i = 0
#         household_street_address = ''
#         household_city = ''
#         household_zip = ''
#
#         # Loop to grab the street address
#         while(i < final_pos):
#             household_street_address += ' {}'.format(household_address_spans[i].text)
#             i += 1
#
#         # Grab city
#         household_city = household_address_spans[final_pos].text.split(',')[0]
#
#         # Grab zip
#         household_zip = re.search(
#             r'(\d{5})',
#             household_address_spans[final_pos].text
#             )
#         if household_zip:
#             household_zip = household_zip.group(0)
#         else:
#             household_zip = '84606'
#
#         # Add to dictionary
#         households[household_name] = (
#             household_street_address.replace(".", "").strip(),
#             household_city,
#             household_zip)
#
#         # Show progress of homes
#         for key, value in households.items():
#             print('\n{}'.format(key))
#             print(value[0])
#             print(value[1])
#             print(value[2])
#
#     # Output when finished
#     except NoSuchElementException:
#         print("\nFinished compiling each household.")
#         household_link = None
#         print(timer.stop(message = 'Time Elapsed: '))
#
#     # Increment
#     counter1 += 1
#
# ## Write to csv file
# with open('data/map_data_backup.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Name', 'Street', 'City', 'Country', 'Zipcode']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     # Write each household to individual rows
#     for key, value in households.items():
#         writer.writerow({
#             'Name': key,
#             'Street': value[0],
#             'City': value[1],
#             'Country': 'United States',
#             'Zipcode': value[2]
#             })
#
# merge_all_to_a_book(glob.glob("data/map_data_backup.csv"), "data/map_data.xlsx")

### For testing purposes ###
households = {}
# Load up new map data
wb = load_workbook(filename='data/map_data.xlsx', read_only=True)
ws = wb['map_data_backup.csv']

for index, row in enumerate(ws.rows):
    if (index != 0):
        households[row[0].value] = (
            row[1].value,
            row[2].value,
            row[3].value,
            )
wb.close()
### End test block ###

##################### Compare map excel file data #####################
current_households = {}
misc_households = {}
upload_households = {}
delete_households = {}

## Load up current household information
wb = load_workbook(filename='data/current_map_data.xlsx', read_only=True)
ws = wb['compiled_data_1.2']

for index, row in enumerate(ws.rows):
    # Skip header info
    if (index != 0):
        # Add to the normal list if a normal member
        if row[6].value == 'Less Active Member' or \
            row[6].value == 'Active Member' or \
            row[6].value == 'Part Member Family':

            current_households[row[1].value] = (
                row[2].value,
                row[3].value,
                row[4].value,
                row[5].value,
                row[6].value,
                row[7].value,
                row[0].value,
                )
            # print(current_households[row[1].value])
        # Put other households in a misc list that will be added to the upload dict at the end
        else:
            misc_households[row[1].value] = (
                row[2].value,
                row[3].value,
                row[4].value,
                row[5].value,
                row[6].value,
                row[7].value,
                row[0].value,
                )
            # print('MISC: ' + str(misc_households[row[1].value]))
wb.close()

## Add household to upload dict if name and match in current households
for key, value in households.items():

    # Check if key (household name) is in the current household
    if key in current_households:

        # Check if the address is the same
        if value[0] == current_households[key][0]:
            upload_households[key] = value

    # Check if address is in a prior household
    elif value[0] in misc_households.values():
        for misc_value[0] in misc_households:
            if value[0] == misc_value[0]:
                upload_households[key] = value

    else:



##################### Upload to Zeemaps #####################

# Quit process
# input()
# driver.quit()
