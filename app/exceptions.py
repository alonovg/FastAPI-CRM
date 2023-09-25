from fastapi import HTTPException, status


class CrmException(HTTPException):
    status_code = 500
    detail = ""
    headers = {}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class UserAlreadyExistsException(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class CannotAddDataToDatabase(CrmException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotUpdateDataToDatabase(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не удалось обновить запись, т.к все поля не были изменены"


class IncorrectEmailOrPasswordException(CrmException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверное имя или пароль"


class TokenAbsentException(CrmException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(CrmException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(CrmException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class CannotFindClient(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Клиент не был найден"


class CannotFindPayMethod(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Платежное средство не было найдено"


class CannotDelPayMethod(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нельзя удалить платежное средство, т.к. есть заказ с этим ПС"


class CannotFindStatus(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Статус заявки не был найден"


class CannotFindOrder(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заявка с указанным номером не найдена"


class CannotFindExecutor(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Исполнитель не был найден"


class CannotFindExecutorInOrder(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не удалось найти исполнителя в заказе"


class ExecutorExistInOrders(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вы не можете удалить этого исполнителя, т.к. он используется в заказах"


class ExecutorAlreadyExist(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Исполнитель с таким именем уже существует"


class CannotFindService(CrmException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Услуга не была найдена"


class ServiceAlreadyExist(CrmException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Услуга с таким именем уже существует"


class CannotGetOrderName(CrmException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Необходимо заполнить имя заявки"
