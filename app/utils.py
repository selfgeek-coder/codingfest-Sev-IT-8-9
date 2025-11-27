import logging

import os
import re
import secrets 
import string

from config import Settings

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

def is_admin(user_id: int) -> bool:
    return user_id in Settings.admins

def gen_random_name(filename: str) -> str:
    """
    генерирует случайное имя файла, сохраняя расширение
    например gen_random_name("test.stl") -> "quOY1U0.stl"
    """

    name, ext = os.path.splitext(filename)
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(7))
    return f"{random_name}{ext}"


def validate_fullname(text: str) -> bool:
    """
    валидатор имени и фамилии
    """
    text = text.strip()

    # разбиваем на слова
    parts = text.split()

    if len(parts) < 2:
        return False

    pattern = r"^[A-Za-zА-Яа-яЁё]{2,40}$"

    for part in parts:
        if not re.match(pattern, part):
            return False

    return True