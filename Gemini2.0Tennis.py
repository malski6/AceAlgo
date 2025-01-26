import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

import time

def upload_video(video_file_name):
  video_file = client.files.upload(path=video_file_name)

  while video_file.state == "PROCESSING":
      print('Waiting for video to be processed.')
      time.sleep(10)
      video_file = client.files.get(name=video_file.name)

  if video_file.state == "FAILED":
    raise ValueError(video_file.state)
  print(f'Video processing complete: ' + video_file.uri)

  return video_file

tennis_video = upload_video('tennis_serve 2022.mov')

# Set model
model_name = "gemini-2.0-flash-exp" 
# System instructions     
system_instructions = """
    You're a high-level tennis instructor knowing what good tennis techniques look like.
    When given a video and a query, call the relevant function only once with the appropriate timecodes and text for the video
  """
#-------------------------------
# Search within videos; get a caption for each steps
import json
from PIL import Image
from IPython.display import display, Markdown, HTML

prompt = "Can you please desribe in detail where this player can improve on her serve and provide rationale for your recommendation"
video = tennis_video
response = client.models.generate_content(
    model=model_name,
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=video.uri,
                    mime_type=video.mime_type),
                ]),
        prompt,
    ],
    config = types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=0.5
    )
)

print(response.text)

# 
