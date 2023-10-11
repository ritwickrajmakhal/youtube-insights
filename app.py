import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mindsdb_sdk
from flask_cors import CORS
from time import sleep

# Create the Flask app
app = Flask(__name__)
# Initialize CORS with your app
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Load the environment variables from the .env file
load_dotenv()

# Check if the environment variables are set
if os.environ.get('MINDSDB_EMAIL') is None:
    raise Exception('Please set the MINDSDB_EMAIL environment variable')
if os.environ.get('MINDSDB_PASSWORD') is None:
    raise Exception(
        'Please set the MINDSDB_PASSWORD environment variable')

# Connect to MindsDB Cloud server
try:
    server = mindsdb_sdk.connect(login=os.environ.get(
        'MINDSDB_EMAIL'), password=os.environ.get('MINDSDB_PASSWORD'))
except:
    raise Exception("Check your internet connection or credentials")

# Create project if not exists
try:
    project = server.get_project('social_insights')
except:
    project = server.create_project('social_insights')

# Add data sources if not exists
try:
    # Check if the environment variables are set
    if os.environ.get('YOUTUBE_API_KEY') is None:
        raise Exception(
            'Please set the YOUTUBE_API_KEY environment variable')
    # Create the database
    mindsdb_youtube = server.create_database(name='mindsdb_youtube', engine='youtube', connection_args={
        'youtube_api_token': os.environ.get('YOUTUBE_API_KEY')})
except:
    mindsdb_youtube = server.get_database('mindsdb_youtube')

def create_model(name, predict, prompt_template):
    # check model is exist or not
    try:
        # Create the model
        model = project.models.create(
            name=name,
            engine='openai',
            predict=predict,
            prompt_template=prompt_template,
        )
        while model.get_status() != 'complete':
            sleep(1)
        return model
    except:
        # Get the model
        return project.models.get(name)

@app.route('/api/youtube', methods=['GET'])
def get_youtube_insights():

    youtube_video_id = request.args.get('youtube_video_id')
    # Create the JSON response with initial sentiment counts
    response = {}

    # Create sentiment_classifier_model
    sentiment_classifier_model = create_model(name='sentiment_classifier_model', predict='sentiment',
                                              prompt_template="describe the sentiment of the comment strictly as 'positive', 'neutral', or 'negative'.'I love the product':positive, 'It is a scam':negative '{{comment}}.':")

    # Predict sentiments
    sentiment_result = server.query(f'''SELECT input.comment, output.sentiment
                                    FROM mindsdb_youtube.get_comments AS input
                                    JOIN social_insights.sentiment_classifier_model AS output
                                    WHERE input.youtube_video_id = \"{youtube_video_id}\" LIMIT 30''').fetch()

    sentiment_counts = sentiment_result['sentiment'].value_counts()
    response["sentiments"] = {
        "positive": int(sentiment_counts.get('positive', 0)),
        "neutral": int(sentiment_counts.get('neutral', 0)),
        "negative": int(sentiment_counts.get('negative', 0))
    }

    # Summarize the comments or predict recommendations
    text_summarization_model = create_model(name='text_summarization_model', predict='summary',
                                    prompt_template="provide an informative summary of the comments comments:{{comments}} using full sentences")
    # gather all comment
    merged_comments = ''.join(sentiment_result['comment'].tolist())
    # Predict summarized comment
    summarizer_result = text_summarization_model.predict({'comments': merged_comments})
    response["summary"] = str(summarizer_result['summary'][0])
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
