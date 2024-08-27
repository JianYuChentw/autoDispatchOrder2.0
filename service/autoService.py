import time
import os
import sys
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from autoSettings import page_data  
from util import load_json


# 加載環境變數
load_dotenv()

def loginGetToken(account, password, appKey):
    url = page_data["loginApi"]

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
    url = page_data["userIdApi"]
    
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
        response = requests.get(url, params=params, headers=headers)

        # 檢查響應狀態碼
        if response.status_code == 200:
            data = response.json()  
            # 提取 ID
            if data.get('code') == 200 and 'data' in data:
                ids = data['data'][0]['caseList'][0]['caseId']
                print(f"獲取到的caseId: {ids}")
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

    url = page_data["userIdGroupApi"]
    
    # 構建請求參數
    params = {
        "id": id
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Token": token  # 使用從登入獲取的 token
    }

    try:
        # 發送 GET 請求
        response = requests.get(url, params=params, headers=headers)

        # 檢查響應狀態碼
        if response.status_code == 200:
            result = response.json()  # 解析後的 JSON 響應
            data = result['result']
            # 篩選並調整資料
            if "userId" in data and "caseUserId" in data and "orgBId1" in data:
                userId = data["userId"]
                caseUserId = data["caseUserId"]
                orgBId1 = data["orgBId1"]
                fromAddr = f"{data.get('county', '')}{data.get('district', '')}{data.get('addr', '')}"

                result = {
                    "userId": userId,
                    "caseUserId": caseUserId,
                    "orgBId1": orgBId1,
                    "fromAddr": fromAddr,
                    "fromAddrRemark":"住家"
                }
                return result
            else:
                print("響應資料中缺少必要欄位")
                return None
        else:
            print(f"請求失敗，狀態碼：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"請求時發生錯誤: {e}")
        return None

def processReservationDataList(dataList):
    processedList = []
    
    for data in dataList:
        ID = data['ID']
        CaseName = data['CaseName']
        reserveDate = f"{data['Date']} {data['Time']}"    
        toAddr = data['destination']
        wheelchairType = data["wheelchairType"]
        remark = data["accompany2"]
        
        if data['accompany1'] == '一般車':
            carCategoryId = 'SYS_CAR_GENERAL'
            carCategoryName = "普通車"
        elif data['accompany1'] == '福祉車':
            carCategoryId = 'SYS_CAR_WEAL'
            carCategoryName = "福祉車"
        else:
            carCategoryId = data['accompany1']  # 如果是其他值，保持原樣
            carCategoryName = "其他車型"  # 根据具体需求设置默认名称

        # 組合結果
        processedData = {
            "ID":ID,
            "CaseName":CaseName,
            "reserveDate": reserveDate,
            "toAddr": toAddr,
            "carCategoryId": carCategoryId,
            "carCategoryName": carCategoryName,
            "wheelchairType": wheelchairType,
            "remark": remark
        }
        
        processedList.append(processedData)
    
    return processedList

def addProcess( token, systemData, reservationData):
    
    url = page_data["reservationApi"]

    data = {
        "userId": systemData["userId"],
        "caseUserId": systemData["caseUserId"],
        "orgId": systemData["orgBId1"],
        "reserveDate": reservationData["reserveDate"],
        "transOrgs": [systemData["orgBId1"]],
        "fromAddr": systemData["fromAddr"],
        "fromAddrRemark":  systemData["fromAddrRemark"],
        "toAddr": reservationData["toAddr"],
        "toAddrRemark": "醫院診所",
        "remark": reservationData["remark"],
        "isBack": False,
        "canShared": True,
        "carCategoryId": reservationData["carCategoryId"],
        "carCategoryName": reservationData["carCategoryName"],
        "wheelchairType": reservationData["wheelchairType"],
        "familyWith": 1,
        "haveNextOrderFlag":  False,
        "isBackOrder": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Token": token  # 使用從登入獲取的 token
    }

    try:        
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            # print(reservationData["CaseName"],"處理完成，回應：",result["message"])
            return {'code':result["code"],'date':reservationData["reserveDate"], "id":reservationData["ID"], "caseName":reservationData["CaseName"], 'message':result["message"]}  
        else:
            print(f"請求失敗，狀態碼：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"請求時發生錯誤: {e}")
        return None


#### 測試區
user_account = os.getenv('USER_ACCOUNT')
user_password = os.getenv('USER_PASSWORD')
appKey = os.getenv('APPKEY')
jsonData = load_json('json_save/DeparTure.json')

# 使用示例
login_response = loginGetToken(user_account, user_password, appKey)
reservationDatas = processReservationDataList(jsonData)

if login_response and "token" in login_response:
    token = login_response["token"]  # 獲取登入返回的 token
    # 使用獲取到的 token 進行使用者資訊查詢
 
    for reservationData in reservationDatas:
     
        uid = getUsersId(reservationData["ID"], token=token)
        uidGroup = getUidGrouop(uid, token) 
        print(addProcess(token, uidGroup, reservationData))
        
    

else:
    print("登入失敗，未能獲取 token")