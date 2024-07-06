import requests

def kalshiLogin(username, password):
    url = "https://trading-api.kalshi.com/trade-api/v2/login"
    payload = {
        "email": username,
        "password": password
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token = response.json()["token"]
        print(f"Login successful. Token: {token}")
        return token
    else:
        print(f"Login failed: {response.status_code} {response.text}")
        return None
    
def getAccountBalance(token):
    url = "https://trading-api.kalshi.com/trade-api/v2/portfolio/balance"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        account_info = response.json()
        balance = account_info.get("balance", None)
        return balance
    else:
        print(f"Failed to retrieve account balance: {response.status_code} {response.text}")
        return None