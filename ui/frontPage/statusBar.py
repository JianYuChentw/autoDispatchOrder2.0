from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject

class StatusBar(QHBoxLayout):
    def __init__(self, status_manager):
        super().__init__()
        self.status_manager = status_manager
        self.setSpacing(10)

        self.login_space = QLabel()
        self.addWidget(self.login_space)
        
        # 登入狀態標籤
        self.login_status_label = QLabel(f"登入狀態：{self.status_manager.get_login_status()}")
        self.login_status_label.setFixedHeight(40)
        self.login_status_label.setStyleSheet("""
            font-size: 20px;
            background-color: red;
            border-radius: 10px;
            padding: 5px;
        """)
        self.addWidget(self.login_status_label)

        # 文件處理狀態標籤
        self.file_status_label = QLabel(f"文件狀態：{self.status_manager.get_file_status()}")
        self.file_status_label.setFixedHeight(40)
        self.file_status_label.setStyleSheet("""
            font-size: 20px;
            background-color: red;
            border-radius: 10px;
            padding: 5px;
        """)
        self.addWidget(self.file_status_label)

        # 選擇檔案
        self.reserved_button = QPushButton("選擇檔案")
        self.reserved_button.setFixedSize(120, 30)
        self.reserved_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #6FB7B7;
                border: none;
                color: black;
                padding: 0 24px;
                text-align: center;
                text-decoration: none;
                border-radius: 2px;
            }
            
            QPushButton:hover {
                background-color: #5CADAD;
            }
        """)
        self.reserved_button.clicked.connect(self.select_excel_file)  # 連接按鈕點擊事件
        self.addWidget(self.reserved_button)
        self.addWidget(self.login_space)

        # 連接狀態管理器的信號到更新方法
        self.status_manager.status_changed.connect(self.update_status_labels)

    def select_excel_file(self):
        # 彈出檔案選擇對話框
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "選擇 Excel 文件", "", "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            # 更新文件狀態並保存選擇的文件路徑
            self.status_manager.update_file_status("準備處理", file_path)

    def update_status_labels(self):
        # 更新標籤內容
        self.login_status_label.setText(f"登入狀態：{self.status_manager.get_login_status()}")
        self.file_status_label.setText(f"文件狀態：{self.status_manager.get_file_status()}")

        # 根據登入狀態改變背景顏色
        login_status = self.status_manager.get_login_status()
        if login_status == "已登入":
            self.login_status_label.setStyleSheet("""
                font-size: 20px;
                background-color: #01B468;
                border-radius: 10px;
                padding: 5px;
            """)
        elif login_status == "未登入":
            self.login_status_label.setStyleSheet("""
                font-size: 20px;
                background-color: red;
                border-radius: 10px;
                padding: 5px;
            """)
        
        # 根據文件狀態改變背景顏色
        file_status = self.status_manager.get_file_status()
        if file_status == "準備處理":
            self.file_status_label.setStyleSheet("""
                font-size: 20px;
                background-color: #FFA042;  
                border-radius: 10px;
                padding: 5px;
            """)
        elif file_status == "無檔案":
            self.file_status_label.setStyleSheet("""
                font-size: 20px;
                background-color: red;
                border-radius: 10px;
                padding: 5px;
            """)
        elif file_status == "完成轉換":
            self.file_status_label.setStyleSheet("""
                font-size: 20px;
                background-color: #01B468;
                border-radius: 10px;
                padding: 5px;
            """)

class StatusManager(QObject):
    # 定義狀態變更信號
    status_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._login_status = "未登入"
        self._file_status = "無檔案"
        self.token = None
        self.selected_file = None  # 新增選擇的文件路徑屬性

    def update_login_status(self, status):
        self._login_status = status
        self.status_changed.emit()  # 發出狀態變更信號

    def update_file_status(self, status, file_path=None):
        self._file_status = status
        self.selected_file = file_path  # 保存選擇的文件路徑
        self.status_changed.emit()  # 發出狀態變更信號

    def get_login_status(self):
        return self._login_status

    def get_file_status(self):
        return self._file_status
    
    def get_selected_file(self):
        return self.selected_file  # 新增方法來獲取選擇的文件路徑
