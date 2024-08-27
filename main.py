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
    #     # 模擬狀態變化
    # QTest.qWait(3000)  # 暫停2秒觀察初始狀態
    # status_manager.update_login_status("已登入")
    # status_manager.update_file_status("處理中")
    
    sys.exit(app.exec())
