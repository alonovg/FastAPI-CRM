from app.dao.base import BaseDAO
from app.performers.executors.models import Executors


class ExecutorDAO(BaseDAO):
    model = Executors
