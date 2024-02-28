from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDateTime, QTimer
import sys
from functools import partial
# from smarket import SMarket

class partialslot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.smarket = SMarket()
        # self.smarket.start()
        self.setWindowTitle("无人超市")
        self.setupUI()

    def act_exit_triggered(self):
        self.statusBar.showMessage("退出", 5000)
        self.close()

    def setupUI(self):
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu("文件(&F)")
        act_start = file_menu.addAction(QIcon("./icons/start.png"), "启动(&S)")
        act_reset = file_menu.addAction(QIcon("./icons/reset.png"), "复位(&R)")
        act_exit = file_menu.addAction(QIcon("./icons/exit.png"), "退出(&X)")
        act_exit.triggered.connect(self.act_exit_triggered)

        file_toolBar = self.addToolBar("文件")
        file_toolBar.addAction(act_start)
        file_toolBar.addAction(act_reset)
        file_toolBar.addAction(act_exit)
        self.statusBar = self.statusBar()
        label = QLabel("版本号：1.0")
        self.statusBar.addPermanentWidget(label)
        self.setGeometry(300,300,400,200)
        self.b1=QLabel("顾客：")
        self.b2=QPushButton("进入超市")
        self.b5=QPushButton("离开超市")
        self.b12=QLabel("咨询：")       
        self.b121=QPushButton("问候")
        self.b122=QPushButton("牛奶在哪")
        self.b123=QPushButton("可乐在哪")
        self.b13=QLabel("购物：")       
        self.b131=QPushButton("购买可乐")
        self.b132=QPushButton("购买牛奶")
        self.b133=QPushButton("结算")

        self.b14=QLabel("空调：")       
        self.b141=QPushButton("打开空调")
        self.b142=QPushButton("关闭空调")
  
        self.b15=QLabel("火情：")       
        self.b151=QPushButton("启动火情")
        self.b152=QPushButton("关闭火情")

        self.b16=QLabel("入侵：")       
        self.b161=QPushButton("启动警报")
        self.b162=QPushButton("关闭警报")

        self.b17=QLabel("状态：")       
        self.b171=QLabel("0 02 33   555 555 3")
        self.b2.clicked.connect(partial(self.onbutton,20,-40))

        lay_main = QVBoxLayout()
        lay=QHBoxLayout()
        lay.addWidget(self.b1)
        lay.addWidget(self.b2)
        lay.addWidget(self.b5)
        lay2=QHBoxLayout()
        lay2.addWidget(self.b12)
        lay2.addWidget(self.b121)
        lay2.addWidget(self.b122)
        lay2.addWidget(self.b123)
        lay3=QHBoxLayout()
        lay3.addWidget(self.b13)
        lay3.addWidget(self.b131)
        lay3.addWidget(self.b132)
        lay3.addWidget(self.b133)

        lay4=QHBoxLayout()
        lay4.addWidget(self.b14)
        lay4.addWidget(self.b141)
        lay4.addWidget(self.b142)

        lay5=QHBoxLayout()
        lay5.addWidget(self.b15)
        lay5.addWidget(self.b151)
        lay5.addWidget(self.b152)

        lay6=QHBoxLayout()
        lay6.addWidget(self.b16)
        lay6.addWidget(self.b161)
        lay6.addWidget(self.b162)

        lay7=QHBoxLayout()
        lay7.addWidget(self.b17)
        lay7.addWidget(self.b171)

        lay_main.addLayout(lay)
        lay_main.addLayout(lay2)
        lay_main.addLayout(lay3)
        lay_main.addLayout(lay4)
        lay_main.addLayout(lay5)
        lay_main.addLayout(lay6)
        lay_main.addLayout(lay7)

        m=QWidget()
        m.setLayout(lay_main)
        self.setCentralWidget(m)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.onTimer)

        self.timer.start(100)

    def onTimer(self):
        # self.smarket.detect()
        pass
 
    def onbutton(self,m,n):
        print("m+n=",m+n)
        QMessageBox.information(self,"���",str(m+n))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =partialslot()
    p.show()
    app.exec()
