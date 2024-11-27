import string
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import logging
from colorama import Fore, Style, init

# Ініціалізація colorama
init(autoreset=True)

# Налаштування кольорового логування


class ColorfulFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


# Налаштування логера
handler = logging.StreamHandler()
formatter = ColorfulFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger()

# Функція для отримання тексту з URL


def fetch_text(url):
    try:
        logger.info("Завантаження тексту з URL...")
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Текст успішно завантажено.")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Помилка завантаження тексту: {e}")
        return None

# Функція для видалення пунктуації


def remove_punctuation(text):
    logger.info("Очищення тексту від пунктуації...")
    return text.translate(str.maketrans('', '', string.punctuation))

# Map функція: створює пару (слово, 1)


def map_function(word):
    return word, 1

# Shuffle функція: групує слова


def shuffle_function(mapped_values):
    logger.info("Групування результатів за ключами...")
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    logger.info("Групування завершено.")
    return shuffled.items()

# Reduce функція: підрахунок частоти


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Функція для виконання MapReduce


def map_reduce(text, top_n=10):
    # Очищення тексту
    cleaned_text = remove_punctuation(text).lower()

    # Розбиття тексту на слова
    words = cleaned_text.split()
    logger.info(f"Кількість слів у тексті: {len(words)}")

    # Map етап
    with ThreadPoolExecutor() as executor:
        mapped = list(executor.map(map_function, words))
    logger.info("Map етап завершено.")

    # Shuffle етап
    shuffled = shuffle_function(mapped)

    # Reduce етап
    with ThreadPoolExecutor() as executor:
        reduced = list(executor.map(reduce_function, shuffled))
    logger.info("Reduce етап завершено.")

    # Сортування результатів
    sorted_word_counts = sorted(reduced, key=lambda x: x[1], reverse=True)
    logger.info("Сортування завершено.")
    return sorted_word_counts[:top_n]

# Функція для візуалізації


def visualize_top_words(word_counts):
    logger.info("Візуалізація результатів...")
    words, counts = zip(*word_counts)
    plt.barh(words, counts, color='skyblue')
    plt.xlabel("Частота")
    plt.ylabel("Слова")
    plt.title("Топ-10 найчастіше вживаних слів")
    plt.gca().invert_yaxis()
    plt.show()
    logger.info("Візуалізація завершена.")


# Головна функція
if __name__ == "__main__":
    # URL для тексту
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = fetch_text(url)
    if text:
        # Виконання MapReduce
        top_words = map_reduce(text, top_n=10)
        logger.info("Топ-10 слів за частотою:")
        for word, count in top_words:
            logger.info(f"{word}: {count}")

        # Візуалізація
        visualize_top_words(top_words)
    else:
        logger.error("Не вдалося завантажити текст для аналізу.")
