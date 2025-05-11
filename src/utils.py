import requests
import json

def get_response(url, header, body):
    try:
        response = requests.post(url, headers=header, json=body)
        if response.status_code != 200:
            raise Exception(f"Non 200 response for {url}")
        return json.loads(response.text)
    except Exception as e:
        raise Exception(e)


def get_header(referer, origin, cookie, extra_header=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Referer": referer,
        "Origin": origin,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Priority": "u=0",
    }
    if extra_header:
        headers.update({'TE': 'trailers'})
    return headers

def get_context(extra_setting=False, update_product=False, get_product=False):

    context = {
        "lang": "en_IN",
        "tz": "Asia/Kolkata",
        "uid": 6,
        "allowed_company_ids": [1],
        "default_available_in_pos": True,
        "create_variant_never": "no_variant",
        "_pos_self_order": True
    } # add_new_product, get_product,
    if extra_setting: # get_single_product
        context.update({
            "params":
                {
                    "action": 450,
                    "actionStack": [{"action": 450}]
                }
        })
    elif get_product:
        if extra_setting:  # get_single_product
            context.update({
                "params":
                    {
                        "action": 494,
                        "actionStack": [{"action": 494}]
                    }
            })

    elif update_product:
        context.update({
            "params": {"actionStack": [{"displayName": "Products", "action": 494, "view_type": "kanban"}],
                       "action": 494}

        })
    return context

def create_payload(id: int, method: str, params: dict):
    payload = {
        "id": id,
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }
    return payload

def get_parm(model, method, args, context, specification):
    params = {
        "model": model,
        "method": method,
        "args": args,
        "kwargs": {
            "context": context,
            "specification": specification
        }
    }
    return params

def get_specifications(type: str = None):
    if type=="get_single_product":
        return {
                "name": {},
                "list_price": {},
                "standard_price": {},
                "qty_available": {},
                "weight": {},
                "volume": {},
                "default_code": {},
                "barcode": {},
                "image_1920": {},
                "description_sale": {},
                "product_variant_count": {},
                "categ_id": {"fields": {"display_name": {}}},
                "currency_id": {"fields": {}}
            }
    elif type== "get_product":
        return {
                    "currency_id": {
                         "fields": {
                              "display_name": {}
                         }
                    },
                    "activity_state": {},
                    "categ_id": {
                         "fields": {
                              "display_name": {}
                         }
                    },
                    "is_favorite": {},
                    "name": {},
                    "default_code": {},
                    "product_variant_count": {},
                    "list_price": {},
                    "qty_available": {},
                    "standard_price": {},
                    "weight": {},
                    "volume": {},
                    "uom_id": {
                         "fields": {
                              "display_name": {}
                         }
                    },
                    "product_properties": {},
                    "image_128": {},
                    "write_date": {},
                    "show_on_hand_qty_status_button": {}
               }
    elif type == "add_product":
        return {
                "l10n_in_hsn_warning": {},
                "product_variant_count": {},
                "is_product_variant": {},
                "attribute_line_ids": {},
                "company_id": {"fields": {}},
                "fiscal_country_codes": {},
                "pricelist_item_count": {},
                "tracking": {},
                "show_on_hand_qty_status_button": {},
                "show_forecasted_qty_status_button": {},
                "qty_available": {},
                "virtual_available": {},
                "uom_name": {},
                "product_document_count": {},
                "reordering_min_qty": {},
                "reordering_max_qty": {},
                "nbr_reordering_rules": {},
                "nbr_moves_in": {},
                "nbr_moves_out": {},
                "id": {},
                "image_1920": {},
                "write_date": {},
                "is_favorite": {},
                "name": {},
                "sale_ok": {},
                "available_in_pos": {},
                "active": {},
                "type": {},
                "is_storable": {},
                "show_qty_update_button": {},
                "combo_ids": {"fields": {"display_name": {}}},
                "service_tracking": {},
                "product_tooltip": {},
                "lot_valuated": {},
                "list_price": {},
                "taxes_id": {
                    "fields": {"display_name": {}},
                    "context": {
                        "default_type_tax_use": "sale",
                        "search_default_sale": 1
                    }
                },
                "tax_string": {},
                "standard_price": {},
                "supplier_taxes_id": {
                    "fields": {"display_name": {}},
                    "context": {
                        "default_type_tax_use": "purchase",
                        "search_default_purchase": 1
                    }
                },
                "categ_id": {"fields": {"display_name": {}}},
                "default_code": {},
                "valid_product_template_attribute_line_ids": {},
                "barcode": {},
                "l10n_in_hsn_code": {},
                "currency_id": {"fields": {}},
                "cost_currency_id": {"fields": {}},
                "product_variant_id": {"fields": {}},
                "product_properties": {},
                "description": {},
                "product_tag_ids": {"fields": {"display_name": {}}},
                "description_sale": {},
                "color": {},
                "to_weight": {},
                "pos_categ_ids": {"fields": {"display_name": {}, "color": {}}},
                "public_description": {},
                "has_available_route_ids": {},
                "route_ids": {"fields": {}},
                "route_from_categ_ids": {"fields": {"display_name": {}}},
                "responsible_id": {"fields": {"display_name": {}}},
                "weight": {},
                "weight_uom_name": {},
                "volume": {},
                "volume_uom_name": {},
                "sale_delay": {},
                "property_stock_production": {"fields": {"display_name": {}}},
                "property_stock_inventory": {"fields": {"display_name": {}}},
                "description_pickingin": {},
                "description_pickingout": {},
                "is_dynamically_created": {},
                "purchase_ok": {},
                "l10n_in_is_gst_registered_enabled": {},
                "display_name": {}
            }
    elif type=="update_product":
        return {
                "l10n_in_hsn_warning": {},
                "product_variant_count": {},
                "is_product_variant": {},
                "attribute_line_ids": {},
                "company_id": {"fields": {}},
                "fiscal_country_codes": {},
                "pricelist_item_count": {},
                "tracking": {},
                "show_on_hand_qty_status_button": {},
                "show_forecasted_qty_status_button": {},
                "qty_available": {},
                "virtual_available": {},
                "uom_name": {},
                "product_document_count": {},
                "reordering_min_qty": {},
                "reordering_max_qty": {},
                "nbr_reordering_rules": {},
                "nbr_moves_in": {},
                "nbr_moves_out": {},
                "id": {},
                "image_1920": {},
                "write_date": {},
                "is_favorite": {},
                "name": {},
                "sale_ok": {},
                "available_in_pos": {},
                "active": {},
                "type": {},
                "is_storable": {},
                "show_qty_update_button": {},
                "combo_ids": {"fields": {"display_name": {}}},
                "service_tracking": {},
                "product_tooltip": {},
                "lot_valuated": {},
                "list_price": {},
                "taxes_id": {"fields": {"display_name": {}}},
                "tax_string": {},
                "standard_price": {},
                "supplier_taxes_id": {"fields": {"display_name": {}}},
                "categ_id": {"fields": {"display_name": {}}},
                "default_code": {},
                "valid_product_template_attribute_line_ids": {},
                "barcode": {},
                "l10n_in_hsn_code": {},
                "currency_id": {"fields": {}},
                "cost_currency_id": {"fields": {}},
                "product_variant_id": {"fields": {}},
                "product_properties": {},
                "description": {},
                "product_tag_ids": {"fields": {"display_name": {}}},
                "description_sale": {},
                "color": {},
                "to_weight": {},
                "pos_categ_ids": {"fields": {"display_name": {}, "color": {}}},
                "public_description": {},
                "has_available_route_ids": {},
                "route_ids": {"fields": {}},
                "route_from_categ_ids": {"fields": {"display_name": {}}},
                "responsible_id": {"fields": {"display_name": {}}},
                "weight": {},
                "weight_uom_name": {},
                "volume": {},
                "volume_uom_name": {},
                "sale_delay": {},
                "property_stock_production": {"fields": {"display_name": {}}},
                "property_stock_inventory": {"fields": {"display_name": {}}},
                "description_pickingin": {},
                "description_pickingout": {},
                "is_dynamically_created": {},
                "purchase_ok": {},
                "l10n_in_is_gst_registered_enabled": {},
                "display_name": {}
            }
    return {
                "l10n_in_hsn_warning": {},
                "product_variant_count": {},
                "service_type": {},
                "visible_expense_policy": {},
                "is_kits": {},
                "is_product_variant": {},
                "attribute_line_ids": {},
                "company_id": {"fields": {}},
                "fiscal_country_codes": {},
                "pricelist_item_count": {},
                "is_published": {},
                "tracking": {},
                "show_on_hand_qty_status_button": {},
                "show_forecasted_qty_status_button": {},
                "qty_available": {},
                "uom_name": {},
                "virtual_available": {},
                "bom_count": {},
                "product_document_count": {},
                "sales_count": {},
                "purchased_product_qty": {},
                "used_in_bom_count": {},
                "mrp_product_qty": {},
                "reordering_min_qty": {},
                "reordering_max_qty": {},
                "nbr_reordering_rules": {},
                "nbr_moves_in": {},
                "nbr_moves_out": {},
                "id": {},
                "image_1920": {},
                "write_date": {},
                "is_favorite": {},
                "name": {},
                "sale_ok": {},
                "purchase_ok": {},
                "available_in_pos": {},
                "active": {},
                "type": {},
                "invoice_policy": {},
                "is_storable": {},
                "combo_ids": {"fields": {"display_name": {}}},
                "service_tracking": {},
                "product_tooltip": {},
                "lot_valuated": {},
                "list_price": {},
                "taxes_id": {"fields": {"display_name": {}}, "context": {"default_type_tax_use": "sale", "search_default_sale": 1}},
                "tax_string": {},
                "standard_price": {},
                "cost_method": {},
                "valuation": {},
                "supplier_taxes_id": {"fields": {"display_name": {}}, "context": {"default_type_tax_use": "purchase", "search_default_purchase": 1}},
                "categ_id": {"fields": {"display_name": {}}},
                "default_code": {},
                "valid_product_template_attribute_line_ids": {},
                "barcode": {},
                "l10n_in_hsn_code": {},
                "currency_id": {"fields": {}},
                "cost_currency_id": {"fields": {}},
                "product_variant_id": {"fields": {}},
                "product_properties": {},
                "description": {},
                "optional_product_ids": {"fields": {"display_name": {}, "color": {}}, "context": {"search_product_product": True}},
                "accessory_product_ids": {"fields": {"display_name": {}}},
                "alternative_product_ids": {"fields": {"display_name": {}},"context": {"search_product_product": True}},
                "description_ecommerce": {},
                "product_tag_ids": {"fields": {"display_name": {}}},
                "public_categ_ids": {"fields": {"display_name": {}}},
                "allow_out_of_stock_order": {},
                "show_availability": {},
                "available_threshold": {},
                "out_of_stock_message": {},
                "product_template_image_ids": {"fields": {"sequence": {}, "image_1920": {}, "write_date": {}, "name": {}},"limit": 40,"order": "sequence ASC"},
                "description_sale": {},
                "expense_policy": {},
                "color": {},
                "to_weight": {},
                "pos_categ_ids": {"fields": {"display_name": {}, "color": {}}},
                "public_description": {},
                "seller_ids": {"fields": {"sequence": {}, "partner_id": {"fields": {"display_name": {}}}, "product_tmpl_id": {"fields": {"display_name": {}}}, "product_name": {}, "product_code": {}, "date_start": {}, "date_end": {}, "min_qty": {}, "price": {}, "discount": {}, "delay": {}, "company_id": {"fields": {}}},"context": {"product_template_invisible_variant": True,"list_view_ref": "purchase.product_supplierinfo_tree_view2"},"limit": 40,"order": "sequence ASC, id ASC"},
                "variant_seller_ids": {"fields": {"sequence": {}, "partner_id": {"fields": {"display_name": {}}}, "product_tmpl_id": {"fields": {"display_name": {}}}, "product_name": {}, "product_code": {}, "date_start": {}, "date_end": {}, "min_qty": {}, "price": {}, "discount": {}, "delay": {}, "company_id": {"fields": {}}},"context": {"model": "product.template","list_view_ref": "purchase.product_supplierinfo_tree_view2"},"limit": 40,"order": "sequence ASC, id ASC"},
                "service_to_purchase": {},
                "purchase_method": {},
                "description_purchase": {},
                "has_available_route_ids": {},
                "route_ids": {"fields": {}},
                "route_from_categ_ids": {"fields": {"display_name": {}}},
                "responsible_id": {"fields": {"display_name": {}}},
                "weight": {},
                "weight_uom_name": {},
                "volume": {},
                "volume_uom_name": {},
                "sale_delay": {},
                "hs_code": {},
                "country_of_origin": {"fields": {"display_name": {}}},
                "description_pickingin": {},
                "description_pickingout": {},
                "property_account_income_id": {"fields": {"display_name": {}}},
                "property_account_expense_id": {"fields": {"display_name": {}}},
                "property_account_creditor_price_difference": {"fields": {"display_name": {}}},
                "display_name": {}
            }


