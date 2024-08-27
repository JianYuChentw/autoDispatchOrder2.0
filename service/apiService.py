import requests

def sendPostRequest(url, payload=None, token=None, headers=None):

    
    if headers is None:
        headers = {
            "Content-Type": "application/json"
        }

    if token:
        if headers is None:
            headers = {}
        headers["X-Token"] = token
    try:
        # 使用 Session 保持一致性
        session = requests.Session()
        response = session.post(url, json=payload, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"發送請求時發生錯誤: {e}")
        return None


def sendGetRequest(url, params=None, token=None, headers=None):

    if token:
        if headers is None:
            headers = {}
        headers["X-Token"] = token
    
    if headers is None:
        headers = {
            "Content-Type": "application/json"
        }

    if params is None:
        params = {}

    try:
        response = requests.get(url, params=params, headers=headers)  #
        return response
    except requests.exceptions.RequestException as e:
        print(f"發送請求時發生錯誤: {e}")
        return None
