## Step 9: YouTube comment summarization

Within the same method of the previous step

8. **Summarize Comments**:

   ```py
   # gather all comment
   merged_comments = ' '.join(sentiment_result['comment'].tolist())
   # summarize comments
   summarizer_result = text_summarization_model.predict(data={'comments': merged_comments})
   # store the summary in response dictionary
   response["comment_summary"] = str(summarizer_result['comment_summary'][0])
   ```

   In this code we are using the `predict` method to predict the `comment_summary` column of the `text_summarization_model` model. We are using the `merged_comments` variable as the input data. We are using the `comment_summary` column as the target column. After getting the result we are storing the result in the `comment_summary` key of the `response` dictionary.

9. **Response Return**:
   ```py
   return jsonify(response)
   ```
   This line returns the API response in JSON format.

Note: Now you can run the flask application using the following command:

```sh
python app.py
```

You can access the API endpoint at [http://localhost:5000/api/youtube?youtube_video_id=KIvfM4g4aG4&limit=15](http://localhost:5000/api/youtube?youtube_video_id=KIvfM4g4aG4&limit=15)

You will get the following response:

```json
{
  "comment_summary": "The comments on the video are quite varied. Some viewers express their admiration for Dhruv Rathee's content and find the video to be the best on his channel. Others mention the incredible story and the determination of the individuals involved. There are also comments about the video being realistic and scary, as well as requests for more videos on different topics such as train accidents and flight mysteries. Some viewers mention that they have heard about this incident in Bear Grylls' show \"Man vs Wild\" and",
  "sentiments": {
    "negative": 3,
    "neutral": 26,
    "positive": 21
  }
}
```

## Conclusion:

In this tutorial we have learned how to create a MindsDB project, data source and model. We have also learned how to use the MindsDB SDK to make predictions. We have also learned how to create a Flask application and use the MindsDB SDK to make predictions in the Flask application.

## What's next?

- You can fit this data into any kind of front end application (web/android) through api calls. 
Example:
![youtube-insights-front-end](./assets/img/youtube-insights-front-end.png)

[<<Previous](./page1.md)
