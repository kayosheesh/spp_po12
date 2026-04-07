"""Analyze popular technologies in GitHub repositories for a chosen topic."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import math
import os
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

GITHUB_API_URL = "https://api.github.com/search/repositories"
REQUEST_TIMEOUT = 30
RESULTS_PER_PAGE = 100
PAGES_TO_LOAD = 2
TOP_LANGUAGES = 7
TOP_REPOSITORIES = 10


@dataclass(slots=True)
class RepositoryInfo:
    """Normalized GitHub repository data."""

    full_name: str
    language: str
    stars: int
    forks: int
    open_issues: int
    updated_at: datetime
    url: str

    @property
    def days_since_update(self) -> int:
        """Return the number of days since last update."""
        delta = datetime.now(timezone.utc) - self.updated_at
        return delta.days


def prompt_topic() -> str:
    """Read the topic from stdin."""
    while True:
        topic = input("Введите тему для анализа: ").strip()
        if topic:
            return topic
        print("Тема не может быть пустой.")


def github_headers() -> dict[str, str]:
    """Return headers for GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def search_repositories(topic: str) -> list[RepositoryInfo]:
    """Load popular repositories for the given topic."""
    repositories: list[RepositoryInfo] = []

    for page in range(1, PAGES_TO_LOAD + 1):
        response = requests.get(
            GITHUB_API_URL,
            headers=github_headers(),
            params={
                "q": f"{topic} in:name,description,readme",
                "sort": "stars",
                "order": "desc",
                "per_page": RESULTS_PER_PAGE,
                "page": page,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        items = response.json().get("items", [])
        if not items:
            break

        repositories.extend(parse_repository(item) for item in items)

    return repositories


def parse_repository(item: dict[str, Any]) -> RepositoryInfo:
    """Convert a GitHub repository payload to a normalized dataclass."""
    language = item.get("language") or "Не указан"
    updated_at = datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00")).astimezone(
        timezone.utc
    )
    return RepositoryInfo(
        full_name=item.get("full_name", "unknown/unknown"),
        language=language,
        stars=int(item.get("stargazers_count", 0)),
        forks=int(item.get("forks_count", 0)),
        open_issues=int(item.get("open_issues_count", 0)),
        updated_at=updated_at,
        url=item.get("html_url", ""),
    )


def analyze_languages(
    repositories: list[RepositoryInfo],
) -> list[tuple[str, float, int]]:
    """Return language usage share for the loaded repositories."""
    counter = Counter(repo.language for repo in repositories)
    total = len(repositories)
    return [
        (language, count / total * 100, count)
        for language, count in counter.most_common(TOP_LANGUAGES)
    ]


def find_top_repository(repositories: list[RepositoryInfo]) -> RepositoryInfo:
    """Return the repository with the highest star count."""
    return max(repositories, key=lambda repo: repo.stars)


def average_forks(repositories: list[RepositoryInfo]) -> float:
    """Return average forks across repositories."""
    return sum(repo.forks for repo in repositories) / len(repositories)


def outdated_share(repositories: list[RepositoryInfo], stale_days: int = 365) -> float:
    """Return share of repositories not updated longer than stale_days."""
    stale_count = sum(1 for repo in repositories if repo.days_since_update > stale_days)
    return stale_count / len(repositories) * 100


def print_report(topic: str, repositories: list[RepositoryInfo]) -> None:
    """Print analysis summary to stdout."""
    print(f"Анализируем {len(repositories)} популярных репозиториев " f'по теме "{topic}"...')
    print("Самые популярные языки:")
    for language, share, _count in analyze_languages(repositories):
        print(f"- {language} ({share:.1f}%)")

    top_repo = find_top_repository(repositories)
    forks_mean = average_forks(repositories)
    stale_percent = outdated_share(repositories)

    print(
        f'Самый звёздный репозиторий: "{top_repo.full_name}" '
        f"({format_number(top_repo.stars)} звёзд)"
    )
    print(f"Среднее количество форков: {format_number(forks_mean)}")
    print(f"{stale_percent:.1f}% репозиториев не обновлялись больше года")


def format_number(value: float) -> str:
    """Format large numbers in compact style."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    if math.isclose(value, round(value)):
        return str(int(round(value)))
    return f"{value:.1f}"


def slugify_topic(topic: str) -> str:
    """Build a safe filename from a topic."""
    sanitized = [char.lower() if char.isalnum() else "_" for char in topic.strip()]
    slug = "".join(sanitized).strip("_")
    return slug or "github_topic"


def build_dataframe(repositories: list[RepositoryInfo]) -> pd.DataFrame:
    """Convert repositories to a DataFrame for plotting."""
    return pd.DataFrame(
        {
            "name": [repo.full_name for repo in repositories],
            "language": [repo.language for repo in repositories],
            "stars": [repo.stars for repo in repositories],
            "forks": [repo.forks for repo in repositories],
            "issues": [repo.open_issues for repo in repositories],
            "days_since_update": [repo.days_since_update for repo in repositories],
        }
    )


def top_language_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Return counts for the most common repository languages."""
    top_languages = data["language"].value_counts().head(TOP_LANGUAGES).reset_index()
    top_languages.columns = ["language", "count"]
    return top_languages


def top_repositories_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Return top repositories sorted for plotting."""
    return data.nlargest(TOP_REPOSITORIES, "stars").sort_values("stars")


def plot_languages_chart(axes: plt.Axes, top_languages: pd.DataFrame) -> None:
    """Plot the most common languages chart."""
    sns.barplot(
        data=top_languages,
        x="count",
        y="language",
        hue="language",
        palette="crest",
        legend=False,
        ax=axes,
    )
    axes.set_title("Популярные языки программирования")
    axes.set_xlabel("Количество репозиториев")
    axes.set_ylabel("Язык")


def plot_activity_chart(figure: plt.Figure, axes: plt.Axes, data: pd.DataFrame) -> None:
    """Plot repository activity and popularity scatter chart."""
    scatter = axes.scatter(
        data["stars"],
        data["issues"],
        s=(data["forks"].clip(lower=1) ** 0.6) * 8,
        c=data["days_since_update"],
        cmap="viridis_r",
        alpha=0.75,
        edgecolors="black",
        linewidths=0.4,
    )
    axes.set_title("Популярность и активность репозиториев")
    axes.set_xlabel("Количество звёзд")
    axes.set_ylabel("Открытые issues")
    color_bar = figure.colorbar(scatter, ax=axes)
    color_bar.set_label("Дней с последнего обновления")


def plot_staleness_histogram(axes: plt.Axes, data: pd.DataFrame) -> None:
    """Plot repository staleness histogram."""
    sns.histplot(
        data["days_since_update"],
        bins=12,
        kde=True,
        color="#4c72b0",
        ax=axes,
    )
    axes.set_title("Старение репозиториев", fontsize=10)
    axes.set_xlabel("Дней без обновления", fontsize=9)
    axes.set_ylabel("Частота", fontsize=9)
    axes.tick_params(axis="both", labelsize=8)


def plot_top_repositories_chart(axes: plt.Axes, most_popular: pd.DataFrame) -> None:
    """Plot the top repositories by stars chart."""
    sns.barplot(
        data=most_popular,
        x="stars",
        y="name",
        hue="name",
        palette="mako",
        legend=False,
        ax=axes,
    )
    axes.set_title("Топ репозиториев по звёздам")
    axes.set_xlabel("Количество звёзд")
    axes.set_ylabel("Репозиторий")


def save_visualizations(topic: str, repositories: list[RepositoryInfo]) -> Path:
    """Create and save charts in a single image file."""
    data = build_dataframe(repositories)
    top_languages = top_language_dataframe(data)
    most_popular = top_repositories_dataframe(data)

    sns.set_theme(style="whitegrid")
    figure, axes = plt.subplots(3, 1, figsize=(14, 18))
    figure.suptitle(
        f'Анализ GitHub-репозиториев по теме "{topic}"',
        fontsize=16,
        y=0.995,
    )

    plot_languages_chart(axes[0], top_languages)
    plot_activity_chart(figure, axes[1], data)
    plot_top_repositories_chart(axes[2], most_popular)
    inset = axes[2].inset_axes([0.64, 0.08, 0.32, 0.42])
    plot_staleness_histogram(inset, data)

    figure.tight_layout(rect=(0, 0, 1, 0.98))
    filename = f"{slugify_topic(topic)}_analysis.png"
    output_path = Path(__file__).resolve().parent / filename
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
    return output_path


def handle_http_error(error: requests.HTTPError) -> None:
    """Print a readable message for GitHub API failures."""
    status_code = error.response.status_code if error.response is not None else "unknown"
    if status_code == 403:
        print(
            "GitHub API вернул 403. Возможно, исчерпан лимит запросов. "
            "Попробуйте позже или задайте GITHUB_TOKEN."
        )
        return
    print(f"Ошибка GitHub API: HTTP {status_code}")


def main() -> None:
    """Run the CLI workflow."""
    topic = prompt_topic()

    try:
        repositories = search_repositories(topic)
    except requests.HTTPError as error:
        handle_http_error(error)
        return
    except requests.RequestException as error:
        print(f"Сетевая ошибка: {error}")
        return

    if not repositories:
        print("По заданной теме репозитории не найдены.")
        return

    print_report(topic, repositories)
    output_path = save_visualizations(topic, repositories)

    print()
    print("Результат сохранён.")
    print(f"Графики: {output_path}")


if __name__ == "__main__":
    main()
