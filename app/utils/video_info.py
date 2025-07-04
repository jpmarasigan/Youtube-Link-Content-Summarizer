from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from datetime import datetime
from .json_handler import *
from nltk import sent_tokenize
import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Parse and get the video ID
def get_video_id(url):
    """Extract video ID from YouTube URL using regex"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:v\/|vi\/|vi=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return 'Invalid URL'


# Preprocess string from transcript
def clean_text(text):
    text = re.sub(r'\[\d+:\d+:\d+\]', '', text)

    # Remove action-text
    text = re.sub(r'\[[^\]]*\]', '', text)

    # Remove [ __ ]
    text = re.sub(r'\[\s*__\s*\]', '', text)

    # Split into sentences
    sentences = sent_tokenize(text)

    # Form into paragraphs
    paragraphs = []
    for i in range(0, len(sentences), 5):  # Change 5 to the number of sentences you want in each paragraph
        paragraph = ' '.join(sentences[i:i+5])
        paragraphs.append(paragraph)

    # Join paragraphs with newline characters
    text = '\n'.join(paragraphs)

    return text


# Get transcript only from dict object
def get_transcript(video_id):
    try:
        # Try to get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print(f"TRANSCRIPT: {transcript}")
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video")
        return None
    except NoTranscriptFound:
        print("No transcript found, trying other languages...")
        try:
            # Try any available language
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                try:
                    return transcript.fetch()
                except:
                    continue
            return None
        except:
            return None
    except VideoUnavailable:
        print("Video is unavailable")
        return None
    except Exception as e:
        # This catches the XML parsing error
        print(f"Error getting transcript: {e}")
        return None
    

# Function to filter out noise from the transcript text
def process_transcript(text):
    cleaned_text = re.sub(r'\[.*?\]|\(.*?\)', '', text)

    # Insert basic punctuation for sentence segmentation
    text = re.sub(r'(?<!\w)([a-zA-Z]+)(?=\s+[A-Z])', r'\1.', cleaned_text)
    
    # Process text with SpaCy
    doc = nlp(text)
    
    # Reconstruct text with proper sentences
    formatted_text = ' '.join([sent.text.capitalize() for sent in doc.sents])
    
    # Additional clean-up: handle double punctuation and spaces
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    formatted_text = re.sub(r'\.\.', '.', formatted_text)

    return ' '.join(cleaned_text.split())


# Get video info
def get_video_info(video_id):
    # Load api key
    api_key = get_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id
    )
    response = request.execute()

    # Get youtube content details
    id = response['items'][0]['id']

    title = response['items'][0]['snippet']['title']

    publish_date = response['items'][0]['snippet']['publishedAt'][:10]
    publish_date = datetime.strptime(publish_date, "%Y-%m-%d").date()

    thumbnail = response['items'][0]['snippet']['thumbnails']['medium']['url']

    channel = response['items'][0]['snippet']['channelTitle']
    
    views = int(response['items'][0]['statistics']['viewCount'])
    views = f"{views:,}"        # make it comma separated per thousands

    # make_yt_info_json(response, id)
    
    # print_video_info(title, publish_date)

    return title, publish_date, thumbnail, channel, views


# Logging data
def print_video_info(title, publish_date):
    print(f"Title: {title}")
    print(f"Published Date: {publish_date}")