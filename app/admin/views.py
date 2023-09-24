from sqladmin import ModelView

from app.clients.models import Clients
from app.orders.models import Orders
from app.paysmethods.models import PaysMethods
from app.performers.executors.models import Executors
from app.performers.orders.models import ExecutorOrders
from app.performers.services.models import Services
from app.statuses.models import Statuses
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class OrdersAdmin(ModelView, model=Orders):
    column_list = [c.name for c in Orders.__table__.c] + [Orders.user] + [Orders.client]
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-bars"


class ExecutorsAdmin(ModelView, model=Executors):
    column_list = [Executors.id, Executors.name]
    name = "Исполнитель"
    name_plural = "Исполнители"
    icon = "fa-solid fa-users"


class ExecutorsOrdersAdmin(ModelView, model=ExecutorOrders):
    column_list = [c.name for c in ExecutorOrders.__table__.c] + [ExecutorOrders.executor] + \
                  [ExecutorOrders.status] + [ExecutorOrders.pays]
    name = "Заявка исполнителя"
    name_plural = "Заявки исполнителей"
    icon = "fa-solid fa-list"


class ServicesAdmin(ModelView, model=Services):
    column_list = [Services.id, Services.name]
    name = "Направление услуги"
    name_plural = "Направления услуг"
    icon = "fa-solid fa-indent"


class StatusesAdmin(ModelView, model=Statuses):
    column_list = [Statuses.id, Statuses.name]
    name = "Статус"
    name_plural = "Стутусы"
    icon = "fa-solid fa-font-awesome"


class PaysMethodsAdmin(ModelView, model=PaysMethods):
    column_list = [PaysMethods.id, PaysMethods.name]
    name = "Платежное средство"
    name_plural = "Платежные средства"
    icon = "fa-money"


class ClientsAdmin(ModelView, model=Clients):
    column_list = [Clients.id, Clients.username]
    name = "Клиент"
    name_plural = "Клиенты"
    icon = "fa-solid fa-street-view"