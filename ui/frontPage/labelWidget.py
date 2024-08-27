from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class LabelWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 文字居中
        self.setText("批量預約系統")
        self.setStyleSheet("font-size: 28px;")  # 調整字體大小
