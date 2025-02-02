import asyncio
import aiohttp
import aiosqlite
import logging
from itertools import product
from bs4 import BeautifulSoup
from config import DB_PATH, BASE_URL, COMBINATION_LENGTH, CONCURRENT_REQUESTS, TIMEOUT, BATCH_SIZE, CHARACTERS

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def fetch_data(session, url):
    """Запрашивает HTML-страницу и возвращает её содержимое."""
    try:
        async with session.get(url, timeout=TIMEOUT) as response:
            if response.status == 200:
                return await response.text()
            logging.warning(f"Failed request {url} with status {response.status}")
    except asyncio.TimeoutError:
        logging.warning(f"Timeout for {url}. Retrying in 5 seconds...")
        await asyncio.sleep(5)
    except aiohttp.ClientError as e:
        logging.error(f"Request error for {url}: {e}")
    return None


async def parse_profile(session, profile_url):
    """Парсит страницу Steam-профиля, извлекая имя и уровень."""
    html_content = await fetch_data(session, profile_url)
    if not html_content:
        return None, None

    soup = BeautifulSoup(html_content, 'html.parser')

    # Проверка на ошибку "Профиль не найден"
    error_message = soup.find('div', {'id': 'message'})
    if error_message and 'Указанный профиль не найден.' in error_message.text:
        return None, None

    name = soup.find('span', class_='actual_persona_name')
    level = soup.find('div', class_='persona_name persona_level')

    return (name.text.strip() if name else "Unknown",
            level.text.replace('Уровень', '').strip() if level else "Unknown")


async def process_combination(combination, session, semaphore, db):
    """Обрабатывает одну комбинацию ID, парсит и сохраняет в БД."""
    profile_url = f"{BASE_URL}{combination}"

    async with semaphore:
        name, level = await parse_profile(session, profile_url)
        if name and level:
            await db.execute(
                "INSERT OR IGNORE INTO users (profile_link, name, level) VALUES (?, ?, ?)",
                (profile_url, name, level)
            )
            logging.info(f"Processed: {profile_url} - {name} - {level}")
            await db.commit()


async def generate_combinations(length):
    """Генерирует комбинации указанной длины."""
    return ["".join(combo) for combo in product(CHARACTERS, repeat=length)]


async def init_db():
    """Инициализирует базу данных."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_link TEXT UNIQUE,
                name TEXT,
                level TEXT
            )
        """)


async def main():
    """Основной цикл сбора данных."""
    await init_db()

    async with aiosqlite.connect(DB_PATH) as db, aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        combinations = await generate_combinations(COMBINATION_LENGTH)

        for i in range(0, len(combinations), BATCH_SIZE):
            batch = combinations[i:i + BATCH_SIZE]
            tasks = [process_combination(comb, session, semaphore, db) for comb in batch]
            await asyncio.gather(*tasks)

    logging.info("Parsing and data insertion complete.")


if __name__ == "__main__":
    asyncio.run(main())
