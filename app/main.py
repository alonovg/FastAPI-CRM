import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import (UsersAdmin, OrdersAdmin, ExecutorsAdmin, ExecutorsOrdersAdmin,
                             ServicesAdmin, StatusesAdmin, PaysMethodsAdmin, ClientsAdmin)
from app.config import settings
from app.database import engine
from app.pages.router import router as router_pages
from app.users.router import router as router_user
from app.clients.router import router as router_client
from app.paysmethods.router import router as router_pays_method
from app.orders.router import router as router_order
from app.statuses.router import router as router_statuses
from app.prometheus.router import router as router_prometheus
from app.performers.services.router import router as router_services
from app.performers.executors.router import router as router_executors
from app.performers.orders.router import router as router_executors_orders
from app.logger import logger


if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

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
app.include_router(router_prometheus)

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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": str(round(process_time, 4))
    })
    return response


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)
