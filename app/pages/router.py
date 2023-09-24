from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates

from app.clients.router import (get_clients, get_one_client_by_id, get_client_order,
                                get_profit_from_all_order, get_sum_from_all_order)
from app.orders.dao import OrderDAO
from app.orders.router import get_order_by_num
from app.pages.dependencies import (get_orders_info_async_func, func_for_calc_gets_spends_2func,
                                    func_for_calc_gets_spends_1func, get_count_executor_by_id)
from app.paysmethods.router import get_pays_methods, get_spend_sum_by_pays, get_sum_by_pays
from app.performers.executors.router import get_executors, get_spend_sum_by_pays_executor
from app.performers.orders.router import get_order_exc_by_num
from app.performers.services.router import get_services, get_spend_sum_by_pays_service
from app.statuses.router import get_statuses
from app.users.router import read_users_me
from app.tasks.tasks import debug_task


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates/")


@router.get("/orders")
async def get_orders_page(
        request: Request,
        order_by: str = Query('order_num', description='Field to order by'),
        order_desc: bool = Query(True, description='Order direction (True for descending)'),
        current_user=Depends(read_users_me),
        orders=Depends(get_orders_info_async_func)
):
    if order_by == 'order_num':
        orders.sort(key=lambda order: order.order_num, reverse=order_desc)
    elif order_by == 'order_date_create':
        orders.sort(key=lambda order: order.order_date_create, reverse=order_desc)
    executors = {}
    for order in orders:
        executors[order.id] = await get_count_executor_by_id(order.order_num)
    debug_task.delay()  # Test celery task
    return templates.TemplateResponse(name="orders/orders.html",
                                      context={
                                          "request": request,
                                          "current_user": current_user,
                                          "order_by": order_by,
                                          "order_desc": order_desc,
                                          "orders": orders,
                                          "executors": executors
                                      })


@router.get("/orders/{order_num}")
async def get_order_num_page(
        order_num: int,
        request: Request,
        current_user=Depends(read_users_me),
        executors=Depends(get_executors),
        statuses=Depends(get_statuses),
        services=Depends(get_services),
        paysmethods=Depends(get_pays_methods)
):
    order_data = await get_order_by_num(order_num)
    executor_order_data = await get_order_exc_by_num(order_num)
    return templates.TemplateResponse(name="orders/order_num.html",
                                      context={"request": request,
                                               "order_data": order_data,
                                               "current_user": current_user,
                                               "executor_order_data": executor_order_data,
                                               "executors": executors,
                                               "statuses": statuses,
                                               "services": services,
                                               "paysmethods": paysmethods
                                               })


@router.get("/create_order")
async def get_order_create_page(
        request: Request,
        current_user=Depends(read_users_me),
        clients=Depends(get_clients),
        paysmethods=Depends(get_pays_methods),
        statuses=Depends(get_statuses)
):
    new_order_num = await OrderDAO.get_last_order_num()
    return templates.TemplateResponse(name="orders/new_order.html", context={
        "request": request,
        "current_user": current_user,
        "new_order_num": new_order_num + 1,
        "clients": clients,
        "paysmethods": paysmethods,
        "statuses": statuses
    })


@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/executors")
async def get_clients_page(
        request: Request,
        current_user=Depends(read_users_me),
        executors=Depends(get_executors),
):
    executors_data = await func_for_calc_gets_spends_1func(executors, get_spend_sum_by_pays_executor)
    return templates.TemplateResponse(name="executors/executors.html", context={
        "request": request,
        "current_user": current_user,
        "executors_data": executors_data
    })


@router.get("/services")
async def get_clients_page(
        request: Request,
        current_user=Depends(read_users_me),
        services=Depends(get_services),
):
    services_data = await func_for_calc_gets_spends_1func(services, get_spend_sum_by_pays_service)
    return templates.TemplateResponse(name="services/services.html", context={
        "request": request,
        "current_user": current_user,
        "services_data": services_data
    })


@router.get("/paysmethods")
async def get_clients_page(
        request: Request,
        current_user=Depends(read_users_me),
        paysmethods=Depends(get_pays_methods),
):
    pays_data = await func_for_calc_gets_spends_2func(paysmethods, get_sum_by_pays, get_spend_sum_by_pays)
    return templates.TemplateResponse(name="paysmethods/paysmethods.html", context={
        "request": request,
        "current_user": current_user,
        "pays_data": pays_data
    })


@router.get("/clients")
async def get_clients_page(
        request: Request,
        current_user=Depends(read_users_me),
        clients=Depends(get_clients),

):
    clients_data = await func_for_calc_gets_spends_2func(clients, get_sum_from_all_order, get_profit_from_all_order)
    return templates.TemplateResponse(name="clients/clients.html", context={
        "request": request,
        "current_user": current_user,
        "clients_data": clients_data,
    })


@router.get("/clients/{client_id}")
async def get_client_id_page(
        request: Request,
        current_user=Depends(read_users_me),
        client=Depends(get_one_client_by_id),
        orders=Depends(get_client_order),
        client_sum=Depends(get_sum_from_all_order),
        client_profit=Depends(get_profit_from_all_order)
):
    executors = {}
    for order in orders:
        executors[order.id] = await get_count_executor_by_id(order.order_num)
    return templates.TemplateResponse(name="clients/client_num.html",
                                      context={
                                          "request": request,
                                          "current_user": current_user,
                                          "client": client,
                                          "orders": orders,
                                          "executors": executors,
                                          "client_sum": client_sum,
                                          "client_profit": client_profit
                                      })
