from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel
from .labelWidget import LabelWidget
from .statusBar import StatusBar
from .buttonPanel import ButtonPanel
from ..processingPage.processingPage import ProcessingPage
from ..transformFilePage.transformFilePage import TransformFilePage  

class FrontPage(QWidget):
    def __init__(self, status_manager):
        super().__init__()

        self.setWindowTitle('首頁')
        self.resize(1000, 600)

        # 創建 QStackedWidget
        self.stack_widget = QStackedWidget(self)

        # 創建首頁內容
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)

        # 調整布局間距和邊距
        home_layout.setSpacing(10)  # 設置控件之間的間距
        home_layout.setContentsMargins(10, 10, 10, 10)  # 設置佈局邊距

        label_widget = LabelWidget()
        status_bar = StatusBar(status_manager)  # 傳遞狀態管理器到 StatusBar

        # 創建 ButtonPanel，並傳遞 stack_widget 和 status_manager
        button_panel = ButtonPanel(self.stack_widget, status_manager)

        home_layout.addWidget(label_widget)
        home_layout.addLayout(status_bar)

        spacer_label = QLabel("")
        spacer_label.setFixedHeight(40)  # 可以調整這個高度來控制空間大小
        home_layout.addWidget(spacer_label)

        home_layout.addWidget(button_panel)

        # 將首頁添加到 QStackedWidget 中
        self.stack_widget.addWidget(home_widget)

        # 創建處理頁面並傳遞 stack_widget 給處理頁面
        processing_page = ProcessingPage(self.stack_widget)
        self.stack_widget.addWidget(processing_page)

        # 創建文件轉換頁面並添加到 QStackedWidget 中
        transform_file_page = TransformFilePage(self.stack_widget, status_manager)
        self.stack_widget.addWidget(transform_file_page)

        # 設置主佈局，將 QStackedWidget 作為唯一控件
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack_widget)

        self.setLayout(main_layout)
