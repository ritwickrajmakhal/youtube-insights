import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mindsdb_sdk
from flask_cors import CORS

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
    raise Exception("Check your internet connection or mindsdb credentials")

# Create project if not exists
try:
    project = server.get_project('youtube_insights')
except:
    project = server.create_project('youtube_insights')

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

# Create ML Engine if not exists
# try:
#     server.ml_engines.create(name='hf_inference_api', handler='huggingface', connection_data={
#                              'api_key': os.environ.get('HF_API_KEY')})
# except:
#     pass


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
        while model.get_status() != 'complete':
            sleep(1)
        return model
    except:
        # Get the model
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

# Summarize the comments or predict recommendations
text_summarization_model = create_model(name='text_summarization_model',
                                        engine='huggingface',
                                        predict='comment_summary',
                                        options={
                                            'task': 'summarization',
                                            'model_name': 'sshleifer/distilbart-cnn-12-6',
                                            'input_column': "comment_long",
                                            'min_output_length': 100,
                                            'max_output_length': 1000
                                        })

# # Predict recommendations
# recommendation_model = create_model(name='recommendation_model', predict='recommendation',
#                                     prompt_template="Please analyze the comments below and generate a compelling recommendation for the video. Comments:{{comments}}")

# # Keyword Extraction
# keyword_extraction_model = create_model(name='keyword_extraction_model', predict='keywords',
#                                         prompt_template="Please extract the keywords from the comments below. Comments:{{comments}}")


@app.route('/api/youtube', methods=['GET'])
def get_youtube_insights():

    youtube_video_id = request.args.get('youtube_video_id')
    max_comments_limit = request.args.get('limit', 10)
    # Create the JSON response with initial sentiment counts
    response = {}

    # Predict sentiments
    sentiment_result = server.query(f'''SELECT input.comment, output.sentiment
                                    FROM mindsdb_youtube.get_comments AS input
                                    JOIN youtube_insights.sentiment_classifier_model AS output
                                    WHERE input.youtube_video_id = \'{youtube_video_id}\'
                                    LIMIT {max_comments_limit};''').fetch()

    sentiment_counts = sentiment_result['sentiment'].value_counts()
    response["sentiments"] = {
        "positive": int(sentiment_counts.get('positive', 0)),
        "neutral": int(sentiment_counts.get('neutral', 0)),
        "negative": int(sentiment_counts.get('negative', 0))
    }

    # gather all comment
    merged_comments = ' '.join(sentiment_result['comment'].tolist())

    if request.args.get('comment_summary', 'false') == 'true':

        # Predict summarized comment
        summarizer_result = text_summarization_model.predict(
            {'comment_long': merged_comments})
        response["comment_summary"] = str(
            summarizer_result['comment_summary'][0])

    # if request.args.get('recommendation', 'false') == 'true':

    #     # Predict recommendations
    #     recommendation_result = recommendation_model.predict(
    #         {'comments': merged_comments})
    #     response["recommendation"] = str(
    #         recommendation_result['recommendation'][0])

    # if request.args.get('keywords', 'false') == 'true':

    #     # Predict keywords
    #     keyword_extraction_result = keyword_extraction_model.predict(
    #         {'comments': merged_comments})
    #     response["keywords"] = str(keyword_extraction_result['keywords'][0])

    return response


if __name__ == '__main__':
    app.run(debug=True)
