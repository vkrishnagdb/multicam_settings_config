import os
import csv
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys

# Path to the folder you want to monitor
folder_to_monitor = "C:\\path\\to\\your\\folder"

# Path to the CSV file
csv_file = "C:\\path\\to\\your\\csv\\file.csv"

# Function to read the CSV file and store values in a dictionary
def read_csv(csv_file):
    data = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            data[row[0]] = row[1]
    return data

# Function to monitor the folder for new directories or files
def monitor_folder(folder, data):
    while True:
        # Get list of directories and files in the folder
        items = os.listdir(folder)
        for item in items:
            item_path = os.path.join(folder, item)
            if os.path.isdir(item_path):
                try:
                    # Check if the directory name is a numerical value
                    value = int(item)
                    if str(value) in data:
                        new_name = data[str(value)]
                        os.rename(item_path, os.path.join(folder, new_name))
                        servicemanager.LogInfoMsg(f"Renamed directory {item} to {new_name}")
                except ValueError:
                    pass  # Ignore non-numeric directory names
        time.sleep(5)  # Check every 5 seconds

class LunaMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "luna_monitor_service"
    _svc_display_name_ = "Luna Monitor Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        main()

def main():
    # Read data from CSV file
    data = read_csv(csv_file)
    
    # Monitor the folder for new directories or files
    monitor_folder(folder_to_monitor, data)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(LunaMonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(LunaMonitorService)
