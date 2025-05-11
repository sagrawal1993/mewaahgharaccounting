from pydantic import BaseModel, Field
from typing import Optional

class DBCredentials(BaseModel):
    cookie: str
    db_url: str


class Product(BaseModel):
    id: int
    name: str
    product_variant_count: Optional[int] = Field(default=0)
    list_price: float
    qty_available: float
    standard_price: float
    weight: float
    volume: float
    # write_data: str


class ProductData(BaseModel):
    name: str

    # Mandatory fields (main_db)
    main_db_weight: float
    main_db_volume: float
    main_db_id: int
    main_db_qty_available: int
    main_db_list_price: float
    main_db_standard_price: float

    # Optional fields (default to None)
    accounting_db_weight: Optional[float] = None
    mewaahghar_store_1_db_weight: Optional[float] = None
    accounting_db_volume: Optional[float] = None
    mewaahghar_store_1_db_volume: Optional[float] = None
    accounting_db_id: Optional[int] = None
    mewaahghar_store_1_db_id: Optional[int] = None
    accounting_db_qty_available: Optional[int] = None
    mewaahghar_store_1_db_qty_available: Optional[int] = None
    accounting_db_list_price: Optional[float] = None
    mewaahghar_store_1_db_list_price: Optional[float] = None
    accounting_db_standard_price: Optional[float] = None
    mewaahghar_store_1_db_standard_price: Optional[float] = None

