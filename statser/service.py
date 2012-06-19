import win32serviceutil
import win32service
import win32event
import os
import sys
import time
 
 
def main():
    '''
    Modulo principal para windows
    '''
    sys.path.insert(0,os.getcwd())
    from Statser import Statser
        
 
class ServiceLauncher(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Statser'
    _scv_display_name_ ='The Stats Collector Service'
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stopevent = threading.Event()
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stopevent.set() 
    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        from Statser import StatserDaemon
        # load config somehow
        daemon = StatserDaemon()
        daemon.start()
        self.stopevent.wait()
        daemon.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

        
if __name__=='__main__':
      win32serviceutil.HandleCommandLine(ServiceLauncher)
