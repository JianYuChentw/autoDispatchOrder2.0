import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class ProcessingPage(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget  # 將 QStackedWidget 傳遞給 ProcessingPage

        main_layout = QVBoxLayout()

        # 上部顯示案件數量和處理按鈕
        top_layout = QHBoxLayout()
        
        self.case_label = QLabel('案件數量：')
        self.case_label.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(self.case_label)

        process_button = QPushButton('開始處理')
        process_button.setFixedSize(100, 40)
        process_button.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(process_button)

        main_layout.addLayout(top_layout)

        # 處理進度
        progress_layout = QHBoxLayout()
        
        progress_label = QLabel('處理進度：')
        progress_label.setStyleSheet("font-size: 18px;")
        progress_layout.addWidget(progress_label)

        progress_bar = QProgressBar()
        progress_bar.setValue(50)
        progress_layout.addWidget(progress_bar)

        progress_percent = QLabel('XX %')
        progress_percent.setStyleSheet("font-size: 18px;")
        progress_layout.addWidget(progress_percent)

        main_layout.addLayout(progress_layout)

        # 處理結果
        result_label = QLabel('處理結果：')
        result_label.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText("顯示處理結果")
        self.result_text.setReadOnly(True)  # 設定為只讀模式
        self.result_text.setStyleSheet("font-size: 16px;")
        self.result_text.setCursor(Qt.CursorShape.IBeamCursor)  # 設置鼠標為I型光標，方便複製
        main_layout.addWidget(self.result_text)

        # 底部按鈕
        bottom_layout = QHBoxLayout()

        export_failures_button = QPushButton('輸出失敗紀錄')
        export_failures_button.setFixedSize(150, 40)
        export_failures_button.setStyleSheet("font-size: 18px;")
        bottom_layout.addWidget(export_failures_button)

        back_button = QPushButton('回前頁')
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("font-size: 18px;")
        back_button.clicked.connect(self.go_back)  # 連接按鈕點擊信號到回前頁的方法
        bottom_layout.addWidget(back_button)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        # 進入頁面時自動讀取 JSON 檔案並更新 UI
        self.load_json_files()

    def load_json_files(self):
        try:
            
            file1_path = 'json_save/DeparTure.json'
            file2_path = 'json_save/ReturnTrip.json'

            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                data1 = json.load(file1)
                data2 = json.load(file2)

                # 假設兩個 JSON 檔案內容都是陣列
                total_cases = len(data1) + len(data2)
                self.case_label.setText(f'案件數量： {total_cases}')

                # 顯示處理結果
                self.result_text.setText(f'已讀取 {total_cases} 筆案件資料')
        except Exception as e:
            self.result_text.setText(f'讀取檔案時發生錯誤：{e}')

    def go_back(self):
        self.stack_widget.setCurrentIndex(0)  # 切換回首頁
