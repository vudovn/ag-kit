import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import refreshSkillsPlugin from './refresh-skills-plugin.js';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), refreshSkillsPlugin()],
});
