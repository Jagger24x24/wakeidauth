import requests
import json
from bs4 import BeautifulSoup



def GetExchangeCode(username, password):
    """Returns the classlink exchangecode
    Username: WakeID Username
    Password: WakeID Password
    """
    headers = {}
    session = requests.Session()  # Create a session object

    # Perform the first GET request
    url = "https://tenant-management-service.classlink.io/login/v2p1/authenticateADFS?code=wakecounty"
    response = session.get(url)

    # Perform the second GET request
    url = "https://wakeid2.wcpss.net/api/rest/authn"
    response = session.get(url, headers=headers)

    # Extract the ID from the response
    id = json.loads(response.content)["id"]

    # Prepare and perform the POST request for username
    url = "https://wakeid2.wcpss.net/api/rest/v2/authn"
    headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    }

    data = json.dumps({
        "id": id,
        "isPasswordRecovery": False,
        "type": "username",
        "username": username,
        "realm": "8e14a77b-2f8a-4047-b703-513997e28dac"  # this just means we are a student
    })
    response = session.post(url=url, data=data, headers=headers)

    # Prepare and perform the POST request for password
    data = json.dumps({
        "id": id,
        "type": "password",
        "password": password,
    })
    response = session.post(url=url, data=data, headers=headers)

    # Prepare and perform the POST request for SAMLResponse
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    response = session.post(url="https://wakeid2.wcpss.net/idp/authn/idauto", data="complete=1", headers=headers)

    # Prepare and perform POST request for classlink exchangeCode
    soup = BeautifulSoup(response.text, 'html.parser')
    input_element = soup.find('input', id='saml-response')
    if input_element:
        SAMLResponse = input_element.get('value') # Get the SAMLReponse value from the html file from previos response
    else:
        return

    url = "https://tenant-management-service.classlink.io/saml/v1p0/3348/SAMLHandler"
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    response = session.post(url=url, data={"SAMLResponse": SAMLResponse})

    exchangeCode = response.url[41:-19] # Extract the classlink exchangeCode from the url

    return exchangeCode