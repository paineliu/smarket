from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDateTime, QTimer, Qt
import sys
from smarket import SMarket
from product import Product

class SMarketWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.smarket = SMarket()
        self.setWindowTitle("无人超市")
        self.setup_ui()
        self.pause = False
        self.lst_message = []

    def setup_ui(self):
        
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu("文件(&F)")
        act_start = file_menu.addAction(QIcon("./icons/start.png"), "启动(&S)")
        act_pause = file_menu.addAction(QIcon("./icons/pause.png"), "暂停(&P)")
        act_reset = file_menu.addAction(QIcon("./icons/reset.png"), "复位(&R)") 
        act_exit  = file_menu.addAction(QIcon("./icons/exit.png"), "退出(&X)")

        file_toolBar = self.addToolBar("文件")
        file_toolBar.addAction(act_start)
        file_toolBar.addAction(act_pause)
        file_toolBar.addAction(act_reset)
        file_toolBar.addAction(act_exit)
        
        act_start.triggered.connect(self.on_act_start)
        act_reset.triggered.connect(self.on_act_reset)
        act_exit.triggered.connect(self.on_act_exit)
        act_pause.triggered.connect(self.on_act_pause)

        self.statusBar = self.statusBar()
        self.label_status = QLabel("版本号：1.0")
        self.statusBar.addPermanentWidget(self.label_status)

        self.setGeometry(300,300,800,200)
        self.label_custom=QLabel("顾客：")
        self.button_enter=QPushButton("进入超市")
        self.button_leave=QPushButton("离开超市")

        self.label_help=QLabel("咨询：")       
        self.button_greeting=QPushButton("问候")
        self.button_where_milk=QPushButton("酸奶在哪")
        self.button_where_cola=QPushButton("可乐在哪")
        
        self.label_shop=QLabel("购物：")       
        self.button_buy_cola=QPushButton("购买可乐")
        self.button_buy_milk=QPushButton("购买酸奶")
        self.button_checkout=QPushButton("结算")

        self.label_fan=QLabel("空调：")       
        self.button_fan_open=QPushButton("打开空调")
        self.button_fan_close=QPushButton("关闭空调")
  
        self.label_fire=QLabel("火情：")       
        self.button_fire_open=QPushButton("启动火情")
        self.button_fire_close=QPushButton("关闭火情")

        self.label_forbid=QLabel("入侵：")       
        self.button_forbid_open=QPushButton("启动警报")
        self.button_forbid_close=QPushButton("关闭警报")

        self.label_status=QLabel("状态：")       
        self.label_status_content=QLabel("\n\n\n\n\n\n\n\n\n\n")
        self.label_status_content.setAlignment(Qt.AlignmentFlag.AlignJustify) 

        self.button_enter.clicked.connect(self.on_act_enter)
        self.button_leave.clicked.connect(self.on_act_leave)

        self.button_greeting.clicked.connect(self.on_act_greeting)
        self.button_where_cola.clicked.connect(self.on_act_where_cola)
        self.button_where_milk.clicked.connect(self.on_act_where_milk)

        self.button_buy_cola.clicked.connect(self.on_act_buy_cola)
        self.button_buy_milk.clicked.connect(self.on_act_buy_milk)
        self.button_checkout.clicked.connect(self.on_act_checkout)

        self.button_fan_open.clicked.connect(self.on_act_fan_open)
        self.button_fan_close.clicked.connect(self.on_act_fan_close)

        self.button_fire_open.clicked.connect(self.on_act_fire_open)
        self.button_fire_close.clicked.connect(self.on_act_fire_close)

        self.button_forbid_open.clicked.connect(self.on_act_forbid_open)
        self.button_forbid_close.clicked.connect(self.on_act_forbid_close)

        lay_main = QVBoxLayout()
        lay1=QHBoxLayout()
        lay1.addWidget(self.label_custom, stretch=1)
        lay1.addWidget(self.button_enter, stretch=3)
        lay1.addWidget(self.button_leave, stretch=3)

        lay2=QHBoxLayout()
        lay2.addWidget(self.label_help, stretch=1)
        lay2.addWidget(self.button_where_cola, stretch=2)
        lay2.addWidget(self.button_where_milk, stretch=2)
        lay2.addWidget(self.button_greeting, stretch=2)
        
        lay3=QHBoxLayout()
        lay3.addWidget(self.label_shop, stretch=1)
        lay3.addWidget(self.button_buy_cola, stretch=2)
        lay3.addWidget(self.button_buy_milk, stretch=2)
        lay3.addWidget(self.button_checkout, stretch=2)

        lay4=QHBoxLayout()
        lay4.addWidget(self.label_fan, stretch=1)
        lay4.addWidget(self.button_fan_open, stretch=3)
        lay4.addWidget(self.button_fan_close, stretch=3)

        lay5=QHBoxLayout()
        lay5.addWidget(self.label_fire, stretch=1)
        lay5.addWidget(self.button_fire_open, stretch=3)
        lay5.addWidget(self.button_fire_close, stretch=3)

        lay6=QHBoxLayout()
        lay6.addWidget(self.label_forbid, stretch=1)
        lay6.addWidget(self.button_forbid_open, stretch=3)
        lay6.addWidget(self.button_forbid_close, stretch=3)

        lay7=QHBoxLayout()
        lay7.addWidget(self.label_status, stretch=1)
        lay7.addWidget(self.label_status_content, stretch=6)

        lay_main.addLayout(lay1)
        lay_main.addLayout(lay2)
        lay_main.addLayout(lay3)
        lay_main.addLayout(lay4)
        lay_main.addLayout(lay5)
        lay_main.addLayout(lay6)
        lay_main.addLayout(lay7)


        widget=QWidget()
        widget.setLayout(lay_main)
        self.setCentralWidget(widget)

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.onTimer)

        self.timer.start(200)

    def onTimer(self):
        if not self.pause:
            state_map = self.smarket.detect()
            if 'message' in state_map:
                self.lst_message.insert(0, state_map['message'])
                self.lst_message = self.lst_message[0:10]
                self.label_status_content.setText('\n'.join(self.lst_message))

    def on_act_start(self):
        if not self.smarket.is_running():
            self.smarket.start()

    def on_act_reset(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.reset_all()

    def on_act_pause(self):
        self.pause = not self.pause

    def on_act_exit(self):

        self.smarket.clean()
        self.close()

    def on_act_enter(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.user_enter()
        # self.statusBar.showMessage("on_act_enter", 5000)

    def on_act_leave(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.user_leave()
        # self.statusBar.showMessage("on_act_leave", 5000)

    def on_act_greeting(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.hello()
        # self.statusBar.showMessage("on_act_greeting", 5000)

    def on_act_where_cola(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.find(Product.COLA)
        # self.statusBar.showMessage("on_act_where_cola", 5000)

    def on_act_where_milk(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.find(Product.MILK)
        # self.statusBar.showMessage("on_act_where_milk", 5000)

    def on_act_buy_cola(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.buy(Product.COLA)
        
    def on_act_buy_milk(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.buy(Product.MILK)
        # self.statusBar.showMessage("on_act_buy_milk", 5000)

    def on_act_checkout(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.pay()
        # self.statusBar.showMessage("on_act_checkout", 5000)

    def on_act_fan_open(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.fan_on()
        # self.statusBar.showMessage("on_act_fan_open", 5000)

    def on_act_fan_close(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.fan_off()
        # self.statusBar.showMessage("on_act_fan_close", 5000)

    def on_act_fire_open(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.flame_on()
        # self.statusBar.showMessage("on_act_fire_open", 5000)

    def on_act_fire_close(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.flame_off()
        # self.statusBar.showMessage("on_act_fire_close", 5000)

    def on_act_forbid_open(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.forbid_on()
        # self.statusBar.showMessage("on_act_forbid_open", 5000)

    def on_act_forbid_close(self):
        if not self.smarket.is_running():
            QMessageBox.information(self, "提示", "请先启动无人超市！")
            return
        self.smarket.forbid_off()
        # self.statusBar.showMessage("on_act_forbid_close", 5000)

    # def onbutton(self):
    #     QMessageBox.information(self, "弹出", "tt")

if __name__ == "__main__":

    app = QApplication(sys.argv)
    win =SMarketWindow()
    win.show()
    app.exec()
