import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    KPIsRouter,
    address_router,
    auth_router,
    cart_items_routes,
    cart_router,
    category_router,
    client_router,
    invoice_items_router,
    invoices_router,
    paypal_router,
    products_router,
    report_router,
    roles_router,
    stocks_router,
    users_router,
    wishlist_router,
)
from api.hello_controller import router

font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
font_bold = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans-Bold.ttf")
# from db import events
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(auth_router, prefix="/auth")
app.include_router(roles_router, prefix="/admin")
app.include_router(users_router, prefix="/admin")
app.include_router(products_router, prefix="")
app.include_router(KPIsRouter, prefix="")
app.include_router(invoices_router, prefix="")
app.include_router(invoice_items_router, prefix="")
app.include_router(stocks_router, prefix="")
app.include_router(cart_router, prefix="")
app.include_router(cart_items_routes, prefix="")
app.include_router(category_router, prefix="")
app.include_router(client_router, prefix="/client")
app.include_router(wishlist_router, prefix="/client")
app.include_router(report_router, prefix="")
app.include_router(address_router, prefix="/client")
app.include_router(paypal_router, prefix="/client")
# @app.on_event("startup")
# def startup_event():
#     init_db()
