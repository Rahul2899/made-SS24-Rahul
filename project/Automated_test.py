import os
import unittest

def check_files(folder, files):
    results = {}
    for filename in files:
        file_path = os.path.join(folder, filename)
        results[filename] = os.path.isfile(file_path)
    return results
class Automated_Test(unittest.TestCase):
    def setUp(self):
        self.dir = "./data/"
    def test_file_existance(self):
        expected_result = {'combined_crop_rainfall.sqlite': True}
        result = check_files(self.dir, ['combined_crop_rainfall.sqlite'])
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
