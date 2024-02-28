from PySide6.QtWidgets import *
from PySide6.QtCore import QDateTime, QTimer
import sys
from functools import partial
from smarket import SMarket

class partialslot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.smarket = SMarket()
        self.smarket.start()
        self.setWindowTitle("无人超市")
        self.setGeometry(300,300,400,200)
        self.b1=QPushButton("启动")
        self.b2=QPushButton("关闭")
        self.b3=QPushButton("打开空调")
        self.b4=QPushButton("关闭空调")
        self.b1.clicked.connect(partial(self.onbutton,10,20))
        self.b2.clicked.connect(partial(self.onbutton,20,-40))
        lay_main = QVBoxLayout()
        lay=QHBoxLayout()
        lay.addWidget(self.b1)
        lay.addWidget(self.b2)
        lay2=QHBoxLayout()
        lay2.addWidget(self.b3)
        lay2.addWidget(self.b4)
        l1 = QWidget()
        l1.setLayout(lay)
        l2 = QWidget()
        l2.setLayout(lay2)

        lay_main.addWidget(l1)
        lay_main.addWidget(l2)
        lay_main.addWidget(l2)
        m=QWidget()
        m.setLayout(lay_main)
        self.setCentralWidget(m)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.onTimer)

        self.timer.start(100)

    def onTimer(self):
        self.smarket.detect()
        pass
 
    def onbutton(self,m,n):
        print("m+n=",m+n)
        QMessageBox.information(self,"���",str(m+n))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =partialslot()
    p.show()
    app.exec()

# app = QApplication([])

# widget = QWidget()
# widget.setGeometry(300,300,400,200)

# layout = QHBoxLayout(widget)

# button1=QPushButton('Open')
# button2=QPushButton('Close')

# layout.addWidget(button1)
# layout.addWidget(button2)

# widget.show()

# app.exec()