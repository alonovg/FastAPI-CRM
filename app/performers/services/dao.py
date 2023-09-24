from app.dao.base import BaseDAO
from app.performers.services.models import Services


class ServiceDAO(BaseDAO):
    model = Services
