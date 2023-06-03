from pydantic import BaseModel

class Products(BaseModel):
    title: str
    description:str
    at_sale: bool = False
    inventory:int