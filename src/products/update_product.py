from src.utils import get_header, get_product_context, get_product_specifications, get_parm, create_payload, get_response
from src.datamodel import Product, DBCredentials


def update_product(product: Product, db_cred: DBCredentials, ):
    product_id = product.id
    url = f"{db_cred.db_url}/web/dataset/call_kw/product.template/web_save"
    referer = f"{db_cred.db_url}/odoo/action-494/{product_id}"
    origin = db_cred.db_url
    model = "product.template"
    params_method = "web_save"
    method = "call"
    req_id = product_id

    args = [   [product_id], # Send list will contains the parameters to update
                {
                    "attribute_line_ids": [],
                    "company_id": False,
                    # "tracking": "none",
                    "qty_available": product.qty_available,
                    "image_1920": False,
                    "is_favorite": False,
                    "name": product.name,
                    "sale_ok": True,
                    "available_in_pos": True,
                    "active": True,
                    "type": "consu",
                    "is_storable": True,
                    "combo_ids": [],
                    "service_tracking": "no",
                    "lot_valuated": False,
                    "list_price": product.list_price,
                    "taxes_id": [],
                    "standard_price": product.standard_price,
                    #"supplier_taxes_id": [],
                    #"categ_id": False,
                    "default_code": False,
                    "barcode": False,
                    #"l10n_in_hsn_code": False,
                    #"product_properties": [],
                    #"description": False,
                    #"product_tag_ids": [],
                    #"description_sale": False,
                    "color": 0,
                    "to_weight": False,
                    #"pos_categ_ids": [],
                    #"public_description": False,
                    #"route_ids": [],
                    # "responsible_id": 6,
                    "weight": product.weight,
                    "volume": product.volume,
                    #"sale_delay": 0,
                    # "property_stock_production": 15,
                    # "property_stock_inventory": 14,
                    #"description_pickingin": False,
                    #"description_pickingout": False
                }
            ]

    headers = get_header(referer=referer, origin=origin, cookie=db_cred.cookie, extra_header=True)
    context = get_product_context(extra_setting=True)
    specification = get_product_specifications(type="update_product")
    params = get_parm(model, params_method, args, context, specification)
    payload = create_payload(req_id, method, params)

    response = get_response(url=url, header=headers, body=payload)
    return response['result'][0]['id']


if __name__ == '__main__':
    product_info = {
        "product": Product(**{
            "id": 21,
            "weight": 0.25,
            "volume": 0,
            "list_price": 400,
            "standard_price": 380,
            "qty_available": 0,
            "name": "Testing Updated",
        }),
        "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
        "db_url": "https://mewaahgharstore.odoo.com",
    }
    print(update_product(**product_info))