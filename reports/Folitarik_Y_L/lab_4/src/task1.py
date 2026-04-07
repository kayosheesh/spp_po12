"""
Скрипт для анализа репозиториев GitHub по ключевому слову.
Собирает данные через GitHub API, анализирует технологии и визуализирует результаты.
Соответствует стандартам PEP8 и требованиям Pylint.
"""

import sys
import warnings
from datetime import datetime, timezone
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Игнорируем внутренние предупреждения библиотек для чистого вывода
warnings.filterwarnings("ignore", category=FutureWarning)


def fetch_repositories(query, per_page=100):
    """
    Получает данные о репозиториях через GitHub Search API.

    Args:
        query (str): Ключевое слово для поиска.
        per_page (int): Количество репозиториев (макс. 100).

    Returns:
        list: Список словарей с данными о репозиториях.
    """
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к API: {error}")
        sys.exit(1)


def process_data(repos):
    """
    Преобразует список репозиториев в Pandas DataFrame.

    Args:
        repos (list): Данные в формате JSON.

    Returns:
        pd.DataFrame: Таблица с обработанными данными.
    """
    data = []
    for repo in repos:
        data.append(
            {
                "name": repo["full_name"],
                "language": repo["language"] or "Unknown",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "issues": repo["open_issues_count"],
                "updated_at": pd.to_datetime(repo["updated_at"]),
            }
        )
    return pd.DataFrame(data)


def print_statistics(df):
    """
    Выводит текстовую аналитику по найденным репозиториям.

    Args:
        df (pd.DataFrame): Таблица данных.
    """
    print("\n--- Аналитика ---")

    # Популярные языки
    lang_counts = df["language"].value_counts(normalize=True) * 100
    print("Самые популярные языки:")
    for lang, percent in lang_counts.head(5).items():
        print(f"- {lang} ({percent:.1f}%)")

    # Самый звездный репозиторий
    top_repo = df.iloc[df["stars"].idxmax()]
    print(
        f"\nСамый звёздный репозиторий: '{top_repo['name']}' "
        f"({top_repo['stars'] // 1000}k звёзд)"
    )

    # Среднее количество форков
    avg_forks = df["forks"].mean()
    print(f"Среднее количество форков: {avg_forks:.1f}")

    # Процент репозиториев, не обновлявшихся больше года
    now = datetime.now(timezone.utc)
    one_year_ago = now - pd.Timedelta(days=365)
    abandoned = df[df["updated_at"] < one_year_ago]
    abandoned_pct = (len(abandoned) / len(df)) * 100
    print(f"{abandoned_pct:.1f}% репозиториев не обновлялись больше года!")


def visualize(df, topic):
    """
    Создает графики: языки, популярность и активность обновлений.

    Args:
        df (pd.DataFrame): Таблица данных.
        topic (str): Тема поиска для названия файла.
    """
    sns.set_theme(style="whitegrid")
    # Используем _, так как объект fig не используется напрямую для вызова методов
    _, axes = plt.subplots(3, 1, figsize=(10, 18))

    # 1. Диаграмма языков
    lang_data = df["language"].value_counts().head(10)
    axes[0].pie(lang_data, labels=lang_data.index, autopct="%1.1f%%", startangle=140)
    axes[0].set_title("Топ-10 языков программирования")

    # 2. График популярности (Звезды)
    top_10_stars = df.nlargest(10, "stars")
    sns.barplot(
        x="stars",
        y="name",
        data=top_10_stars,
        ax=axes[1],
        hue="name",
        palette="viridis",
        legend=False,
    )
    axes[1].set_title("Топ-10 репозиториев по звёздам")

    # 3. График активности (Старение)
    df_plot = df.copy()
    # Удаляем таймзону перед конвертацией в период месяца для исключения UserWarning
    df_plot["month"] = (
        df_plot["updated_at"].dt.tz_localize(None).dt.to_period("M").astype(str)
    )
    update_counts = df_plot["month"].value_counts().sort_index()

    update_counts.plot(
        kind="line", marker="o", ax=axes[2], color="tab:blue", linewidth=2
    )
    axes[2].set_title("Активность обновлений (по месяцам)")
    axes[2].set_xlabel("Месяц последнего обновления")
    axes[2].set_ylabel("Кол-во репозиториев")
    plt.xticks(rotation=45)

    plt.tight_layout()
    filename = f"{topic.replace(' ', '_')}_analysis.png"
    plt.savefig(filename)
    print(f"\nГрафики успешно сохранены в файл: {filename}")


def main():
    """
    Главная функция: сбор, обработка и визуализация данных.
    """
    user_input = input("Введите тему для анализа: ").strip()
    topic = user_input if user_input else "machine learning"

    print(f"Анализируем популярные репозитории по теме '{topic}'...")

    # Получение данных
    repos_json = fetch_repositories(topic)
    if not repos_json:
        print("Репозитории не найдены.")
        return

    # Обработка
    dataframe = process_data(repos_json)

    # Вывод результатов
    print_statistics(dataframe)
    visualize(dataframe, topic)


if __name__ == "__main__":
    main()
