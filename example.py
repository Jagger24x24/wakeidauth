import WakeIDAuth
import getpass
import json
import requests

username = input("Enter username: ")
password = getpass.getpass("Enter your password: ")
exchangeCode = WakeIDAuth.GetExchangeCode(username, password)

if exchangeCode:
    response = requests.get(url=f"https://applications.apis.classlink.com/exchangeCode?code={exchangeCode}&response_type=code")
    profile = json.loads(response.text)

    displayname = profile["user"]["displayName"]
    print(f"Welcome back", profile["user"]["displayName"])
    print("Email:", profile["user"]["email"])
else:
    print("Incorrect username or password.")