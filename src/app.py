import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.products.get_product import get_product_list
# Mocked data (you can later replace it with live API data)
product_info = {
    "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
    "db_url": "https://mewaahgharstore.odoo.com",
}

from src.products.product_management import get_newly_added_product
products = []

# Sidebar
st.sidebar.title("Product Sync Panel")
st.sidebar.markdown("Use the buttons on the right to sync product data.")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Products:** {len(products)}")

# Compare Buttons
st.sidebar.markdown("### Newly Added Items")
if st.sidebar.button("🔍 New Items to Main DB"):
    products = get_newly_added_product(db_type="main_db")
    st.success("New Items Added to Main DB triggered.")

if st.sidebar.button("🔍 New Items to Accounting DB"):
    st.success("New Items Added to Accounting DB triggered..")
    products = get_newly_added_product(db_type="accounting_db")

if st.sidebar.button("🔍 New Items to Mewaah Ghar Store 1 DB"):
    st.success("New Items Added to Mewaah Ghar store 1 triggered.")
    products = get_newly_added_product(db_type="mewaahghar_store_1_db")

st.sidebar.markdown("---")

# Main title
st.title("Product List & Sync Dashboard")

# Button to sync all products
if st.button("🔄 Sync ALL Products to Accounting DB and POS_1_DB"):
    st.success("All products synced successfully to Accounting DB and POS_1_DB.")

# Editable product list
for i, product in enumerate(products):
    with st.container():
        st.markdown(f"### {product.name}")
        col1, col2, col3 = st.columns(3)

        with col1:
            list_price = st.number_input("List Price (₹)", value=product.list_price, key=f"lp_{i}")
            qty_available = st.number_input("Qty Available", value=product.qty_available, key=f"qty_{i}")
        with col2:
            standard_price = st.number_input("Standard Price (₹)", value=product.standard_price, key=f"sp_{i}")
            weight = st.number_input("Weight (kg)", value=product.weight, key=f"wt_{i}")
        with col3:
            volume = st.number_input("Volume (L)", value=product.volume, key=f"vol_{i}")

            if st.button("📥 Sync to Accounting", key=f"acc_{product.id}"):

                st.success(f"{product.name} synced to Accounting DB.")

            if st.button("🖥️ Sync to POS_1_DB", key=f"pos_{product.id}"):
                st.success(f"{product.name} synced to POS_1_DB.")

        st.markdown("---")