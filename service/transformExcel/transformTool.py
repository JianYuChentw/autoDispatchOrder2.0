import json
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta

def convertDate(excel_date):
    if isinstance(excel_date, datetime):
        return excel_date.date()  # 如果是 datetime 對象，直接返回日期部分
    else:
        # 假設excel_date 是浮點數或整數表示的天數
        base_date = datetime(1899, 12, 30)  # Excel的日期基準（注意：有時 Excel 的基準日期是 1899-12-31）
        converted_date = base_date + timedelta(days=excel_date)
        return converted_date.date()


# 轉換時間數字為格式化時間字串
def convertTime(time_obj):
    if isinstance(time_obj, time):
        # 直接將時間轉換為總分鐘數
        total_minutes = time_obj.hour * 60 + time_obj.minute
    elif isinstance(time_obj, (int, float)):  # 假設 time_obj 是小數
        # 將小數形式的時間轉換為分鐘
        total_minutes = round(time_obj * 24 * 60)
    else:
        raise ValueError(f"未知的時間格式: {time_obj}")
    
    # 返回總分鐘數或其他你需要的格式
    return total_minutes

def format24Hour(original_time):
    # 解析時間字串並轉換為 UTC 時間
    date = datetime.strptime(original_time, '%Y-%m-%d %H:%M:%S')
    hours = date.hour
    minutes = date.minute

    # 使用 zfill 確保小時和分鐘都是兩位數
    formatted_hours = str(hours).zfill(2)
    formatted_minutes = str(minutes).zfill(2)

    # 返回格式化後的 24 小時制時間字串
    return f'{formatted_hours}:{formatted_minutes}'

def loadJson(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)

