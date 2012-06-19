import win32serviceutil
import win32service
import win32event
import servicemanager as sm
import threading
import os
import sys
import time
 
 
        
 
class ServiceLauncher(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Statser'
    _svc_display_name_ ='Statser Collector Service'
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        sm.LogInfoMsg("sent stop event")
        self.daemon.stop()
        win32event.SetEvent(self.hWaitStop)
        sm.LogInfoMsg("Statser - STOPPED")
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        from daemon import GraphiteDaemon
        # load config somehow
	sm.LogInfoMsg(os.getcwd())
	self.daemon = GraphiteDaemon(conf_file="c:\statser.json")
	
	sm.LogInfoMsg("Statser Started with config : %s" % str(self.daemon.conf))
        try:
          self.daemon.start()
          self.ReportServiceStatus(win32service.SERVICE_RUNNING)
          win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        except Exception,e:
          sm.LogInfoMsg("Exception %s"%str(e))
          self.SvcStop()

        
if __name__=='__main__':
      sys.path.append(os.getcwd())
      win32serviceutil.HandleCommandLine(ServiceLauncher)
