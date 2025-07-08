# Youtube Link Content Summarizer

## Overview
This project is a web application built with Flask that summarizes the content of YouTube videos. It takes a YouTube video link as input and provides a concise summary of the video's content. This can be helpful for users who want to quickly understand the key points of a video without watching the entire duration.

## Features
* Accepts youtube video link as input.
* Utilizes Natural Language Processing (NLP) techniques to generate summaries.
* Provides a user-friendly web interface for input and summary display.
* Responsive design for seamless usage on different devices.

## Technologies Used
* HTML
* Python
* Flask
* NLTK (Natural Language Toolkit)
* Youtube API

## Installation
1. Clone the repository
    ```sh
    git clone https://github.com/jpmarasigan/Youtube-Link-Content-Summarizer.git
    ```
    
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the spaCy model:
    ```sh
    python -m spacy download en_core_web_sm
    ```

4. Run the application:
    ```sh
    python run.py
    ```

