import unittest
from map_z_scraper import *

class MapTestCast(unittest.TestCase):

    def test_decimal(self):
        '''Test there's no decimals in the household street address'''
        no_decimals = True
        for value in households:
            if '.' in value[2]:
                no_decimals = False
        self.assertTrue(no_decimals)

    def test_null_value(self):
        '''Make sure no null values exist in the list scraped from the web '''
        not_null = True
        for value in households:
            if value[1] is None or value[2] is None:
                not_null = False
        self.assertTrue(not_null)

    def test_successfully_added(self):
        '''Test if every household has been added from the web scraped list'''
        successfully_added = True

        for value in households:
            match = False
            for upload_value in upload_households:
                if value[1] == upload_value[1] and value[2] == upload_value[2]:
                    match = True
            if match == False:
                successfully_added = False

        self.assertTrue(successfully_added)

    def test_deleted_households(self):
        '''Make sure the deleted households have truly been replaced'''
        successfully_to_be_deleted = True

        for value in households:
            match = False
            for upload_value in upload_households:
                if value[2] == upload_value[2]:
                    match = True
            if match == False:
                successfully_to_be_deleted = False

        self.assertTrue(successfully_to_be_deleted)


if __name__ == '__main__':
    unittest.main()
