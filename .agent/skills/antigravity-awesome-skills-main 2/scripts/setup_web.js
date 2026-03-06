import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..');
const WEB_APP_PUBLIC = path.join(ROOT_DIR, 'web-app', 'public');

// Ensure public dir exists
if (!fs.existsSync(WEB_APP_PUBLIC)) {
    fs.mkdirSync(WEB_APP_PUBLIC, { recursive: true });
}

// 1. Copy skills_index.json
const sourceIndex = path.join(ROOT_DIR, 'skills_index.json');
const destIndex = path.join(WEB_APP_PUBLIC, 'skills.json');

console.log(`Copying ${sourceIndex} -> ${destIndex}...`);
fs.copyFileSync(sourceIndex, destIndex);

// 2. Copy skills directory content
// Note: Symlinking is better, but Windows often requires admin for symlinks. 
// We will try to copy for reliability in this environment.
const sourceSkills = path.join(ROOT_DIR, 'skills');
const destSkills = path.join(WEB_APP_PUBLIC, 'skills');

console.log(`Copying skills directory...`);

// Recursive copy function (follows symlinks to copy resolved content)
function copyFolderSync(from, to) {
    if (!fs.existsSync(to)) fs.mkdirSync(to, { recursive: true });

    fs.readdirSync(from).forEach(element => {
        const srcPath = path.join(from, element);
        const destPath = path.join(to, element);
        const stat = fs.statSync(srcPath); // statSync follows symlinks

        if (stat.isFile()) {
            fs.copyFileSync(srcPath, destPath);
        } else if (stat.isDirectory()) {
            copyFolderSync(srcPath, destPath);
        }
        // Skip other types (e.g. sockets, FIFOs)
    });
}

// Check if destination exists and remove it to ensure fresh copy
if (fs.existsSync(destSkills)) {
    fs.rmSync(destSkills, { recursive: true, force: true });
}

copyFolderSync(sourceSkills, destSkills);

console.log('✅ Web app assets setup complete!');
