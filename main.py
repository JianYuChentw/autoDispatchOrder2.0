import sys
from PyQt6.QtWidgets import QApplication
from ui.frontPage.frontPage import FrontPage  
from ui.frontPage.statusBar import StatusManager 

from PyQt6.QtTest import QTest



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 初始化狀態管理器
    status_manager = StatusManager()


    # 創建窗口實例並傳遞狀態管理器
    window = FrontPage(status_manager=status_manager)
    window.show()
    
    sys.exit(app.exec())
