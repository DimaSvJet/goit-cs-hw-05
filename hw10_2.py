import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

import requests


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching text: {e}")
        return None

# Функція для видалення знаків пунктуації


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word.lower(), 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce


def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    # if search_words:
    #    words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(result, top_num=10):
    if not result:
        print("No words found in the text.")
        return

    sorted_words = sorted(
        result.items(), key=lambda item: item[1], reverse=True)

    top_words = sorted_words[:top_num]

    wolds = [item[0] for item in top_words]
    counts = [item[1] for item in top_words]

    plt.figure(figsize=(8, 6))
    sns.barplot(x=counts, y=wolds, palette="pastel")

    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Words', fontsize=14)
    plt.title('Word Frequency Histogram (Seaborn)', fontsize=16)
    plt.show()


if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        # search_words = ['war', 'peace', 'love']
        # result = map_reduce(text, search_words)
        result = map_reduce(text)
        if not result:
            print("No words found in the text.")
            exit(1)
        visualize_top_words(result)

        print("Результат підрахунку слів:", result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
