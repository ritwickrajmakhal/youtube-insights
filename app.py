import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mindsdb_sdk
from flask_cors import CORS
import threading

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
    print("Connected to MindsDB Cloud server")
except:
    raise Exception("Check your internet connection or mindsdb credentials")

# Create project if not exists
try:
    project = server.get_project('youtube_insights')
    print("Project already exists")
except:
    project = server.create_project('youtube_insights')
    print("Project created")

# Add data sources if not exists
try:
    # Check if the environment variables are set
    if os.environ.get('YOUTUBE_API_KEY') is None:
        raise Exception(
            'Please set the YOUTUBE_API_KEY environment variable')
    # Create the database
    mindsdb_youtube = server.create_database(name='mindsdb_youtube', engine='youtube', connection_args={
        'youtube_api_token': os.environ.get('YOUTUBE_API_KEY')})
    print("Database created")
except:
    mindsdb_youtube = server.get_database('mindsdb_youtube')
    print("Database already exists")


def create_model(name: str, engine: str, predict: str, options: dict):
    from time import sleep
    # check model is exist or not
    try:
        # Create the model
        model = project.models.create(
            name=name,
            engine=engine,
            predict=predict,
            options=options
        )
        print(f"Model {name} created")
        # Wait for the model to be trained
        while model.get_status() != 'complete':
            sleep(1)
            print("Training the model...")
        return model
    except:
        # Get the model
        print(f"Model {name} already exists")
        return project.models.get(name)


# Create sentiment_classifier_model
sentiment_classifier_model = create_model(name='sentiment_classifier_model',
                                          engine='huggingface',
                                          predict='sentiment',
                                          options={
                                              'task': 'text-classification',
                                              'model_name': 'cardiffnlp/twitter-roberta-base-sentiment',
                                              'input_column': 'comment',
                                              'labels': ['negative', 'neutral', 'positive']
                                          })

# Create text summarization model
text_summarization_model = create_model(name='text_summarization_model',
                                        engine='openai',
                                        predict='comment_summary',
                                        options={
                                            'prompt_template': "provide an informative summary of the comments comments:{{comments}} using full sentences",
                                            'api_key': os.environ.get('OPENAI_API_KEY')
                                        })

# Create keyword recommendation model
recommendation_model = create_model(name='recommendation_model',
                                    engine='openai',
                                    predict='recommendation',
                                    options={
                                            'prompt_template': "Based on the comments from YouTube videos, strictly tell me the topic names that a YouTuber can consider to grow their channel. Example: 'Python' if peoples are talking about python. comments:{{comments}}",
                                            'api_key': os.environ.get('OPENAI_API_KEY')
                                    })

# response dictionary
response = {}


def get_summarization(data):
    """makes a summary of the comments

    Args:
        data (dict): comments
        example: {'comments': 'comment1 comment2 comment3'}
    """
    # predict the summary
    summarizer_result = text_summarization_model.predict(
        data=data)
    # store the summary in response dictionary
    response["comment_summary"] = str(summarizer_result['comment_summary'][0])


def get_recommendation(data):
    """makes a summary of the comments

    Args:
        data (dict): comments
        example: {'comments': 'comment1 comment2 comment3'}
    """
    # predict the recommendation
    recommendation_result = recommendation_model.predict(
        data=data)
    # store the recommendation in response dictionary
    response["recommendation"] = str(
        recommendation_result['recommendation'][0])


@app.route('/api/youtube', methods=['GET'])
def get_youtube_insights():

    # Get the youtube video id from the request string
    youtube_video_id = request.args.get('youtube_video_id')
    # Get the max comments limit from the request string
    max_comments_limit = request.args.get('limit', 10)
    # Get the comment_summary switch from the request string
    comment_summary = request.args.get('comment_summary', 'false')
    # Get the recommendation switch from the request string
    recommendation = request.args.get('recommendation', 'false')

    # Predict sentiments
    sentiment_result = server.query(f'''SELECT input.comment, output.sentiment
                                    FROM mindsdb_youtube.get_comments AS input
                                    JOIN youtube_insights.sentiment_classifier_model AS output
                                    WHERE input.youtube_video_id = \'{youtube_video_id}\'
                                    LIMIT {max_comments_limit};''').fetch()
    # store the sentiments in response dictionary
    sentiment_counts = sentiment_result['sentiment'].value_counts()
    response["sentiments"] = {
        "positive": int(sentiment_counts.get('positive', 0)),
        "neutral": int(sentiment_counts.get('neutral', 0)),
        "negative": int(sentiment_counts.get('negative', 0))
    }

    # gather all comment
    merged_comments = ' '.join(sentiment_result['comment'].tolist())

    if comment_summary == 'true':

        # Predict summary
        t1 = threading.Thread(target=get_summarization, args=(
            {'comments': merged_comments},))
        t1.start()

    if recommendation == 'true':

        # Predict recommendations
        t2 = threading.Thread(target=get_recommendation,
                              args=({'comments': merged_comments},))
        t2.start()

    # wait for the threads to finish
    t1.join() if comment_summary == 'true' else None
    t2.join() if recommendation == 'true' else None

    return response


if __name__ == '__main__':
    app.run(debug=True)
