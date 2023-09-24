from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from app.database import Base


class ExecutorOrders(Base):
    __tablename__ = "executor_orders"

    id = Column(Integer, primary_key=True)
    order_name = Column(String, nullable=True)
    order_num = Column(ForeignKey("orders.id"), nullable=False)
    order_executor = Column(ForeignKey("executors.id"), nullable=False)
    order_status = Column(ForeignKey("statuses.id"), nullable=False)
    order_send_pay = Column(Boolean, nullable=False)
    order_pay_method = Column(ForeignKey("pays_methods.id"), nullable=True)
    order_sum = Column(Float, nullable=True)
    order_service = Column(ForeignKey("services.id"), nullable=False)
    order_date_create = Column(Date, nullable=False)
    order_date_close = Column(Date, nullable=True)

    order = relationship("Orders", back_populates="executor_orders")
    executor = relationship("Executors", back_populates="executor_orders")
    status = relationship("Statuses", back_populates="executor_orders")
    pays = relationship("PaysMethods", back_populates="executor_orders")
    service = relationship("Services", back_populates="executor_orders")

    def __str__(self):
        return f"Executor Order: {self.order_name}"