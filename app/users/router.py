from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, CannotAddDataToDatabase, IncorrectEmailOrPasswordException, \
    UserIsNotPresentException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.tasks.tasks import send_user_confirmation_email

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация & Авторизация"]
)


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(name=user_data.name)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(name=user_data.name, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase
    find_user = await UserDAO.find_one_or_none(id=new_user.id)
    send_user_confirmation_email.delay(dict(find_user))
    return find_user


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.name, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("crm_access_token", access_token)
    return {"access_token": access_token}


@router.get("/logout")
def logout_user(response: Response):
    response.delete_cookie("crm_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/user/{id}")
async def read_users_by_id(user_id: int):
    user = await UserDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserIsNotPresentException
    return user.name
