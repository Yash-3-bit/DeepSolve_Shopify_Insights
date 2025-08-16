from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

class Product(BaseModel):
    id: Optional[int]
    title: str
    handle: Optional[str] = None
    price: Optional[str] = None
    url: Optional[str] = None

class FAQ(BaseModel):
    question: str
    answer: str

class BrandContextRequest(BaseModel):
    website_url: HttpUrl

class BrandContextResponse(BaseModel):
    brand_name: Optional[str]
    product_catalog: List[Product] = []
    hero_products: List[Product] = []
    privacy_policy: Optional[str]
    refund_policy: Optional[str]
    faqs: List[FAQ] = []
    social_handles: Dict[str, str] = {}
    contact_details: Dict[str, str] = {}
    about: Optional[str]
    important_links: Dict[str, str] = {}
