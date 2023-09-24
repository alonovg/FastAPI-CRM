from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Statuses(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    order = relationship("Orders", back_populates="status")
    executor_orders = relationship("ExecutorOrders", back_populates="status")

    def __str__(self):
        return f"Status: {self.name}"