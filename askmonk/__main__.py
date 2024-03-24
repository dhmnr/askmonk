import click
import os
from .get_topics import get_topics, get_summaries


@click.command()
@click.argument("query", required=True)
@click.option(
    "--repo",
    "-r",
    type=str,
    required=False,
    help="Path to the repository",
)
def main(query: str, repo: str):

    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, ".mistral_api_key")

    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
    except Exception as e:
        print(f"Error reading the api key file: {e}")
        raise
    topics = get_topics(query, api_key=api_key)
    for topic in topics:
        print(topic)
        print(get_summaries(topic, api_key))
