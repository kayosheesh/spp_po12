"""
Модуль для лабораторной работы №4.
Вариант 7: Автоматический мониторинг популярных репозиториев GitHub.
"""
import json
import requests


def search_github_repos(keyword):
    """
    Поиск топ-10 репозиториев по ключевому слову через GitHub Search API.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": keyword,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    try:
        print(f"\nИщем топ-10 репозиториев по запросу '{keyword}'...")
        # Исправлено: добавлен timeout=10 для предотвращения зависания
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            result_list = []

            print(f"\nТоп-10 репозиториев по запросу '{keyword}':")
            for i, repo in enumerate(items, 1):
                repo_info = {
                    "name": repo['full_name'],
                    "description": repo['description'] or "Нет описания",
                    "stars": repo['stargazers_count'],
                    "forks": repo['forks_count'],
                    "last_commit": repo['pushed_at']
                }
                result_list.append(repo_info)
                print(f"{i}. {repo_info['name']} - ⭐{repo_info['stars']:,}, "
                      f"{repo_info['forks']:,} (Last commit: {repo_info['last_commit'][:10]})")

            save_to_json(result_list)
        elif response.status_code == 403:
            print("Ошибка: Превышен лимит запросов к API. Подождите немного.")
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")

    # Исправлено: ловим конкретные ошибки запросов вместо общего Exception
    except requests.exceptions.RequestException as error:
        print(f"Ошибка сети: {error}")


def save_to_json(data):
    """
    Сохранение результатов в JSON-файл.
    """
    filename = "github_top_repos.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"\nРезультаты успешно сохранены в {filename}")


if __name__ == "__main__":
    user_keyword = input("Введите ключевое слово для поиска репозиториев: ")
    if user_keyword.strip():
        search_github_repos(user_keyword)
    else:
        print("Ключевое слово не может быть пустым.")
