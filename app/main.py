from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import (UsersAdmin, OrdersAdmin, ExecutorsAdmin, ExecutorsOrdersAdmin,
                             ServicesAdmin, StatusesAdmin, PaysMethodsAdmin, ClientsAdmin)
from app.database import engine
from app.pages.router import router as router_pages
from app.users.router import router as router_user
from app.clients.router import router as router_client
from app.paysmethods.router import router as router_pays_method
from app.orders.router import router as router_order
from app.statuses.router import router as router_statuses
from app.performers.services.router import router as router_services
from app.performers.executors.router import router as router_executors
from app.performers.orders.router import router as router_executors_orders


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_user)
app.include_router(router_client)
app.include_router(router_pays_method)
app.include_router(router_statuses)
app.include_router(router_services)
app.include_router(router_executors)
app.include_router(router_executors_orders)
app.include_router(router_order)
app.include_router(router_pages)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(OrdersAdmin)
admin.add_view(ExecutorsAdmin)
admin.add_view(ExecutorsOrdersAdmin)
admin.add_view(ServicesAdmin)
admin.add_view(StatusesAdmin)
admin.add_view(PaysMethodsAdmin)
admin.add_view(ClientsAdmin)

# Домены, которые могу обращаться к API
origins = [
    "http://localhost:3000"
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"]
)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
