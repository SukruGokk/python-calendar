#@author: Şükrü Erdem Gök
#@date:18/06/2020
#Python 3.8 Windows 10

#CALENDAR

#Lib
from sys import exit, argv
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QInputDialog, QLineEdit, QLabel
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE

#Hide console
the_program_to_hide = GetForegroundWindow()
ShowWindow(the_program_to_hide , SW_HIDE)

#Main gui class
class CalendarDemo(QWidget):

	#Initializer
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        self.setGeometry(0, 0, 400, 350)
        self.activityText = ""
        self.counter = 0
        self.initUI()
        self.setWindowIcon(QIcon('icon.png'))

    #Dialog window to get text
    def getText(self, year, month, day):
        text, okPressed = QInputDialog.getText(self, "ADD ACTIVITY", "ACTIVITY: ", QLineEdit.Normal, "")
        if okPressed and text != '':
           self.activityText = "{} \ {} \ {}   {}".format(year, month, day, text)

    def initUI(self):
    	#Calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setMinimumSize(400, 300)
        self.calendar.setFont(QFont("Berlin Sans FB", 15))

        #Activity Label
        self.activity = QLabel(self)

        self.activity.move(20,310)
        self.activity.setFont(QFont("Berlin Sans FB", 15))

        #If there is no file named activity.txt, it creates
        try:
            activity = open("activity.txt", "r")
            self.activity.setText(activity.read())
            activity.close()

        except:
            activity = open("activity.txt", "w")
            activity.close()

        #If there is no file named save.txt, it creates
        try:
            save = open("save.txt", "r")
            saveLines = save.readlines()
            selectedYear = int(saveLines[0])
            selectedMonth = int(saveLines[1])
            selectedDay = int(saveLines[2])

        except:
            save = open("save.txt", "w")
            save.write("{}\n{}\n{}".format(datetime.now().year, datetime.now().month, datetime.now().day))
            save.close()

            save = open("save.txt", "r")
            saveLines = save.readlines()
            selectedYear = int(saveLines[0])
            selectedMonth = int(saveLines[1])
            selectedDay = int(saveLines[2])

        #If it's first time that user opened this app or there is no save.txt file, select today else select last selected date
        self.calendar.setSelectedDate(QDate(selectedYear, selectedMonth, selectedDay))

        self.calendar.clicked.connect(self.click)


    #Onclick, run this function
    def click(self, qDate):
        save = open("save.txt", "r")
        saveLines = save.readlines()

        #One click
        selectedYear = int(saveLines[0])
        selectedMonth = int(saveLines[1])
        selectedDay = int(saveLines[2])

        #Double click
        if qDate.year() == selectedYear and qDate.month() == selectedMonth and qDate.day() == selectedDay:
            self.getText(selectedYear, selectedMonth, selectedDay)

            self.activity.setProperty("text", self.activityText)
            self.activity.adjustSize()

            activity = open("activity.txt", "w")
            activity.write(self.activityText)
            activity.close()

        file = open("save.txt", "w")
        file.write("{}\n{}\n{}\n".format(qDate.year(), qDate.month(), qDate.day()))
        file.close()

#To run everything
def main():
    app = QApplication(argv)
    demo = CalendarDemo()
    demo.show()
    exit(app.exec_())

if __name__ == "__main__":
	main()