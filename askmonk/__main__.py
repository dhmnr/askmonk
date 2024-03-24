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
        print(f"<h1>{topic}</h1>")
        print(f"<p>{get_summaries(topic, api_key)}</p>")
        print("<br>")
        # generate quizzes
    print("<br>")
    print(
        """
    <h1>Simple Quiz</h1>

    <form name="quiz">
        <p>1. What is 2 + 2?</p>
        <input type="radio" id="q1a1" name="q1" value="3"> 3<br>
        <input type="radio" id="q1a2" name="q1" value="4"> 4<br>
        <input type="radio" id="q1a3" name="q1" value="5"> 5<br>

        <p>2. Which planet is known as the Red Planet?</p>
        <input type="radio" id="q2a1" name="q2" value="Venus"> Venus<br>
        <input type="radio" id="q2a2" name="q2" value="Saturn"> Saturn<br>
        <input type="radio" id="q2a3" name="q2" value="Mars"> Mars<br>

        <p>3. What is the boiling point of water?</p>
        <input type="radio" id="q3a1" name="q3" value="100"> 100°C<br>
        <input type="radio" id="q3a2" name="q3" value="90"> 90°C<br>
        <input type="radio" id="q3a3" name="q3" value="110"> 110°C<br>

        <input type="button" value="Submit" onclick="calculateScore()">
    </form>

    <div id="result"></div>

    <script type="text/javascript">
        function calculateScore() {
            var score = 0;
            var totalQuestions = 3;
            
            // Question 1
            if (document.getElementById('q1a2').checked) {
                score++;
            }

            // Question 2
            if (document.getElementById('q2a3').checked) {
                score++;
            }

            // Question 3
            if (document.getElementById('q3a1').checked) {
                score++;
            }

            // Display result
            var result = "Your score: " + score + " out of " + totalQuestions;
            document.getElementById('result').innerHTML = result;
        }
    </script>"""
    )
