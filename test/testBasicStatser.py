
import unittest
import sys
sys.path.append("..")

from statser.collector import StatserPsutil as Statser

class TestBasicStatser(unittest.TestCase):
    def test_init(self):
        a = Statser(prefix="balls")
        self.assertEqual(a.conf["prefix"],"balls")
    def test_add_data(self):
        a = Statser()
        a.add_data("aids","balls")
        self.assertTrue(a.db)
        self.assertEqual(a.db[0]["name"],"aids")
        self.assertEqual(a.db[0]["data"],"balls")
    def test_clean(self):
        a = Statser()
        a.add_data("aids","balls")
        a.clean_db()
        self.assertFalse(a.db)


if __name__ == '__main__':
        unittest.main()
