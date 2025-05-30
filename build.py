import os
import shutil
from jinja2 import Environment, FileSystemLoader

CACHE_DIR = 'cache'
STATIC_DIR = 'static_site'

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

def build_static_site():
    # Create static site directory
    if os.path.exists(STATIC_DIR):
        shutil.rmtree(STATIC_DIR)
    os.makedirs(STATIC_DIR)
    
    # Create videos directory in static site
    os.makedirs(os.path.join(STATIC_DIR, 'videos'))
    
    # Copy all videos to static site
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(('.mp4', '.webm', '.mkv')):
            shutil.copy2(
                os.path.join(CACHE_DIR, filename),
                os.path.join(STATIC_DIR, 'videos', filename)
            )
    
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Get video list
    videos = get_videos()
    
    # Generate index.html
    template = env.get_template('index.html')
    with open(os.path.join(STATIC_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(template.render(videos=videos))
    
    # Generate individual video pages
    video_template = env.get_template('video.html')
    for video in videos:
        video_dir = os.path.join(STATIC_DIR, 'video', video['name'])
        os.makedirs(video_dir, exist_ok=True)
        with open(os.path.join(video_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(video_template.render(video=video))

if __name__ == '__main__':
    build_static_site()
    print("Static site built successfully!") 