# Steam ID Parser 🚀

Этот проект представляет собой асинхронный парсер Steam-профилей, который перебирает возможные идентификаторы пользователей и сохраняет данные (имя и уровень) в базу данных SQLite.

## 🔧 Функционал
- Асинхронные запросы к Steam Community с помощью `aiohttp`.
- Использование `aiosqlite` для работы с базой данных без блокировки.
- Ограничение количества одновременных запросов (`asyncio.Semaphore`).
- Обход ошибки "Профиль не найден".
- Логирование процессов для удобного отслеживания.

## 📦 Установка
Убедитесь, что у вас установлен **Python 3.8+**, затем выполните:
```sh
git clone https://github.com/yourusername/steam-id-parser.git
cd steam-id-parser
pip install -r requirements.txt
```

## ⚙️ Настройка
Все основные параметры настраиваются в файле config.py:
```py
DB_PATH = "user_data.db"  # Путь к базе данных
BASE_URL = "https://steamcommunity.com/id/"
COMBINATION_LENGTH = 3  # Длина перебираемых ID
CONCURRENT_REQUESTS = 50  # Количество одновременных запросов
TIMEOUT = 30  # Таймаут запроса (сек)
BATCH_SIZE = 500  # Количество задач в одном батче
CHARACTERS = "abcdefghijklmnopqrstuvwxyz1234567890-_"
```
Вы можете изменить COMBINATION_LENGTH, если хотите проверять более длинные или короткие Steam ID.


## ▶️ Запуск
После установки зависимостей просто запустите:
```py
python main.py
```
Скрипт начнет парсинг и запись данных в SQLite.


## 💾 Структура БД
Создается таблица users со следующими полями:
| Поле | Тип данных | Описание |
|-------------|------------|--------------------------|
| id | INTEGER | Уникальный идентификатор |
| profile_link | TEXT | Ссылка на профиль Steam |
| name | TEXT | Имя пользователя |
| level | TEXT | Уровень пользователя |


## 🛠 Технологии  
- **Python 3.8+**  
- [aiohttp](https://docs.aiohttp.org/en/stable/) – асинхронные HTTP-запросы  
- [aiosqlite](https://aiosqlite.omnilib.dev/) – асинхронная работа с БД  
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – парсинг HTML  
- [asyncio](https://docs.python.org/3/library/asyncio.html) – конкурентное выполнение  


## Лицензия
Проект распространяется под лицензией MIT. Вы можете свободно использовать и модифицировать код.
