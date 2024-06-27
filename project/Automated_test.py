import os
import unittest

def is_file_exist(folder, file):
    res = False
    file_path = os.path.join(folder, file)
    if os.path.isfile(file_path):
        return True
    
    return False
    



class Automated_Test(unittest.TestCase):
    def setUp(self):
        self.folder = "../data/"

    def test_db_created(self):
        expected_result = True
        result = is_file_exist(self.folder, 'combined_crop_rainfall.sqlite')
        self.assertEqual(result, expected_result,"Db Filename should be 'combined_crop_rainfall.sqlite'")


if __name__ == "__main__":
    unittest.main()
