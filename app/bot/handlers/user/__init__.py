from .make_order import router as order_router
from .my_orders import router as myorders_router
from .start import router as start_router

handlers = [
    order_router,
    myorders_router,
    start_router
]