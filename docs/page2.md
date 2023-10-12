### Step 7: Create a MindsDB model
- Now that we have a mindsdb project and a mindsdb data source, we can create a mindsdb model. To create a mindsdb model we have to use the `create` method. You can read more about the `create` method [here](https://docs.mindsdb.com/sdk_python/create_model).

    ```py
    def create_model(name:str, predict:str, prompt_template:str):
        from time import sleep
        # check model is exist or not
        try:
            # Create the model if not exist
            model = project.models.create(
                name=name, # model name
                engine='openai', # model engine
                predict=predict, # model predict column
                prompt_template=prompt_template, # model prompt template
                api_key=os.environ.get('OPENAI_API_KEY') # openai api key
            )
            # Wait for the model to be ready
            while model.get_status() != 'complete':
                sleep(1)
            return model
        except:
            # Get the model if exist
            return project.models.get(name)
    ```

    In this code snippet we are checking if the model exists and if it doesn't exist we are creating a new model.

### Step 8: YouTube comment sentiment analysis

1. **API Endpoint Definition**:
   ```py
   @app.route('/api/youtube', methods=['GET'])
   ```
   This code defines a route in a Flask application for the HTTP GET request to the URL path '/api/youtube'.

2. **Function Definition**:
   ```py
   def get_youtube_insights():
   ```
   This is the function that will be executed when the route is accessed.

3. **Request Parameters**:
   ```py
   youtube_video_id = request.args.get('youtube_video_id')
   max_comments_limit = request.args.get('limit', 10)
   ```
   These lines extract query parameters from the GET request. 'youtube_video_id' is a required parameter, and 'limit' is an optional parameter with a default value of 10.

4. **Response Dictionary**:
   ```py
   response = {}
   ```
   An empty dictionary called 'response' is created to store the API response data.

5. **Model Creation**:
   ```py
   sentiment_classifier_model = create_model(
       name='sentiment_classifier_model',
       predict='sentiment',
       prompt_template="describe the sentiment of the comment strictly as 'positive', 'neutral', or 'negative'.'I love the product':positive, 'It is a scam':negative '{{comment}}.':"
   )
   ```
   In this code we are creating a model called `sentiment_classifier_model` using the `create_model` function we created in the previous step. The model is using the `openai` engine and the `sentiment` column is the column we want to predict. The `prompt_template` is the template that will be used to train the model.

6. **Sentiment Prediction**:
   ```py
   sentiment_result = server.query(f'''SELECT input.comment, output.sentiment
                                    FROM mindsdb_youtube.get_comments AS input
                                    JOIN youtube_insights.sentiment_classifier_model AS output
                                    WHERE input.youtube_video_id = \"{youtube_video_id}\"
                                    LIMIT {max_comments_limit}''').fetch()
   ```
   In this code we are using the `query` method to query the model we created in the previous step. The query is selecting the `comment` and `sentiment` columns from the `get_comments` table and joining it with the `sentiment_classifier_model` model. The `youtube_video_id` is the video id of the video we want to get the comments for. The `max_comments_limit` is the maximum number of comments we want to get. The `fetch` method is used to execute the query and get the results.

7. **Sentiment Counts**:
   ```py
   sentiment_counts = sentiment_result['sentiment'].value_counts()
   ```
   This line appears to count the occurrences of each sentiment (positive, neutral, negative) in the results and stores them in 'sentiment_counts'. Know more about the `value_counts` method [here](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html).

8. **Response Building**:
   ```py
   response["sentiments"] = {
       "positive": int(sentiment_counts.get('positive', 0)),
       "neutral": int(sentiment_counts.get('neutral', 0)),
       "negative": int(sentiment_counts.get('negative', 0))
   }
   ```
   This code constructs the API response by creating a dictionary within the 'response' dictionary. It includes the counts of positive, neutral, and negative sentiments as integers.
9. **Response Return**:
   ```py
   return jsonify(response)
   ```
   This line returns the API response in JSON format.

Note: Now you can run the flask application using the following command:
```sh
python app.py
```
You can access the API endpoint at http://localhost:5000/api/youtube?youtube_video_id=raWFGQ20OfA

You will get the following response:
```json
{
  "sentiments": {
    "positive": 2,
    "neutral": 0,
    "negative": 0
  }
}
```

## Conclusion:
Similarly, you can create other models and use them to get insights from YouTube comments. You can also use the same approach to get insights from other data sources. You can find the complete code for this project [here](../app.py). Happy coding!

[<<Previous](./page1.md)
