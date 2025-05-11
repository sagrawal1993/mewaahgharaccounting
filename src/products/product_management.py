from src.constants import main_db_cred, accounting_db_cred, pos_db_cred, product_data_file
from src.products.get_product import get_product_list
from src.datamodel import Product, ProductData

main_db_product_list = get_product_list(**main_db_cred.model_dump())
accounting_db_product_list = get_product_list(**accounting_db_cred.model_dump())
pos_db_product_list = get_product_list(**pos_db_cred.model_dump())

main_db_product_map = {product.id: product for product in main_db_product_list}
accounting_db_product_map = {product.id: product for product in accounting_db_product_list}
pos_db_product_map = {product.id: product for product in pos_db_product_list}
#
# print(main_db_product_map)
# print(accounting_db_product_map)
# print(pos_db_product_map)

import pandas as pd
product_df = pd.read_csv(product_data_file)
print(product_df)

# print(main_db_product_list[0])
# print(accounting_db_product_list[0])
# print(pos_db_product_list[0])

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


def get_different_product(comparison_type: str):
    # first = None
    # second = None
    # if comparison_type == "main_accounting":
    #     first = main_db_product_list
    #     second = accounting_db_product_ist
    # elif comparison_type == "main_pos":
    #     first = main_db_product_list
    #     second = pos_db_product_list
    # elif comparison_type == "pos_accounting":
    #     first = pos_db_product_list
    #     second = accounting_db_product_ist

    changed_in_main_accounting_db = []
    changed_in_main_pos_db = []
    for i, row in product_df.iterrows():
        print(i, row)
        accounting_pid = row['accounting_db_id']
        pos_1_db_id = row['mewaahghar_store_1_db_id']
        main_db_id = row['main_db_id']
        account_product = accounting_db_product_map[accounting_pid]
        pos_1_product = pos_db_product_map[pos_1_db_id]
        main_product = main_db_product_map[main_db_id]

        #compare_product(account_product, pos_1_product)
        accounting_db_changed = compare_product(main_product, account_product)
        pos_1_db_changed = compare_product(pos_1_product, main_product)
        if accounting_db_changed:
            changed_in_main_accounting_db.append((main_product, account_product))
        if pos_1_db_changed:
            changed_in_main_pos_db.append((main_product, pos_1_product))

    # for p1 in first:
    #     for p2 in second:
    #         compare_product(p1, p2)

    return changed_in_main_pos_db, changed_in_main_accounting_db

def get_newly_added_product(db_type='main_db'):
    if db_type=="main_db":
        db_product_map = main_db_product_map
        column_name = 'main_db_id'
    elif db_type == "accounting_db":
        db_product_map = accounting_db_product_map
        column_name = 'accounting_db_id'
    elif db_type == "mewaahghar_store_1_db":
        db_product_map = pos_db_product_map
        column_name = 'mewaahghar_store_1_db_id'

    newely_added_items = []
    for id, product in db_product_map.items():
        if id not in set(product_df[column_name].tolist()):
            newely_added_items.append(product)
    return newely_added_items

def sync_product_of_main_db_with_files():
    product_df = pd.read_csv(product_data_file)
    existing_product_map = { row['main_db_id']: ProductData(**row.dropna().to_dict()) for _, row in product_df.iterrows()}
    for main_db_product_id, main_db_product in main_db_product_map.items():
        if main_db_product_id not in existing_product_map:
            existing_product_map[main_db_product_id] = ProductData(**{
                "name": main_db_product.name,
                "main_db_weight": main_db_product.weight,
                "main_db_volume": main_db_product.volume,
                "main_db_id": main_db_product.id,
                "main_db_qty_available": main_db_product.qty_available,
                "main_db_list_price": main_db_product.list_price,
                "main_db_standard_price": main_db_product.standard_price,
                })
        else:
            existing_product_data = existing_product_map[main_db_product_id]
            existing_product_data.name = main_db_product.name
            existing_product_data.main_db_weight = main_db_product.weight
            existing_product_data.main_db_volume = main_db_product.volume
            existing_product_data.main_db_id = main_db_product.id
            existing_product_data.main_db_qty_available = main_db_product.qty_available
            existing_product_data.main_db_list_price = main_db_product.list_price
            existing_product_data.main_db_standard_price = main_db_product.standard_price
    product_df = pd.DataFrame([ product_data.model_dump() for product_data in existing_product_map.values()])
    product_df.to_csv(product_data_file)
    return product_df

def sync_product_to_db(product: Product, db_type: str = "main_db"):
    db_product_map = main_db_product_map
    column_name = 'main_db_id'
    db_cred = main_db_cred
    if db_type == "accounting_db":
        db_product_map = accounting_db_product_map
        column_name = 'accounting_db_id'
        db_cred = accounting_db_cred
    elif db_type == "mewaahghar_store_1_db":
        db_product_map = pos_db_product_map
        column_name = 'mewaahghar_store_1_db_id'
        db_cred = pos_db_cred
    product_df = pd.read_csv(product_data_file)

    from src.products.add_new_product import add_product
    if id not in set(product_df[column_name].tolist()):
        added_id = add_product(product, db_cred)

    return newely_added_items

def sync_product_to_pos_store_1_db(product: Product):
    return

if __name__ == '__main__':
    # newly_added_product = get_newly_added_product()
    # print(newly_added_product)
    print(sync_product_of_main_db_with_files())