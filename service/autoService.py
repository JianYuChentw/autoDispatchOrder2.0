import time
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from autoSettings import page_data  
from util import load_json


print(os.getcwd())
# 加載環境變數
load_dotenv()
user_account = os.getenv('USER_ACCOUNT')
user_password = os.getenv('USER_PASSWORD')
appKey = os.getenv('APPKEY')


def loginGetToken(account, password, appKey):
    url = "https://khh.mass.org.tw/api/check/login"

    payload = {
        "Account": account,
        "Password": password,
        "AppKey": appKey
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # 使用 Session 保持一致性
        session = requests.Session()
        response = session.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("登入成功，Token為：", response.json()['token'])

            return response.json()
        else:
            print(f"登入失敗，狀態碼：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"登入時發生錯誤: {e}")
        return None  

def getUsersId(key, token, userType="", page=1, limit=10):
    # API 目標地址
    base_url = "https://khh.mass.org.tw/api/users/loadwithtype"
    
    # 構建請求參數
    params = {
        "page": page,
        "limit": limit,
        "key": key,
        "userType": userType
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Token": token 
    }

    try:
        # 發送 GET 請求
        response = requests.get(base_url, params=params, headers=headers)

        # 檢查響應狀態碼
        if response.status_code == 200:
            print("請求成功，響應內容如下：")
            data = response.json()  
            # 提取 ID
            if data.get('code') == 200 and 'data' in data:
                ids = data['data'][0]['caseList'][0]['caseId']
                print(f"獲取到的caseId: {ids[0]}")
                return int(ids)
            else:
                print("未找到有效的使用者數據")
                return None
        else:
            print(f"請求失敗，狀態碼：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"請求時發生錯誤: {e}")
        return None

def getUidGrouop(id, token):
    # API 目標地址
    base_url = "https://khh.mass.org.tw/api/caseusers/get"
    
    # 構建請求參數
    params = {
        "id": id
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Token": token  # 使用從登入獲取的 token
    }

    try:
        # 構建請求物件
        req = requests.Request('GET', base_url, params=params, headers=headers)
        prepared = req.prepare()

        # 打印最終的 URL
        print(f"最終發出的請求 URL: {prepared.url}")

        # 發送 GET 請求
        response = requests.Session().send(prepared)

        # 檢查響應狀態碼
        if response.status_code == 200:
            print("請求成功，響應內容如下：")
            return response.json()  # 返回解析後的 JSON 響應
        else:
            print(f"請求失敗，狀態碼：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"請求時發生錯誤: {e}")
        return None



# 使用示例
login_response = loginGetToken("khccomp004", "Aa12345678", "SYS_USERTYPE_ADMIN")

if login_response and "token" in login_response:
    token = login_response["token"]  # 獲取登入返回的 token
    # 使用獲取到的 token 進行使用者資訊查詢
    uid = getUsersId(key="E120230198", token=token)
    print(type(uid))
    uidGroup = getUidGrouop(uid, token) 
    print(uidGroup)
    

else:
    print("登入失敗，未能獲取 token")