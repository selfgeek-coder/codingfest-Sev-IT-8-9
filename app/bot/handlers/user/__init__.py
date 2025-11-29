from .make_order_handler import router as order_router
from .my_orders_handler import router as my_orders_router
from .main_menu_handler import router as main_menu_router
from .cart_handler import router as cart_router

handlers = [
    order_router,
    my_orders_router,
    main_menu_router,
    cart_router
]