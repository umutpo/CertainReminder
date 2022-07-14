import tkinter
from tkinter import messagebox
import time
import threading

USER_INPUT_WAIT_TEXT = "What would you like to do?\n1) Set Reminder 2) Delete Reminder 3) List Reminders 4) Quit"
USER_INPUT_REMINDER_TEXT = "What is the reminder?"
USER_INPUT_HOUR_TEXT = "What time would you like to set for this reminder? Please enter in 24-hour format(hh:mm)"
USER_INPUT_DELETE_TEXT = "Enter the reminder's number you would like to delete:"
LIST_REMINDERS_TITLE_TEXT = "Current active reminders:"

def show_warning(reminder):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes("-topmost", 1)
    messagebox.showwarning("Reminder", reminder)

class TimerThread(threading.Thread):
    should_quit = False
    reminders = []

    def __init__(self):
        super(TimerThread, self).__init__()
    
    def run(self):
        while True:
            time.sleep(1)
            for i in range(len(self.reminders)):
                self.reminders[i][2] -= 1
                if self.reminders[i][2] <= 0:
                    show_warning(self.reminders[i][0])
                    self.removeReminder(i)
            if self.should_quit:
                break
    
    def addReminder(self, reminder, timer):
        # Time format is hh:mm
        hour_difference = int(timer[0:2]) - time.localtime().tm_hour
        minute_difference = int(timer[3:5]) - time.localtime().tm_min
        second_difference = 0 - time.localtime().tm_sec
        timer_time = hour_difference * 3600 + minute_difference * 60 + second_difference
        self.reminders.append([reminder, timer, timer_time])
    
    def removeReminder(self, index):
        self.reminders.pop(index)
    
    def getReminders(self):
        return self.reminders
    
    def quit(self):
        self.should_quit = True
    
def main():
    timerThread = TimerThread()
    timerThread.start()
    
    def listReminders():
        reminders = timerThread.getReminders()
        if len(reminders):
            for i in range(len(reminders)):
                print("Reminder " + str(i + 1) + ": " + reminders[i][0] + " set for " + reminders[i][1])
        else:
            print("None")
    
    while True:
        try:
            print(USER_INPUT_WAIT_TEXT)
            user_choice = input("> ")
            match user_choice:
                case '1':
                    print(USER_INPUT_REMINDER_TEXT)
                    reminder = input("> ")
                    print(USER_INPUT_HOUR_TEXT)
                    timer = input("> ")
                    print("Setting \"" + reminder + "\" for " + timer)
                    timerThread.addReminder(reminder, timer)
                case '2':
                    print(LIST_REMINDERS_TITLE_TEXT)
                    listReminders()
                    print(USER_INPUT_DELETE_TEXT)
                    deleted_index = input("> ")
                    timerThread.removeReminder(int(deleted_index) - 1)
                case '3':
                    print(LIST_REMINDERS_TITLE_TEXT)
                    listReminders()
                case '4':
                    print("Goodbye!")
                    break
        except KeyboardInterrupt:
            print("Interrupted")
            break
    
    timerThread.quit()

if __name__ == '__main__':
    main()