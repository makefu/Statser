from time import sleep
import threading
from collector import StatserPsutil
class BasicDaemon(StatserPsutil, threading.Thread):
    def __init__(self,**kwargs):
        StatserPsutil.__init__(self,**kwargs)
        threading.Thread.__init__(self)
        self.stopevent = threading.Event()
        self.interval=10 #seconds

    def run(self):
        while True:
            if self.stopevent.isSet():
                break
            self.collect_all()
            print self._write_graphite_msg(self.db)
            print
            self.clean_db()
            sleep(self.interval)

    def stop(self):
        self.stopevent.set()
        sleep(1)

if __name__ == "__main__":
    a = BasicDaemon()
    a.start()
    sleep(20)
    a.stop()
