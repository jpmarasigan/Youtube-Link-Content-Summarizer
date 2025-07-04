import os
from dotenv import load_dotenv

# # Create json format of youtube link video info
# def make_yt_info_json(response, video_id):
#     filename = f'json_yt_info/{video_id}.json'
#     with open(filename, 'w') as f:
#         json.dump(response, f, indent=4)

#     with open(filename, 'r') as f:
#         file_content = json.load(f)

#     if file_content == response:
#         print(f"Checksum passed {filename}")
#     else:
#         print(f"Checksum failed {filename}")

load_dotenv()

# Retrieve youtube api key
def get_api_key():
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        raise ValueError('Youtube API key not found in environment variables')
    return api_key