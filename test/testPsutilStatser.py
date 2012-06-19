import unittest
import sys
sys.path.append("..")

from Statser import Statser

class TestBasicStatser(unittest.TestCase):
    def test_collect_disk(self):
        s = Statser()
        s.collect_disk_io()
        self.assertTrue(s.db)
    def test_collect_disk_whitelist(self):
        s = Statser()
        s.collect_disk_io(["sda1"])
        self.assertTrue(s.db)
        for e in s.db:
            # make sure that every entry has only sda1 in the name
            self.assertTrue("sda1" in e["name"])

    def test_collect_network(self):
        s = Statser()
        s.collect_network_io()
        self.assertTrue(s.db)

    def test_collect_disk_whitelist(self):
        s = Statser()
        s.collect_network_io(["lo"])
        self.assertTrue(s.db)
        for e in s.db:
            self.assertTrue("lo" in e["name"])

    def test_collect_disk_usage(self):
        s = Statser()
        s.collect_disk_usage()
        self.assertTrue(s.db)
    

    def test_collect_disk_usage_root(self):
        """
        test both, translation of the name / to root and the whitelist
        """
        s = Statser()
        s.collect_disk_usage("/")
        self.assertTrue(s.db)
        for e in s.db:
            self.assertTrue("root" in e["name"])

if __name__ == '__main__':
        unittest.main()
