from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class PaysMethods(Base):
    __tablename__ = "pays_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    order = relationship("Orders", back_populates="pays")
    executor_orders = relationship("ExecutorOrders", back_populates="pays")

    def __str__(self):
        return f"Payment: {self.name}"