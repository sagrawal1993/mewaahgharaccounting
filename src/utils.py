import requests
import json
# key for accounting db: 9a614ef02fed1638611e0db4c732a7a87d9860aa
def get_response(url, header, body):
    try:
        response = requests.post(url, headers=header, json=body)
        if response.status_code != 200:
            print(response.text)
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

def get_product_context(extra_setting=False, update_product=False, get_product=False):

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

        }
    }

    if specification:
        params["kwargs"].update({"specification": specification})
    return params

def get_product_specifications(type: str = None):
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


def get_order_specifications(specific_order=False, type="pos"):
    if type=="sale":
        return {
                "message_needaction": {

                },
                "currency_id": {
                    "fields": {

                    }
                },
                "name": {

                },
                "date_order": {

                },
                "commitment_date": {

                },
                "expected_date": {

                },
                "partner_id": {
                    "fields": {
                        "display_name": {

                        }
                    }
                },
                "user_id": {
                    "fields": {
                        "display_name": {

                        }
                    }
                },
                "activity_ids": {
                    "fields": {

                    }
                },
                "activity_exception_decoration": {

                },
                "activity_exception_icon": {

                },
                "activity_state": {

                },
                "activity_summary": {

                },
                "activity_type_icon": {

                },
                "activity_type_id": {
                    "fields": {
                        "display_name": {

                        }
                    }
                },
                "team_id": {
                    "fields": {
                        "display_name": {

                        }
                    }
                },
                "company_id": {
                    "fields": {

                    }
                },
                "amount_untaxed": {

                },
                "amount_tax": {

                },
                "amount_total": {

                },
                "tag_ids": {
                    "fields": {
                        "display_name": {

                        },
                        "color": {

                        }
                    }
                },
                "state": {

                },
                "effective_date": {

                },
                "delivery_status": {

                },
                "invoice_status": {

                },
                "client_order_ref": {

                },
                "validity_date": {

                }
            }
    if specific_order:
        return {
            "state":{

            },
            "has_refundable_lines":{

            },
            "failed_pickings":{

            },
            "picking_count":{

            },
            "sale_order_count":{

            },
            "refund_orders_count":{

            },
            "refunded_order_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "attendee_count":{

            },
            "name":{

            },
            "date_order":{

            },
            "session_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "employee_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "user_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "order_edit_tracking":{

            },
            "is_edited":{

            },
            "partner_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "res_partner_search_mode":"customer"
               }
            },
            "fiscal_position_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "lines":{
               "fields":{
                  "name":{

                  },
                  "full_product_name":{

                  },
                  "l10n_in_hsn_code":{

                  },
                  "product_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "is_edited":{

                  },
                  "qty":{

                  },
                  "customer_note":{

                  },
                  "price_unit":{

                  },
                  "is_total_cost_computed":{

                  },
                  "total_cost":{

                  },
                  "margin":{

                  },
                  "margin_percent":{

                  },
                  "discount":{

                  },
                  "tax_ids_after_fiscal_position":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "tax_ids":{

                  },
                  "price_subtotal":{},
                  "price_subtotal_incl":{},
                  "currency_id":{
                     "fields":{}
                  },
                  "refunded_qty":{},
                  "notice":{}
               },
               "limit":40,
               "order":""
            },
            "amount_tax":{},
            "amount_total":{},
            "amount_paid":{},
            "margin":{},
            "margin_percent":{},
            "is_total_cost_computed":{},
            "currency_id":{
               "fields":{}
            },
            "payment_ids":{
               "fields":{
                  "currency_id":{
                     "fields":{}
                  },
                  "payment_date":{},
                  "payment_method_id":{
                     "fields":{
                        "display_name":{}
                     }
                  },
                  "amount":{},
                  "payment_method_payment_mode":{},
                  "card_no":{},
                  "card_brand":{},
                  "cardholder_name":{}
               },
               "limit":40,
               "order":""
            },
            "amount_difference":{},
            "session_move_id":{
               "fields":{
                  "display_name":{}
               }
            },
            "pos_reference":{},
            "tracking_number":{},
            "country_code":{},
            "pricelist_id":{
               "fields":{
                  "display_name":{}
               }
            },
            "floating_order_name":{},
            "email":{},
            "mobile":{},
            "general_note":{},
            "available_payment_method_ids":{},
            "nb_print":{},
            "display_name":{}
         }
    return {
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
    }


def get_order_context(specific_order=False, type="pos"):
    context = {
        "lang": "en_IN",
        "tz": "Asia/Kolkata",
        "uid": 2,
        "allowed_company_ids": [
            1
        ],
        "bin_size": True,
    }
    if type == "sale":
        context.update({"current_company_id": 1})
    elif specific_order:
        context.update({"params":{
               "actionStack":[
                  {
                     "displayName":"Orders",
                     "action":"pos-orders",
                     "view_type":"list"
                  }
               ],
               "action":"pos-orders",
               "globalState":{
                  "useSampleModel":False,
                  "searchModel":"{\"nextGroupId\":14,\"nextGroupNumber\":15,\"nextId\":22,\"query\":[],\"searchItems\":{\"1\":{\"type\":\"field\",\"fieldName\":\"name\",\"fieldType\":\"char\",\"description\":\"Order Ref\",\"groupId\":1,\"id\":1},\"2\":{\"type\":\"field\",\"fieldName\":\"pos_reference\",\"fieldType\":\"char\",\"description\":\"Receipt Number\",\"groupId\":2,\"id\":2},\"3\":{\"type\":\"field\",\"fieldName\":\"date_order\",\"fieldType\":\"datetime\",\"description\":\"Date\",\"groupId\":3,\"id\":3},\"4\":{\"type\":\"field\",\"fieldName\":\"tracking_number\",\"fieldType\":\"char\",\"description\":\"Order Number\",\"groupId\":4,\"id\":4},\"5\":{\"type\":\"field\",\"fieldName\":\"cashier\",\"fieldType\":\"char\",\"description\":\"Cashier name\",\"groupId\":5,\"id\":5},\"6\":{\"type\":\"field\",\"fieldName\":\"partner_id\",\"fieldType\":\"many2one\",\"description\":\"Customer\",\"groupId\":6,\"id\":6},\"7\":{\"type\":\"field\",\"fieldName\":\"session_id\",\"fieldType\":\"many2one\",\"description\":\"Session\",\"groupId\":7,\"id\":7},\"8\":{\"type\":\"field\",\"fieldName\":\"config_id\",\"fieldType\":\"many2one\",\"description\":\"Point of Sale\",\"groupId\":8,\"id\":8},\"9\":{\"type\":\"field\",\"filterDomain\":\"[('lines.product_id', 'ilike', self)]\",\"fieldName\":\"lines\",\"fieldType\":\"one2many\",\"description\":\"Product\",\"groupId\":9,\"id\":9},\"10\":{\"type\":\"filter\",\"domain\":\"[('state', '=', 'invoiced')]\",\"groupNumber\":10,\"name\":\"invoiced\",\"description\":\"Invoiced\",\"groupId\":10,\"id\":10},\"11\":{\"type\":\"filter\",\"domain\":\"[('state', '=', 'done')]\",\"groupNumber\":10,\"name\":\"posted\",\"description\":\"Posted\",\"groupId\":10,\"id\":11},\"12\":{\"type\":\"filter\",\"domain\":\"[('state', '=', 'cancel')]\",\"groupNumber\":10,\"name\":\"cancelled\",\"description\":\"Cancelled\",\"groupId\":10,\"id\":12},\"13\":{\"type\":\"dateFilter\",\"fieldName\":\"date_order\",\"fieldType\":\"datetime\",\"defaultGeneratorIds\":[\"month\"],\"optionsParams\":{\"startYear\":-2,\"endYear\":0,\"startMonth\":-2,\"endMonth\":0,\"customOptions\":[]},\"domain\":\"[]\",\"groupNumber\":12,\"name\":\"order_date\",\"description\":\"Order Date\",\"groupId\":11,\"id\":13},\"14\":{\"type\":\"groupBy\",\"fieldName\":\"session_id\",\"fieldType\":\"many2one\",\"groupNumber\":14,\"name\":\"session\",\"description\":\"Session\",\"groupId\":12,\"id\":14},\"15\":{\"type\":\"groupBy\",\"fieldName\":\"cashier\",\"fieldType\":\"char\",\"groupNumber\":14,\"name\":\"by_cashier\",\"description\":\"Cashier\",\"groupId\":12,\"id\":15},\"16\":{\"type\":\"groupBy\",\"fieldName\":\"config_id\",\"fieldType\":\"many2one\",\"groupNumber\":14,\"name\":\"config_id\",\"description\":\"Point of Sale\",\"groupId\":12,\"id\":16},\"17\":{\"type\":\"groupBy\",\"fieldName\":\"partner_id\",\"fieldType\":\"many2one\",\"groupNumber\":14,\"name\":\"customer\",\"description\":\"Customer\",\"groupId\":12,\"id\":17},\"18\":{\"type\":\"groupBy\",\"fieldName\":\"state\",\"fieldType\":\"selection\",\"groupNumber\":14,\"name\":\"status\",\"description\":\"Status\",\"groupId\":12,\"id\":18},\"19\":{\"type\":\"dateGroupBy\",\"fieldName\":\"date_order\",\"fieldType\":\"datetime\",\"defaultIntervalId\":\"month\",\"groupNumber\":14,\"name\":\"order_month\",\"description\":\"Order Date\",\"groupId\":12,\"id\":19},\"20\":{\"type\":\"comparison\",\"comparisonOptionId\":\"previous_period\",\"description\":\"Order Date: Previous Period\",\"dateFilterId\":13,\"groupId\":13,\"id\":20},\"21\":{\"type\":\"comparison\",\"comparisonOptionId\":\"previous_year\",\"description\":\"Order Date: Previous Year\",\"dateFilterId\":13,\"groupId\":13,\"id\":21}},\"searchPanelInfo\":{\"className\":\"\",\"fold\":False,\"viewTypes\":[\"kanban\",\"list\"],\"loaded\":False,\"shouldReload\":False},\"sections\":[]}"
               }
            }})
    else: context.update(
        {"params": {
            "action": "pos-orders",
            "actionStack": [{"action": "pos-orders"}]
        },
        "current_company_id": 1
    })
    return context

def get_customer_context(add_new=False):
    if add_new:
        return {
            "lang":"en_IN",
            "tz":"Asia/Kolkata",
            "uid":2,
            "allowed_company_ids":[
               1
            ],
            "params":{
               "actionStack":[
                  {
                     "displayName":"Customers",
                     "action":"customers",
                     "view_type":"kanban"
                  }
               ],
               "action":"customers",
               "globalState":{
                  "useSampleModel":False,
                  "searchModel":"{\"nextGroupId\":14,\"nextGroupNumber\":21,\"nextId\":22,\"query\":[],\"searchItems\":{\"1\":{\"type\":\"field\",\"filterDomain\":\"['|', '|', '|', '|', ('complete_name', 'ilike', self), ('ref', 'ilike', self), ('email', 'ilike', self), ('vat', 'ilike', self), ('company_registry', 'ilike', self)]\",\"fieldName\":\"name\",\"fieldType\":\"char\",\"description\":\"Name\",\"groupId\":1,\"id\":1},\"2\":{\"type\":\"field\",\"fieldName\":\"contact_address_complete\",\"fieldType\":\"char\",\"description\":\"Address\",\"groupId\":2,\"id\":2},\"3\":{\"type\":\"field\",\"domain\":\"[('is_company', '=', True)]\",\"operator\":\"child_of\",\"fieldName\":\"parent_id\",\"fieldType\":\"many2one\",\"description\":\"Related Company\",\"groupId\":3,\"id\":3},\"4\":{\"type\":\"field\",\"filterDomain\":\"[('email', 'ilike', self)]\",\"fieldName\":\"email\",\"fieldType\":\"char\",\"description\":\"Email\",\"groupId\":4,\"id\":4},\"5\":{\"type\":\"field\",\"fieldName\":\"phone_mobile_search\",\"fieldType\":\"char\",\"description\":\"Phone Number\",\"groupId\":5,\"id\":5},\"6\":{\"type\":\"field\",\"operator\":\"child_of\",\"fieldName\":\"category_id\",\"fieldType\":\"many2many\",\"description\":\"Tag\",\"groupId\":6,\"id\":6},\"7\":{\"type\":\"field\",\"fieldName\":\"user_id\",\"fieldType\":\"many2one\",\"description\":\"Salesperson\",\"groupId\":7,\"id\":7},\"8\":{\"type\":\"filter\",\"domain\":\"[('is_company', '=', False)]\",\"groupNumber\":9,\"name\":\"type_person\",\"description\":\"Individuals\",\"groupId\":8,\"id\":8},\"9\":{\"type\":\"filter\",\"domain\":\"[('is_company', '=', True)]\",\"groupNumber\":9,\"name\":\"type_company\",\"description\":\"Companies\",\"groupId\":8,\"id\":9},\"10\":{\"type\":\"field\",\"invisible\":\"1\",\"fieldName\":\"fiscal_country_codes\",\"fieldType\":\"char\",\"description\":\"Fiscal Country Codes\",\"groupId\":9,\"id\":10},\"11\":{\"type\":\"filter\",\"domain\":\"[('customer_rank','>', 0)]\",\"groupNumber\":12,\"name\":\"customer\",\"isDefault\":True,\"defaultRank\":-5,\"description\":\"Customer Invoices\",\"groupId\":10,\"id\":11},\"12\":{\"type\":\"filter\",\"domain\":\"[('supplier_rank','>', 0)]\",\"groupNumber\":12,\"name\":\"supplier\",\"description\":\"Vendor Bills\",\"groupId\":10,\"id\":12},\"13\":{\"type\":\"filter\",\"domain\":\"[('followup_status', 'in', ('in_need_of_action', 'with_overdue_invoices'))]\",\"groupNumber\":14,\"name\":\"filter_with_overdue_invoices\",\"description\":\"Overdue Invoices\",\"groupId\":11,\"id\":13},\"14\":{\"type\":\"filter\",\"domain\":\"[('followup_status', '=', 'in_need_of_action')]\",\"groupNumber\":14,\"name\":\"filter_in_need_of_action\",\"description\":\"Requires Follow-up\",\"groupId\":11,\"id\":14},\"15\":{\"type\":\"filter\",\"domain\":\"[('active', '=', False)]\",\"groupNumber\":16,\"name\":\"inactive\",\"description\":\"Archived\",\"groupId\":12,\"id\":15},\"16\":{\"type\":\"filter\",\"domain\":\"[('my_activity_date_deadline', '<', context_today().strftime('%Y-%m-%d'))]\",\"invisible\":\"1\",\"groupNumber\":16,\"name\":\"activities_overdue\",\"description\":\"Late Activities\",\"groupId\":12,\"id\":16},\"17\":{\"type\":\"filter\",\"domain\":\"[('my_activity_date_deadline', '=', context_today().strftime('%Y-%m-%d'))]\",\"invisible\":\"1\",\"groupNumber\":16,\"name\":\"activities_today\",\"description\":\"Today Activities\",\"groupId\":12,\"id\":17},\"18\":{\"type\":\"filter\",\"domain\":\"[('my_activity_date_deadline', '>', context_today().strftime('%Y-%m-%d'))]\",\"invisible\":\"1\",\"groupNumber\":16,\"name\":\"activities_upcoming_all\",\"description\":\"Future Activities\",\"groupId\":12,\"id\":18},\"19\":{\"type\":\"groupBy\",\"fieldName\":\"user_id\",\"fieldType\":\"many2one\",\"groupNumber\":20,\"name\":\"salesperson\",\"description\":\"Salesperson\",\"groupId\":13,\"id\":19},\"20\":{\"type\":\"groupBy\",\"fieldName\":\"parent_id\",\"fieldType\":\"many2one\",\"groupNumber\":20,\"name\":\"group_company\",\"description\":\"Company\",\"groupId\":13,\"id\":20},\"21\":{\"type\":\"groupBy\",\"fieldName\":\"country_id\",\"fieldType\":\"many2one\",\"groupNumber\":20,\"name\":\"group_country\",\"description\":\"Country\",\"groupId\":13,\"id\":21}},\"searchPanelInfo\":{\"className\":\"\",\"fold\":False,\"viewTypes\":[\"kanban\",\"list\"],\"loaded\":False,\"shouldReload\":True},\"sections\":[]}"
               }
            },
            "res_partner_search_mode":"customer",
            "default_is_company":True,
            "default_customer_rank":1
         }
    return {
                    "lang": "en_IN",
                    "tz": "Asia/Calcutta",
                    "uid": 2,
                    "allowed_company_ids": [1],
                    "bin_size": True,
                    "params": {
                        "view_type": "list",
                        "action": "customers",
                        "actionStack": [{"action": "customers"}]
                    },
                    "res_partner_search_mode": "customer",
                    "default_is_company": True,
                    "default_customer_rank": 1,
                    "current_company_id": 1
                }

def get_customer_specification(add_new=False):
    if add_new:
        return {
            "same_vat_partner_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "show_address":False,
                  "show_vat":False
               }
            },
            "vat_label":{

            },
            "partner_gid":{

            },
            "additional_info":{

            },
            "same_company_registry_partner_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "show_address":False,
                  "show_vat":False
               }
            },
            "company_registry_label":{

            },
            "l10n_in_gst_state_warning":{

            },
            "pos_order_count":{

            },
            "currency_id":{
               "fields":{

               }
            },
            "total_invoiced":{

            },
            "supplier_invoice_count":{

            },
            "total_due":{

            },
            "payment_token_count":{

            },
            "image_1920":{

            },
            "write_date":{

            },
            "company_type":{

            },
            "name":{

            },
            "parent_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "default_is_company":True,
                  "show_vat":True
               }
            },
            "company_name":{

            },
            "type":{

            },
            "street":{

            },
            "street2":{

            },
            "city":{

            },
            "zip":{

            },
            "state_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "country_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "l10n_in_gst_treatment":{

            },
            "partner_vat_placeholder":{

            },
            "perform_vies_validation":{

            },
            "vat":{

            },
            "vies_valid":{

            },
            "l10n_in_gstin_verified_date":{

            },
            "l10n_in_pan":{

            },
            "function":{

            },
            "phone_blacklisted":{

            },
            "phone":{

            },
            "phone_sanitized":{

            },
            "is_blacklisted":{

            },
            "email":{

            },
            "website":{

            },
            "lang":{

            },
            "category_id":{
               "fields":{
                  "display_name":{

                  },
                  "color":{

                  }
               }
            },
            "child_ids":{
               "fields":{
                  "color":{

                  },
                  "type":{

                  },
                  "is_company":{

                  },
                  "avatar_128":{

                  },
                  "write_date":{

                  },
                  "name":{

                  },
                  "function":{

                  },
                  "email":{

                  },
                  "zip":{

                  },
                  "city":{

                  },
                  "state_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "country_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "phone":{

                  },
                  "street":{

                  },
                  "street2":{

                  },
                  "company_id":{
                     "fields":{

                     }
                  },
                  "fiscal_country_codes":{

                  },
                  "comment":{

                  },
                  "lang":{

                  }
               },
               "context":{
                  "hide_country_from_state":1,
                  "default_type":"other"
               },
               "limit":40
            },
            "user_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_payment_term_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_inbound_payment_method_line_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_product_pricelist":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_supplier_payment_term_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_outbound_payment_method_line_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "barcode":{

            },
            "property_account_position_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "company_registry_placeholder":{

            },
            "partner_company_registry_placeholder":{

            },
            "company_registry":{

            },
            "ref":{

            },
            "company_id":{
               "fields":{

               }
            },
            "industry_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_stock_customer":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "property_stock_supplier":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "duplicated_bank_account_partners_count":{

            },
            "show_credit_limit":{

            },
            "followup_line_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "followup_status":{

            },
            "followup_reminder_type":{

            },
            "followup_next_action_date":{

            },
            "followup_responsible_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "invoice_sending_method":{

            },
            "invoice_edi_format":{

            },
            "invoice_template_pdf_report_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "peppol_eas":{

            },
            "peppol_endpoint":{

            },
            "credit":{

            },
            "days_sales_outstanding":{

            },
            "use_partner_credit_limit":{

            },
            "credit_limit":{

            },
            "comment":{

            },
            "partner_longitude":{

            },
            "partner_latitude":{

            },
            "display_pan_warning":{

            },
            "country_code":{

            },
            "has_moves":{

            },
            "active":{

            },
            "is_company":{

            },
            "user_ids":{

            },
            "l10n_in_is_gst_registered_enabled":{

            },
            "fiscal_country_codes":{

            },
            "l10n_in_gstin_status_feature_enabled":{

            },
            "l10n_in_gstin_verified_status":{

            },
            "active_lang_count":{

            },
            "display_invoice_edi_format":{

            },
            "available_invoice_template_pdf_report_ids":{

            },
            "display_invoice_template_pdf_report_id":{

            },
            "display_name":{

            }
         }
    return {
                    "complete_name": {},
                    "phone": {},
                    "mobile": {},
                    "email": {},
                    "user_id": {"fields": {"display_name": {}}},
                    "activity_ids": {"fields": {}},
                    "activity_exception_decoration": {},
                    "activity_exception_icon": {},
                    "activity_state": {},
                    "activity_summary": {},
                    "activity_type_icon": {},
                    "activity_type_id": {"fields": {"display_name": {}}},
                    "street": {},
                    "city": {},
                    "state_id": {"fields": {"display_name": {}}},
                    "country_id": {"fields": {"display_name": {}}},
                    "vat": {},
                    "invoice_edi_format": {},
                    "category_id": {"fields": {"display_name": {}, "color": {}}},
                    "followup_responsible_id": {"fields": {"display_name": {}}},
                    "followup_reminder_type": {},
                    "followup_status": {},
                    "followup_next_action_date": {},
                    "followup_line_id": {"fields": {"display_name": {}}},
                    "total_due": {},
                    "total_overdue": {}
                }

def place_order_context(validate_analytics=False):
    out =  {
            "lang":"en_IN",
            "tz":"Asia/Kolkata",
            "uid":2,
            "allowed_company_ids":[
               1
            ]
         }
    if validate_analytics:
        out.update({"validate_analytic": True})
    return out

def place_order_specification():
    return {
            "locked":{

            },
            "authorized_transaction_ids":{

            },
            "state":{

            },
            "partner_credit_warning":{

            },
            "duplicated_order_ids":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "delivery_count":{

            },
            "pos_order_count":{

            },
            "expense_count":{

            },
            "invoice_count":{

            },
            "purchase_order_count":{

            },
            "mrp_production_count":{

            },
            "name":{

            },
            "partner_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "display_website":True,
                  "res_partner_search_mode":"customer",
                  "show_address":1,
                  "show_vat":True
               }
            },
            "delivery_set":{

            },
            "is_all_service":{

            },
            "recompute_delivery_price":{

            },
            "l10n_in_gst_treatment":{

            },
            "partner_invoice_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "default_type":"invoice",
                  "show_address":False,
                  "show_vat":False
               }
            },
            "partner_shipping_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "default_type":"delivery",
                  "show_address":False,
                  "show_vat":False
               }
            },
            "validity_date":{

            },
            "date_order":{

            },
            "has_active_pricelist":{

            },
            "show_update_pricelist":{

            },
            "country_code":{

            },
            "company_id":{
               "fields":{

               }
            },
            "currency_id":{
               "fields":{

               }
            },
            "pricelist_id":{
               "fields":{

               }
            },
            "tax_country_id":{
               "fields":{

               }
            },
            "tax_calculation_rounding_method":{

            },
            "payment_term_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "order_line":{
               "fields":{
                  "sequence":{

                  },
                  "display_type":{

                  },
                  "product_uom_category_id":{
                     "fields":{

                     }
                  },
                  "product_type":{

                  },
                  "product_updatable":{

                  },
                  "is_downpayment":{

                  },
                  "product_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "product_template_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "product_template_attribute_value_ids":{

                  },
                  "product_custom_attribute_value_ids":{

                  },
                  "product_no_variant_attribute_value_ids":{

                  },
                  "is_configurable_product":{

                  },
                  "linked_line_id":{
                     "fields":{

                     }
                  },
                  "virtual_id":{

                  },
                  "linked_virtual_id":{

                  },
                  "selected_combo_items":{

                  },
                  "combo_item_id":{
                     "fields":{

                     }
                  },
                  "name":{

                  },
                  "is_reward_line":{

                  },
                  "product_uom_qty":{

                  },
                  "qty_delivered":{

                  },
                  "virtual_available_at_date":{

                  },
                  "qty_available_today":{

                  },
                  "free_qty_today":{

                  },
                  "scheduled_date":{

                  },
                  "forecast_expected_date":{

                  },
                  "warehouse_id":{
                     "fields":{

                     }
                  },
                  "move_ids":{

                  },
                  "qty_to_deliver":{

                  },
                  "is_mto":{

                  },
                  "display_qty_widget":{

                  },
                  "qty_delivered_method":{

                  },
                  "qty_invoiced":{

                  },
                  "qty_to_invoice":{

                  },
                  "product_uom_readonly":{

                  },
                  "product_uom":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "customer_lead":{

                  },
                  "product_packaging_qty":{

                  },
                  "product_packaging_id":{
                     "fields":{
                        "display_name":{

                        }
                     },
                     "context":{
                        "list_view_ref":"product.product_packaging_tree_view",
                        "form_view_ref":"product.product_packaging_form_view"
                     }
                  },
                  "recompute_delivery_price":{

                  },
                  "is_delivery":{

                  },
                  "price_unit":{

                  },
                  "price_subtotal":{

                  },
                  "purchase_price":{

                  },
                  "margin":{

                  },
                  "margin_percent":{

                  },
                  "technical_price_unit":{

                  },
                  "tax_id":{
                     "fields":{
                        "display_name":{

                        }
                     },
                     "context":{
                        "active_test":True
                     }
                  },
                  "discount":{

                  },
                  "price_total":{

                  },
                  "tax_calculation_rounding_method":{

                  },
                  "state":{

                  },
                  "invoice_status":{

                  },
                  "currency_id":{
                     "fields":{

                     }
                  },
                  "price_tax":{

                  },
                  "company_id":{
                     "fields":{

                     }
                  },
                  "product_document_ids":{

                  },
                  "is_product_archived":{

                  },
                  "order_id":{
                     "fields":{

                     }
                  },
                  "available_product_document_ids":{

                  }
               },
               "limit":200,
               "order":"sequence ASC, id ASC"
            },
            "note":{

            },
            "tax_totals":{

            },
            "margin":{

            },
            "amount_untaxed":{

            },
            "margin_percent":{

            },
            "loyalty_data":{

            },
            "sale_order_option_ids":{
               "fields":{
                  "sequence":{

                  },
                  "product_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "name":{

                  },
                  "quantity":{

                  },
                  "uom_id":{
                     "fields":{
                        "display_name":{

                        }
                     }
                  },
                  "product_uom_category_id":{
                     "fields":{

                     }
                  },
                  "price_unit":{

                  },
                  "discount":{

                  },
                  "is_present":{

                  }
               },
               "limit":40,
               "order":"sequence ASC, id ASC"
            },
            "quotation_document_ids":{

            },
            "customizable_pdf_form_fields":{

            },
            "user_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "team_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "kanban_view_ref":"sales_team.crm_team_view_kanban"
               }
            },
            "is_abandoned_cart":{

            },
            "cart_recovery_email_sent":{

            },
            "require_signature":{

            },
            "require_payment":{

            },
            "prepayment_percent":{

            },
            "reference":{

            },
            "client_order_ref":{

            },
            "tag_ids":{
               "fields":{
                  "display_name":{

                  },
                  "color":{

                  }
               }
            },
            "show_update_fpos":{

            },
            "fiscal_position_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "invoice_status":{

            },
            "warehouse_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "incoterm":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "incoterm_location":{

            },
            "picking_policy":{

            },
            "shipping_weight":{

            },
            "commitment_date":{

            },
            "expected_date":{

            },
            "show_json_popover":{

            },
            "json_popover":{

            },
            "effective_date":{

            },
            "delivery_status":{

            },
            "origin":{

            },
            "opportunity_id":{
               "fields":{
                  "display_name":{

                  }
               },
               "context":{
                  "default_type":"opportunity"
               }
            },
            "campaign_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "medium_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "source_id":{
               "fields":{
                  "display_name":{

                  }
               }
            },
            "has_archived_products":{

            },
            "company_price_include":{

            },
            "is_pdf_quote_builder_available":{

            },
            "display_name":{

            }
         }