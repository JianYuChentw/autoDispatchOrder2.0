from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from .labelWidget import LabelWidget
from .statusBar import StatusBar
from .buttonPanel import ButtonPanel

class FrontPage(QWidget):
    def __init__(self, status_manager):
        super().__init__()

        self.setWindowTitle('首頁')
        self.resize(1000, 600)

        # 主布局 - 水平和垂直居中
        outer_layout = QHBoxLayout()  # 外層水平方向佈局
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 水平居中

        main_layout = QVBoxLayout()  # 垂直佈局
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 垂直居中

        # 添加组件到主布局
        label_widget = LabelWidget()
        status_bar = StatusBar(status_manager)  # 傳遞狀態管理器到 StatusBar
        button_panel = ButtonPanel()

        main_layout.addWidget(label_widget)
        main_layout.addLayout(status_bar)
        main_layout.addWidget(button_panel)

        outer_layout.addLayout(main_layout)  # 把垂直佈局加入到水平方向的佈局中

        self.setLayout(outer_layout)  # 將外層佈局設定為主佈局
