from app.dao.base import BaseDAO
from app.paysmethods.models import PaysMethods


class PaysMethodDAO(BaseDAO):
    model = PaysMethods
