from flask import Flask, render_template, redirect, url_for, send_from_directory
import json
import os
import gdown
import requests
from urllib.parse import urlparse, parse_qs
import threading
import time

app = Flask(__name__)

CACHE_DIR = 'cache'

def get_file_id_from_url(url):
    """Extract file ID from Google Drive URL."""
    parsed_url = urlparse(url)
    if 'drive.google.com' in parsed_url.netloc:
        if '/file/d/' in url:
            return url.split('/file/d/')[1].split('/')[0]
        elif 'id=' in url:
            return parse_qs(parsed_url.query)['id'][0]
    return None

def download_video(video):
    """Download video from Google Drive if not already downloaded."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    video_path = os.path.join(CACHE_DIR, f"{video['name']}.{video['type']}")
    
    if not os.path.exists(video_path):
        file_id = get_file_id_from_url(video['url'])
        if file_id:
            print(f"Downloading {video['display_name']}...")
            output = gdown.download(
                f"https://drive.google.com/uc?id={file_id}",
                video_path,
                quiet=False
            )
            if not output:
                raise Exception(f"Failed to download video: {video['name']}")
            print(f"Downloaded {video['display_name']}")
        else:
            raise Exception(f"Invalid Google Drive URL: {video['url']}")
    
    return video_path

def preload_videos():
    """Preload all videos in the background."""
    try:
        with open('videos.json', 'r') as f:
            videos = json.load(f)['videos']
            
        def download_all():
            for video in videos:
                try:
                    download_video(video)
                except Exception as e:
                    print(f"Error downloading video {video['name']}: {str(e)}")
        
        # Start download in a separate thread
        thread = threading.Thread(target=download_all)
        thread.daemon = True
        thread.start()
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading videos.json: {str(e)}")

def load_videos():
    """Load video metadata."""
    try:
        with open('videos.json', 'r') as f:
            return json.load(f)['videos']
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.route('/')
def index():
    videos = load_videos()
    return render_template('index.html', videos=videos)

@app.route('/video/<name>')
def video(name):
    videos = load_videos()
    video = next((v for v in videos if v['name'] == name), None)
    if video:
        return render_template('video.html', video=video)
    return redirect(url_for('index'))

@app.route('/videos/<path:filename>')
def serve_video(filename):
    """Serve video files from the cache directory."""
    return send_from_directory(CACHE_DIR, filename)

if __name__ == '__main__':
    # Start preloading videos
    preload_videos()
    app.run(debug=True) 