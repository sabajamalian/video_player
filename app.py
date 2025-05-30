from flask import Flask, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

CACHE_DIR = 'cache'

def get_videos():
    """Get list of videos from cache directory."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    videos = []
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(('.mp4', '.webm', '.mkv')):
            name = os.path.splitext(filename)[0]
            videos.append({
                'name': name,
                'display_name': name.replace('_', ' ').title(),
                'type': filename.split('.')[-1]
            })
    return videos

@app.route('/')
def index():
    videos = get_videos()
    return render_template('index.html', videos=videos)

@app.route('/video/<name>')
def video(name):
    videos = get_videos()
    video = next((v for v in videos if v['name'] == name), None)
    if video:
        return render_template('video.html', video=video)
    return redirect(url_for('index'))

@app.route('/videos/<path:filename>')
def serve_video(filename):
    """Serve video files from the cache directory."""
    return send_from_directory(CACHE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 