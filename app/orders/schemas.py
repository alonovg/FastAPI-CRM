from pydantic import BaseModel


class SOrder(BaseModel):
    order_num: int


class SNewOrder(BaseModel):
    order_name: str
    order_client: int
    order_get_pay: bool
    order_pay_method: int
    order_sum: float
    order_status: int
