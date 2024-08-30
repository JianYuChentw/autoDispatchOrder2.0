import time
import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from service.autoSettings import page_data  
from util import (loadJson, processReservationDataList)
from service.apiService import (sendPostRequest, sendGetRequest )


# 加載環境變數
load_dotenv()

def loginGetToken(payload):
    url = page_data["loginApi"]
    response = sendPostRequest(url, payload)
    responseData = response.json()
    
    if responseData["code"] == 200:
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
        
        if data['count']<1:
            return {'code': 200, "message":"無該個案", "caseId":None}
        
        if data.get('code') == 200 and 'data' in data:
            ids = data['data'][0]['caseList'][0]['caseId']
            print(f"獲取到的caseId: {ids}")
            return {'code': 200, "message":"取得資訊", "caseId":int(ids) }
    else:
        if data.get['code'] == 401:
            return {'code': 401, "message":"登入失敗", "caseId":None}
        
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

def processSingleReservation(reservationData, token):
    uidResult = getUsersId(reservationData["ID"], token)

    if uidResult['code'] == 401:
        print("憑證失效，重新獲取 token...")
        payload = {
        "Account": os.getenv('USER_ACCOUNT'),
        "Password": os.getenv('USER_PASSWORD'),
        "AppKey": os.getenv('APPKEY')
    }
        token = loginGetToken(payload)

        if not token:
            print("重新登入失敗，停止操作")
            return {"error": "重新登入失敗"}

        print('獲取新的 token 成功')
        uidResult = getUsersId(reservationData["ID"], token)

    if uidResult['code'] == 200 and not uidResult.get('caseId'):
        print("無該案個案")
        return None

    if uidResult.get('caseId'):
        uidGroup = getUidGrouop(uidResult['caseId'], token)
        process_result = addProcess(token, uidGroup, reservationData)
        return process_result

    return None


def addReverProcess(token, systemData, reservationData):
    url = page_data["reservationApi"]

    data = {
        "userId": systemData["userId"],
        "caseUserId": systemData["caseUserId"],
        "orgId": systemData["orgBId1"],
        "reserveDate": reservationData["reserveDate"],
        "transOrgs": [systemData["orgBId1"]],

        "fromAddr": reservationData["toAddr"],
        "fromAddrRemark":"醫院診所",
        "toAddr": systemData["fromAddr"],
        "toAddrRemark": systemData["fromAddrRemark"],

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

def reverProcessSingleReservation(reservationData, token):
    uidResult = getUsersId(reservationData["ID"], token)

    if uidResult['code'] == 401:
        print("憑證失效，重新獲取 token...")
        payload = {
        "Account": os.getenv('USER_ACCOUNT'),
        "Password": os.getenv('USER_PASSWORD'),
        "AppKey": os.getenv('APPKEY')
    }
        token = loginGetToken(payload)

        if not token:
            print("重新登入失敗，停止操作")
            return {"error": "重新登入失敗"}

        print('獲取新的 token 成功')
        uidResult = getUsersId(reservationData["ID"], token)

    if uidResult['code'] == 200 and not uidResult.get('caseId'):
        print("無該案個案")
        return None

    if uidResult.get('caseId'):
        uidGroup = getUidGrouop(uidResult['caseId'], token)
        process_result = addReverProcess(token, uidGroup, reservationData)
        return process_result

    return None



#### 測試區

# jsonData = loadJson('jsonSave/DeparTure.json')
# jsonData2 = loadJson('jsonSave/ReturnTrip.json')
# payload = {
#         "Account": os.getenv('USER_ACCOUNT'),
#         "Password": os.getenv('USER_PASSWORD'),
#         "AppKey": os.getenv('APPKEY')
#     }
# # 使用示例
# login_response = loginGetToken(payload)
# reservationDatas = processReservationDataList(jsonData)
# reservationDatas2 = processReservationDataList(jsonData2)

# deparTureResults=[]
# returnTripResults=[]
# if login_response and "token" in login_response:
#     token = login_response["token"]  # 獲取登入返回的 token
#     # 使用獲取到的 token 進行使用者資訊查詢
 
#     for reservationData in reservationDatas:
#         result = processSingleReservation(reservationData, token)
#         if result:
#             deparTureResults.append(result)

#     for reservationData in reservationDatas2:
#         result = reverProcessSingleReservation(reservationData, token)
#         if result:
#             returnTripResults.append(result)
            

#     # 打印所有結果
#     print('去程：', deparTureResults)
#     print('回程：', returnTripResults)

# else:
#     print("登入失敗，未能獲取 token")



