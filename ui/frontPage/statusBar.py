from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, QObject

class StatusBar(QHBoxLayout):
    def __init__(self, status_manager):
        super().__init__()
        self.status_manager = status_manager
        self.setSpacing(30)
        
        # 登入狀態標籤
        self.login_status_label = QLabel(f"登入狀態：{self.status_manager.get_login_status()}")
        self.login_status_label.setStyleSheet("font-size: 16px;")
        self.addWidget(self.login_status_label)

        # 文件處理狀態標籤
        self.file_status_label = QLabel(f"文件狀態：{self.status_manager.get_file_status()}")
        self.file_status_label.setStyleSheet("font-size: 16px;")
        self.addWidget(self.file_status_label)

        # 預留按鈕
        self.reserved_button = QPushButton("預留按鈕")
        self.reserved_button.setFixedSize(150, 40)
        self.reserved_button.setStyleSheet("font-size: 16px;")
        self.addWidget(self.reserved_button)

        # 連接狀態管理器的信號到更新方法
        self.status_manager.status_changed.connect(self.update_status_labels)

    def update_status_labels(self):
        # 更新標籤內容
        self.login_status_label.setText(f"登入狀態：{self.status_manager.get_login_status()}")
        self.file_status_label.setText(f"文件狀態：{self.status_manager.get_file_status()}")

class StatusManager(QObject):
    # 定義狀態變更信號
    status_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._login_status = "未登入"
        self._file_status = "未處理"

    def update_login_status(self, status):
        self._login_status = status
        self.status_changed.emit()  # 發出狀態變更信號

    def update_file_status(self, status):
        self._file_status = status
        self.status_changed.emit()  # 發出狀態變更信號

    def get_login_status(self):
        return self._login_status

    def get_file_status(self):
        return self._file_status