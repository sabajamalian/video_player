const fs = require('fs');
const path = require('path');

const CACHE_DIR = 'cache';
const STATIC_DIR = 'public';

// Ensure directories exist
if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR);
}
if (!fs.existsSync(STATIC_DIR)) {
    fs.mkdirSync(STATIC_DIR);
}
if (!fs.existsSync(path.join(STATIC_DIR, 'videos'))) {
    fs.mkdirSync(path.join(STATIC_DIR, 'videos'));
}

// Get list of videos
const videos = fs.readdirSync(CACHE_DIR)
    .filter(filename => filename.endsWith('.mp4') || filename.endsWith('.webm') || filename.endsWith('.mkv'))
    .map(filename => {
        const name = path.parse(filename).name;
        return {
            name: name,
            display_name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            type: path.extname(filename).slice(1)
        };
    });

// Generate videos.json
fs.writeFileSync(
    path.join(STATIC_DIR, 'videos.json'),
    JSON.stringify(videos, null, 2)
);

// Copy videos to static directory
videos.forEach(video => {
    const sourcePath = path.join(CACHE_DIR, `${video.name}.${video.type}`);
    const destPath = path.join(STATIC_DIR, 'videos', `${video.name}.${video.type}`);
    fs.copyFileSync(sourcePath, destPath);
});

// Copy static HTML files
fs.copyFileSync('index.html', path.join(STATIC_DIR, 'index.html'));
fs.copyFileSync('video.html', path.join(STATIC_DIR, 'video.html'));

// Create video directories and copy video.html to each
videos.forEach(video => {
    const videoDir = path.join(STATIC_DIR, 'video', video.name);
    if (!fs.existsSync(videoDir)) {
        fs.mkdirSync(videoDir, { recursive: true });
    }
    fs.copyFileSync('video.html', path.join(videoDir, 'index.html'));
});

console.log('Static site built successfully!'); 