from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFrame, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from .statusBar import StatusManager
from service.autoService import loginGetToken
from ui.dialogs.loginDialog import LoginDialog

class ButtonPanel(QFrame):
    def __init__(self, stack_widget, status_manager):
        super().__init__()
        self.stack_widget = stack_widget
        self.status_manager = status_manager
        button_layout = QVBoxLayout()
        button_layout.setSpacing(25)

        # 創建按鈕並設置固定大小
        systenLogin = QPushButton('系統登入')
        systenLogin.setFixedSize(200, 50)
        systenLogin.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        systenLogin.clicked.connect(self.login_action)

        fileTranslate = QPushButton('文件轉換')
        fileTranslate.setFixedSize(200, 50)
        fileTranslate.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                background-color: #A6A6D2;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #9999CC;
            }
        """)
        fileTranslate.clicked.connect(self.navigate_to_file_translate_page)  # 連接文件轉換按鈕的點擊事件

        fastAction = QPushButton('快速執行')
        fastAction.setFixedSize(200, 50)
        fastAction.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                background-color: #FF5151;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #FF2D2D;
            }
        """)
        fastAction.clicked.connect(self.show_processing_page)

        # 添加按鈕到按鈕布局
        button_layout.addWidget(systenLogin, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(fileTranslate, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(fastAction, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(button_layout)

    def login_action(self):
        # 創建並顯示登入對話框
        dialog = LoginDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_credentials()

            # 構建 payload
            payload = {
                "Account": username,
                "Password": password,
                "AppKey": os.getenv('APPKEY')
            }

            # 調用 loginGetToken 來獲取 token
            token = loginGetToken(payload)
            if token:
                self.status_manager.update_login_status("已登入")
                self.status_manager.token = token  # 保存 token

                # 更新環境變數
                os.environ['USER_ACCOUNT'] = username
                os.environ['USER_PASSWORD'] = password
            else:
                QMessageBox.warning(self, '登入失敗', '帳號或密碼錯誤，請重試。')

    def show_processing_page(self):
        # 檢查是否已經有 token
        if not self.status_manager.token:
            message_box = QMessageBox(self)
            message_box.setWindowTitle('需要登入')
            message_box.setText('請先進行系統登入。')
            
            # 使用自定義圖示
            pixmap = QPixmap('ui/img/crossIcon.png')
            message_box.setIconPixmap(pixmap)
            
            message_box.exec()
            return
        
        # 如果有 token，切換到處理頁面
        self.stack_widget.setCurrentIndex(1)

    def navigate_to_file_translate_page(self):
        # 無論是否已經登入，都可以切換到文件轉換頁面
        self.stack_widget.setCurrentIndex(2)  # 假設文件轉換頁面的索引為2
