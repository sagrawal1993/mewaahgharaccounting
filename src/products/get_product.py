from src.utils import get_header, get_context, get_specifications, get_parm, create_payload, get_response
from src.datamodel import Product, DBCredentials


def get_product_list(db_cred: DBCredentials, offset: int = 0, limit: int = 500):
    url = f"{db_cred.db_url}/web/dataset/call_kw/product.template/web_save"
    referer = f"{db_cred.db_url}/odoo/action-450"
    origin = db_cred.db_url
    model = "product.template"
    params_method = "web_search_read"
    method = "call"
    req_id = 30
    args = [ ]
    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_context(get_product=True)
    specification = get_specifications(type="get_product")
    params = get_parm(model, params_method, args, context, specification)

    params['kwargs'].update({"count_limit":10001,
                             "domain":[],
                            "offset": offset,
                            "order": "",
                            "limit": limit,})

    payload = create_payload(req_id, method, params)

    response = get_response(url=url, header=headers, body=payload)

    if 'result' not in response:
        print(response)
        raise Exception("Result not part of outcome")
    elif 'records' not in response['result']:
        print(response)
        raise Exception("record not part of result")

    return [ Product(**product) for product in response['result']['records']]


if __name__ == '__main__':
    product_info = {
        "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
        "db_url": "https://mewaahgharstore.odoo.com",
    }
    print(get_product_list(**product_info))