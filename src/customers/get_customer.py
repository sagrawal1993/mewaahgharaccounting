from src.constants import main_db_cred, pos_db_cred
from src.utils import get_header, get_customer_specification, get_customer_context, get_parm, create_payload, get_response
from src.datamodel import DBCredentials, Customer, CompanyType


def get_customer_list(db_cred: DBCredentials, offset: int = 0, limit: int = 500 ):
    url = f"{db_cred.db_url}/web/dataset/call_kw/res.partner/web_search_read"
    referer = f"{db_cred.db_url}/odoo/customers"
    origin = db_cred.db_url
    model = "res.partner"
    params_method = "web_search_read"
    method = "call"
    req_id = 30
    args = [ ]
    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_customer_context()
    specification = get_customer_specification()
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

def handle_customer(customer: Customer, db_cred: DBCredentials):
    url = f"{db_cred.db_url}/web/dataset/call_kw/res.partner/web_save"
    referer = f"{db_cred.db_url}/odoo/customers/new"
    origin = db_cred.db_url
    model = "res.partner"
    params_method = "web_save"
    method = "call"
    req_id = 30
    args = [
                [customer.id] if customer.id != -1 else [],
                {
                    "partner_gid": 0,
                    "additional_info": False,
                    "image_1920": False,
                    "company_type": customer.company_type,
                    "name": customer.name,
                    "parent_id": False,
                    "company_name": False,
                    "type": "contact",
                    "street": customer.street,
                    "street2": False,
                    "city": False,
                    "zip": False,
                    "state_id": False,
                    "country_id": False,
                    "l10n_in_gst_treatment": False,
                    "vat": customer.gstin,
                    "vies_valid": False,
                    "l10n_in_pan": False,
                    "function": False,
                    "phone": customer.phone_number,
                    "email": customer.email,
                    "website": False,
                    "lang": "en_IN",
                    "category_id": [],
                    "child_ids": [],
                    "user_id": False,
                    "property_payment_term_id": False,
                    "property_inbound_payment_method_line_id": False,
                    "property_product_pricelist": 1,
                    "property_supplier_payment_term_id": False,
                    "property_outbound_payment_method_line_id": False,
                    "barcode": False,
                    "property_account_position_id": False,
                    "company_registry": False,
                    "ref": False,
                    "company_id": False,
                    "industry_id": False,
                    # "property_stock_customer": 5,
                    # "property_stock_supplier": 4,
                    "followup_line_id": False,
                    "followup_reminder_type": "automatic",
                    "followup_next_action_date": False,
                    "followup_responsible_id": False,
                    "invoice_sending_method": False,
                    "invoice_edi_format": False,
                    "invoice_template_pdf_report_id": False,
                    "peppol_eas": False,
                    "peppol_endpoint": False,
                    "use_partner_credit_limit": False,
                    "credit_limit": 0,
                    "comment": False,
                    "partner_longitude": 0,
                    "partner_latitude": 0
                }
            ]
    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_customer_context(add_new=True)
    specification = get_customer_specification(add_new=True)
    params = get_parm(model, params_method, args, context, specification)
    payload = create_payload(req_id, method, params)
    response = get_response(url=url, header=headers, body=payload)
    print(response)
    return response['result'][0]['id']


if __name__ == '__main__':
    db_cred = main_db_cred
    #get_customer_list(db_cred)
    handle_customer(Customer(name="function_test_company_changed", phone_number="+919026368175", company_type=CompanyType().person), pos_db_cred)