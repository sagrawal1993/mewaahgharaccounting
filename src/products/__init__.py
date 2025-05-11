# This module will be used for product management.
# This will

import requests
import json

url = "https://www.mewaahghar.com/web/dataset/call_kw/product.template/web_search_read"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Referer": "https://www.mewaahghar.com/odoo/action-450",
    "Origin": "https://www.mewaahghar.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Connection": "keep-alive",
    "Cookie": "frontend_lang=en_IN; session_id=vVUi4_CbCwYblIv5sGYMJUjDYJCFFOVLVeniDvkkf4vfqJhC2aQHQ6Y03RP1BnIf8tD4SllFVKShj5XiOZ2i; cids=1; tz=Asia/Kolkata",
    "TE": "trailers"
}

payload = {
    "id": 9,
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "product.template",
        "method": "web_search_read",
        "args": [],
        "kwargs": {
            "specification": {
                "currency_id": {"fields": {"display_name": {}}},
                "activity_state": {},
                "categ_id": {"fields": {"display_name": {}}},
                "is_favorite": {},
                "name": {},
                "default_code": {},
                "product_variant_count": {},
                "list_price": {},
                "qty_available": {},
                "uom_id": {"fields": {"display_name": {}}},
                "product_properties": {},
                "image_128": {},
                "write_date": {},
                "show_on_hand_qty_status_button": {}
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
                "params": {
                    "action": 450,
                    "actionStack": [{"action": 450}]
                },
                "default_available_in_pos": True,
                "create_variant_never": "no_variant",
                "_pos_self_order": True,
                "current_company_id": 1
            },
            "count_limit": 10001,
            "domain": [["available_in_pos", "=", True]]
        }
    }
}


def get_products():
    response = requests.post(url, headers=headers, json=payload)
    return json.loads(response.text)