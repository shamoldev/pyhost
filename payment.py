import requests

js = {"method":"users.log_in","params":{"login":"942935307","password":"20070127"}}


h = {
    "Authority": "payme.uz",
    "Method": "POST",
    "Path": "/api/users.log_in",
    "Scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,uz;q=0.8",
    "Adrum": "isAjax:true",
    "Api-Session": "ca87981a236066fcf3f736002fedfda3; SxG=urEb=4Ru9rXKMWJ12sNyRt%g7X1HEaBS9eWZMppNxy4dgxDKzV#Wh3fA7?6C; active; 1691168733034; 900000",
    "App-Version": "2.39",
    "Content-Length": "78",
    "Content-Type": "application/json; charset=UTF-8",
    "Cookie": "_ga=GA1.1.1618562227.1689868260; _ym_uid=168986826135649916; _ym_d=1689868261; _fbp=fb.1.1689868262876.1461094644; ngx-device=7cafc34c2ae59927d9af029e405e5b4379939ce14308040feb20d00790522964; cookiesession1=678A3E16D17E4B2FB92A488E4163B9F3; ADRUM=s=1691167870063&r=https%3A%2F%2Fpayme.uz%2Flogin; _ym_isad=2; _ga_W9V4BPZNLX=GS1.1.1691167772.8.1.1691168028.60.0.0; _ga_PFZ4HL7H2T=GS1.1.1691167772.8.1.1691168029.0.0.0",
    "Device": "64b9583fb017d105175b3100; FdO1FxzBP5E#M@sy0W5#EMjJ=ZNPZUt1NpR=2Nfqo6igwb6pQ5YQN%5%pyB2e35w;",
    "Origin": "https://payme.uz",
    "Referer": "https://payme.uz/login",
    "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Track-Id": "7cafc34c2ae59927d9af029e405e5b4379939ce14308040feb20d00790522964",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "X-Accept-Language": "ru"
}
# response = requests.post("https://payme.uz/api/users.log_in",json=js,headers=h)
# print(response.headers)
def create_payment(amount):
    amount = amount * 100
    json_data = {
        "method": "p2p.create",
        "params": {
            "card_id": "646773387044c9d1c452ee14",
            # "title": "✅Tolov : @Pyhostuzbot",
            "amount": amount
        }
    }
    try:
        response = requests.post("https://payme.uz/api/users.log_in",json=js,headers=h)
        #print(response.headers)
        res = requests.post("https://payme.uz/api/p2p.create", json=json_data, headers=response.headers)
        return res.json()['result']['cheque']['_id']
    except Exception as e:
        print("Error:", res.json())
        return False


def check_payment(payid):
    json = {"method":"cheque.get","params":{"id":f"{payid}"}}  
    try:
        response = requests.post("https://payme.uz/api/users.log_in",json=js,headers=h)
        
        res = requests.post("https://payme.uz/api/cheque.get", json=json, headers=response.headers).json()
        if res['result']['cheque']['pay_time']==0:
            return False
        else:
            return True
    except Exception as e:
        print("Error:", e)
        return False