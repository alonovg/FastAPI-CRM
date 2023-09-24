from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        name, password = form["username"], form["password"]
        user = await authenticate_user(name, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user = await get_current_user(token)
        if not user:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
