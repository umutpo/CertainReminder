import getpass
import os

USER_NAME = getpass.getuser()
file_path = os.path.dirname(os.path.realpath(__file__)) + '\\app.exe'
bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
with open(bat_path + '\\' + "CertainReminder.bat", "w+") as bat_file:
    bat_file.write(r'start "" "%s"' % file_path)
    