import logging

import os
import secrets 
import string

def setup_logging():
    """
    конфигурирует логирование
    формат:
    [INFO] 2025-11-27 20:35:23,143 aiogram.dispatcher: Start polling
    """
    
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
    )

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

def gen_random_name(filename: str) -> str:
    """
    генерирует случайное имя файла, сохраняя расширение
    например gen_random_name("test.stl") -> "quOY1U0.stl"
    """

    name, ext = os.path.splitext(filename)
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(7))
    return f"{random_name}{ext}"