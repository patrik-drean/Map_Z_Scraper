import time, re, csv, glob, pprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from lib.stopwatch import Timer
from pyexcel.cookbook import merge_all_to_a_book
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Font, Fill, PatternFill

##################### Web scrape website #####################

timer = Timer()
timer.start()
pp = pprint.PrettyPrinter(indent=4)

# # Open firefox browser
# driver = webdriver.Firefox()
#
# # Navigate to URL
# driver.get("https://lds.org")
#
# # Navigate to login
# account_button = driver.find_element_by_xpath("//*[contains(text(), 'My Account')]")
# account_button.click()
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
# directory_button = driver.find_element_by_xpath("//*[contains(text(), 'Directory')]")
# directory_button.click()
#
# ## Grab information and put into dictionary
# households = []
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
#         # Add to list
#         households.append((
#             '',
#             household_name,
#             household_street_address.replace(".", "").strip(),
#             household_city,
#             'United States',
#             household_zip,
#             'Active Member',
#             '',
#             ))
#
#         # Show progress of homes
#         for value in households:
#             print('\n{}'.format(value[1]))
#             print(value[2])
#             print(value[3])
#             print(value[5])
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
#     fieldnames = [
#         'Location Code',
#         'Name',
#         'Street',
#         'City',
#         'Country',
#         'Zipcode',
#         'Category',
#         'Description',]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     # Write each household to individual rows
#     for value in households:
#         writer.writerow({
#             'Location Code': value[0],
#             'Name': value[1],
#             'Street': value[2],
#             'City': value[3],
#             'Country': value[4],
#             'Zipcode': value[5],
#             'Category': value[6],
#             'Description': value[7],
#             })
#
# # Convert csv file to xlsx
# merge_all_to_a_book(glob.glob("data/map_data_backup.csv"), "data/map_data.xlsx")

### For testing purposes ###
households = []
# Load up new map data
wb = load_workbook(filename='data/map_data.xlsx', read_only=True)
ws = wb['map_data_backup.csv']

for index, row in enumerate(ws.rows):
    if (index != 0):
        households.append((
            row[0].value,
            row[1].value,
            row[2].value,
            row[3].value,
            row[4].value,
            row[5].value,
            row[6].value,
            row[7].value,
            ))

wb.close()
### End test block ###

##################### Compare map excel file data #####################
current_households = []
misc_households = []

upload_households = []
change_households = []
add_households = []
delete_households = []

## Load up current household information
##TODO will have to change worksheet on official map
wb = load_workbook(filename='data/current_map_data.xlsx', read_only=True)
ws = wb['compiled_data_1.2']

for index, row in enumerate(ws.rows):
    # Skip header info
    if (index != 0):
        # Add to the normal list if a normal member
        if row[6].value == 'Less Active Member' or \
            row[6].value == 'Active Member' or \
            row[6].value == 'Part Member Family':

            current_households.append((
                row[0].value,
                row[1].value,
                row[2].value,
                row[3].value,
                row[4].value,
                row[5].value,
                row[6].value,
                row[7].value,
                ))

        # Put other households in a misc list that will be added to the upload list at the end
        else:
            misc_households.append([
                row[0].value,
                row[1].value,
                row[2].value,
                row[3].value,
                row[4].value,
                row[5].value,
                row[6].value,
                row[7].value,
                ])

wb.close()


### Add household to upload lists if name and match in current households

for value in households:
    is_current_household = False
    is_misc_household = False

    # Check if household name and address is in the current household
    for current_value in current_households:
        # If the name and address already matches, add current household to upload list
        if value[1] == current_value[1] and value[2] == current_value[2]:
            upload_households.append(current_value)
            is_current_household = True

    # Check if address is in a prior household
    if is_current_household == False:
        for misc_value in misc_households:

            # If address is the same as a prior household, update the prior household and add to upload list
            if value[2] == misc_value[2]:
                misc_value[1] = value[1]
                misc_value[6] = value[6]
                misc_value[7] = value[7]

                change_households.append(misc_value)
                is_misc_household = True

    # Upload any of the remaining new households
    if is_current_household == False and is_misc_household == False:
        # Change color to indicate a new household
        add_households.append(value)


## Find households to be deleted
upload_misc_households = []

for misc_value in misc_households:
    no_match = True

    # Find if prior residencies need to be deleted
    for upload_value in upload_households:
        if misc_value[2] == upload_value[2]:
            print(upload_value[2])
            print(misc_value[2])
            delete_households.append(misc_value)
            no_match = False
            print(misc_value)

    # Add to official misc list if there was no match
    if no_match:
        upload_misc_households.append(misc_value)



# TODO Don't know what this was for
# for current_value in current_households:
#     # Find if prior residencies need to be deleted
#     for upload_value in upload_households:
#         if misc_value[1] == upload_value[1]:
#             delete_households.append(misc_value)




## Upload to official upload excel sheet
csv_counter = 0
add_counter = 0
change_counter = 0
delete_counter = 0

with open('data/updated_map_data_backup.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'Location Code',
        'Name',
        'Street',
        'City',
        'Country',
        'Zipcode',
        'Category',
        'Description',]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write each household to individual rows
    print(len(add_households))
    print(len(change_households))
    print(len(delete_households))
    print(len(upload_households))
    print(len(upload_misc_households))
    print()
    for value in add_households:
        writer.writerow({
            'Location Code': value[0],
            'Name': value[1],
            'Street': value[2],
            'City': value[3],
            'Country': value[4],
            'Zipcode': value[5],
            'Category': value[6],
            'Description': value[7],
            })
        add_counter += 1
        csv_counter += 1


    for value in change_households:
        writer.writerow({
            'Location Code': value[0],
            'Name': value[1],
            'Street': value[2],
            'City': value[3],
            'Country': value[4],
            'Zipcode': value[5],
            'Category': value[6],
            'Description': value[7],
            })
        change_counter += 1
        csv_counter += 1

    for value in delete_households:
        writer.writerow({
            'Location Code': value[0],
            'Name': value[1],
            'Street': value[2],
            'City': value[3],
            'Country': value[4],
            'Zipcode': value[5],
            'Category': value[6],
            'Description': value[7],
            })
        delete_counter += 1
        csv_counter += 1

    for value in upload_households:
        writer.writerow({
            'Location Code': value[0],
            'Name': value[1],
            'Street': value[2],
            'City': value[3],
            'Country': value[4],
            'Zipcode': value[5],
            'Category': value[6],
            'Description': value[7],
            })
        csv_counter += 1

    for value in upload_misc_households:
        writer.writerow({
            'Location Code': value[0],
            'Name': value[1],
            'Street': value[2],
            'City': value[3],
            'Country': value[4],
            'Zipcode': value[5],
            'Category': value[6],
            'Description': value[7],
            })
        csv_counter += 1

# Format to xlsx file
merge_all_to_a_book(glob.glob("data/updated_map_data_backup.csv"), "data/updated_map_data.xlsx")

## Format colors for add, change, and delete households

# Load updated excel book
wb = load_workbook(filename='data/updated_map_data.xlsx')
ws = wb['updated_map_data_backup.csv']

if add_counter != 0:
    # Load color fills for each added households
    fill = PatternFill(patternType='solid', fgColor='6bf977')
    start_cell = 'A' + str(2)
    end_cell = 'H' + str(1 + add_counter)

    for row in ws[start_cell : end_cell]:
        for cell in row:
            cell.fill = fill

if change_counter != 0:
    # Load color fills for each changed households
    fill = PatternFill(patternType='solid', fgColor='faff77')
    start_cell = 'A' + str(2 + add_counter)
    end_cell = 'H' + str(1 + add_counter + change_counter)

    for row in ws[start_cell : end_cell]:
        for cell in row:
            cell.fill = fill

if delete_counter != 0:
    # Load color fills for each changed households
    fill = PatternFill(patternType='solid', fgColor='f96f57')
    start_cell = 'A' + str(2 + add_counter + change_counter)
    end_cell = 'H' + str(1 + add_counter + change_counter + delete_counter)

    for row in ws[start_cell : end_cell]:
        for cell in row:
            cell.fill = fill


print(add_counter)
print(change_counter)
print(delete_counter)
print(csv_counter)


# Save with color updates
wb.save('data/updated_map_data.xlsx')


##################### Upload to Zeemaps #####################

# Quit process
# input()
# driver.quit()
