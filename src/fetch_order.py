import requests
import json

# Define the URL
url = 'https://mewa-ghar.odoo.com/web/dataset/call_kw/pos.order/web_search_read'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://mewa-ghar.odoo.com/odoo/pos-orders',
    'Origin': 'https://mewa-ghar.odoo.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': 'frontend_lang=en_IN; cids=1; utm_source=db; utm_medium=module; session_id=rEUmekqdfClw203uzvUUPti0Hoo8KWUWkV7xAwcBLKLHqzRUtHzpvUVGBlEF_ZVjKBdBequHs6Y0BQLUHfKf; tz=Asia/Kolkata',
    'TE': 'trailers',
}

# Define the data payload
data = {
    "id": 9,
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "pos.order",
        "method": "web_search_read",
        "args": [],
        "kwargs": {
            "specification": {
                "currency_id": {"fields": {}},
                "name": {},
                "session_id": {"fields": {"display_name": {}}},
                "date_order": {},
                "config_id": {"fields": {"display_name": {}}},
                "pos_reference": {},
                "tracking_number": {},
                "partner_id": {"fields": {"display_name": {}}},
                "employee_id": {"fields": {"display_name": {}}},
                "amount_total": {},
                "state": {},
                "is_edited": {}
            },
            "offset": 0,
            "order": "",
            "limit": 80,
            "context": {
                "lang": "en_IN",
                "tz": "Asia/Calcutta",
                "uid": 2,
                "allowed_company_ids": [1],
                "bin_size": True,
                "params": {"action": "pos-orders", "actionStack": [{"action": "pos-orders"}]},
                "current_company_id": 1
            },
            "count_limit": 10001,
            "domain": []
        }
    }
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful.")
    print(response.json())  # Print the response from the server
else:
    print(f"Request failed with status code {response.status_code}")
