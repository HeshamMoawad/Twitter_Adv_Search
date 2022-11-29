
from PyQt5 import QtCore, QtWidgets ,QtGui
from MyPyQt5 import  QSideMenuNewStyle ,MyThread,pyqtSignal ,MyMessageBox
from pages import Page1 , Page2 
from mainclass import Twitter
from styles import Styles
import sqlite3

class MyMainWindow(object):


    def Setup(self,MainWindow:QtWidgets.QMainWindow):
        self.con = sqlite3.connect("Data\Database.db")
        self.cur = self.con.cursor()

        self.MainWindow = MainWindow
        MainWindow.resize(800,600)
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # MainWindow.setWindowIcon(QtGui.QIcon("Data\Icons\Capture.PNG"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.Menu = QSideMenuNewStyle(
            self.centralwidget,
            ButtonsCount = 2 ,
            PagesCount = 2 ,
            ExitButtonIconPath = "Data/Icons/reject.png" ,
            DefultIconPath = "Data\Icons\list.png" , 
            ClickIconPath = "Data/Icons/arrowheads-of-thin-outline-to-the-left.png",
            ButtonsFrameFixedwidth = 150 ,
            MaxButtonIconPath = "Data\Icons\maximize.png",
            MiniButtonIconPath = "Data\Icons\delete.png",
            Mini_MaxButtonIconPath = "Data\Icons\minimize.png",
            )

        FirstPageMenu = self.Menu.GetPage(0)
        SecPageMenu = self.Menu.GetPage(1)
        self.Menu.DarkModetoggle.stateChanged.connect(self.dark_mode)
        self.Menu.MenuButton.setShortcut("Ctrl+m")
        self.ButtonDashBoard = self.Menu.GetButton(0)
        # self.ButtonDashBoard.setStyleSheet("color:#f2dbba;")
        self.ButtonDashBoard.setText("DashBoard")
        self.ButtonDashBoard.setFixedHeight(40)
        self.ButtonAcc = self.Menu.GetButton(1)
        # self.ButtonAcc.setStyleSheet("color:#f2dbba;")
        self.ButtonAcc.setText("Accounts")
        self.ButtonAcc.setFixedHeight(40)
        self.Page1Class = Page1(FirstPageMenu)
        
        self.Page2Class = Page2(SecPageMenu)
        # self.Menu.MenuButton.setStyleSheet(Styles.BUTTON)
        self.Menu.MenuButton.setStyleSheet(Styles.BUTTON)
        self.setStylesheet("color:#f2dbba;background-color:#1d284f;font:13px bold;")
        self.Menu.MenuButton.setStyleSheet(Styles.BUTTON_SIDE_)
        self.ButtonAcc.setStyleSheet(Styles.BUTTON_SIDE_)
        self.ButtonDashBoard.setStyleSheet(Styles.BUTTON_SIDE_)
        self.Page1Class.StartButton.setStyleSheet(Styles.BUTTON_SIDE_)
        self.Page1Class.StopButton.setStyleSheet(Styles.BUTTON_SIDE_)




################  Connections And Signals And Thread
        self.Thread = Thread()
        self.Message = MyMessageBox()
        self.Thread.statues.connect(self.Menu.MainLabel.setText)
        self.Thread.LeadSignal.connect(self.LeadFunc)
        self.Thread.mesg.connect(self.msg)
        # self.Thread.Twitter.LeadSignal.connect(self.Page1Class.treewidget.appendData)

        self.ButtonDashBoard.clicked.connect(lambda : self.Menu.setCurrentPage(0))
        self.ButtonAcc.clicked.connect(lambda : self.Menu.setCurrentPage(1))
        self.Page1Class.StartButton.clicked.connect(self.Thread.start)
        self.Page1Class.StopButton.clicked.connect(lambda : self.Thread.kill(True))
################ Important to Run --------------
        try : 
            requests.get("https://www.google.com")
            self.InterNetConnection = True
        except Exception as e :
            self.InterNetConnection = False 

        if not self.InterNetConnection :
            self.Message.showCritical(text="No InterNetConnection here امشى اطلع بره" ) 
        elif self.InterNetConnection :
            self.Message.showInfo(text="كله under control")

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def exist(self,table,column,val):
        self.cur.execute(f"""SELECT * FROM {table} WHERE {column} = '{val}'; """)
        return True if self.cur.fetchall() != [] else False

    def LeadFunc(self,lead:list):
        if lead[0] != None :
            if not self.exist("links","Link",f"{lead[0]}"):
                self.Page1Class.treewidget.appendData(items=lead)
                try:
                    self.cur.execute(f"""INSERT INTO links ('Link','Handle','Descreption','ID')VALUES("{lead[0]}","{lead[1]}","{lead[2]}","{lead[3]}");""")
                    self.con.commit()
                except Exeption as e:
                    print(e)
                print(f"\n{lead}\n")

        
    def setStylesheet(self,style:str):
        self.MainWindow.setStyleSheet(style)
    def msg (self,text):
        self.Message.showInfo(text=text)

    def dark_mode(self):
        #1d284f
        #white
        if self.Menu.DarkModetoggle.isChecked():
            self.Menu.Hidetoggle.setCheckedColor("#c21919")
            self.Menu.DarkModetoggle.setCheckedColor("#c21919")
            self.setStylesheet("color:white;background-color:black;font:13px bold;")
            self.Menu.MenuButton.setStyleSheet(Styles.BUTTON_SIDE)
            self.ButtonAcc.setStyleSheet(Styles.BUTTON_SIDE)
            self.ButtonDashBoard.setStyleSheet(Styles.BUTTON_SIDE)
            self.Page1Class.StartButton.setStyleSheet(Styles.BUTTON_SIDE)
            self.Page1Class.StopButton.setStyleSheet(Styles.BUTTON_SIDE)
        else:
            self.Menu.MenuButton.setStyleSheet(Styles.BUTTON)
            self.Menu.Hidetoggle.setCheckedColor("#00B0FF")
            self.setStylesheet("color:#f2dbba;background-color:#1d284f;font:13px bold;")
            self.Menu.MenuButton.setStyleSheet(Styles.BUTTON_SIDE_)
            self.ButtonAcc.setStyleSheet(Styles.BUTTON_SIDE_)
            self.ButtonDashBoard.setStyleSheet(Styles.BUTTON_SIDE_)
            self.Page1Class.StartButton.setStyleSheet(Styles.BUTTON_SIDE_)
            self.Page1Class.StopButton.setStyleSheet(Styles.BUTTON_SIDE_)


#1d284f
#white
class Thread(MyThread):
    LeadSignal = pyqtSignal(list)
    mesg = pyqtSignal(str)

    def run(self) -> None:
        if ui.Page1Class.KeyWordLineEdit.text() != "" or ui.Page1Class.lineEdit.text() != "":
            self.statues.emit("Starting")
            self.Twitter = Twitter(ui.Menu.Hidetoggle.isChecked())
            
            self.Twitter.LeadSignal.connect(self.LeadSignal.emit)
            if ui.Page1Class.lineEdit.isEnabled():
                handle = ui.Page1Class.lineEdit.text().replace(" ","")
                self.statues.emit(f"Start Scrape Links From {handle}")
                ui.Page1Class.setKey(handle)
                try:
                    self.Twitter.search_URL_handle(handle)
                except Exception as e :
                    self.mesg.emit(f'Error in Scrape Handle -> \n{e}')
                self.Twitter.exit()
                self.statues.emit("Ended")
                self.mesg.emit("Ended")

            elif ui.Page1Class.KeyWordLineEdit.isEnabled() :
                keyword = ui.Page1Class.KeyWordLineEdit.text()
                ui.Page1Class.setKey(keyword)
                self.statues.emit(f"Start Scrape Links From KeyWord {keyword}")
                for type in [self.Twitter.TYPE_TOP,self.Twitter.TYPE_LATEST,self.Twitter.TYPE_PHOTO,self.Twitter.TYPE_VEDIO]:
                    try:
                        self.Twitter.search_URL_KeyWord(keyword,type,self.Twitter.WA_REGEX)
                    except Exception as e :
                        self.mesg.emit(f'Error in Scrape KeyWord with Type {type} -> \n{e}')
                self.Twitter.exit()
                self.statues.emit("Ended")
                self.mesg.emit("Ended")





if __name__ == "__main__":
    import sys,requests
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(16,16))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(24,24))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(32,32))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(48,48))
    app_icon.addFile('Data\Icons\Capture.PNG', QtCore.QSize(256,256))
    app.setWindowIcon(app_icon)

    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.Setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
