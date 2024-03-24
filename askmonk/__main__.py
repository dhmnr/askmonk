import click
import os
import json
from .get_topics import get_topics, get_summaries, get_questions
from .repo import create_vector_data, retrieve_, _set_settings_, get_mongo_client

from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch


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

    _set_settings_()

    client = get_mongo_client()

    mongo_store = MongoDBAtlasVectorSearch(client, 
                                     index_name='mistr', 
                                     db_name='attn_db', 
                                     collection_name='vec')

    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, ".mistral_api_key")

    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
    except Exception as e:
        print(f"Error reading the api key file: {e}")
        raise
    answer = retrieve_(store=mongo_store, query=query)
    topics = get_topics(query, api_key=api_key)
    print(f"<p>{answer}</p>")
    questions = []
    for topic in topics:
        print(f"<h1>{topic}</h1>")
        
        print(f"<p>{get_summaries(topic, api_key)}</p>")
        print("<br>")
        question = get_questions(topic, api_key)
        # print(question)
        questions.append(json.loads(question))
        # generate quizzes
    print("<br>")
    print("<h1>Quiz</h1>")
    print('<form name="quiz">')
    for qn, question in enumerate(questions):
        print(f"<h2>{question['question']}</h2>")
        for option in question["options"].keys():
            print(
                f'<input type="radio" id="q{qn+1}{option}" name="q{qn+1}" value="{question["options"][option]}"> {question["options"][option]}<br>'
            )
    print('<input type="button" value="Submit" onclick="calculateScore()">')
    print("</form>")

    print('<div id="result"></div>')

    print('<script type="text/javascript">')
    print("function calculateScore() {")
    print("      var score = 0;")
    print(f"      var totalQuestions = {len(questions)};")
    for qn, question in enumerate(questions):
        print(
            f"""
            if (document.getElementById('q{qn+1}{question['correct_answer']}').checked) {{
                score++;
            }}  
            """
        )

    print(
        """
            var result = "Your score: " + score + " out of " + totalQuestions;
            document.getElementById('result').innerHTML = result;
        }
        </script>"""
    )
