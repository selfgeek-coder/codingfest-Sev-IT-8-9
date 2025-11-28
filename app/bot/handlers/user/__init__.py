from .make_order import router as order_router
from .my_orders import router as my_orders_router
from .main_menu import router as main_menu_router
from .cart import router as cart_router

handlers = [
    order_router,
    my_orders_router,
    main_menu_router,
    cart_router
]