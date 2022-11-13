
from PyQt5 import QtCore, QtWidgets
from MyPyQt5 import  QSideMenuNewStyle ,MyThread
from pages import Page1 , Page2 


class MyMainWindow(object):


    def Setup(self,MainWindow:QtWidgets.QMainWindow):
        MainWindow.resize(600,600)

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

################  Connections And Signals 

        self.ButtonDashBoard.clicked.connect(lambda : self.Menu.setCurrentPage(0))
        self.ButtonAcc.clicked.connect(lambda : self.Menu.setCurrentPage(1))

################ Important to Run --------------

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        



class Thread(MyThread):

    def run(self) -> None:
        
        pass





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.Setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
