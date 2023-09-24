from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Services(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    executor_orders = relationship("ExecutorOrders", back_populates="service")

    def __str__(self):
        return f"Service: {self.name}"