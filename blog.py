# Import the unittest framework
import unittest
# Import the code from our script file
from my_code_block import *

# Create our own test case class that inherits from the base TestCase class
class AddressTestCase(unittest.TestCase):

    # In unittest, each test function must begin with 'test_'
    def test_address_in_list(self):
        # This assert checks that the address is in the list by seeing if it's equal
        self.assertEqual(addresses[0], '634 Tomato Way')

    def test_decimal(self):
        no_decimals = True

        # This loops through each address to check if it has a decimal in it
        for value in formatted_addresses:
            if '.' in value:
                no_decimals = False

        # Run an assert on whether or not there were decimals in one of the addresses.
        self.assertTrue(no_decimals)


# This is to actually run the test
if __name__ == '__main__':
    unittest.main()
