# YouTube Insights with MindsDB and YouTube API

YouTube Insights is a Flask web application that uses MindsDB and the YouTube API to analyze sentiment and summarize comments for a given YouTube video. This project helps you gain insights into the sentiments expressed in comments on YouTube videos and provides a summarized overview of the comments.

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

## API Endpoints

- `GET /api/youtube`: Analyze sentiment and get comment summaries for a specific YouTube video.

  - Parameters:

    - `youtube_video_id`: The YouTube video ID for which you want to analyze comments.
    - `limit`: The maximum number of comments to analyze. Defaults to 10.

  - Example request:

    ```
    GET http://localhost:5000/api/youtube?youtube_video_id=your-video-id?limit=10
    ```

  - Example response:
    ```json
    {
      "keywords": "Python, React, OpenSource...",
      "recommendation": "recommendations...",
      "sentiments": {
        "negative": 0,
        "neutral": 3,
        "positive": 0
      },
      "summary": "Comment summary..."
    }
    ```

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