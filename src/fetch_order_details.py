import requests
import json

# Define the URL
url = 'https://mewaahghar.odoo.com/web/dataset/call_kw/pos.order/web_read'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://mewaahghar.odoo.com/odoo/pos-orders',
    'Origin': 'https://mewaaahghar.odoo.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': 'frontend_lang=en_IN; cids=1; utm_source=db; utm_medium=module; session_id=rEUmekqdfClw203uzvUUPti0Hoo8KWUWkV7xAwcBLKLHqzRUtHzpvUVGBlEF_ZVjKBdBequHs6Y0BQLUHfKf; tz=Asia/Kolkata',
    'Priority': 'u=0'
}

# Define the data payload
data = {
    "id": 12,
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "pos.order",
        "method": "web_read",
        "args": [[1096]],  # The list containing the ID [1096]
        "kwargs": {
            "context": {
                "lang": "en_IN",
                "tz": "Asia/Calcutta",
                "uid": 2,
                "allowed_company_ids": [1],
                "bin_size": True,
                "params": {
                    "action": "pos-orders",
                    "actionStack": [{"action": "pos-orders"}]
                }
            },
            "specification": {
                "state": {},
                "has_refundable_lines": {},
                "failed_pickings": {},
                "picking_count": {},
                "sale_order_count": {},
                "refund_orders_count": {},
                "refunded_order_id": {"fields": {"display_name": {}}},
                "name": {},
                "date_order": {},
                "session_id": {"fields": {"display_name": {}}},
                "employee_id": {"fields": {"display_name": {}}},
                "user_id": {"fields": {"display_name": {}}},
                "order_edit_tracking": {},
                "is_edited": {},
                "partner_id": {"fields": {"display_name": {}}},
                "fiscal_position_id": {"fields": {"display_name": {}}},
                "lines": {
                    "fields": {
                        "name": {},
                        "full_product_name": {},
                        "l10n_in_hsn_code": {},
                        "product_id": {"fields": {"display_name": {}}},
                        "is_edited": {},
                        "qty": {},
                        "customer_note": {},
                        "price_unit": {},
                        "is_total_cost_computed": {},
                        "total_cost": {},
                        "margin": {},
                        "margin_percent": {},
                        "discount": {},
                        "tax_ids_after_fiscal_position": {"fields": {"display_name": {}}},
                        "tax_ids": {},
                        "price_subtotal": {},
                        "price_subtotal_incl": {},
                        "currency_id": {"fields": {}},
                        "refunded_qty": {},
                        "notice": {}
                    },
                    "limit": 40,
                    "order": ""
                },
                "amount_tax": {},
                "amount_total": {},
                "amount_paid": {},
                "margin": {},
                "margin_percent": {},
                "is_total_cost_computed": {},
                "currency_id": {"fields": {}},
                "payment_ids": {
                    "fields": {
                        "currency_id": {"fields": {}},
                        "payment_date": {},
                        "payment_method_id": {"fields": {"display_name": {}}},
                        "amount": {},
                        "payment_method_payment_mode": {},
                        "card_no": {},
                        "card_brand": {},
                        "cardholder_name": {}
                    },
                    "limit": 40,
                    "order": ""
                },
                "amount_difference": {},
                "session_move_id": {"fields": {"display_name": {}}},
                "pos_reference": {},
                "tracking_number": {},
                "country_code": {},
                "pricelist_id": {"fields": {"display_name": {}}},
                "floating_order_name": {},
                "email": {},
                "mobile": {},
                "general_note": {},
                "available_payment_method_ids": {},
                "nb_print": {},
                "display_name": {}
            }
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
