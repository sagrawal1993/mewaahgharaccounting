import sys, os
from datamodel import ProductData

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
# Mocked data (you can later replace it with live API data)
product_info = {
    "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
    "db_url": "https://mewaahgharstore.odoo.com",
}

from src.products.product_management import sync_data, get_product_difference_in_main_db, \
    get_product_current_state, syncing_product

#get_not_synced_product_to_accounting_db, get_not_synced_product_to_mewaahghar_pos_1_db,sync_product_of_main_db_with_files, syncing_new_product, syncing_updated_product,
sync_data()
products = []
updated_products = []
product_data = []
# Sidebar
st.sidebar.title("Product Sync Panel")
st.sidebar.markdown("Use the buttons on the right to sync product data.")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Products:** {len(products)}")

#products, updated_products = get_product_difference_in_main_db()

# Compare Buttons
st.sidebar.markdown("### Newly Added Items")

if st.sidebar.button("🔍 New Product Added to Main DB"):

    products, _ = get_product_difference_in_main_db()
    st.success("New Items Added to Main DB triggered.")

if st.sidebar.button("🔍 Updated Product in Main DB"):
    # st.success("New Items Added to Accounting DB triggered..")
    _, updated_products = get_product_difference_in_main_db()

not_enabled_product_ids = []
if st.sidebar.button("Product not enabled"):
    # st.success("New Items Added to Accounting DB triggered..")
    from src.products.product_management import existing_product_mapping
    not_enabled_product_ids = [ key for key, prod_data in existing_product_mapping.items() if prod_data.accounting_db_enabled or prod_data.mewaahghar_store_1_db_enabled]



# if st.sidebar.button("🔍 Product Not Synced in Accounting DB"):
#     st.success("Product Sync to Accounting DB triggered..")
#     product_data = get_not_synced_product_to_accounting_db()
#
# if st.sidebar.button("🔍 Product Not Synced in MeWaah Ghar POS"):
#     st.success("Product Sync to MeWaah Ghar triggered..")
#     product_data = get_not_synced_product_to_mewaahghar_pos_1_db()

st.sidebar.markdown("---")

# Main title
st.title("Product List & Sync Dashboard")

# if st.button("🔄 Sync Product from Main DB", key="sync_main_db"):
#     sync_product_of_main_db_with_files()
#     sync_data()
#     st.success("All products from main DB synced successfully to intermediate DB")

# # Button to sync all products
# if st.button("🔄 Sync ALL Products to Accounting DB and POS_1_DB", key="sync_all_product"):
#     st.success("All products synced successfully to Accounting DB and POS_1_DB.")
#
# Newly Added Products.
for i, product in enumerate(products[:10]):
    with st.container():
        st.markdown(f"##### {product.name}")
        # Read-only main DB info
        #st.markdown("###### 🧾 Main DB Info (Read-Only)")
        main_cols = st.columns(5)
        main_cols[0].text_input("Main Weight", value=product.weight, disabled=True, key=f"main_wt_{i}")
        main_cols[1].text_input("Main Volume", value=product.volume, disabled=True, key=f"main_vol_{i}")
        main_cols[2].text_input("Qty Available", value=product.qty_available, disabled=True,
                                key=f"main_qty_{i}")
        main_cols[3].text_input("List Price", value=product.list_price, disabled=True, key=f"main_lp_{i}")
        main_cols[4].text_input("Standard Price", value=product.standard_price, disabled=True,
                                key=f"main_sp_{i}")

        product_data = ProductData()
        st.markdown("###### Accounting DB ")
        acc_product = product.model_copy()
        acc_product.name = st.text_input("Product Name", value = acc_product.name, key=f"acc_nm_{i}")
        acc_cols = st.columns(6)
        acc_product.weight = acc_cols[0].number_input("Main Weight", value=acc_product.weight,  key=f"acc_wt_{i}")
        acc_product.volume = acc_cols[1].number_input("Main Volume", value=acc_product.volume,  key=f"acc_vol_{i}")
        acc_product.qty_available = acc_cols[2].number_input("Qty Available", value=acc_product.qty_available, key=f"acc_qty_{i}")
        acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price, key=f"acc_lp_{i}")
        acc_product.standard_price = acc_cols[4].number_input("Standard Price", value=acc_product.standard_price, key=f"acc_sp_{i}")
        acc_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"acc_enabled_{i}")  # ← added here

        st.markdown("###### MeWaah Ghar Store 1 DB")
        pos_product = product.model_copy()
        pos_product.name = st.text_input("Product Name", value = pos_product.name, key=f"pos_nm_{i}")
        acc_cols = st.columns(6)
        pos_product.weight = acc_cols[0].number_input("Main Weight", value=pos_product.weight,  key=f"pos_wt_{i}")
        pos_product.volume = acc_cols[1].number_input("Main Volume", value=pos_product.volume,  key=f"pos_vol_{i}")
        pos_product.qty_available = acc_cols[2].number_input("Qty Available", value=pos_product.qty_available, key=f"pos_qty_{i}")
        pos_product.list_price = acc_cols[3].number_input("List Price", value=pos_product.list_price, key=f"pos_lp_{i}")
        pos_product.standard_price = acc_cols[4].number_input("Standard Price", value=pos_product.standard_price, key=f"pos_sp_{i}")
        pos_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"pos_enabled_{i}")  # ← added here

        # with acc_cols[5]:
        if st.button("Sync product", key=f"add_prod_sync_{i}"):
            print("syncing product")
            product_sync_data = {
                "main_db_product": product,
                "account_db_product": acc_product,
                "pos_1_db_product": pos_product,
                "product_data": product_data,
            }
            syncing_product(**product_sync_data)
            sync_data()
            st.success('Synced the product to POS db')

        st.markdown("---")


for i, product in enumerate(updated_products):
    with st.container():
        st.markdown(f"##### {product.name}")

        main_cols = st.columns(5)
        main_cols[0].text_input("Updated Weight", value=product.weight, disabled=True, key=f"main_wt_{i}")
        main_cols[1].text_input("Updated Volume", value=product.volume, disabled=True, key=f"main_vol_{i}")
        main_cols[2].text_input("Updated Qty Available", value=product.qty_available, disabled=True,
                                key=f"main_qty_{i}")
        main_cols[3].text_input("Updated List Price", value=product.list_price, disabled=True, key=f"main_lp_{i}")
        main_cols[4].text_input("Updated Standard Price", value=product.standard_price, disabled=True,
                                key=f"main_sp_{i}")

        product_data, current_main, acc_product, pos_product = get_product_current_state(product.id)

        main_cols[0].text_input("Old Weight", value=current_main.weight, disabled=True, key=f"c_main_wt_{i}")
        main_cols[1].text_input("Old Volume", value=current_main.volume, disabled=True, key=f"c_main_vol_{i}")
        main_cols[2].text_input("Old Qty Available", value=current_main.qty_available, disabled=True,
                                key=f"c_main_qty_{i}")
        main_cols[3].text_input("Old List Price", value=current_main.list_price, disabled=True, key=f"c_main_lp_{i}")
        main_cols[4].text_input("Old Standard Price", value=current_main.standard_price, disabled=True,
                                key=f"c_main_sp_{i}")


        if product_data.accounting_db_enabled:
            st.markdown("###### Accounting DB ")
            acc_product.name = st.text_input("Product Name", value = acc_product.name, key=f"acc_nm_{i}")
            acc_cols = st.columns(6)
            acc_product.weight = acc_cols[0].number_input("Main Weight", value=acc_product.weight,  key=f"acc_wt_{i}")
            acc_product.volume = acc_cols[1].number_input("Main Volume", value=acc_product.volume,  key=f"acc_vol_{i}")
            acc_product.qty_available = acc_cols[2].number_input("Qty Available", value=acc_product.qty_available, key=f"acc_qty_{i}")
            acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price, key=f"acc_lp_{i}")
            acc_product.standard_price = acc_cols[4].number_input("Standard Price", value=acc_product.standard_price, key=f"acc_sp_{i}")
            product_data.accounting_db_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"acc_enabled_{i}")  # ← added here

        if product_data.mewaahghar_store_1_db_enabled:
            st.markdown("###### MeWaah Ghar Store 1 DB")
            pos_product.name = st.text_input("Product Name", value = pos_product.name, key=f"pos_nm_{i}")
            acc_cols = st.columns(6)
            pos_product.weight = acc_cols[0].number_input("Main Weight", value=pos_product.weight,  key=f"pos_wt_{i}")
            pos_product.volume = acc_cols[1].number_input("Main Volume", value=pos_product.volume,  key=f"pos_vol_{i}")
            pos_product.qty_available = acc_cols[2].number_input("Qty Available", value=pos_product.qty_available, key=f"pos_qty_{i}")
            pos_product.list_price = acc_cols[3].number_input("List Price", value=pos_product.list_price, key=f"pos_lp_{i}")
            pos_product.standard_price = acc_cols[4].number_input("Standard Price", value=pos_product.standard_price, key=f"pos_sp_{i}")
            product_data.mewaahghar_store_1_db_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"pos_enabled_{i}")  # ← added here

        if st.button("Sync product", key=f"update_prod_sync_{i}"):
            print("syncing product")
            product_sync_data = {
                "main_db_product": product,
                "account_db_product": acc_product,
                "pos_1_db_product": pos_product,
                "product_data": product_data
            }
            syncing_product(**product_sync_data)
            sync_data()
            st.success('Synced the product to POS db')

        st.markdown("---")



for i, product_id in enumerate(not_enabled_product_ids):
    with st.container():
        product_data, product, acc_product, pos_product = get_product_current_state(product_id)
        acc_exist = True
        pos_exist = True
        if not acc_product:
            acc_product = product.model_copy()
            acc_exist = False
        if not pos_product:
            pos_product = product.model_copy()
            pos_exist = False
        st.markdown(f"##### {product.name}")
        # Read-only main DB info
        main_cols = st.columns(5)
        main_cols[0].text_input("Updated Weight", value=product.weight, disabled=True, key=f"main_wt_{i}")
        main_cols[1].text_input("Updated Volume", value=product.volume, disabled=True, key=f"main_vol_{i}")
        main_cols[2].text_input("Updated Qty Available", value=product.qty_available, disabled=True,
                                key=f"main_qty_{i}")
        main_cols[3].text_input("Updated List Price", value=product.list_price, disabled=True, key=f"main_lp_{i}")
        main_cols[4].text_input("Updated Standard Price", value=product.standard_price, disabled=True,
                                key=f"main_sp_{i}")

        if not product_data.accounting_db_enabled:
            st.markdown("###### Accounting DB ")
            acc_product.name = st.text_input("Product Name", value = acc_product.name, key=f"acc_nm_{i}")
            acc_cols = st.columns(6)
            acc_product.weight = acc_cols[0].number_input("Main Weight", value=acc_product.weight,  key=f"acc_wt_{i}")
            acc_product.volume = acc_cols[1].number_input("Main Volume", value=acc_product.volume,  key=f"acc_vol_{i}")
            acc_product.qty_available = acc_cols[2].number_input("Qty Available", value=acc_product.qty_available, key=f"acc_qty_{i}")
            acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price, key=f"acc_lp_{i}")
            acc_product.standard_price = acc_cols[4].number_input("Standard Price", value=acc_product.standard_price, key=f"acc_sp_{i}")
            product_data.accounting_db_enabled = acc_cols[5].checkbox("Enabled", value=False, key=f"acc_enabled_{i}")  # ← added here

        if not product_data.mewaahghar_store_1_db_enabled:
            st.markdown("###### MeWaah Ghar Store 1 DB")
            pos_product.name = st.text_input("Product Name", value = pos_product.name, key=f"pos_nm_{i}")
            acc_cols = st.columns(6)
            pos_product.weight = acc_cols[0].number_input("Main Weight", value=pos_product.weight,  key=f"pos_wt_{i}")
            pos_product.volume = acc_cols[1].number_input("Main Volume", value=pos_product.volume,  key=f"pos_vol_{i}")
            pos_product.qty_available = acc_cols[2].number_input("Qty Available", value=pos_product.qty_available, key=f"pos_qty_{i}")
            pos_product.list_price = acc_cols[3].number_input("List Price", value=pos_product.list_price, key=f"pos_lp_{i}")
            pos_product.standard_price = acc_cols[4].number_input("Standard Price", value=pos_product.standard_price, key=f"pos_sp_{i}")
            product_data.mewaahghar_store_1_db_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"pos_enabled_{i}")  # ← added here

        if st.button("Sync product", key=f"enable_prod_sync_{i}"):
            print("syncing product")
            product_sync_data = {
                "main_db_product": product,
                "account_db_product": acc_product,
                "pos_1_db_product": pos_product,
                "product_data": product_data
            }
            syncing_product(**product_sync_data)
            sync_data()
            st.success('Synced the product to POS db')

        st.markdown("---")
