from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit, QHBoxLayout, QPushButton

class ProcessingPage(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget  # 將 QStackedWidget 傳遞給 ProcessingPage

        main_layout = QVBoxLayout()

        # 上部顯示案件數量和處理按鈕
        top_layout = QHBoxLayout()
        
        case_label = QLabel('案件數量： XXX')
        case_label.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(case_label)

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

        result_text = QTextEdit()
        result_text.setPlaceholderText("顯示處理結果")
        main_layout.addWidget(result_text)

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

    def go_back(self):
        self.stack_widget.setCurrentIndex(0)  # 切換回首頁
