import time
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from autoSettings import page_data  
from util import (load_json, processReservationDataList)
from apiService import (sendPostRequest, sendGetRequest )


# 加載環境變數
load_dotenv()

def loginGetToken(payload):
    url = page_data["loginApi"]
    response = sendPostRequest(url, payload)
    
    if response:
        print("登入成功，Token為：", response.json()['token'])
        return response.json()
    else:
        print("登入失敗")
        return None

def getUsersId(IdKey, token):
    url = page_data["userIdApi"]
    
    params = {
        "page": 1,
        "limit": 10,
        "key": IdKey,
        "userType": ""
    }
    
    response = sendGetRequest(url, params=params, token=token)
    
    if response:
        data = response.json()
        if data.get('code') == 200 and 'data' in data:
            ids = data['data'][0]['caseList'][0]['caseId']
            print(f"獲取到的caseId: {ids}")
            return int(ids)
        else:
            print("未找到有效的使用者數據")
            return None
    else:
        print("請求失敗")
        return None

def getUidGrouop(id, token):
    url = page_data["userIdGroupApi"]
    
    params = {
        "id": id
    }
    
    response = sendGetRequest(url, params=params, token=token)
    
    if response:
        result = response.json()['result']
        if "userId" in result and "caseUserId" in result and "orgBId1" in result:
            userId = result["userId"]
            caseUserId = result["caseUserId"]
            orgBId1 = result["orgBId1"]
            fromAddr = f"{result.get('county', '')}{result.get('district', '')}{result.get('addr', '')}"
            
            return {
                "userId": userId,
                "caseUserId": caseUserId,
                "orgBId1": orgBId1,
                "fromAddr": fromAddr,
                "fromAddrRemark": "住家"
            }
        else:
            print("響應資料中缺少必要欄位")
            return None
    else:
        print("請求失敗")
        return None

def addProcess(token, systemData, reservationData):
    url = page_data["reservationApi"]

    data = {
        "userId": systemData["userId"],
        "caseUserId": systemData["caseUserId"],
        "orgId": systemData["orgBId1"],
        "reserveDate": reservationData["reserveDate"],
        "transOrgs": [systemData["orgBId1"]],
        "fromAddr": systemData["fromAddr"],
        "fromAddrRemark": systemData["fromAddrRemark"],
        "toAddr": reservationData["toAddr"],
        "toAddrRemark": "醫院診所",
        "remark": reservationData["remark"],
        "isBack": False,
        "canShared": True,
        "carCategoryId": reservationData["carCategoryId"],
        "carCategoryName": reservationData["carCategoryName"],
        "wheelchairType": reservationData["wheelchairType"],
        "familyWith": 1,
        "haveNextOrderFlag": False,
        "isBackOrder": True
    }

    response = sendPostRequest(url, payload=data, token=token)
    
    if response:
        result = response.json()
        return {
            'code': result["code"],
            'date': reservationData["reserveDate"],
            'id': reservationData["ID"],
            'caseName': reservationData["CaseName"],
            'message': result["message"]
        }
    else:
        print("請求失敗")
        return None


#### 測試區

jsonData = load_json('json_save/DeparTure.json')
payload = {
        "Account": os.getenv('USER_ACCOUNT'),
        "Password": os.getenv('USER_PASSWORD'),
        "AppKey": os.getenv('APPKEY')
    }
# 使用示例
login_response = loginGetToken(payload)
reservationDatas = processReservationDataList(jsonData)

if login_response and "token" in login_response:
    token = login_response["token"]  # 獲取登入返回的 token
    # 使用獲取到的 token 進行使用者資訊查詢
 
    for reservationData in reservationDatas:
     
        uid = getUsersId(reservationData["ID"], token)
        uidGroup = getUidGrouop(uid, token) 
        print(addProcess(token, uidGroup, reservationData))
        

else:
    print("登入失敗，未能獲取 token")