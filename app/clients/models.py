from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

    order = relationship("Orders", back_populates="client", lazy="select")

    def __str__(self):
        return f"Client: {self.username}"


