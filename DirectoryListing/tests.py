import requests, json
import unittest


# Create your tests here.
class TestFileRepositoryAPI(unittest.TestCase):
    def test_access_available_files_api(self):
        resp = requests.get('http://localhost:8000/api/available_files')
        print(resp.status_code)
        self.assertEqual(resp.status_code, 200)

    def test_access_archived_files_api(self):
        resp = requests.get('http://localhost:8000/api/archived_files')
        print(resp.status_code)
        self.assertEqual(resp.status_code, 200)



if __name__ == '__main__':
    unittest.main()
