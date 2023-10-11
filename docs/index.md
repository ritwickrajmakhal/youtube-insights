# YouTube Insights with MindsDB and YouTube API - Tutorial

## Introduction

YouTube Insights is a Flask web application that uses MindsDB and the YouTube API to analyze sentiment and summarize comments for a given YouTube video. This project helps you gain insights into the sentiments expressed in comments on YouTube videos and provides a summarized overview of the comments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - Step 1: [Create a virtual environment and activate it](#step-1-create-a-virtual-environment-and-activate-it)
  - Step 2: [Creating a basic Flask app](#step-2-creating-a-basic-flask-app)
  - Step 3: [Install the MindsDB Python SDK](#step-3-install-the-mindsdb-python-sdk)
  - Step 4: [Create a MindsDB project](#step-4-create-a-mindsdb-project)

## Prerequisites

Before getting started, make sure you have the following prerequisites installed and set up:

- [Python 3.x](https://www.python.org/downloads/)
- [YouTube API Key](https://developers.google.com/youtube/registering_an_application)
- [OpenAI API Key](https://openai.com/)
- [MindsDB Cloud Account](https://mindsdb.com/)
- [Visual Studio Code](https://code.visualstudio.com/) with `Thunder Client` extension installed
- Internet connection

## Getting Started

### Step 1: Create a virtual environment and activate it

- First create a fresh folder for your project and navigate to it in your terminal. Then create a virtual environment and activate it:

  ```ps
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

- Now that you have a basic Flask app, you can install `python-dotenv` and load your environment variables. First, create a file called `.env` and add the following code to it:

  ```ps
  MINDSDB_EMAIL=your-mindsdb-email
  MINDSDB_PASSWORD=your-mindsdb-password
  YOUTUBE_API_KEY=your-youtube-api-key
  OPENAI_API_KEY=your-openai-api-key
  ```

- Go to your terminal and install `python-dotenv`:

  ```ps
  pip install python-dotenv
  ```

- Create a file called `.env` and add the following code to it:

  ```ps
  MINDSDB_EMAIL=your-mindsdb-email
  MINDSDB_PASSWORD=your-mindsdb-password
  YOUTUBE_API_KEY=your-youtube-api-key
  OPENAI_API_KEY=your-openai-api-key
  ```

- Load your environment variables in `app.py`:

  ```py
  from flask import Flask
  from dotenv import load_dotenv
  import os

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

### Step 4: Install the MindsDB Python SDK and import it

- Now that you have a basic Flask app, you can install the MindsDB Python SDK. First, install the MindsDB Python SDK:

  ```ps
  pip install mindsdb_sdk
  ```

- Then import the MindsDB SDK in `app.py`:

  ```py
    ...
    import mindsdb_sdk
    ...
  ```

### Step 5: Create a MindsDB project

- To create a mindsdb project in python we have first make a connection to the mindsdb server.

  ```py
      ...
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
      ...
  ```

  In this code snippet we are checking if the environment variables are set and then we are connecting to the mindsdb server using the `connect` method. You can read more about the `connect` method [here](https://docs.mindsdb.com/using-mindsdb/connecting-to-mindsdb).

- Now we are ready to create a mindsdb project. To create a mindsdb project we have to use the `create_project` method. You can read more about the `create_project` method [here](https://docs.mindsdb.com/using-mindsdb/creating-a-project).

  ```py
      ...
      # Create project if not exists
      try:
          project = server.get_project('youtube_insights')
      except:
          project = server.create_project('youtube_insights')
      ...
  ```

  In this code snippet we are checking if the project exists and if it doesn't exist we are creating a new project.

### Step 6: Add a MindsDB Data source

- Now that we have a mindsdb project, we can create a mindsdb data source. To create a mindsdb data source we have to use the `create_database` method. You can read more about the `create_database` method [here](https://docs.mindsdb.com/using-mindsdb/creating-a-data-source).

  ```py
    ...
    # Add data sources if not exists
    try:
        # Check if the environment variables are set
        if os.environ.get('YOUTUBE_API_KEY') is None:
            raise Exception(
                'Please set the YOUTUBE_API_KEY environment variable')
        # Create the database if not exist
        mindsdb_youtube = server.create_database(name='mindsdb_youtube', engine='youtube', connection_args={
            'youtube_api_token': os.environ.get('YOUTUBE_API_KEY')})
    except:
        # Get the database if exist
        mindsdb_youtube = server.get_database('mindsdb_youtube')
    ...
  ```
    In this code snippet we are checking if the data source exists and if it doesn't exist we are creating a new data source.
