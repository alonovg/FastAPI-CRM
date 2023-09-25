import pytest
from fastapi import Depends

from app.users.models import Users
from app.users.auth import get_password_hash, authenticate_user
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user


@pytest.mark.parametrize("name, password", [
    ("test_register_user", "test_pass"),
])
async def test_user_category(name, password):
    """
    Находим пользователя по имени
    Регистрируем пользователя
    Проверка входа
    Удаляем пользователя
    """
    existing_user = await UserDAO.find_one_or_none(name=name)
    assert existing_user is None
    hashed_password = get_password_hash(password)
    new_user = await UserDAO.add(name=name, hashed_password=hashed_password)
    assert new_user is not None
    find_user = await UserDAO.find_one_or_none(id=new_user.id)
    assert find_user.name == name
    login = await authenticate_user(name, password)
    assert login is not None
    del_user = await UserDAO.delete(id=new_user.id)
    assert del_user is None



