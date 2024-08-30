from ..frontPage.statusBar import StatusManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt
import os, json
from dotenv import load_dotenv
from service.transformExcel.transformService import extractDataFromDepartureExcel, json_serial
from util import processReservationDataList, resverProcessReservationDataList
load_dotenv()



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
        self.start_button.clicked.connect(self.startFileConversion)

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

    def startFileConversion(self):
        # 獲取選中的文件
        selected_file = self.status_manager.get_selected_file()
        if selected_file:
            try:
                # 導入環境變數
                departure_json_file_path = os.getenv('DEPARTURE_JSON')
                rdeparture_json_file_path = os.getenv('RETURN_TRIP_JSON')
        
                # 執行文件轉換
                formatted_data = extractDataFromDepartureExcel(selected_file)
                

                departure_result = formatted_data.get('departureResult', [])
                return_trip_result = formatted_data.get('returnTripResult', [])
                # 檢查未解決案件
                unresolved_cases = formatted_data.get('unresolvedCases', [])
                
                if unresolved_cases:
                    # 打印未解決的案件
                    unresolved_messages = "\n".join(
                        [f"時間: {case['Time']}, 姓名: {case['CaseName']}, 上車地點: {case['Departure']}, 下車地點: {case['Destination']}"
                        for case in unresolved_cases]
                    )
                    self.result_text.setText(f"文件 {selected_file} 已轉換，但有未解決案件：\n{unresolved_messages}")
                    QMessageBox.warning(self, '部分失敗', '文件已轉換，但有部分案件未能解決。')
                else:
                    # 如果所有案件都已解決
                    self.result_text.setText(f"文件 {selected_file} 已成功轉換，所有案件已處理完畢。")
                    QMessageBox.information(self, '成功', '文件已成功轉換，所有案件已處理完畢。')

                # 將departureResult寫入對應的JSON文件
                if departure_json_file_path:
                    with open(departure_json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(departure_result, json_file, ensure_ascii=False, indent=2, default=json_serial)
                else:
                    print("環境變量 'departure_json_file_path' 未設置。")


                # 將returnTripResult寫入對應的JSON文件
                if rdeparture_json_file_path:
                    with open(rdeparture_json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(return_trip_result, json_file, ensure_ascii=False, indent=2, default=json_serial)
                else:
                    print("環境變量 'rdeparture_json_file_path' 未設置。")


                # 更新狀態
                self.status_manager.update_file_status("完成轉換", selected_file)

            except Exception as e:
                # 處理異常情況
                self.result_text.setText(f"文件轉換失敗：{e}")
                QMessageBox.critical(self, '錯誤', f'文件轉換失敗：{e}')
        else:
            # 未選擇文件時的提示
            QMessageBox.warning(self, '無檔案', '請先選擇一個 Excel 文件。')


    def go_back(self):
        # 返回到前一個頁面，假設它是 QStackedWidget 的索引 0
        self.stack_widget.setCurrentIndex(0)
