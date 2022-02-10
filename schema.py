from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    uuid: str
    name: str
    email: str

    class Config:
        orm_mode = True


class MeterType(BaseModel):
    id: int
    uuid: str
    name: str
    description: str
    customer_id: int

    class Config:
        orm_mode = True

