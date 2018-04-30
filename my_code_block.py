addresses = ['634 Tomato Way', '233 E. 500 S.', '1800 N. Python Lane']
formatted_addresses = []

# Loop to replace '.' with nothing and add to the formatted_addresses list
for value in addresses:
    value = value.replace('.', '')
    formatted_addresses.append(value)
