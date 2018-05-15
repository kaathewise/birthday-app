import unittest
import mock
from datetime import date

from . import main

class TestApp(unittest.TestCase):
    def test_message(self):
        main.get_today = lambda: date(2010, 1, 1)
        self.assertEqual(
            main.get_message('John', date(2000, 1, 15)),
            'Hello, John! Your birthday is in 14 days')

if __name__ == '__main__':
    unittest.main()
