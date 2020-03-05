import unittest

from src.main.code import devconfig


class MyTestCase(unittest.TestCase):
    def test_connection(self):

        self.assertIsNotNone(self,devconfig.connect_db(), msg="connecteddd")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
