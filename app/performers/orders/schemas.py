from pydantic import BaseModel


class SNewExecutorOrder(BaseModel):
    order_num: int
    order_executor: int
    order_status: int
    order_send_pay: bool
    order_pay_method: int
    order_sum: float
    order_service: int
