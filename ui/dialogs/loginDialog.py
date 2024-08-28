from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QCheckBox, QHBoxLayout
from PyQt6.QtCore import Qt
import os

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
