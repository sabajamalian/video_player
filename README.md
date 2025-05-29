# Video Player Web Application

A simple web application that pre-downloads videos from Google Drive and serves them locally with a lightweight video player interface.

## Setup

1. Create a `videos.json` file in the project root with your video metadata:
   ```json
   {
       "videos": [
           {
               "name": "unique-video-name",
               "display_name": "Video Display Name",
               "url": "https://drive.google.com/file/d/YOUR_FILE_ID/view",
               "type": "mp4"
           }
       ]
   }
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Development

Run the Flask application:
```bash
python app.py
```

The application will:
1. Create a `cache` directory for storing downloaded videos
2. Start downloading all videos in the background
3. Serve the videos locally using a lightweight HTML5 video player
4. Be available at `http://localhost:5000`

## Deployment to Netlify

1. Push your code to a Git repository
2. Connect your repository to Netlify
3. Configure the build settings:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.`
   - Python version: 3.9

## Features

- Pre-downloads all videos during startup
- Stores videos in a cache directory for faster access
- Serves videos locally for better performance
- Clean, responsive interface
- URL-friendly video names
- Minimal dependencies
- Ready for Netlify deployment

## Adding Videos

To add a new video:

1. Get the Google Drive URL for your video
2. Add a new entry to `videos.json` with:
   - `name`: A unique identifier for the URL (e.g., "my-video-1")
   - `display_name`: The name shown to users
   - `url`: The Google Drive URL
   - `type`: The video format (e.g., "mp4")

The video will be automatically downloaded when the application starts. You can monitor the download progress in the console output.
