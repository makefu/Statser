import unittest
import sys
from time import sleep
sys.path.append("..")
from statser.daemon import BasicMessageDaemon

class TestBasicStatserDaemon(unittest.TestCase):
    def test_core_functionality(self):
        """
        check if the daemon is actually working
        """
        a = BasicMessageDaemon(interval=0.5)
        a.start()
        a.stop()
        self.assertFalse(a.db)
if __name__ == '__main__':
        unittest.main()
