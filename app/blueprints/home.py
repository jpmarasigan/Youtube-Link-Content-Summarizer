from flask import Blueprint, render_template, request
from ..utils.transcript import *
from ..utils.summarizer import * 

# Create a blueprint for the home page
home = Blueprint('home', __name__)

@home.route('/', methods=['POST', 'GET'])
def home_page():
    # Log routing
    log_routing(request)

    summary = []        # empty list to store the summary state
    if request.method == 'POST': 
        link = request.form.get('yt-link')
        if link:
            video_id = get_video_id(link)
            transcript = get_transcript(video_id)

            # NLP for summarization
            word_list = token(transcript)
            sent_list = sent_token(transcript)
            filtered_words = remove_stopwords(word_list)
            word_frequency = word_freq(filtered_words)
            word_frequency = max_freq(word_frequency)
            sent_scores = sentence_scores(sent_list, word_frequency)
            summary = get_summary(sent_scores)
        else:
            summary.append('INPUT MUST NOT BE EMPTY')

    return render_template('home.html', summary=summary)


def log_routing(request):
    print("Route: ", request.path)
    print("Method: ", request.method)