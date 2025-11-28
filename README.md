# Telegram-Бот для заказа 3d печатной продукции 
Telegram-бот, позволяющий пользователям оформлять заказы на печатную продукцию.
Бот принимает данные от пользователя, обрабатывает их, сохраняет в базу данных и формирует служебные файлы для дальнейшей обработки заказов.

## Технологический стек
- Python 3.11+

- Aiogram — асинхронный Telegram-фреймворк
- SQLAlchemy + SQLite — хранение заказов и данных пользователей
- openpyxl — генерация и обработка Excel-файлов
- numpy-stl — работа с STL-моделями при необходимости расчётов или анализа 3D-форм

### Установка и запуск
1. Склонируйте репозиторий
```bash
git clone https://github.com/selfgeek-coder/codingfest-Sev-IT-8-9.git ./
```

2. Установите необходимые библиотеки
```bash
pip install -r req.txt
```

3. Создайте файл '.env' в корне проекта
```bash
DATABASE_URL="sqlite:///database.db"
TOKEN="ваш_telegram_bot_token"
ADMINS=123456789,987654321
```
- DATABASE_URL — строка подключения к SQLite (можно не менять
- TOKEN — токен вашего Telegram-бота
- ADMINS — список Telegram-ID администраторов через запятую (не обязательно несколько, можно заполнить только одного администратора)

4. Запустите проект
```bash
python main.py
```

### Структура проекта 
```
└── 📁app
    └── 📁bot
        └── 📁handlers
            └── 📁admin
                ├── __init__.py
                ├── panel.py
            └── 📁user
                ├── __init__.py
                ├── cart.py
                ├── main_menu.py
                ├── make_order.py
                ├── my_orders.py
        └── 📁keyboards
            └── 📁admin
                ├── main_menu.py
                ├── panel_menu.py
            └── 📁user
                ├── back_kb.py
                ├── cart_menu.py
                ├── main_menu.py
                ├── make_order_menu.py
        └── 📁states
            ├── order_fsm.py
    └── 📁database
        └── 📁models
            ├── cart.py
            ├── orders.py
            ├── user.py
        └── 📁repositories
            ├── cart_repository.py
            ├── order_repository.py
            ├── user_repository.py
        ├── database.py
        ├── session.py
    └── 📁enums
        ├── order_status.py
    └── 📁services
        ├── calc_service.py
        ├── cart_service.py
        ├── order_service.py
        ├── user_service.py
    ├── excel.py
    └── utils.py
```

### Возможности бота
- Создание заказов, отслеживание их статусов (пользователь)

- Управление статусами заказов, выгрузка excel таблицы (админ)

### Небольшие видеообзоры возможностей бота
- Пользователь [Видео](https://drive.google.com/file/d/1wIurFfH6ES7LUMHX0S1fGklibmk2z9oO/view?usp=sharing)
- Администратор [Видео](https://drive.google.com/file/d/1L34L1Xh1KoFIuuBWiuu1QkdzV8b21tXM/view?usp=sharing)
