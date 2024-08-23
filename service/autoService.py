import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from autoSettings import page_data  
from util import load_json


print(os.getcwd())
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



# 批量執行去程預約
def batchDeparTureReserve(driver, jsonData):


    searchCaseInputXpath = page_data['searchCaseInput']
    reserveBtnXpath = page_data['reserveBtn']
    dateInputXpath = page_data['dateInput']
    timeInputXpath = page_data['timeInput']
    destinationInputXpath = page_data['destinationInput']
    destinationTypeInputXpath = page_data['destinationTypeInput']
    trueRideTogetherXpath = page_data['trueRideTogether']
    carTypeInputXpath = page_data['carTypeInput']
    wheelchairTypeInputXpath = page_data['wheelchairTypeInput']
    numberOfPeopleInputXpath = page_data['numberOfPeopleInput']
    remarkInputXpath = page_data['remarkInput']
    implementReserveBtnXpath = page_data['implementReserveBtn']
    trueReserveHintXpath = page_data['trueReserveHint']



    for obj in jsonData:
        searchCaseInput = driver.find_element(By.XPATH, searchCaseInputXpath)
        searchCaseInput.send_keys(obj['ID'], Keys.ENTER)

        reserveBtn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, reserveBtnXpath))
        )
        reserveBtn.click()

        dateInput = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, dateInputXpath))
        )
        dateInput.send_keys(obj['Date'], Keys.TAB)

        driver.switch_to.active_element.send_keys(obj['Time'])
        
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        

        driver.switch_to.active_element.send_keys(obj['destination'])
        driver.switch_to.active_element.send_keys(Keys.TAB)
        
        driver.switch_to.active_element.send_keys(obj['醫院診所'])

        
        trueRideTogether = driver.find_element(By.XPATH, trueRideTogetherXpath)
        trueRideTogether.click()

        carTypeInput = driver.find_element(By.XPATH, carTypeInputXpath)
        carTypeInput.send_keys(obj['accompany1'])

        
        wheelchairTypeInput = driver.find_element(By.XPATH, wheelchairTypeInputXpath)
        wheelchairTypeInput.send_keys(obj['wheelchairType'])

        numberOfPeopleInput = driver.find_element(By.XPATH, numberOfPeopleInputXpath)
        numberOfPeopleInput.send_keys(2)


        remarkInput = driver.find_element(By.XPATH, remarkInputXpath)
        remarkInput.send_keys(obj['accompany2'])

        time.sleep(5)
# def batchReturnTripReserve(driver, jsonData):

def main():
    # 啟用 WebDriver
    driver = init_webdriver()

    try:
        # 執行登入操作
        login(driver)
 
        searchCasePage(driver)
        jsonData = load_json('json_save/DeparTure.json')
        batchDeparTureReserve(driver, jsonData)
        time.sleep(5)
    finally:
        # 確保不管發生什麼都會關閉瀏覽器
        driver.quit()

if __name__ == "__main__":
    main()
