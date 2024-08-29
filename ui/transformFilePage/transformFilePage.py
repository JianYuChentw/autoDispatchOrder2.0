from ..frontPage.statusBar import StatusManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt

class TransformFilePage(QWidget):
    def __init__(self, stack_widget, status_manager):
        super().__init__()
        self.stack_widget = stack_widget
        self.status_manager = status_manager

        # 主佈局
        layout = QVBoxLayout()

        # 開始轉換文件按鈕
        self.start_button = QPushButton('開始轉換文件')
        self.start_button.setFixedSize(200, 50)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.start_file_conversion)

        # 標籤：轉換結果
        self.result_label = QLabel('轉換結果：')
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px;")

        # 顯示轉換結果的文本框
        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("font-size: 16px;")
        self.result_text.setReadOnly(True)  # 設置為只讀模式

        # 回到前頁按鈕
        self.back_button = QPushButton('回到前頁')
        self.back_button.setFixedSize(200, 50)
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #d3d3d3;
                border: none;
                color: black;
                padding: 12px 24px;
                text-align: center;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b0b0b0;
            }
        """)
        self.back_button.clicked.connect(self.go_back)

        # 將元件添加到佈局
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_text)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def start_file_conversion(self):
        # 獲取選中的文件
        selected_file = self.status_manager.get_selected_file()
        if selected_file:
            try:
                # 執行文件轉換
                # transformExcel(selected_file)
                self.status_manager.update_file_status("完成轉換", selected_file)

                # 更新結果到文本框
                self.result_text.setText(f"文件 {selected_file} 已成功轉換。")
                QMessageBox.information(self, '成功', '文件已成功轉換。')

            except Exception as e:
                self.result_text.setText(f"文件轉換失敗：{e}")
                QMessageBox.critical(self, '錯誤', f'文件轉換失敗：{e}')
        else:
            QMessageBox.warning(self, '無檔案', '請先選擇一個 Excel 文件。')

    def go_back(self):
        # 返回到前一個頁面，假設它是 QStackedWidget 的索引 0
        self.stack_widget.setCurrentIndex(0)
