from src.constants import main_db_cred, accounting_db_cred, pos_db_cred, product_mapping_file, mewaahghar_store_1_db_product_file, accounting_db_product_file, main_db_product_file
from src.products.get_product import get_product_list
from src.datamodel import Product, ProductData
import pandas as pd
from src.products.add_new_product import add_product
from src.products.update_product import update_product

product_mapping_df = pd.DataFrame([])
main_product_df = pd.DataFrame([])
accounting_product_df = pd.DataFrame([])
mewaahghar_store_1_product_df = pd.DataFrame([])

main_db_product_map = {}
accounting_db_product_map = {}
pos_db_product_map = {}
existing_product_mapping = {}

def sync_data():
    global product_mapping_df
    global main_db_product_map
    global main_product_df
    global accounting_product_df
    global mewaahghar_store_1_product_df
    global accounting_db_product_map
    global pos_db_product_map
    global existing_product_mapping
    product_mapping_df = pd.read_csv(product_mapping_file)
    main_product_df = pd.read_csv(main_db_product_file)
    accounting_product_df = pd.read_csv(accounting_db_product_file)
    mewaahghar_store_1_product_df = pd.read_csv(mewaahghar_store_1_db_product_file)

    existing_product_mapping = {row['main_db_id']: ProductData(**row.dropna().to_dict()) for _, row in product_mapping_df.iterrows()}

    main_db_product_list = get_product_list(main_db_cred)
    accounting_db_product_list = get_product_list(accounting_db_cred)
    pos_db_product_list = get_product_list(pos_db_cred)

    main_db_product_map = {product.id: product for product in main_db_product_list}
    accounting_db_product_map = {product.id: product for product in accounting_db_product_list}
    pos_db_product_map = {product.id: product for product in pos_db_product_list}


def compare_product(product_1: Product, product_2: Product):
    if product_1.name.strip().lower() != product_2.name.strip().lower():
        return False
    elif product_1.volume != product_2.volume:
        return False
    elif product_1.weight != product_2.weight:
        return False
    elif product_1.list_price != product_2.list_price:
        return False
    elif product_1.qty_available != product_2.qty_available:
        return False
    elif product_1.standard_price != product_2.standard_price:
        return False
    return True


def check_if_main_product_updated(product_1: Product, product_2: Product):
    if product_1.name.strip().lower() != product_2.name.strip().lower():
        return True
    elif product_1.volume != product_2.volume:
        return True
    elif product_1.weight != product_2.weight:
        return True
    elif product_1.list_price != product_2.list_price:
        return True
    # elif db_product.qty_available != existing_product_data.qty_available:
    #     return False
    # Leaving qty_available, as qty would changed during day and might always mismatch.
    # We can check this if orders are already begin executed, we can check it separately.
    elif product_1.standard_price != product_2.standard_price:
        return True
    return False


def get_product_difference_in_main_db():

    existing_product_map = { row['id']: Product(**row.dropna().to_dict()) for _, row in main_product_df.iterrows()}
    global existing_product_mapping
    global main_db_product_map

    newely_added_items = []
    updated_items = []
    for product_id, product in main_db_product_map.items():
        try:
            if product_id not in existing_product_mapping:
                newely_added_items.append(product)
            elif check_if_main_product_updated(product, existing_product_map[product_id]):
                updated_items.append(product)
            else:
                updated_items.append(product)
        except Exception as e:
            print(product, existing_product_map[product_id])
            print(e)
    return newely_added_items, updated_items


def get_product_current_state(main_db_id: str):
    global existing_product_mapping
    global accounting_product_df
    global main_product_df
    global mewaahghar_store_1_product_df
    product_data = existing_product_mapping[main_db_id]
    tmp_df = accounting_product_df[accounting_product_df['id']==product_data.accounting_db_id]
    accounting_product = Product(**tmp_df.to_dict('records')[0]) if product_data.accounting_db_enabled and len(tmp_df) else None
    tmp_df = mewaahghar_store_1_product_df[mewaahghar_store_1_product_df['id'] == product_data.mewaahghar_store_1_db_id]
    mewaahghar_product = Product(**tmp_df.to_dict('records')[0]) if product_data.mewaahghar_store_1_db_enabled and len(tmp_df) else None
    main_product = Product(**main_product_df[main_product_df['id']==main_db_id].to_dict('records')[0])
    return product_data, main_product, accounting_product, mewaahghar_product


def get_product_descripency(product_df, db_product_map):
    current_acc_product_map ={ row['id']: Product(**row) for row in product_df.to_dict('records')}
    db_keys = set(db_product_map.keys())
    file_keys = set(db_product_map.keys())
    descripent_product = []
    data_mismatch = []
    if db_keys.difference(file_keys) or file_keys.difference(db_keys):
        descripent_product = descripent_product + list(db_keys.difference(file_keys)) + list(file_keys.difference(db_keys))
    for key in db_keys.intersection(file_keys):
        if check_if_main_product_updated(db_product_map[key], current_acc_product_map[key]):
            data_mismatch.append((db_product_map[key], current_acc_product_map[key]))
    return descripent_product, data_mismatch

# def get_not_synced_product_to_accounting_db():
#     not_synced_products = []
#     for _, row in product_df.iterrows():
#         product_data = ProductData(**row.dropna().to_dict())
#         if not product_data.accounting_db_synced and product_data.accounting_db_enabled:
#             not_synced_products.append(product_data)
#     return not_synced_products

# def get_not_synced_product_to_mewaahghar_pos_1_db():
#     not_synced_products = []
#     for _, row in product_df.iterrows():
#         product_data = ProductData(**row.dropna().to_dict())
#         if not product_data.mewaahghar_store_1_db_synced and product_data.mewaahghar_store_1_db_enabled:
#             not_synced_products.append(product_data)
#     return not_synced_products

# def get_updated_product(db_type='main_db'):
#     # This will give the list of product
#
#     db_product_map = main_db_product_map
#     column_name = 'main_db_id'
#     if db_type == "accounting_db":
#         db_product_map = accounting_db_product_map
#         column_name = 'accounting_db_id'
#     elif db_type == "mewaahghar_store_1_db":
#         db_product_map = pos_db_product_map
#         column_name = 'mewaahghar_store_1_db_id'
#
#     updated_items = []
#     for i, row in product_df.iterrows():
#         product_data = ProductData(**row.todict())
#         if product_data.model_dump()[column_name] in db_product_map:
#             pass
#         else:
#             updated_items.append(product_data)
#     return updated_items

# def sync_product_of_main_db_with_files():
#     #product_df = pd.read_csv(product_data_file)
#     existing_product_map = { row['main_db_id']: ProductData(**row.dropna().to_dict()) for _, row in product_df.iterrows()}
#     for main_db_product_id, main_db_product in main_db_product_map.items():
#         if main_db_product_id not in existing_product_map:
#             existing_product_map[main_db_product_id] = ProductData(**{
#                 "name": main_db_product.name,
#                 "main_db_weight": main_db_product.weight,
#                 "main_db_volume": main_db_product.volume,
#                 "main_db_id": main_db_product.id,
#                 "main_db_qty_available": main_db_product.qty_available,
#                 "main_db_list_price": main_db_product.list_price,
#                 "main_db_standard_price": main_db_product.standard_price,
#                 })
#         else:
#             existing_product_data = existing_product_map[main_db_product_id]
#             existing_product_data.name = main_db_product.name
#             existing_product_data.main_db_weight = main_db_product.weight
#             existing_product_data.main_db_volume = main_db_product.volume
#             existing_product_data.main_db_id = main_db_product.id
#             existing_product_data.main_db_qty_available = main_db_product.qty_available
#             existing_product_data.main_db_list_price = main_db_product.list_price
#             existing_product_data.main_db_standard_price = main_db_product.standard_price
#             existing_product_data.accounting_db_synced = False
#             existing_product_data.mewaahghar_store_1_db_synced = False
#     product_df = pd.DataFrame([ product_data.model_dump() for product_data in existing_product_map.values()])
#     product_df.to_csv(product_data_file)
#     return product_df

# def sync_product_to_accounting_db(main_db_product_id: int, product: Product):
#     product_df = pd.read_csv(product_data_file)
#     # Assuming that all the data would be present in the product_df, as we will sync first all of the product
#     # from main db and update to other dbs
#     product_data = ProductData(**product_df[product_df[f"main_db_id"]==main_db_product_id].iloc[0].to_dict())
#     product_data.accounting_db_enabled = product.enabled
#     if product.enabled:
#         if product_data.accounting_db_id is None:
#             updated_id = add_product(product, accounting_db_cred)
#         else:
#             updated_id = update_product(product=product, db_cred=accounting_db_cred)
#             assert product_data.accounting_db_id == updated_id
#         product_data.accounting_db_weight = product.weight
#         product_data.accounting_db_volume = product.volume
#         product_data.accounting_db_id = updated_id
#         product_data.accounting_db_qty_available = product.qty_available
#         product_data.accounting_db_list_price = product.list_price
#         product_data.accounting_db_standard_price = product.standard_price
#         product_df[product_df[f"main_db_id"]==main_db_product_id].iloc[0] = product_data.to_dict()
#     else:
#         product_df[product_df[f"main_db_id"] == main_db_product_id].iloc[0] = product_data.to_dict()
#     product_df.to_csv(product_data_file)
#     return
#

# def sync_product_to_pos_1_db(main_db_product_id: int, product: Product):
#     product_df = pd.read_csv(product_data_file)
#     # Assuming that all the data would be present in the product_df, as we will sync first all of the product
#     # from main db and update to other dbs
#     product_data = ProductData(**product_df[product_df[f"main_db_id"]==main_db_product_id].iloc[0].to_dict())
#     product_data.mewaahghar_store_1_db_enabled = product.enabled
#
#     if product.enabled:
#         if product_data.mewaahghar_store_1_db_id is None:
#             updated_id = add_product(product, pos_db_cred)
#         else:
#             updated_id = update_product(product=product, db_cred=pos_db_cred)
#             assert product_data.mewaahghar_store_1_db_id == updated_id
#         product_data.mewaahghar_store_1_db_weight = product.weight
#         product_data.mewaahghar_store_1_db_volume = product.volume
#         product_data.mewaahghar_store_1_db_id = updated_id
#         product_data.mewaahghar_store_1_db_qty_available = product.qty_available
#         product_data.mewaahghar_store_1_db_list_price = product.list_price
#         product_data.mewaahghar_store_1_db_standard_price = 0#product.standard_price
#         product_df[product_df[f"main_db_id"]==main_db_product_id].iloc[0] = product_data.to_dict()
#     else:
#         product_df[product_df[f"main_db_id"] == main_db_product_id].iloc[0] = product_data.to_dict()
#     product_df.to_csv(product_data_file)
#     return


# def syncing_updated_product(main_db_product: Product, account_db_product: Product, pos_1_db_product: Product, product_data: ProductData):
#     global accounting_product_df
#     global main_product_df
#     global mewaahghar_store_1_product_df
#     global product_mapping_df
#
#     # print(main_db_product)
#     # print(account_db_product)
#     # print(pos_1_db_product)
#
#     if product_data.accounting_db_enabled:
#         account_db_product.id = update_product(product=account_db_product, db_cred=accounting_db_cred)
#         product_data.accounting_db_synced = True
#     if product_data.mewaahghar_store_1_db_enabled:
#         pos_1_db_product.id = update_product(product=pos_1_db_product, db_cred=pos_db_cred)
#         product_data.mewaahghar_store_1_db_synced = True
#
#     product_mapping_df = pd.DataFrame([ rec if rec['main_db_id']!=product_data.main_db_id else product_data.model_dump() for rec in product_mapping_df.to_dict('records')])
#     product_mapping_df.to_csv(product_mapping_file, index=False)
#     main_product_df = pd.DataFrame([ rec if rec['id'] != main_db_product.id else main_db_product.model_dump() for rec in main_product_df.to_dict('records')])
#     main_product_df.to_csv(main_db_product_file, index=False)
#     if product_data.accounting_db_enabled:
#         accounting_product_df = pd.DataFrame([ rec if rec['id'] != account_db_product.id else account_db_product.model_dump() for rec in accounting_product_df.to_dict('records')])
#         accounting_product_df.to_csv(accounting_db_product_file, index=False)
#     if product_data.mewaahghar_store_1_db_enabled:
#         mewaahghar_store_1_product_df = pd.DataFrame([ rec if rec['id'] != pos_1_db_product.id else pos_1_db_product.model_dump() for rec in mewaahghar_store_1_product_df.to_dict('records')])
#         mewaahghar_store_1_product_df.to_csv(mewaahghar_store_1_db_product_file, index=False)
#     print("done with syncing updated product.")
#
#
# def syncing_new_product(main_db_product, account_db_product, pos_1_db_product, accounting_enabled, pos_1_enabled):
#     global accounting_product_df
#     global main_product_df
#     global mewaahghar_store_1_product_df
#     global product_mapping_df
#
#     # print(main_db_product)
#     # print(account_db_product)
#     # print(pos_1_db_product)
#
#     if accounting_enabled:
#         account_db_product.id = add_product(account_db_product, accounting_db_cred)
#     if pos_1_enabled:
#         pos_1_db_product.id = add_product(pos_1_db_product, pos_db_cred)
#
#     product_data = ProductData(main_db_id=main_db_product.id,
#                                accounting_db_id=account_db_product.id if accounting_enabled else -1,
#                                mewaahghar_store_1_db_id=pos_1_db_product.id if pos_1_enabled else -1,
#                                accounting_db_enabled=accounting_enabled,
#                                mewaahghar_store_1_db_enabled=pos_1_enabled,
#                                accounting_db_synced=True,
#                                mewaahghar_store_1_db_synced=True,
#                                )
#
#     product_mapping_df = pd.DataFrame(product_mapping_df.to_dict('records') + [product_data.model_dump()])
#     product_mapping_df.to_csv(product_mapping_file, index=False)
#     main_product_df = pd.DataFrame(main_product_df.to_dict('records')+[main_db_product.model_dump()])
#     main_product_df.to_csv(main_db_product_file, index=False)
#     if accounting_enabled:
#         accounting_product_df = pd.DataFrame(accounting_product_df.to_dict('records') + [account_db_product.model_dump()])
#         accounting_product_df.to_csv(accounting_db_product_file, index=False)
#     if pos_1_enabled:
#         mewaahghar_store_1_product_df = pd.DataFrame(mewaahghar_store_1_product_df.to_dict('records') + [pos_1_db_product.model_dump()])
#         mewaahghar_store_1_product_df.to_csv(mewaahghar_store_1_db_product_file, index=False)
#     print("done with syncing")

def syncing_product(main_db_product: Product, account_db_product: Product, pos_1_db_product: Product, product_data: ProductData):
    global accounting_product_df
    global main_product_df
    global mewaahghar_store_1_product_df
    global product_mapping_df

    if product_data.accounting_db_enabled:
        if product_data.accounting_db_id != -1:
            account_db_product.id = update_product(product=account_db_product, db_cred=accounting_db_cred)
            product_data.accounting_db_synced = True
            updated_data_points = [ rec if rec['id'] != account_db_product.id else account_db_product.model_dump() for rec in accounting_product_df.to_dict('records')]
        else:
            account_db_product.id = add_product(product=account_db_product, db_cred=accounting_db_cred)
            product_data.accounting_db_id = account_db_product.id
            product_data.accounting_db_synced = True
            updated_data_points = accounting_product_df.to_dict('records') + [account_db_product.model_dump()]
        accounting_product_df = pd.DataFrame(updated_data_points)
        accounting_product_df.to_csv(accounting_db_product_file, index=False)

    if product_data.mewaahghar_store_1_db_enabled:
        if product_data.mewaahghar_store_1_db_id != -1:
            pos_1_db_product.id = update_product(product=pos_1_db_product, db_cred=pos_db_cred)
            product_data.mewaahghar_store_1_db_synced = True
            updated_data_points = [ rec if rec['id'] != pos_1_db_product.id else pos_1_db_product.model_dump() for rec in mewaahghar_store_1_product_df.to_dict('records')]
        else:
            pos_1_db_product.id = add_product(product=pos_1_db_product, db_cred=pos_db_cred)
            product_data.mewaahghar_store_1_db_id = pos_1_db_product.id
            product_data.mewaahghar_store_1_db_synced = True
            updated_data_points = mewaahghar_store_1_product_df.to_dict('records') + [pos_1_db_product.model_dump()]
        mewaahghar_store_1_product_df = pd.DataFrame(updated_data_points)
        mewaahghar_store_1_product_df.to_csv(mewaahghar_store_1_db_product_file, index=False)

    if product_data.main_db_id != -1:
        updated_data_points = [ rec if rec['id'] != main_db_product.id else main_db_product.model_dump() for rec in main_product_df.to_dict('records')]
    else:
        updated_data_points = main_product_df.to_dict('records')+[main_db_product.model_dump()]

    main_product_df = pd.DataFrame(updated_data_points)
    main_product_df.to_csv(main_db_product_file, index=False)

    if product_data.main_db_id != -1:
        updated_data_points = [ rec if rec['main_db_id']!=product_data.main_db_id else product_data.model_dump() for rec in product_mapping_df.to_dict('records')]
    else:
        product_data.main_db_id = main_db_product.id
        updated_data_points = product_mapping_df.to_dict('records') + [product_data.model_dump()]
    product_mapping_df = pd.DataFrame(updated_data_points)
    product_mapping_df.to_csv(product_mapping_file, index=False)
    print("done with syncing updated product.")


# if __name__ == '__main__':
    # newly_added_product = get_newly_added_product()
    # print(newly_added_product)
    #print(sync_product_of_main_db_with_files())