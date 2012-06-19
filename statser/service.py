import win32serviceutil
import win32service
import win32event
import threading
import os
import sys
import time
 
 
        
 
class ServiceLauncher(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Statser'
    _svc_display_name_ ='The Stats Collector Service'
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stopevent = threading.Event()
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stopevent.set() 
    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        from daemon import GraphiteDaemon
        # load config somehow
        daemon = GraphiteDaemon()
        daemon.start()
        self.stopevent.wait()
        daemon.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

        
if __name__=='__main__':
      sys.path.append(os.getcwd())
      win32serviceutil.HandleCommandLine(ServiceLauncher)
