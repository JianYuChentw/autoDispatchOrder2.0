import json 

def loadJson(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)

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

def resverProcessReservationDataList(dataList):
    processedList = []
    
    for data in dataList:
        ID = data['ID']
        CaseName = data['CaseName']
        reserveDate = f"{data['Date']} {data['Time']}"    
        toAddr = data['Departure']
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



