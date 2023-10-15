# YouTube Insights using MindsDB SDK - Tutorial

## Introduction

YouTube Insights is a Flask web application that uses MindsDB SDK to analyze sentiment and summarize comments for a given YouTube video. This project helps you gain insights into the sentiments expressed in comments on YouTube videos and provides a summarized overview of the comments.

Note: We will make a simpler version of YouTube Insights project in this tutorial. The full project can be found [here](https://github.com/ritwickrajmakhal/youtube-insights).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - Step 1: [Create a virtual environment and activate it](#step-1-create-a-virtual-environment-and-activate-it)
  - Step 2: [Creating a basic Flask app](#step-2-creating-a-basic-flask-app)
  - Step 3: [Install python-dotenv and load environment variables](#step-3-install-python-dotenv-and-load-environment-variables)
  - Step 4: [Install the MindsDB Python SDK and import it](./page1.md/#step-4-install-the-mindsdb-python-sdk-and-import-it)
  - Step 5: [Create a MindsDB project](./page1.md/#step-5-create-a-mindsdb-project)
  - Step 6: [Add a MindsDB Data source (Importing YouTube's Comments)](./page1.md/#step-6-add-a-mindsdb-data-source)
  - Step 7: [Create a MindsDB model](./page2.md/#step-7-create-a-mindsdb-model)
  - Step 8: [YouTube comment sentiment analysis](./page2.md/#step-8-youtube-comment-sentiment-analysis)
  - Step 9: [YouTube comment summarization](./page2.md/#step-9-youtube-comment-summarization)
  - Step 10: [Making request to our Flask app](./page3.md/#step-10-making-request-to-our-flask-app)
- Conclusion: [What's next?](./page3.md/#conclusion-whats-next)
## Prerequisites

Before getting started, make sure you have the following prerequisites installed and set up:

- [Python 3.x](https://www.python.org/downloads/)
- [YouTube API Key](https://developers.google.com/youtube/registering_an_application)
- [MindsDB Cloud Account](https://mindsdb.com/)
- [Visual Studio Code](https://code.visualstudio.com/) or any other code editor
- Internet connection

## Getting Started

### Step 1: Create a virtual environment and activate it

- First create a fresh folder called `youtube-insights` for your project and navigate to it in your terminal. Then create a virtual environment and activate it:

  ```ps
  mkdir youtube-insights
  cd youtube-insights
  python -m venv venv
  source venv/bin/activate  # On Windows, use venv\Scripts\activate
  ```

- After activating your virtual environment, you should see your terminal look something like this:

  ```ps
  PS D:\youtube-insights> python -m venv venv
  PS D:\youtube-insights> venv\Scripts\activate
  (venv) PS D:\youtube-insights>
  ```

### Step 2: Creating a basic Flask app

- Now that you have your virtual environment set up, you can install Flask and create a basic Flask app. First, install Flask:

  ```ps
  pip install Flask
  ```

- Then create a file called `app.py`.

  Folder structure should look like this:

  ```ps
  youtube-insights
                ├── app.py
                └── venv
  ```

- Add the following code to `app.py`:

  ```py
  from flask import Flask
  app = Flask(__name__)

  if __name__ == '__main__':
      app.run(debug=True)
  ```

  Note: If you don't know what Flask is, you can read more about it [here](https://flask.palletsprojects.com/en/2.0.x/).

### Step 3: Install python-dotenv and load environment variables

- Go to your terminal and install `python-dotenv`:

  ```ps
  pip install python-dotenv
  ```

- Now create a file called `.env` and add the following code to it:

  ```
  MINDSDB_EMAIL=your-mindsdb-email
  MINDSDB_PASSWORD=your-mindsdb-password
  YOUTUBE_API_KEY=your-youtube-api-key
  OPENAI_API_KEY=your-openai-api-key
  ```

- Load your environment variables in `app.py`:

  ```py
  from flask import Flask, jsonify, request
  from dotenv import load_dotenv
  import os

  # Load the environment variables from the .env file
  load_dotenv()

  app = Flask(__name__)

  if __name__ == '__main__':
      app.run(debug=True)
  ```

- Now you can run your Flask app by running the following command in your terminal:

  ```ps
  python app.py
  ```

  You should see something like this in your terminal:

  ```ps
  (venv) PS D:\youtube-insights> python app.py
  * Serving Flask app 'app'
  * Debug mode: on
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  * Running on http://127.0.0.1:5000
  Press CTRL+C to quit
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: 635-029-923
  ```

  Note: You can stop your Flask app by pressing `CTRL+C` in your terminal.

[Next>>](./page1.md)