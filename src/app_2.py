import sys, os
from datamodel import ProductData

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.products.product_management import (
    sync_data,
    get_product_difference_in_main_db,
    get_product_current_state,
    syncing_product
)

# Initialize session state variables if they don't exist
if 'products' not in st.session_state:
    st.session_state.products = []
if 'updated_products' not in st.session_state:
    st.session_state.updated_products = []
if 'not_enabled_product_ids' not in st.session_state:
    st.session_state.not_enabled_product_ids = []
if 'sync_status' not in st.session_state:
    st.session_state.sync_status = ""

# Product info configuration
product_info = {
    "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
    "db_url": "https://mewaahgharstore.odoo.com",
}


# Function to handle product sync operations
def perform_sync(product_sync_data):
    try:
        syncing_product(**product_sync_data)
        sync_data()
        st.session_state.sync_status = "Success! Product synced successfully."
        return True
    except Exception as e:
        st.session_state.sync_status = f"Error syncing product: {str(e)}"
        return False


# Functions for button actions
def refresh_new_products():
    with st.spinner("Fetching new products..."):
        new_products, _ = get_product_difference_in_main_db()
        st.session_state.products = new_products
        st.session_state.sync_status = f"Found {len(new_products)} new products in Main DB."


def refresh_updated_products():
    with st.spinner("Fetching updated products..."):
        _, updated_products = get_product_difference_in_main_db()
        st.session_state.updated_products = updated_products
        st.session_state.sync_status = f"Found {len(updated_products)} updated products in Main DB."


def refresh_disabled_products():
    with st.spinner("Fetching disabled products..."):
        from src.products.product_management import existing_product_mapping
        not_enabled_product_ids = [
            key for key, prod_data in existing_product_mapping.items()
            if not (prod_data.accounting_db_enabled or prod_data.mewaahghar_store_1_db_enabled)
        ]
        st.session_state.not_enabled_product_ids = not_enabled_product_ids
        st.session_state.sync_status = f"Found {len(not_enabled_product_ids)} disabled products."


# Page configuration
st.set_page_config(
    page_title="Product Sync Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# Sidebar
st.sidebar.title("Product Sync Panel")
st.sidebar.markdown("Use the buttons below to sync product data.")
st.sidebar.markdown("---")

# Initialize counters for metrics display
new_count = len(st.session_state.products)
updated_count = len(st.session_state.updated_products)
disabled_count = len(st.session_state.not_enabled_product_ids)

# Display metrics
col1, col2, col3 = st.sidebar.columns(3)
col1.metric("New", new_count)
col2.metric("Updated", updated_count)
col3.metric("Disabled", disabled_count)

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Operations")

# Action buttons
if st.sidebar.button("🔍 Fetch New Products"):
    refresh_new_products()

if st.sidebar.button("🔄 Fetch Updated Products"):
    refresh_updated_products()

if st.sidebar.button("⚠️ Fetch Disabled Products"):
    refresh_disabled_products()

if st.sidebar.button("🔄 Sync All Data"):
    with st.spinner("Syncing all data..."):
        sync_data()
        st.session_state.sync_status = "All data synchronized successfully."

st.sidebar.markdown("---")

# Main title
st.title("Product List & Sync Dashboard")

# Status message display
if st.session_state.sync_status:
    status_type = "success" if "Success" in st.session_state.sync_status else "error" if "Error" in st.session_state.sync_status else "info"
    if status_type == "success":
        st.success(st.session_state.sync_status)
    elif status_type == "error":
        st.error(st.session_state.sync_status)
    else:
        st.info(st.session_state.sync_status)

# Tab navigation for different product views
tab1, tab2, tab3 = st.tabs(["New Products", "Updated Products", "Disabled Products"])

# Tab 1: New Products
with tab1:
    if not st.session_state.products:
        st.info("No new products found. Click 'Fetch New Products' to check for new items.")

    for i, product in enumerate(st.session_state.products[:5]):
        with st.container():
            st.markdown(f"##### {product.name}")

            # Read-only main DB info
            with st.expander("Main DB Info (Read-Only)", expanded=True):
                main_cols = st.columns(5)
                main_cols[0].text_input("Weight", value=product.weight, disabled=True, key=f"main_wt_{i}")
                main_cols[1].text_input("Volume", value=product.volume, disabled=True, key=f"main_vol_{i}")
                main_cols[2].text_input("Qty Available", value=product.qty_available, disabled=True,
                                        key=f"main_qty_{i}")
                main_cols[3].text_input("List Price", value=product.list_price, disabled=True, key=f"main_lp_{i}")
                main_cols[4].text_input("Standard Price", value=product.standard_price, disabled=True,
                                        key=f"main_sp_{i}")

            product_data = ProductData()

            # Accounting DB section
            with st.expander("Accounting DB Settings", expanded=True):
                acc_product = product.model_copy()
                acc_product.name = st.text_input("Product Name", value=acc_product.name, key=f"acc_nm_{i}")
                acc_cols = st.columns(6)
                acc_product.weight = acc_cols[0].number_input("Weight", value=acc_product.weight, key=f"acc_wt_{i}")
                acc_product.volume = acc_cols[1].number_input("Volume", value=acc_product.volume, key=f"acc_vol_{i}")
                acc_product.qty_available = acc_cols[2].number_input("Qty Available", value=acc_product.qty_available,
                                                                     key=f"acc_qty_{i}")
                acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price,
                                                                  key=f"acc_lp_{i}")
                acc_product.standard_price = acc_cols[4].number_input("Standard Price",
                                                                      value=acc_product.standard_price,
                                                                      key=f"acc_sp_{i}")
                product_data.accounting_db_enabled = acc_cols[5].checkbox("Enabled", value=True, key=f"acc_enabled_{i}")

            # MeWaah Ghar Store DB section
            with st.expander("MeWaah Ghar Store 1 DB Settings", expanded=True):
                pos_product = product.model_copy()
                pos_product.name = st.text_input("Product Name", value=pos_product.name, key=f"pos_nm_{i}")
                pos_cols = st.columns(6)
                pos_product.weight = pos_cols[0].number_input("Weight", value=pos_product.weight, key=f"pos_wt_{i}")
                pos_product.volume = pos_cols[1].number_input("Volume", value=pos_product.volume, key=f"pos_vol_{i}")
                pos_product.qty_available = pos_cols[2].number_input("Qty Available", value=pos_product.qty_available,
                                                                     key=f"pos_qty_{i}")
                pos_product.list_price = pos_cols[3].number_input("List Price", value=pos_product.list_price,
                                                                  key=f"pos_lp_{i}")
                pos_product.standard_price = pos_cols[4].number_input("Standard Price",
                                                                      value=pos_product.standard_price,
                                                                      key=f"pos_sp_{i}")
                product_data.mewaahghar_store_1_db_enabled = pos_cols[5].checkbox("Enabled", value=True,
                                                                                  key=f"pos_enabled_{i}")

            # Sync button
            if st.button("📤 Sync Product", key=f"add_prod_sync_{i}", type="primary"):
                product_sync_data = {
                    "main_db_product": product,
                    "account_db_product": acc_product if product_data.accounting_db_enabled else None,
                    "pos_1_db_product": pos_product if product_data.mewaahghar_store_1_db_enabled else None,
                    "product_data": product_data,
                }
                if perform_sync(product_sync_data):
                    # Remove from list if synced successfully
                    st.session_state.products.pop(i)
                    st.rerun()

            st.markdown("---")

# Tab 2: Updated Products
with tab2:
    if not st.session_state.updated_products:
        st.info("No updated products found. Click 'Fetch Updated Products' to check for updates.")

    for i, product in enumerate(st.session_state.updated_products):
        with st.container():
            st.markdown(f"##### {product.name}")

            # Get current state
            product_data, current_main, acc_product, pos_product = get_product_current_state(product.id)

            # Display comparison between current and updated
            with st.expander("Main DB Comparison", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Current Values")
                    curr_cols = st.columns(5)
                    curr_cols[0].text_input("Weight", value=current_main.weight, disabled=True, key=f"c_main_wt_{i}")
                    curr_cols[1].text_input("Volume", value=current_main.volume, disabled=True, key=f"c_main_vol_{i}")
                    curr_cols[2].text_input("Qty Available", value=current_main.qty_available, disabled=True,
                                            key=f"c_main_qty_{i}")
                    curr_cols[3].text_input("List Price", value=current_main.list_price, disabled=True,
                                            key=f"c_main_lp_{i}")
                    curr_cols[4].text_input("Standard Price", value=current_main.standard_price, disabled=True,
                                            key=f"c_main_sp_{i}")

                with col2:
                    st.subheader("Updated Values")
                    upd_cols = st.columns(5)
                    upd_cols[0].text_input("Weight", value=product.weight, disabled=True, key=f"upd_main_wt_{i}")
                    upd_cols[1].text_input("Volume", value=product.volume, disabled=True, key=f"upd_main_vol_{i}")
                    upd_cols[2].text_input("Qty Available", value=product.qty_available, disabled=True,
                                           key=f"upd_main_qty_{i}")
                    upd_cols[3].text_input("List Price", value=product.list_price, disabled=True,
                                           key=f"upd_main_lp_{i}")
                    upd_cols[4].text_input("Standard Price", value=product.standard_price, disabled=True,
                                           key=f"upd_main_sp_{i}")

            # Accounting DB section (if enabled)
            if product_data.accounting_db_enabled and acc_product:
                with st.expander("Accounting DB Settings", expanded=True):
                    acc_product.name = st.text_input("Product Name", value=acc_product.name, key=f"upd_acc_nm_{i}")
                    acc_cols = st.columns(6)
                    acc_product.weight = acc_cols[0].number_input("Weight", value=acc_product.weight,
                                                                  key=f"upd_acc_wt_{i}")
                    acc_product.volume = acc_cols[1].number_input("Volume", value=acc_product.volume,
                                                                  key=f"upd_acc_vol_{i}")
                    acc_product.qty_available = acc_cols[2].number_input("Qty Available",
                                                                         value=acc_product.qty_available,
                                                                         key=f"upd_acc_qty_{i}")
                    acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price,
                                                                      key=f"upd_acc_lp_{i}")
                    acc_product.standard_price = acc_cols[4].number_input("Standard Price",
                                                                          value=acc_product.standard_price,
                                                                          key=f"upd_acc_sp_{i}")
                    product_data.accounting_db_enabled = acc_cols[5].checkbox("Enabled",
                                                                              value=product_data.accounting_db_enabled,
                                                                              key=f"upd_acc_enabled_{i}")
            else:
                with st.expander("Accounting DB Settings", expanded=False):
                    st.warning("Product not enabled in Accounting DB")
                    if st.button("Enable in Accounting DB", key=f"enable_acc_{i}"):
                        acc_product = product.model_copy()
                        product_data.accounting_db_enabled = True
                        st.rerun()

            # MeWaah Ghar Store DB section (if enabled)
            if product_data.mewaahghar_store_1_db_enabled and pos_product:
                with st.expander("MeWaah Ghar Store 1 DB Settings", expanded=True):
                    pos_product.name = st.text_input("Product Name", value=pos_product.name, key=f"upd_pos_nm_{i}")
                    pos_cols = st.columns(6)
                    pos_product.weight = pos_cols[0].number_input("Weight", value=pos_product.weight,
                                                                  key=f"upd_pos_wt_{i}")
                    pos_product.volume = pos_cols[1].number_input("Volume", value=pos_product.volume,
                                                                  key=f"upd_pos_vol_{i}")
                    pos_product.qty_available = pos_cols[2].number_input("Qty Available",
                                                                         value=pos_product.qty_available,
                                                                         key=f"upd_pos_qty_{i}")
                    pos_product.list_price = pos_cols[3].number_input("List Price", value=pos_product.list_price,
                                                                      key=f"upd_pos_lp_{i}")
                    pos_product.standard_price = pos_cols[4].number_input("Standard Price",
                                                                          value=pos_product.standard_price,
                                                                          key=f"upd_pos_sp_{i}")
                    product_data.mewaahghar_store_1_db_enabled = pos_cols[5].checkbox("Enabled",
                                                                                      value=product_data.mewaahghar_store_1_db_enabled,
                                                                                      key=f"upd_pos_enabled_{i}")
            else:
                with st.expander("MeWaah Ghar Store 1 DB Settings", expanded=False):
                    st.warning("Product not enabled in MeWaah Ghar Store 1 DB")
                    if st.button("Enable in Store DB", key=f"enable_pos_{i}"):
                        pos_product = product.model_copy()
                        product_data.mewaahghar_store_1_db_enabled = True
                        st.rerun()

            # Sync button
            if st.button("📤 Sync Product", key=f"update_prod_sync_{i}", type="primary"):
                product_sync_data = {
                    "main_db_product": product,
                    "account_db_product": acc_product if product_data.accounting_db_enabled else None,
                    "pos_1_db_product": pos_product if product_data.mewaahghar_store_1_db_enabled else None,
                    "product_data": product_data
                }
                if perform_sync(product_sync_data):
                    # Remove from list if synced successfully
                    st.session_state.updated_products.pop(i)
                    st.rerun()

            st.markdown("---")

# Tab 3: Disabled Products
with tab3:
    if not st.session_state.not_enabled_product_ids:
        st.info("No disabled products found. Click 'Fetch Disabled Products' to check for disabled items.")

    for i, product_id in enumerate(st.session_state.not_enabled_product_ids):
        with st.container():
            product_data, product, acc_product, pos_product = get_product_current_state(product_id)

            # Create copies if products don't exist
            acc_exist = True
            pos_exist = True
            if not acc_product:
                acc_product = product.model_copy()
                acc_exist = False
            if not pos_product:
                pos_product = product.model_copy()
                pos_exist = False

            st.markdown(f"##### {product.name}")

            # Main DB info
            with st.expander("Main DB Info (Read-Only)", expanded=True):
                main_cols = st.columns(5)
                main_cols[0].text_input("Weight", value=product.weight, disabled=True, key=f"dis_main_wt_{i}")
                main_cols[1].text_input("Volume", value=product.volume, disabled=True, key=f"dis_main_vol_{i}")
                main_cols[2].text_input("Qty Available", value=product.qty_available, disabled=True,
                                        key=f"dis_main_qty_{i}")
                main_cols[3].text_input("List Price", value=product.list_price, disabled=True, key=f"dis_main_lp_{i}")
                main_cols[4].text_input("Standard Price", value=product.standard_price, disabled=True,
                                        key=f"dis_main_sp_{i}")

            # Accounting DB section
            with st.expander("Accounting DB Settings", expanded=not product_data.accounting_db_enabled):
                acc_product.name = st.text_input("Product Name", value=acc_product.name, key=f"dis_acc_nm_{i}")
                acc_cols = st.columns(6)
                acc_product.weight = acc_cols[0].number_input("Weight", value=acc_product.weight, key=f"dis_acc_wt_{i}")
                acc_product.volume = acc_cols[1].number_input("Volume", value=acc_product.volume,
                                                              key=f"dis_acc_vol_{i}")
                acc_product.qty_available = acc_cols[2].number_input("Qty Available", value=acc_product.qty_available,
                                                                     key=f"dis_acc_qty_{i}")
                acc_product.list_price = acc_cols[3].number_input("List Price", value=acc_product.list_price,
                                                                  key=f"dis_acc_lp_{i}")
                acc_product.standard_price = acc_cols[4].number_input("Standard Price",
                                                                      value=acc_product.standard_price,
                                                                      key=f"dis_acc_sp_{i}")
                product_data.accounting_db_enabled = acc_cols[5].checkbox("Enable in Accounting DB",
                                                                          value=product_data.accounting_db_enabled,
                                                                          key=f"dis_acc_enabled_{i}")
                if not acc_exist:
                    st.info("Product will be created in Accounting DB if enabled")

            # MeWaah Ghar Store DB section
            with st.expander("MeWaah Ghar Store 1 DB Settings",
                             expanded=not product_data.mewaahghar_store_1_db_enabled):
                pos_product.name = st.text_input("Product Name", value=pos_product.name, key=f"dis_pos_nm_{i}")
                pos_cols = st.columns(6)
                pos_product.weight = pos_cols[0].number_input("Weight", value=pos_product.weight, key=f"dis_pos_wt_{i}")
                pos_product.volume = pos_cols[1].number_input("Volume", value=pos_product.volume,
                                                              key=f"dis_pos_vol_{i}")
                pos_product.qty_available = pos_cols[2].number_input("Qty Available", value=pos_product.qty_available,
                                                                     key=f"dis_pos_qty_{i}")
                pos_product.list_price = pos_cols[3].number_input("List Price", value=pos_product.list_price,
                                                                  key=f"dis_pos_lp_{i}")
                pos_product.standard_price = pos_cols[4].number_input("Standard Price",
                                                                      value=pos_product.standard_price,
                                                                      key=f"dis_pos_sp_{i}")
                product_data.mewaahghar_store_1_db_enabled = pos_cols[5].checkbox("Enable in Store DB",
                                                                                  value=product_data.mewaahghar_store_1_db_enabled,
                                                                                  key=f"dis_pos_enabled_{i}")
                if not pos_exist:
                    st.info("Product will be created in Store DB if enabled")

            # Sync button
            if st.button("📤 Sync Product", key=f"enable_prod_sync_{i}", type="primary"):
                product_sync_data = {
                    "main_db_product": product,
                    "account_db_product": acc_product if product_data.accounting_db_enabled else None,
                    "pos_1_db_product": pos_product if product_data.mewaahghar_store_1_db_enabled else None,
                    "product_data": product_data
                }
                if perform_sync(product_sync_data):
                    # Remove from list if synced successfully
                    st.session_state.not_enabled_product_ids.pop(i)
                    st.rerun()

            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("© MeWaah Ghar Store - Product Sync Dashboard")