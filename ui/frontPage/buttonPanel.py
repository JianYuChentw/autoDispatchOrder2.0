from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFrame, QDialog, QLabel, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox, QCheckBox, QHBoxLayout
from PyQt6.QtCore import Qt
import os
from service.autoService import loginGetToken

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('登入')

        layout = QVBoxLayout()

        # 創建表單布局
        form_layout = QFormLayout()

        # 從環境變數讀取帳號和密碼
        default_username = os.getenv('USER_ACCOUNT', '')
        default_password = os.getenv('USER_PASSWORD', '')

        # 帳號輸入
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('請輸入帳號')
        self.username_input.setText(default_username)
        form_layout.addRow('帳號:', self.username_input)

        # 密碼輸入和顯示/隱藏密碼的按鈕
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # 設置為密碼模式
        self.password_input.setPlaceholderText('請輸入密碼')
        self.password_input.setText(default_password)

        # 顯示/隱藏密碼的按鈕
        self.show_password_checkbox = QCheckBox("顯示密碼")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # 組合密碼框和顯示/隱藏按鈕
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_checkbox)
        form_layout.addRow('密碼:', password_layout)

        layout.addLayout(form_layout)

        # 創建提交和取消按鈕
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()

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
        systenLogin.setStyleSheet("font-size: 22px;")
        systenLogin.clicked.connect(self.login_action)

        fileTranslate = QPushButton('文件轉換')
        fileTranslate.setFixedSize(200, 50)
        fileTranslate.setStyleSheet("font-size: 22px;")

        fastAction = QPushButton('快速執行')
        fastAction.setFixedSize(200, 50)
        fastAction.setStyleSheet("font-size: 22px;")
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
            if token == None:
                self.status_manager.update_login_status("未登入")
                QMessageBox.warning(self, '登入失敗', '帳號或密碼錯誤，請重試。')

    def show_processing_page(self):
        # 切換到處理頁面
        self.stack_widget.setCurrentIndex(1)
