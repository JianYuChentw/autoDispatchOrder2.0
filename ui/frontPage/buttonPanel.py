from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
class ButtonPanel(QFrame):
    def __init__(self):
        super().__init__()
        button_layout = QVBoxLayout()
        button_layout.setSpacing(30)

        # 創建按鈕並設置固定大小
        systenLogin = QPushButton('系統登入')
        systenLogin.setFixedSize(200, 50)
        systenLogin.setStyleSheet("font-size: 22px;")

        fileTranslate = QPushButton('文件轉換')
        fileTranslate.setFixedSize(200, 50)
        fileTranslate.setStyleSheet("font-size: 22px;")

        fastAction = QPushButton('快速執行')
        fastAction.setFixedSize(200, 50)
        fastAction.setStyleSheet("font-size: 22px;")

        # 添加按鈕到按鈕布局
        button_layout.addWidget(systenLogin, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(fileTranslate, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(fastAction, alignment=Qt.AlignmentFlag.AlignCenter)

        

        # 將按鈕布局設置到按鈕框架中
        self.setLayout(button_layout)
