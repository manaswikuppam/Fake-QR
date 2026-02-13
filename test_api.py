import requests

url = "http://127.0.0.1:8000/scan"
payload = {"url": "http://secure-login.update.xyz"}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
