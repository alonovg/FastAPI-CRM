from app.dao.base import BaseDAO
from app.statuses.models import Statuses


class StatusDAO(BaseDAO):
    model = Statuses
