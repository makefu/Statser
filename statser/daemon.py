from time import sleep
import threading
import sys
from collector import StatserPsutil
class BasicMessageDaemon(StatserPsutil, threading.Thread):
    def __init__(self,**conf):
        StatserPsutil.__init__(self,**conf)
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
	if not "interval" in self.conf: self.conf["interval"] = 10#seconds

    def run(self):
        while not self.stopevent.isSet():
            self.collect_all()
            print self._write_graphite_msg(self.db)
            self.clean_db()
            sleep(self.conf["interval"])

    def stop(self):
        self.stopevent.set()

class GraphiteDaemon(StatserPsutil, threading.Thread):
    def __init__(self,**conf):
        """
	Graphite daemon uses:
	   interval (default 10)
	"""
        StatserPsutil.__init__(self,**conf)
	if not "interval" in self.conf: self.conf["interval"] = 10#seconds
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
	try: self.connect_graphite()
	except: log.error("initial connection to graphite failed...")

    def run(self):
        while not self.stopevent.isSet():
            self.collect_all()
            self.send_graphite()
            self.clean_db()
            sleep(self.conf["interval"])
        

    def stop(self):
        self.stopevent.set()
        sleep(self.conf["interval"])
        

if __name__ == "__main__":
    a = GraphiteDaemon(conf_file="statser.json")
    a.start()
    sleep(10)
    a.stop()
