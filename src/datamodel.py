from pydantic import BaseModel, Field
from typing import Optional, List

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

class CompanyType(BaseModel):
    person: str = "person"
    company: str = "company"

class Customer(BaseModel):
    id: int = Field(default=-1)
    name: str
    phone_number: str
    company_type: str = Field(default=CompanyType().person)
    gstin: Optional[str] = Field(default=False)
    email: str = Field(default=False)
    street: str = Field(default=False)


class ProductData(BaseModel):
    main_db_id: int = Field(default=-1)
    accounting_db_id: int = Field(default=-1)
    mewaahghar_store_1_db_id: int = Field(default=-1)
    accounting_db_enabled: bool = Field(default=True)
    mewaahghar_store_1_db_enabled: bool = Field(default=True)
    accounting_db_synced: bool = Field(default=False)
    mewaahghar_store_1_db_synced: bool = Field(default=False)


class ItemPlace(BaseModel):
    id: int
    name: str
    product_id: int
    qty: int
    price_unit: int

class Order(BaseModel):
    id: int = Field(default=-1)
    # date_order: str
    user_id: int
    lines: List[ItemPlace]

