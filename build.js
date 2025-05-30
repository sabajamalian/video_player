const fs = require('fs');
const path = require('path');

const CACHE_DIR = 'cache';
const PUBLIC_DIR = 'public';
const VIDEOS_DIR = path.join(PUBLIC_DIR, 'videos');

// Create public and videos directories if they don't exist
if (!fs.existsSync(PUBLIC_DIR)) {
    fs.mkdirSync(PUBLIC_DIR, { recursive: true });
}
if (!fs.existsSync(VIDEOS_DIR)) {
    fs.mkdirSync(VIDEOS_DIR, { recursive: true });
}

// Check if cache directory exists
if (!fs.existsSync(CACHE_DIR)) {
    console.log('Cache directory not found. Creating empty videos.json...');
    // Create empty videos.json
    fs.writeFileSync(
        path.join(PUBLIC_DIR, 'videos.json'),
        JSON.stringify([], null, 2)
    );
    console.log('Build completed successfully!');
    process.exit(0);
}

// Get list of videos from cache
const videos = [];
try {
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
} catch (error) {
    console.error('Error during build:', error);
    process.exit(1);
} 