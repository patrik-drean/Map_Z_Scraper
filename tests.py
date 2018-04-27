import unittest
# from map_z_scraper import *
from openpyxl import load_workbook

class MapTestCast(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.new_households = {}
        super().__init__(*args, **kwargs)

    def setUp(self):
        '''Load up new map data and current map data into two lists'''
        # Load up new map data
        wb = load_workbook(filename='data/map_data.xlsx', read_only=True)
        ws = wb['map_data_backup.csv']

        for index, row in enumerate(ws.rows):
            if (index != 0):
                self.new_households[row[0].value] = (
                    row[1].value,
                    row[2].value,
                    row[3].value)
                print(self.new_households[row[0].value])

        # Load up current map data
        wb = load_workbook(filename='data/map_data.xlsx', read_only=True)
        ws = wb['map_data_backup.csv']

        for index, row in enumerate(ws.rows):
            if (index != 0):
                self.new_households[row[0].value] = (
                    row[1].value,
                    row[2].value,
                    row[3].value)
                print(self.new_households[row[0].value])

    def test_decimal(self):
        '''Test there's no decimals in the households'''
        no_decimals = True
        for key, value in self.new_households.items():
            if '.' in value[0]:
                no_decimals = False
        self.assertTrue(no_decimals)

if __name__ == '__main__':
    unittest.main()
