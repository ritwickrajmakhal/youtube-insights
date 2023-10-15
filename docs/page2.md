### Step 7: Create a MindsDB model

- Now that we have a mindsdb project and a mindsdb data source, we can create a mindsdb model. To create a mindsdb model we have to use the `create` method. You can read more about the `create` method [here](https://docs.mindsdb.com/sdk_python/create_model).

  ```py
  def create_model(name: str, engine: str, predict: str, options: dict):
     from time import sleep
     # check model is exist or not
     try:
        # Create the model if it doesn't exist
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
        # Get the model if it already exists
        print(f"Model {name} already exists")
        return project.models.get(name)
  ```

  In this code snippet we are checking if the model exists and if it doesn't exist we are creating a new model. If the model exists we are getting the model. We are using the `create` method to create the model. We are using the `name` parameter to set the name of the model. We are using the `engine` parameter to set the engine of the model. We are using the `predict` parameter to set the predict column of the model. We are using the `options` parameter to set the options of the model. `options` are different for different engines.

- **Sentiment Classifier Model Creation**:

  We will use our previously created custom method `create_model` to create a model.

  ```py
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
  ```

  In this code snippet we are creating a model called `sentiment_classifier_model` using the `create_model` function we created in the previous step. We are using the `huggingface` engine to create the model. We are using the `cardiffnlp/twitter-roberta-base-sentiment` model to train the model. We are using the `comment` column as the input column and the `sentiment` column as the target column. We are using the `negative`, `neutral`, and `positive` labels for the target column. You can read more about the `huggingface` engine [here](https://docs.mindsdb.com/integrations/ai-engines/huggingface).

  Note: `options` are different for different engines.

- **Text Summarization Model Creation**:

  ```py
  # Create text summarization model
  text_summarization_model = create_model(name='text_summarization_model',
                                         engine='openai',
                                         predict='comment_summary',
                                         options={
                                            'prompt_template': "provide an informative summary of the comments comments:{{comments}} using full sentences",
                                            'api_key': os.environ.get('OPENAI_API_KEY')
                                         })
  ```

  In this code snippet we are creating a model called `text_summarization_model` using the `create_model` function we created in the previous step. We are using the `openai` engine to create the model. We are using the `comment_summary` column as the target column. We are using the `OPENAI_API_KEY` environment variable as the `api_key` connection argument. We are using the `prompt_template` parameter to set the prompt template of the model. You can read more about the `openai` engine [here](https://docs.mindsdb.com/integrations/ai-engines/openai).

### Step 8: Predict Sentiment of YouTube Comments

1. **API Endpoint Definition**:

   ```py
   app = Flask(__name__)
   @app.route('/api/youtube', methods=['GET'])
   def get_youtube_insights():
   ```

   This is the function that will be executed when the route is accessed.

2. **Request Parameters**:

   ```py
   # Get request parameters from the URL
   youtube_video_id = request.args.get('youtube_video_id')
   max_comments_limit = request.args.get('limit', 10)
   ```

   These lines extract query parameters from the GET request. 'youtube_video_id' is a required parameter, and 'limit' is an optional parameter with a default value of 10.

3. **Response Dictionary**:

   ```py
   # Create response dictionary
   response = {}
   ```

   An empty dictionary called 'response' is created to store the API response data.

4. **Sentiment Prediction**:

   ```py
   # predict sentiment for comments of the video
   sentiment_result = server.query(f'''SELECT input.comment, output.sentiment
                                    FROM mindsdb_youtube.get_comments AS input
                                    JOIN youtube_insights.sentiment_classifier_model AS output
                                    WHERE input.youtube_video_id = \"{youtube_video_id}\"
                                    LIMIT {max_comments_limit}''').fetch()
   ```

   In this code we are using the `query` method to query the model we created in the previous step. The query is selecting the `comment` and `sentiment` columns from the `get_comments` table and joining it with the `sentiment_classifier_model` model. The `youtube_video_id` is the video id of the video we want to get the comments for. The `max_comments_limit` is the maximum number of comments we want to get. The `fetch` method is used to execute the query and get the results.

5. **Sentiment Counts**:

   ```py
   sentiment_counts = sentiment_result['sentiment'].value_counts()
   ```

   This code counts the number of positive, neutral, and negative sentiments in the result.

6. **Response Building**:

   ```py
   response["sentiments"] = {
        "positive": int(sentiment_counts.get('positive', 0)),
        "neutral": int(sentiment_counts.get('neutral', 0)),
        "negative": int(sentiment_counts.get('negative', 0))
    }
   ```

   This code constructs the API response by creating a dictionary within the 'response' dictionary. It includes the counts of positive, neutral, and negative sentiments as integers.

[<<Previous](./page1.md) [Next>>](./page3.md)
