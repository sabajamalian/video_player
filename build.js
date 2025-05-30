const fs = require('fs');
const path = require('path');

const CACHE_DIR = 'cache';
const PUBLIC_DIR = 'public';
const VIDEOS_DIR = path.join(PUBLIC_DIR, 'videos');

// Create videos directory if it doesn't exist
if (!fs.existsSync(VIDEOS_DIR)) {
    fs.mkdirSync(VIDEOS_DIR, { recursive: true });
}

// Get list of videos from cache
const videos = [];
for (const filename of fs.readdirSync(CACHE_DIR)) {
    if (filename.endsWith('.mp4')) {
        const name = path.parse(filename).name;
        videos.push({
            name: name,
            display_name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            type: 'mp4'
        });
    }
}

// Write videos.json
fs.writeFileSync(
    path.join(PUBLIC_DIR, 'videos.json'),
    JSON.stringify(videos, null, 2)
);

// Copy videos to public directory
for (const video of videos) {
    const sourcePath = path.join(CACHE_DIR, `${video.name}.${video.type}`);
    const destPath = path.join(VIDEOS_DIR, `${video.name}.${video.type}`);
    fs.copyFileSync(sourcePath, destPath);
    console.log(`Copied ${video.name}.${video.type} to public directory`);
}

console.log('Build completed successfully!'); 