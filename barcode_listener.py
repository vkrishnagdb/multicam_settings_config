import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time

class BarcodeService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BarcodeService"
    _svc_display_name_ = "Barcode Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_running = False

    def main(self):
        while self.is_running:
            # Your barcode processing logic goes here
            print("Barcode processing...")
            time.sleep(5)  # Simulate some work

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(BarcodeService)
