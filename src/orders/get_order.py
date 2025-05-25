import requests

from src.constants import main_db_cred, accounting_db_cred
from src.datamodel import DBCredentials, Order, ItemPlace
from src.utils import get_header, get_order_context, get_order_specifications, get_parm, create_payload, get_response, \
    place_order_specification, place_order_context


#url = 'https://mewaahghar.odoo.com/web/dataset/call_kw/pos.order/web_search_read'
#curl 'http://ec2-13-201-230-81.ap-south-1.compute.amazonaws.com:8069/web/dataset/call_kw/sale.order/web_search_read' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/json' -H 'Origin: http://ec2-13-201-230-81.ap-south-1.compute.amazonaws.com:8069' -H 'Connection: keep-alive' -H 'Referer: http://ec2-13-201-230-81.ap-south-1.compute.amazonaws.com:8069/odoo/orders' -H 'Cookie: frontend_lang=en_US; session_id=6Yv3eCBMlFyiFATjDsxDzGO3Mb3e3JJk4Dxm9NhJXud5Yam_eT7o7WgeJCzVb_STIObKlgMYJP6sZzl0nruy; cids=1' --data-raw '{"id":42,"jsonrpc":"2.0","method":"call","params":{"model":"sale.order","method":"web_search_read","args":[],"kwargs":{"specification":{"message_needaction":{},"currency_id":{"fields":{}},"name":{},"date_order":{},"commitment_date":{},"expected_date":{},"partner_id":{"fields":{"display_name":{}}},"user_id":{"fields":{"display_name":{}}},"activity_ids":{"fields":{}},"activity_exception_decoration":{},"activity_exception_icon":{},"activity_state":{},"activity_summary":{},"activity_type_icon":{},"activity_type_id":{"fields":{"display_name":{}}},"team_id":{"fields":{"display_name":{}}},"company_id":{"fields":{}},"amount_untaxed":{},"amount_tax":{},"amount_total":{},"tag_ids":{"fields":{"display_name":{},"color":{}}},"state":{},"effective_date":{},"delivery_status":{},"invoice_status":{},"client_order_ref":{},"validity_date":{}},"offset":0,"order":"","limit":80,"context":{"lang":"en_IN","tz":"Asia/Kolkata","uid":2,"allowed_company_ids":[1],"bin_size":true,"current_company_id":1},"count_limit":10001,"domain":[["state","not in",["draft","sent","cancel"]]]}}}'

def get_order_list(db_cred: DBCredentials, type: str, offset: int = 0, limit: int = 500 ):
    model = "pos.order"
    if type == "sale":
        model = "sale.order"
    url = f"{db_cred.db_url}/web/dataset/call_kw/{model}/web_search_read"
    referer = f"{db_cred.db_url}/odoo/{'sale-orders'  if type == 'sale' else 'pos-orders'}"
    origin = db_cred.db_url
    params_method = "web_search_read"
    method = "call"
    req_id = 30
    args = [ ]
    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_order_context(type=type)
    specification = get_order_specifications(type=type)
    params = get_parm(model, params_method, args, context, specification)
    params['kwargs'].update({"count_limit":10001,
                             "domain":[],
                            "offset": offset,
                            "order": "",
                            "limit": limit,})
    payload = create_payload(req_id, method, params)
    print(payload)
    response = get_response(url=url, header=headers, body=payload)

    if 'result' not in response:
        print(response)
        raise Exception("Result not part of outcome")
    elif 'records' not in response['result']:
        print(response)
        raise Exception("record not part of result")

    #return [ Product(**product) for product in response['result']['records']]
    print(response)

    # payload = {
    #     "id": 9,
    #     "jsonrpc": "2.0",
    #     "method": "call",
    #     "params": {
    #         "model": "pos.order",
    #         "method": "web_search_read",
    #         "args": [],
    #         "kwargs": {
    #             "specification": {
    #                 "currency_id": {"fields": {}},
    #                 "name": {},
    #                 "session_id": {"fields": {"display_name": {}}},
    #                 "date_order": {},
    #                 "config_id": {"fields": {"display_name": {}}},
    #                 "pos_reference": {},
    #                 "tracking_number": {},
    #                 "partner_id": {"fields": {"display_name": {}}},
    #                 "employee_id": {"fields": {"display_name": {}}},
    #                 "amount_total": {},
    #                 "state": {},
    #                 "is_edited": {}
    #             },
    #             "offset": 0,
    #             "order": "",
    #             "limit": 80,
    #             "context": {
    #                 "lang": "en_IN",
    #                 "tz": "Asia/Calcutta",
    #                 "uid": 2,
    #                 "allowed_company_ids": [1],
    #                 "bin_size": True,
    #                 "params": {
    #                     "action": "pos-orders",
    #                     "actionStack": [{"action": "pos-orders"}]
    #                 },
    #                 "current_company_id": 1
    #             },
    #             "count_limit": 10001,
    #             "domain": []
    #         }
    #     }
    # }

    # response = requests.post(url, headers=headers, json=payload)
    #
    # # Print response
    # print(response.status_code)
    # print(response.json())

def get_specific_order(order_id: int, db_cred: DBCredentials, type: str):
    model = "pos.order"
    if type == "sale":
        model = "sale.order"
    url = f"{db_cred.db_url}/web/dataset/call_kw/{model}/web_read"
    referer = f"{db_cred.db_url}/odoo/{'pos-orders' if type != 'sale' else 'sale-order'}"
    origin = db_cred.db_url
    params_method = "web_read"
    method = "call"
    req_id = 30
    args = [ [order_id]]
    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_order_context(specific_order=True, type='sale')
    specification = get_order_specifications(specific_order=True, type='sale')
    params = get_parm(model, params_method, args, context, specification)
    payload = create_payload(req_id, method, params)
    print(payload)
    response = get_response(url=url, header=headers, body=payload)
    print(response)
    return

def place_order(order: Order, db_cred: DBCredentials):
    url = f"{db_cred.db_url}/web/dataset/call_kw/sale.order/web_save"
    referer = f"{db_cred.db_url}/odoo/orders/new"
    origin = db_cred.db_url
    model = "sale.order"
    params_method = "web_save"
    method = "call"
    req_id = 30

    args = [[],
            {
                "locked": False,
                "partner_id": 11,
                "recompute_delivery_price": False,
                "l10n_in_gst_treatment": "consumer",
                "partner_invoice_id": 11,
                "partner_shipping_id": 11,
                "validity_date": "2025-06-24",
                "date_order": "2025-05-24 19:26:51",
                "show_update_pricelist": False,
                "company_id": 1,
                "pricelist_id": False,
                "payment_term_id": 1,
                "order_line": [
                    [
                        0,
                        "virtual_283",
                        {
                            "sequence": 10,
                            "display_type": False,
                            "is_downpayment": False,
                            "product_id": item.product_id,
                            "product_template_id": 183,
                            "product_custom_attribute_value_ids": [],
                            "product_no_variant_attribute_value_ids": [],
                            "linked_line_id": False,
                            "virtual_id": False,
                            "linked_virtual_id": False,
                            "selected_combo_items": False,
                            "combo_item_id": False,
                            "name": item.name,
                            "product_uom_qty": item.qty,
                            "move_ids": [],
                            "product_uom": 1,
                            "customer_lead": 0,
                            "product_packaging_qty": 0,
                            "product_packaging_id": False,
                            "is_delivery": False,
                            "price_unit": item.price_unit,
                            "purchase_price": 0,
                            "technical_price_unit": item.price_unit,
                            "tax_id": [],
                            "discount": 0,
                            "product_document_ids": []
                        }
                    ] for item in order.lines
                ],
                "note": f"<p>Terms &amp; Conditions: <a href=\"{db_cred.db_url}/terms\" target=\"_blank\" rel=\"noreferrer noopener\">{db_cred.db_url}/terms</a></p>",
                "sale_order_option_ids": [],
                "quotation_document_ids": [],
                "customizable_pdf_form_fields": False,
                "user_id": order.user_id,
                "team_id": 1,
                "cart_recovery_email_sent": False,
                "require_signature": True,
                "require_payment": False,
                "prepayment_percent": 1,
                "client_order_ref": False,
                "tag_ids": [],
                "show_update_fpos": False,
                "fiscal_position_id": 3,
                "warehouse_id": 1,
                "incoterm": False,
                "incoterm_location": False,
                "picking_policy": "direct",
                "commitment_date": False,
                "origin": False,
                "opportunity_id": False,
                "campaign_id": False,
                "medium_id": False,
                "source_id": False
            }
            ]

    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie)
    context = place_order_context()
    specification = place_order_specification()
    params = get_parm(model, params_method, args, context, specification)
    payload = create_payload(req_id, method, params)
    response = get_response(url=url, header=headers, body=payload)
    print(response)
    return response['result'][0]['id']

def confirm_order(order: Order, db_cred: DBCredentials):
    url = f"{db_cred.db_url}/web/dataset/call_button/sale.order/action_confirm"
    referer = f"{db_cred.db_url}/odoo/orders/new"
    origin = db_cred.db_url
    model = "sale.order"
    params_method = "action_confirm"
    method = "call"
    req_id = 30

    args = [[order.id]]

    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie)
    context = place_order_context(validate_analytics=True)
    params = get_parm(model, params_method, args, context, {})
    payload = create_payload(req_id, method, params)
    response = get_response(url=url, header=headers, body=payload)
    print(response)
    return response['id']




if __name__ == '__main__':
    db_cred = accounting_db_cred
    #get_order_list(db_cred)
    #get_specific_order(db_cred=db_cred, order_id=2230)
    # items = [ItemPlace(id=184, product_id=184, name="achar 1", qty=2, price_unit=60), ItemPlace(id=183, product_id=183, name="achar 2", qty=2, price_unit=80)]
    # order = Order(id=-1, user_id=2,lines=items)
    # order_id = place_order(order, db_cred)
    # order.id = order_id
    # confirm_order(order, db_cred)
    get_order_list(db_cred, "sale")
    #get_specific_order(20, db_cred, "sale")