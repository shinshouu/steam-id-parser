import os

# Основные настройки
DB_PATH = os.getenv("DB_PATH", "user_data.db")
BASE_URL = "https://steamcommunity.com/id/"
COMBINATION_LENGTH = 3  # Длина комбинации ID
CONCURRENT_REQUESTS = 50  # Количество одновременных запросов
TIMEOUT = 30  # Таймаут для запроса (секунды)
BATCH_SIZE = 500  # Количество задач в одном батче

# Доступные символы в Steam ID
CHARACTERS = "abcdefghijklmnopqrstuvwxyz1234567890-_"
