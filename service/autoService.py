import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from autoSettings import page_data  

# 加載環境變數
load_dotenv()

# 初始化頁面
def init_webdriver():
    # 設置 WebDriver
    driver = webdriver.Chrome()

    # 打開目標網站
    url = page_data['loginPage']
    driver.get(url)

    account_input_locator = page_data['accountInput']
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, account_input_locator))
        )
    return driver

# 登入頁
def login(driver):

    accountInputLocator = page_data['accountInput']
    passwordInputLocator = page_data['passwordInput']
    loginButtonLocator = page_data['loginButton']
    accountTag = page_data['fonePageAccountTag']

    user_account = os.getenv('USER_ACCOUNT')
    user_password = os.getenv('USER_PASSWORD')

    # 檢查環境變數是否正確設置
    if user_account is None or user_password is None:
        raise ValueError("USER_ACCOUNT or USER_PASSWORD environment variable is not set.")

    

    # 輸入帳號
    account_input = driver.find_element(By.XPATH, accountInputLocator)
    account_input.send_keys(user_account)

    # 輸入密碼
    password_input = driver.find_element(By.XPATH, passwordInputLocator)
    password_input.send_keys(user_password)

    # 點擊登入按鈕
    login_button = driver.find_element(By.XPATH, loginButtonLocator)
    login_button.click()

    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, accountTag))
        )

# 案件搜尋頁
def searchCasePage(driver):
    load_dotenv()
    url = page_data['casePage']
    driver.get(url)

    searchCaseInput = page_data['searchCaseInput']
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, searchCaseInput))
        )
    print('取得searchCase位置')



# 執行預約

def main():
    # 啟用 WebDriver
    driver = init_webdriver()

    try:
        # 執行登入操作
        login(driver)
 
        searchCasePage(driver)
        time.sleep(5)
    finally:
        # 確保不管發生什麼都會關閉瀏覽器
        driver.quit()

if __name__ == "__main__":
    main()
