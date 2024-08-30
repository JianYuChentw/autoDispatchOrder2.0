import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from service.autoService import processSingleReservation, reverProcessSingleReservation
from util import processReservationDataList, resverProcessReservationDataList

class ProcessingThread(QThread):
    update_progress = pyqtSignal(int)
    update_result = pyqtSignal(str)

    def __init__(self, jsonData, jsonData2, token, parent=None):
        super().__init__(parent)
        self.jsonData = jsonData
        self.jsonData2 = jsonData2
        self.token = token

    def run(self):
        total_cases = len(self.jsonData) + len(self.jsonData2)
        processed_cases = 0

        deparTureResults = []
        returnTripResults = []
        deparTurErroCase = []
        returnTripErroCase = []

        # 處理 DeparTure.json 的數據

        for reservationData in self.jsonData:
            result = processSingleReservation(reservationData, self.token['token'])
            if result:
                deparTureResults.append(result)
                if result['code'] == 500 :
                    deparTurErroCase.append(result)
                
            processed_cases += 1
            progress_percent = int((processed_cases / total_cases) * 100)
            self.update_progress.emit(progress_percent)
            self.update_result.emit(f"處理完成: {processed_cases}/{total_cases} - 去程")

        # 處理 ReturnTrip.json 的數據
        for reservationData in self.jsonData2:
            result = reverProcessSingleReservation(reservationData, self.token['token'])
            if result:
                returnTripResults.append(result)
                if result['code'] == 500 :
                    returnTripErroCase.append(result)

            processed_cases += 1
            progress_percent = int((processed_cases / total_cases) * 100)
            self.update_progress.emit(progress_percent)
            self.update_result.emit(f"處理完成: {processed_cases}/{total_cases} - 回程")

        # 處理結束，發送最終結果
        self.update_result.emit("所有案件處理完成。")

        for erro_case in deparTurErroCase:
            formatted_message = (
                f"<span style='color:red;'>時間: {erro_case['date']} - "
                f"姓名: {erro_case['caseName']} - "
                f"失敗原因: {erro_case['message']}</span>"
            )
            self.update_result.emit(formatted_message)
        
        for erro_case in returnTripErroCase:
            formatted_message = (
                f"<span style='color:red;'>時間: {erro_case['date']} - "
                f"姓名: {erro_case['caseName']} - "
                f"失敗原因: {erro_case['message']}</span>"
            )
            self.update_result.emit(formatted_message)




class ProcessingPage(QWidget):
    def __init__(self, stack_widget, status_manager):
        super().__init__()
        self.stack_widget = stack_widget
        self.status_manager = status_manager
        self.processing_thread = None

        main_layout = QVBoxLayout()

        # 上部顯示案件數量和處理按鈕
        top_layout = QHBoxLayout()
        
        self.case_label = QLabel('案件數量：')
        self.case_label.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(self.case_label)

        self.process_button = QPushButton('開始處理')
        self.process_button.setFixedSize(100, 40)
        self.process_button.setStyleSheet("font-size: 18px;")
        self.process_button.clicked.connect(self.start_processing)
        top_layout.addWidget(self.process_button)

        main_layout.addLayout(top_layout)

        # 處理進度
        progress_layout = QHBoxLayout()
        
        progress_label = QLabel('處理進度：')
        progress_label.setStyleSheet("font-size: 18px;")
        progress_layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_percent = QLabel('0 %')
        self.progress_percent.setStyleSheet("font-size: 18px;")
        progress_layout.addWidget(self.progress_percent)

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

    def start_processing(self):
        # 確認 token 是否存在
        if not self.status_manager.token:
            self.result_text.setText("尚未登入系統，無法處理案件。")
            return

        token = self.status_manager.token

        # 讀取 JSON 資料
        deparTurePath = 'jsonSave/DeparTure.json'
        returnTripPath = 'jsonSave/ReturnTrip.json'
        jsonData = self.load_json_file(deparTurePath)
        jsonData2 = self.load_json_file(returnTripPath)

        if not jsonData or not jsonData2:
            self.result_text.setText("讀取 JSON 文件時發生錯誤。")
            return

        total_cases = len(jsonData) + len(jsonData2)
        self.case_label.setText(f'案件數量： {total_cases}')

        # 初始化處理線程
        self.processing_thread = ProcessingThread(processReservationDataList(jsonData), resverProcessReservationDataList(jsonData2), token)
        self.processing_thread.update_progress.connect(self.update_progress_bar)
        self.processing_thread.update_result.connect(self.append_result_text)
        self.processing_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
        self.progress_percent.setText(f'{value} %')

    def append_result_text(self, text):
        self.result_text.append(text)

    def load_json_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            self.result_text.setText(f'讀取檔案時發生錯誤：{e}')
            return None

    def go_back(self):
        self.stack_widget.setCurrentIndex(0)  # 切換回首頁
