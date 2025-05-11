import os
from src.datamodel import DBCredentials
data_folder = f"{os.path.dirname(__file__)}/../data/"

product_data_file = f"{data_folder}/product_mapping_data.csv"
pos_database_info = {
    "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=O3_lBABFt89nV4yjQyem2rCPZUQJXD-JK4cFcRgNcq1cVKhzRnRk5hJcG6U1JaEd-56BMfww1FD5ET3HKLs5; cids=1; frontend_lang=en_IN",
    "db_url": "https://mewaahgharstore.odoo.com",
}

# accounting_database_info = {
#     "cookie": "frontend_lang=en_US; session_id=6Yv3eCBMlFyiFATjDsxDzGO3Mb3e3JJk4Dxm9NhJXud5Yam_eT7o7WgeJCzVb_STIObKlgMYJP6sZzl0nruy; cids=1; tz=Asia/Kolkata",
#     "db_url": "http://ec2-13-201-230-81.ap-south-1.compute.amazonaws.com:8069",
# }

accounting_database_info = {
    "cookie": "utm_source=db; utm_medium=auth; tz=Asia/Kolkata; session_id=9r3W9bMHquPO0tDU7QNQS1gGTlRywt78mrzv_r8bbxFM6bFyB6liqvHLviBPNliJupS4_5N88y1aSgGzAli1; cids=1",
    "db_url": "https://mewaahgharaccounting.odoo.com",
}

main_database_info = {
    "cookie": "session_id=2djNe3-Mm1-UaEIX2bLLk92VqbPAu0Ocvk_6JQKvY4KnENRJxUTPG_xPhc3oS4GalGlRlhvcFsqonJNbn_dX; frontend_lang=en_IN; cids=1; utm_source=db; utm_medium=auth",
    "db_url": "https://mewaahghar.odoo.com",
}

main_db_cred = DBCredentials(**main_database_info)
pos_db_cred = DBCredentials(**pos_database_info)
accounting_db_cred = DBCredentials(**accounting_database_info)