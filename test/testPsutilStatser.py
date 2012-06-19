import unittest
import sys
import platform
sys.path.append("..")

from Statser import Statser

class TestPsutilStatser(unittest.TestCase):
    def test_collect_disk(self):
        s = Statser()
        s.collect_disk_io()
        self.assertTrue(s.db)
    def test_collect_disk_whitelist(self):
        s = Statser()
        if platform.system() == "Windows":
          d = "PhysicalDrive0"
        else:
          d = "sda1"
        s.collect_disk_io([d])
        self.assertTrue(s.db)
        for e in s.db:
            # make sure that every entry has only sda1 in the name
            self.assertTrue(d in e["name"])

    def test_collect_network(self):
        s = Statser()
        s.collect_network_io()
        self.assertTrue(s.db)

    def test_collect_network_whitelist(self):
        s = Statser()
        needle="lo"
        if platform.system() == "Windows":
          lo="MS TCP Loopback interface"
          needle=lo.replace(" ","_")
        else:
          lo="lo"
        s.collect_network_io([lo])
        self.assertTrue(s.db)
        for e in s.db:
            self.assertTrue(needle in e["name"])

    def test_collect_disk_usage(self):
        s = Statser()
        s.collect_disk_usage()
        self.assertTrue(s.db)
    

    def test_collect_disk_usage_root(self):
        """
        test both, translation of the name / to root and the whitelist
        """
        s = Statser()
        needle="root"
        if platform.system() == "Windows":
          s.collect_disk_usage("C:\\\\")
          needle="C"
        else:
          s.collect_disk_usage("/")

        self.assertTrue(s.db)
        for e in s.db:
            self.assertTrue(needle in e["name"])

if __name__ == '__main__':
        unittest.main()
