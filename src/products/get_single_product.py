from src.utils import get_header, get_context, get_specifications, get_parm, create_payload, get_response
from src.datamodel import Product, DBCredentials


def get_single_product(product_id: int, db_cred: DBCredentials):
    url = f"{db_cred.db_url}/web/dataset/call_kw/product.template/web_read"
    referer = f"{db_cred.db_url}/odoo/action-450"
    origin = db_cred.db_url
    model = "product.template"
    params_method = "web_read"
    method = "call"
    req_id = 30
    args = [product_id]

    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_context(extra_setting=True)
    specification = get_specifications(type="get_single_product")
    params = get_parm(model, params_method, args, context, specification)
    payload = create_payload(req_id, method, params)

    response = get_response(url=url, header=headers, body=payload)
    return Product(**response['result'][0])

if __name__ == '__main__':
    product_id = 5
    product_info = {
        "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
        "db_url": "https://mewaahgharstore.odoo.com",
        "product_id": product_id
    }
    print(get_single_product(**product_info))