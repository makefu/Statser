from time import sleep
import threading
import sys
from collector import StatserPsutil
class BasicMessageDaemon(StatserPsutil, threading.Thread):
    def __init__(self,**kwargs):
        StatserPsutil.__init__(self,**kwargs)
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
        self.interval=kwargs.get("interval",10) #seconds

    def run(self):
        while not self.stopevent.isSet():
            self.collect_all()
            print self._write_graphite_msg(self.db)
            self.clean_db()
            sleep(self.interval)

    def stop(self):
        self.stopevent.set()

if __name__ == "__main__":
    a = BasicDaemon()
    a.start()
    #sleep(20)
    #a.stop()
