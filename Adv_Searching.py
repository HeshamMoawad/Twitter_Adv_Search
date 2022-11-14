
from PyQt5 import QtCore, QtWidgets 
from MyPyQt5 import  QSideMenuNewStyle ,MyThread
from pages import Page1 , Page2 
from mainclass import Twitter

class MyMainWindow(object):


    def Setup(self,MainWindow:QtWidgets.QMainWindow):
        MainWindow.resize(800,600)
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
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


        self.ButtonDashBoard = self.Menu.GetButton(0)
        self.ButtonDashBoard.setText("DashBoard")
        self.ButtonDashBoard.setFixedHeight(40)
        self.ButtonAcc = self.Menu.GetButton(1)
        self.ButtonAcc.setText("Accounts")
        self.ButtonAcc.setFixedHeight(40)
        self.Page1Class = Page1(FirstPageMenu)
        self.Page2Class = Page2(SecPageMenu)

################  Connections And Signals And Thread
        self.Thread = Thread()
        
        self.Thread.statues.connect(self.Menu.MainLabel.setText)
        # self.Thread.Twitter.LeadSignal.connect(self.Page1Class.treewidget.appendData)

        self.ButtonDashBoard.clicked.connect(lambda : self.Menu.setCurrentPage(0))
        self.ButtonAcc.clicked.connect(lambda : self.Menu.setCurrentPage(1))
        self.Page1Class.StartButton.clicked.connect(self.Thread.start)
        self.Page1Class.StopButton.clicked.connect(lambda : self.Thread.kill(True,self.Thread.Twitter))
################ Important to Run --------------

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        



class Thread(MyThread):
    

    def run(self) -> None:
        self.statues.emit("Starting")
        self.Twitter = Twitter(ui.Menu.Hidetoggle.isChecked())
        self.Twitter.LeadSignal.connect(ui.Page1Class.treewidget.appendData)
        if ui.Page1Class.lineEdit.isEnabled():
            self.statues.emit("Start Scrape Links From Handle")
            self.Twitter.search_URL_handle(ui.Page1Class.lineEdit.text())

        else: 
            if ui.Page1Class.KeyWordLineEdit.isEnabled() :
                keyword = ui.Page1Class.KeyWordLineEdit.text()
                self.statues.emit(f"Start Scrape Links From KeyWord {keyword}")
                for type in [self.Twitter.TYPE_TOP,self.Twitter.TYPE_LATEST,self.Twitter.TYPE_PHOTO,self.Twitter.TYPE_VEDIO]:
                    self.Twitter.search_URL_KeyWord(keyword,type,self.Twitter.WA_REGEX)

        
        
        





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.Setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
