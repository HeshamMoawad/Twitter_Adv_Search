
from PyQt5 import QtCore, QtWidgets
import typing , pyperclip
from datetime import datetime
from MyPyQt5 import MyQTreeWidget , MyCustomContextMenu , MyMessageBox
# from PyQt5.QtGui import QKeySequence


class Page1(object):

    def __init__(self,parent:typing.Optional[QtWidgets.QWidget]):
        self.parent = parent
        self.msg = MyMessageBox()
        self.Name = ""
        self.verticalLayout = QtWidgets.QVBoxLayout(parent)
        self.HandleFrame = QtWidgets.QFrame(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.HandleFrame.sizePolicy().hasHeightForWidth())
        self.HandleFrame.setSizePolicy(sizePolicy)
        self.HandleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.HandleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.HandleFrame)
        self.HandleLabel = QtWidgets.QLabel(self.HandleFrame) # HandleLabel
        self.HandleLabel.setText("Handle")
        self.HandleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout.addWidget(self.HandleLabel)
        self.lineEdit = QtWidgets.QLineEdit(self.HandleFrame)
        self.lineEdit.setStyleSheet("background-color:white;color:black;")
        self.lineEdit.setPlaceholderText("@Handle ......")
        self.lineEdit.textChanged.connect(self.text_Changed_Slot_handle)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setStretch(0,1)
        self.horizontalLayout.setStretch(1,3)
        self.verticalLayout.addWidget(self.HandleFrame)
#################################  sec Frame (KeyWord_Frame)
        
        self.KeyWord_Frame = QtWidgets.QFrame(parent)
        self.KeyWord_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.KeyWord_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.KeyWord_Frame)
        self.KeyWordLabel = QtWidgets.QLabel(self.KeyWord_Frame)
        self.KeyWordLabel.setText("KeyWord")
        self.KeyWordLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_3.addWidget(self.KeyWordLabel)
        self.KeyWordLineEdit = QtWidgets.QLineEdit(self.KeyWord_Frame)
        self.KeyWordLineEdit.setPlaceholderText("KeyWord Here .....")
        self.KeyWordLineEdit.setStyleSheet("background-color:white;color:black;")
        self.KeyWordLineEdit.textChanged.connect( self.text_Changed_Slot_keyword) #self.lineEdit.setDisabled(False) 
        self.horizontalLayout_3.addWidget(self.KeyWordLineEdit)
        self.horizontalLayout_3.setContentsMargins(0,0,0,0)
        self.horizontalLayout_3.setStretch(0,1)
        self.horizontalLayout_3.setStretch(1,3)
        self.verticalLayout.addWidget(self.KeyWord_Frame)


#################################  third Frame (Buttons_Frame)

        self.Buttons_Frame = QtWidgets.QFrame(parent)
        self.Buttons_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Buttons_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Buttons_Frame)
        self.StartButton = QtWidgets.QPushButton(self.Buttons_Frame) # StartButton
        self.StartButton.setFlat(True)
        self.StartButton.setText("Start")
        self.StartButton.setShortcut("Enter")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.StartButton.setSizePolicy(sizePolicy)
        self.StartButton.setDisabled(True)
        self.horizontalLayout_2.addWidget(self.StartButton)
        self.StopButton = QtWidgets.QPushButton(self.Buttons_Frame) # StopButton
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setFlat(True)
        self.StopButton.setText("Stop")
        self.StopButton.setShortcut("space")
        self.horizontalLayout_2.addWidget(self.StopButton)
        self.horizontalLayout_2.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.Buttons_Frame)
        self.CounterLabel = QtWidgets.QLabel(parent)  # CounterLabel
        self.CounterLabel.setText("Counter : 0")
        self.CounterLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.treewidget = MyQTreeWidget(parent)   # TreeWidget 
        self.treewidget.setStyleSheet("background-color:white;color:black;")
        self.treewidget.setColumns(["Links","Handle","Description"])
        self.treewidget.onLengthChanged.connect(self.counter)
        self.treewidget.setColumnWidth(0,250)
        self.treewidget.setColumnWidth(1,100)
        self.treewidget.setColumnWidth(2,250)
        self.treewidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treewidget.customContextMenuRequested.connect(self.menu)
        self.verticalLayout.addWidget(self.treewidget)

        self.verticalLayout.addWidget(self.CounterLabel)

        self.verticalLayout.setContentsMargins(3,3,3,3)
        self.verticalLayout.setStretch(0, 1)  # handle frame
        self.verticalLayout.setStretch(1, 1)  # keyword 
        self.verticalLayout.setStretch(2, 1)  # buttons frame
        self.verticalLayout.setStretch(3, 10) # treewidget
        self.verticalLayout.setStretch(4, 1)  # label count
    
    def setStyleSheet(self,style:str):
        self.parent.setStyleSheet(style)
        
    def text_Changed_Slot_handle(self):
        if self.lineEdit.text().__len__() > 0:
            self.KeyWordLineEdit.setDisabled(True)
            self.StartButton.setDisabled(False)
        else :
            self.KeyWordLineEdit.setDisabled(False)
            self.StartButton.setDisabled(True)

    def text_Changed_Slot_keyword(self):
        if self.KeyWordLineEdit.text().__len__() > 0:
            self.lineEdit.setDisabled(True)
            self.StartButton.setDisabled(False)
        else :
            self.lineEdit.setDisabled(False)
            self.StartButton.setDisabled(True)



    def counter(self,count:int):
        self.CounterLabel.setText(f"Counter : {count}")

    def key(self):
        return self.Name

    def setKey(self,val):
        self.Name = val

    def menu(self):
        menu = MyCustomContextMenu([
        "Copy Link", # 0    
        "Copy Handle", # 1
        "Copy Description", # 2
        "Delete Row" , # 3
        "Export All To Excel", # 4
        "Copy Links List", # 5
        "Copy Handles List", # 6
        "Copy Descriptions List", # 7
        "Copy Links and Handles", # 8
        "Copy All", # 9
        "Clear Results", # 10
        ])
        # menu.connectShortcut(3,QKeySequence("Ctrl+e"))
        menu.multiConnect(functions=[
            lambda : self.copy(0), # 0
            lambda : self.copy(1), # 1
            lambda : self.copy(2), # 2
            self.delete , # 3
            lambda: self.export(self.Name) , # 4
            lambda : pyperclip.copy(self.treewidget.extract_data_to_string(0)) if self.treewidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data In Column !") , # 5
            lambda : pyperclip.copy(self.treewidget.extract_data_to_string(1)) if self.treewidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data In Column !"),  # 6
            lambda : pyperclip.copy(self.treewidget.extract_data_to_string(2)) if self.treewidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data In Column !"), # 7
            lambda: pyperclip.copy(self.treewidget.extract_data_to_DataFrame(range_of=range(0,2)).to_string(index=False)) if self.treewidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data Found !") , # 8
            lambda: pyperclip.copy(self.treewidget.extract_data_to_DataFrame().to_string(index=False)) if self.treewidget._ROW_INDEX != 0 else self.msg.showWarning(text="No Data Found !") , # 9
            self.treewidget.clear , # 10
        ])
        
        menu.show()

    def copy(self , index:int):
        try :
            pyperclip.copy(self.treewidget.currentItem().text(index))
        except :
            self.msg.showWarning(text="No Item Selected please Select one !")

    def delete(self):
        try:
            self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(self.treewidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")

    def export(self,name:typing.Optional[str]):
        if self.treewidget._ROW_INDEX > 0 :
            self.treewidget.extract_data_to_DataFrame().to_excel(f"Data/Exports/{name}[{datetime.now().date()}].xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.now().date()}].xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")

    # def text_connection(self):
    #     self.lineEdit.setDisabled(True) if len(self.lineEdit.text()) > 0 else self.lineEdit.setDisabled(False)


class Page2(object):
    def __init__(self,parent:typing.Optional[QtWidgets.QWidget]) -> None:
        self.groupBox = QtWidgets.QGroupBox(parent) # MainGroupBox
        self.groupBox.setTitle("Accounts")
        self.gridlayout = QtWidgets.QGridLayout(parent) # GridLayout
        self.groupBox.setFixedHeight(100)
        self.vertloayout = QtWidgets.QVBoxLayout(self.groupBox) # VertGroupBoxLayout
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame) # HorFrameLayout 
        self.userlinedit = QtWidgets.QLineEdit(self.frame) # UserLineEdit
        self.userlinedit.setPlaceholderText("UserName in Twitter Account")
        self.horizontalLayout.addWidget(self.userlinedit)
        self.pwdlinedit = QtWidgets.QLineEdit(self.frame) # PwdLineEdit
        self.pwdlinedit.setPlaceholderText("Password in Twitter Account")
        self.horizontalLayout.addWidget(self.pwdlinedit)
        self.vertloayout.addWidget(self.frame)
        self.gridlayout.addWidget(self.groupBox,0,0,QtCore.Qt.AlignmentFlag.AlignTop)

        

