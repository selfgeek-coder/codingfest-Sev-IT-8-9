import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
    )

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)