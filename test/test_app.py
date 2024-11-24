import unittest
from app import app
from flask import url_for
from file_manager import log_file_path
import json

with open(log_file_path, "r") as file:
        data = json.load(file)

class TestAppFunctionality(unittest.TestCase):
    def setUp(self):
        # Set up the Flask app for testing
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        # Clean up after each test
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_run_main_route(self):
        original_entries = len(data) 
        response = self.app.post('/run_main')
        postprocess_entries = len(data) 
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(postprocess_entries, original_entries+1)

    def test_run_periodical_route(self):
        original_entries = len(data) 
        response = self.app.post('/run_periodical', data={'frequency': 1, 'occurrences': 2})
        postprocess_entries = len(data) 
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(postprocess_entries, original_entries+2)

    def test_return_dated_route(self):
        response = self.app.post('/return_dated', data={'date': '2024-01-01'})
        self.assertEqual(response.status_code, 200)

    def test_return_all_route(self):
        response = self.app.post('/return_all_readings')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()