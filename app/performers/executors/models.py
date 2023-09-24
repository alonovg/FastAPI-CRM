from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Executors(Base):
    __tablename__ = "executors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    executor_orders = relationship("ExecutorOrders", back_populates="executor")

    def __str__(self):
        return f"Executor: {self.name}"
    