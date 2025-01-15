import os
import shutil
import logging
import subprocess
import shutil
from win32com.client import Dispatch

class Launcher():
    
    def __init__(self):
        pass

    def get_version_number(self, app_location):
        parser = Dispatch("Scripting.FileSystemObject")
        version = parser.GetFileVersion(app_location)
        return version

    def connect_to_share(self, remote_path, username, password):
        try:
            # NET USE \\gaicreport.corp.castsoftware.com\wwwgaicreport\apps /user:gaicreportwriter PineApple23!!
            # Build the NET USE command to connect to the network share
            net_use_command = f'NET USE {remote_path} /user:{username} {password}'

            # Execute the NET USE command
            subprocess.run(net_use_command, shell=True, check=True)

            print(f"Connected to {remote_path} successfully.\n")
            logging.info(f"Connected to {remote_path} successfully.\n")

        except subprocess.CalledProcessError as e:
            print(f"Error connecting to {remote_path}: {e}\n")
            logging.error(f"Error connecting to {remote_path}: {e}\n")

    def disconnect_from_share(self, remote_path):
        try:
            # Build the NET USE command to disconnect from the network share
            net_use_command = f'NET USE {remote_path} /delete'

            # Execute the NET USE command
            subprocess.run(net_use_command, shell=True, check=True)

            print(f"Disconnected from {remote_path} successfully.\n")
            logging.info(f"Disconnected from {remote_path} successfully.\n")

        except subprocess.CalledProcessError as e:
            print(f"Error disconnecting from {remote_path}: {e}\n")
            logging.error(f"Error disconnecting from {remote_path}: {e}\n")

    def copy_file_to_vm(self, remote_path, local_path, username, password):
        try:
            # Connect to the network share
            self.connect_to_share(remote_path, username, password)

            remote_file = remote_path+r"\Platform_Health_Check.exe"
            # print(remote_file)

            remote_file_version = self.get_version_number(remote_file)

            # print(remote_file_version)

            if os.path.exists(local_path+r"\Platform_Health_Check.exe"):
                local_file_version = self.get_version_number(local_path+r"\Platform_Health_Check.exe")
            else:
                local_file_version = None

            # print(local_file_version)

            if remote_file_version != local_file_version:
                # Copy the file to the local VM
                shutil.copy(remote_file, local_path)
                print(f"Platform_Health_Check.exe Version-{remote_file_version} copied successfully from {remote_path} to {local_path}.\n")
                logging.info(f"Platform_Health_Check.exe Version-{remote_file_version} copied successfully from {remote_path} to {local_path}.\n")
            else:
                print(f"Both {remote_path} and {local_path} has same version-{remote_file_version} of the Platform_Health_Check.exe\n")
                logging.info(f"Both {remote_path} and {local_path} has same version-{remote_file_version} of the Platform_Health_Check.exe\n")


        except FileNotFoundError:
            print(f"Error: The remote file {remote_path} does not exist.\n")
            logging.error(f"Error: The remote file {remote_path} does not exist.\n")
        except Exception as e:
            print(f"Error: {e}\n")
            logging.error(f"Error: {e}\n")
        finally:
            # Disconnect from the network share after copying
            self.disconnect_from_share(remote_path)

if __name__ == "__main__":

    try:
        logging.basicConfig(filename="C:\\CAST\\Platform_Health_Check\\Launcher_Logs.txt", level=logging.INFO, format="%(asctime)s %(message)s", filemode='w')

        local_exe_path = f'C:\\CAST\\Platform_Health_Check' 

        remote_path =r"\\gaicreport.corp.castsoftware.com\wwwgaicreport\apps"
        username = "gaicreportwriter"
        password = "PineApple23!!"
      
        launcher_obj = Launcher()

        launcher_obj.copy_file_to_vm(remote_path, local_exe_path, username, password)
    
    except Exception as e:
        print(f"Error: {e}\n")
        logging.error(f"Error: {e}\n")