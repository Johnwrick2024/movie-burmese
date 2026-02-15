from flask import Flask, request, jsonify 
from youtube_transcript_api import YouTubeTranscriptApi 
from deep_translator import GoogleTranslator 
import re 

app = Flask(__name__) 

def extract_video_id(url): 
    match = re.search(r"(?:v=|\/shorts\/)([a-zA-Z0-9_-]+)", url) 
    if match: 
        return match.group(1) 
    return None 
  
@app.route("/") 
def home(): 
    return "API running" 
  
@app.route("/generate", methods=["POST"]) 
def generate(): 
    data = request.get_json() 
    url = data["url"] 
    video_id = extract_video_id(url) 
    transcript = YouTubeTranscriptApi.get_transcript(video_id) 
    text = "" 
    for t in transcript: text += t["text"] + " " 
    burmese = GoogleTranslator(source="auto", target="my").translate(text) 
    return jsonify({ "original": text, "burmese": burmese 
    }) 
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=10000)
