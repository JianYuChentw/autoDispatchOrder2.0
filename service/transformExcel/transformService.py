import re, openpyxl, os, json
from datetime import date
from .transformTool import convertTime, format24Hour, convertDate, loadJson


# 時間重構
def roundToNearestQuarterHour(total_minutes):
    # 分鐘數轉換為小時和分鐘
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # 四捨五入到最近的15分鐘
    rounded_minutes = round(minutes / 15) * 15

    # 如果四捨五入後的分鐘數大於等於60，則進位到下一個小時
    if rounded_minutes >= 60:
        hours += 1
        rounded_minutes = 0

    # 返回格式化的時間字符串
    return f'{str(hours).zfill(2)}:{str(rounded_minutes).zfill(2)}'


# 特殊時間判定
def checkAndFormatTime(time_number):
    # 如果 time_number 不是字符串，則先將其轉換為字符串
    if isinstance(time_number, int) or isinstance(time_number, float):
        time_string = convertTime(time_number)
    else:
        time_string = str(time_number)

    # 分割時間字符串，僅提取小時和分鐘部分
    time_parts = time_string.split(':')
    if len(time_parts) < 2:
        raise ValueError(f"Invalid time format: {time_string}")
    
    hour = int(time_parts[0])
    minute = int(time_parts[1])

    if minute in [0, 15, 30, 45]:
        # 如果分鐘是 00、15、30 或 45，則不返回任何內容
        return ''
    else:
        # 如果分鐘不是 00、15、30 或 45，則返回輸入的時間字符串
        return time_string

# 車款過濾
def mapEquipmentToVehicle(equipment):
    carModel = loadJson('jsonSave/carModel.json')
    # 將設備名稱映射到車輛類型
    if equipment in carModel:
        return carModel[equipment]
    else:
        print(f"\033[31m未登載車輛資料: \033[37m{equipment}\033[0m")
        return '未定類型'

# 取地址不包含括弧
def removeContentInLastParentheses(input_text):
    # 使用正規表示式來匹配最後一對括號內的內容（包括括號），但排除空格
    regex = r'\(([^)\s]+)\)(?![^(]*\))'

    # 使用 replace 方法將匹配到的內容替換為空字串
    modified_text = re.sub(regex, '', input_text)

    return modified_text


# 醫院格式轉換器待完成
def hospitalConversion(hospitalName, case_name):

    hospitalData = loadJson('jsonSave/hospitalSave.json')
    # 去除括號及括號內文字並去除多餘的空格
    cleanedHospitalName = re.sub(r'\([^)]*\)', '', hospitalName).strip()

    # 檢查清理後的醫院名稱是否在資料中
    if cleanedHospitalName in hospitalData:
        return hospitalData[cleanedHospitalName]
    else:
        # 打印未登載資料的警告訊息（可以用來進行紀錄或除錯）
        # print(f"\033[31m未登載資料院所: \033[37m{case_name} \033[33m{hospitalName}\033[0m")
        return False
    

# 取地址備註
def extractContentInLastParentheses(inputText):
    specialLocation = loadJson('jsonSave/hospitalSpecialLocationSave.json')
    # 過濾地點備註的正則表達式，包含括號
    regex = r'\([^)]*\)(?![^(]*\))'
    matches = re.findall(regex, inputText)

    # 特殊地點加入備註
    if inputText in specialLocation:
        if not matches:
            matches = []
        # 將特殊地點的備註加上括號並添加到 matches
        matches.append(f"({specialLocation[inputText]})")

    if matches:
        return ''.join(matches)
    else:
        return ''

# 輪椅過濾
def wheelchairTypeSwitch(equipment):
    equipmentToVehicleMap = {
        '無輪椅.長照': '無',
        '輪椅.長照': '普通輪椅',
        '加寬輪椅.長照': '普通輪椅',
        '收折輪椅.長照': '普通輪椅(可收折)',
        '高背輪椅.長照': '高背輪椅',
        '拐杖.長照': '無',
        '四腳拐.長照': '無',
        '助行器.長照': '無',
        '電動輪椅.長照': '電動輪椅',
        '娃娃車.長照': '普通輪椅',
        '大型輪椅.長照': '高背輪椅',
        '大台電動輪椅.長照': '電動高背輪椅',
    }

    return equipmentToVehicleMap.get(equipment, '無相應資料')

# 移除客服備註
def filterTextWithKeywords(text, keywords=None):
    if keywords is None:
        keywords = ['補收', '月結']  # 可依需求新增更多關鍵字

    # 使用正則表達式建構匹配模式，不區分大小寫
    pattern = re.compile('|'.join(keywords), re.IGNORECASE)

    # 使用正則表達式測試文字
    if pattern.search(text):  # 如果文字中包含關鍵字
        return text  # 則保留文字內容
    else:
        return ''

# 轉換ＥＸＣＥＬ
def extractDataFromDepartureExcel(filePath):
    workbook = openpyxl.load_workbook(filePath)
    sheet = workbook.active  # 預設讀取第一個表
    data = list(sheet.iter_rows(values_only=True))

    # 假設表頭在第一行，將其取出作為鍵名
    headers = data[0]
    data = [dict(zip(headers, row)) for row in data[1:]]

    departureResult = []
    returnTripResult = []
    unresolvedCases = []  # 新增一個陣列來儲存未解決的案件

    for row in data:
        typeCode = row['碼別'] == '長照'
        if not typeCode:
            print(f"\033[31m非長照碼別\033[37m {roundToNearestQuarterHour(convertTime(row['時間']))} {row['個案姓名']} {row['碼別']}\033[33m")
            continue

        # 先移除括弧中的內容，再替換換行符
        raw_departure = removeContentInLastParentheses(row['上車地點']).replace('\r\n', '').replace('\n', '').replace('\r', '').strip()
        raw_destination = removeContentInLastParentheses(row['下車地點']).replace('\r\n', '').replace('\n', '').replace('\r', '').strip()
        
        departure = hospitalConversion(raw_departure, row['個案姓名'])
        destination = hospitalConversion(raw_destination, row['個案姓名'])

        # 根據需求過濾資料
        if departure is False and destination is False:
            
            #  移除換行符號 
            cleaned_departure = row['上車地點'].replace('\r\n', '').replace('\n', '').replace('\r', '').strip()
            cleaned_destination = row['下車地點'].replace('\r\n', '').replace('\n', '').replace('\r', '').strip()

            unresolvedCase = {
                'Time': roundToNearestQuarterHour(convertTime(row['時間'])),
                'CaseName': row['個案姓名'],
                'Departure': cleaned_departure,
                'Destination': cleaned_destination
            }
            unresolvedCases.append(unresolvedCase)  # 加入未解決的案件到陣列中
            print(f"\033[31m未登載資料院所\033[37m {unresolvedCase['Time']} {unresolvedCase['CaseName']} {unresolvedCase['Departure']} {unresolvedCase['Destination']}\033[33m")
            continue

        result = None
        if destination:
            result = {
                'Date': convertDate(row['日期']),
                'Time': roundToNearestQuarterHour(convertTime(row['時間'])),
                'ID': row['身分證號'],
                'CaseName': row['個案姓名'],
                'Departure': raw_departure,
                'destination': destination or row['下車地點'],
                'accompany1': mapEquipmentToVehicle(row['備註']),
                'wheelchairType': wheelchairTypeSwitch(row['備註']),
                'accompany2': ' '.join(
                    filter(None, [
                        checkAndFormatTime(row['時間']),
                        extractContentInLastParentheses(row['上車地點']),
                        extractContentInLastParentheses(
                            removeContentInLastParentheses(row['下車地點'])
                        ),
                        row.get('備註二', '')
                    ])
                ),
            }
            departureResult.append(result)
        elif departure:
            result = {
                'Date': convertDate(row['日期']),
                'Time': roundToNearestQuarterHour(convertTime(row['時間'])),
                'ID': row['身分證號'],
                'CaseName': row['個案姓名'],
                'Departure': departure or row['上車地點'],
                'destination': raw_destination,
                'accompany1': mapEquipmentToVehicle(row['備註']),
                'wheelchairType': wheelchairTypeSwitch(row['備註']),
                'accompany2': ' '.join(
                    filter(None, [
                        checkAndFormatTime(row['時間']),
                        extractContentInLastParentheses(row['下車地點']),
                        extractContentInLastParentheses(
                            removeContentInLastParentheses(row['上車地點'])
                        ),
                        row.get('備註二', '')
                    ])
                ),
            }
            returnTripResult.append(result)

    # 回傳時新增 unresolvedCases
    return {
        'departureResult': departureResult,
        'returnTripResult': returnTripResult,
        'unresolvedCases': unresolvedCases
    }

# # 自定義的 JSON 序列化器，用來處理 date 類型
def json_serial(obj):
    if isinstance(obj, (date,)):
        return obj.isoformat()
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")


# 測試提取數據
# formatted_data = extractDataFromDepartureExcel('/Users/jian-yuchen/Desktop/autoDispatchOrder2.0/test.xlsx')
# # print(formatted_data)


# departure_json_file_path = "jsonSave/TTDeparTure.json"
# rdeparture_json_file_path = "jsonSave/rRDeparTure.json"

# # 確保formatted_data包含departureResult和returnTripResult
# departure_result = formatted_data.get('departureResult', [])
# return_trip_result = formatted_data.get('returnTripResult', [])
# unresolved_cases = formatted_data.get('unresolvedCases', [])  # 取得未解決案件的資料

# # 將departureResult寫入對應的JSON文件
# if departure_json_file_path:
#     with open(departure_json_file_path, 'w', encoding='utf-8') as json_file:
#         json.dump(departure_result, json_file, ensure_ascii=False, indent=2, default=json_serial)
# else:
#     print("環境變量 'departure_json_file_path' 未設置。")

# # 將returnTripResult寫入對應的JSON文件
# if rdeparture_json_file_path:
#     with open(rdeparture_json_file_path, 'w', encoding='utf-8') as json_file:
#         json.dump(return_trip_result, json_file, ensure_ascii=False, indent=2, default=json_serial)
# else:
#     print("環境變量 'rdeparture_json_file_path' 未設置。")

# # 打印未解決案件
# if unresolved_cases:
#     print("\033[31m未解決的案件列表:\033[0m")
#     for case in unresolved_cases:
#         print(f"時間: {case['Time']}, 姓名: {case['CaseName']}, 上車地點: {case['Departure']}, 下車地點: {case['Destination']}")
# else:
#     print("無未解決案件。")
