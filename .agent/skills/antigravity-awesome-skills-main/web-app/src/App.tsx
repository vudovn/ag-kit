import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Home } from './pages/Home';
import { SkillDetail } from './pages/SkillDetail';
import { BookOpen, Github } from 'lucide-react';

function App(): React.ReactElement {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50">
        <header className="sticky top-0 z-50 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
          <div className="container flex h-14 max-w-screen-2xl items-center mx-auto px-4">
            <Link to="/" className="mr-8 flex items-center space-x-2">
              <BookOpen className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              <span className="hidden font-bold sm:inline-block">Antigravity Skills</span>
            </Link>
            <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">

              <nav className="flex items-center space-x-6 text-sm font-medium">
                <a
                  href="https://github.com/sickn33/antigravity-awesome-skills"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center text-slate-600 transition-colors hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-50"
                >
                  <Github className="h-5 w-5 mr-2" />
                  GitHub Repository
                </a>
              </nav>
            </div>
          </div>
        </header>
        <main className="container max-w-screen-2xl mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/skill/:id" element={<SkillDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
