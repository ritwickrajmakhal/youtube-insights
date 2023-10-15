# YouTube Insights using MindsDB SDK

YouTube Insights is a Flask web application that uses MindsDB SDK to analyze sentiment and summarize comments for a given YouTube video. This project helps you gain insights into the sentiments expressed in comments on YouTube videos and provides a summarized overview of the comments. It also provides a list of potential topic names that a YouTuber can consider to grow their channel.

## Key Features

- Analyze sentiment of comments on a YouTube video.
- Spam analysis of comments on a YouTube video.
- Generate a summary of the comments on a YouTube video.
- Generate a list of potential topic names that a YouTuber can consider to grow their channel.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before getting started, make sure you have the following prerequisites installed and set up:

- [Python 3.x](https://www.python.org/downloads/)
- [YouTube API Key](https://developers.google.com/youtube/registering_an_application)
- [OpenAI API Key](https://openai.com/)
- [MindsDB Cloud Account](https://mindsdb.com/)
- Internet connection

## Getting Started

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ritwickrajmakhal/youtube-insights.git
   ```

2. Change into the project directory:

   ```bash
   cd youtube-insights
   ```

3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the project directory and set the following environment variables:

   ```
   MINDSDB_EMAIL=your-mindsdb-email
   MINDSDB_PASSWORD=your-mindsdb-password
   YOUTUBE_API_KEY=your-youtube-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

2. Make sure you have an internet connection to connect to the MindsDB Cloud server.

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. The application will start and be accessible at `http://localhost:5000`. You can make requests to the `/api/youtube` endpoint to analyze sentiment and get comment summaries for a specific YouTube video.

   Note : It may take some time to login to MindsDB Cloud and load the models.

## API Endpoints

- `GET /api/youtube`: Analyze sentiment and get comment summaries for a specific YouTube video.

  - Parameters:

    - `youtube_video_id`: The YouTube video ID for which you want to analyze comments.
    - `limit`: The maximum number of comments to analyze. Defaults to 10.
    - `sentiment`: Whether to generate a sentiment analysis of the comments. Defaults to `false`.
    - `spam`: Whether to generate a spam analysis of the comments. Defaults to `false`.
    - `comment_summary`: Whether to generate a summary of the comments. Defaults to `false`.
    - `recommendation`: Whether to generate a list of potential topic names that a YouTuber can consider to grow their channel. Defaults to `false`.

  - Example request:

    ```
    http://127.0.0.1:5000/api/youtube?youtube_video_id=KIvfM4g4aG4&limit=5&comment_summary=true&recommendation=true&sentiment=true&spam=true
    ```

  - Example response:

  ```json
  {
    "comment_summary": "The comments in the conversation revolve around the topic of mystery videos. One person asks what other mystery videos the others would like to see. Another comment provides a link to join a website called \"academy.dhruvrathee.com\" and offers a 40% discount code for the first 400 people. However, it is mentioned that the course is in English. Another comment expresses amazement at a video seen on YouTube where the search and rescue team did not have a piece of",
    "recommendation": "Based on the comments, some potential topic names that a YouTuber can consider to grow their channel could be:\n\n1. Mystery Videos\n2. Search and Rescue Techniques\n3. Failed Search Operations\n4. Reflecting Sunlight for Search and Rescue\n5. Language Learning (English)\n6. Online Courses and Discounts\n7. Dhruv Rathee Academy\n8. YouTube Channel Growth Strategies\n9. Effective Use of Glass in Search Operations\n10. Critiques of Search and Rescue",
    "sentiments": {
      "negative": 2,
      "neutral": 2,
      "positive": 1
    },
    "spams": 1
  }
  ```

  Note: Again, as models are rate limited, it may take some time to get the response (Approx: 2min/request).

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them.
4. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request on the original repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
