from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_num = Column(Integer, nullable=False)
    order_creator = Column(ForeignKey("users.id"))
    order_name = Column(String, nullable=False)
    order_date_create = Column(Date, nullable=False)
    order_date_close = Column(Date, nullable=True)
    order_client = Column(ForeignKey("clients.id"), nullable=False)
    order_get_pay = Column(Boolean, nullable=False)
    order_pay_method = Column(ForeignKey("pays_methods.id"), nullable=True)
    order_sum = Column(Float, nullable=True)
    order_status = Column(ForeignKey("statuses.id"))
    order_profit = Column(Float, nullable=True)

    user = relationship("Users", back_populates="order")
    client = relationship("Clients", back_populates="order")
    pays = relationship("PaysMethods", back_populates="order")
    status = relationship("Statuses", back_populates="order")
    executor_orders = relationship("ExecutorOrders", back_populates="order")

    def __str__(self):
        return f"Order: {self.order_num}"


