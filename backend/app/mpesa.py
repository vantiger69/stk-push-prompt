import os
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv



load_dotenv()


def generate_password():
    shortcode = os.getenv("BUSINESS_SHORTCODE")
    passkey = os.getenv("PASSKEY")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data = shortcode + passkey + timestamp
    print(f"BusinessShortCode: {shortcode}")
    print(f"Timestamp: {timestamp}")
    print(f"To encode : {shortcode + passkey + timestamp}")


    password = base64.b64encode(data.encode())
    print(f"Encoded Password: {password}")

    

    password = password.decode("utf-8")
    print("Generated password:",password)
    return password, timestamp




def get_access_token():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    print("Consumer Key:", consumer_key)
    print("Consumer Secret:", consumer_secret)
    
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)


    data = response.json()

    print("Access Token Response:",data)

    access_token = data.get("access_token")


    if not access_token:
        raise Exception(f"Failed to receive access token.Response: {data}")
    return response.json()["access_token"]



def stk_push(phone_number, amount):

    
    token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"



    password,timestamp = generate_password()
    headers  = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }




    payload = {
        "BusinessShortCode": os.getenv("BUSINESS_SHORTCODE"),
        "Password":password,
        "Timestamp":timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount":amount,
        "PartyA":phone_number,
        "PartyB":os.getenv("BUSINESS_SHORTCODE"),
        "PhoneNumber":phone_number,
        "CallBackURL":os.getenv("CALLBACK_URL"),
        "AccountReference":"Test123",
        "TransactionDesc":"Test payment",
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Response status code:", response.status_code)
    print("Response here:", response.text)

    try:
        reponse_json = response.json()
    except ValueError:
        print("Error: Response is not JSON")
    return reponse_json, payload.get("password"), payload.get("Timestamp"), response.status_code
    