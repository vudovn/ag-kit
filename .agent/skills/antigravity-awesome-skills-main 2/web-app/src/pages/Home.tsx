import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Book, AlertCircle, ArrowRight, RefreshCw, ArrowUpDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { supabase } from '../lib/supabase';
import { SkillStarButton } from '../components/SkillStarButton';
import type { Skill, StarMap, SyncMessage, CategoryStats } from '../types';

export function Home(): React.ReactElement {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [filteredSkills, setFilteredSkills] = useState<Skill[]>([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [stars, setStars] = useState<StarMap>({});
  const [sortBy, setSortBy] = useState('default');
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<SyncMessage | null>(null);

  useEffect(() => {
    const fetchSkillsAndStars = async () => {
      try {
        // Fetch basic skill data
        const res = await fetch('/skills.json');
        const data = await res.json();

        setSkills(data);
        setFilteredSkills(data);

        // Fetch star counts if supabase is configured
        if (supabase) {
          const { data: starData, error } = await supabase
            .from('skill_stars')
            .select('skill_id, star_count');

          if (!error && starData) {
            const starMap: StarMap = {};
            starData.forEach((item: { skill_id: string; star_count: number }) => {
              starMap[item.skill_id] = item.star_count;
            });
            setStars(starMap);
          }
        }
      } catch (err) {
        console.error('Failed to load skills', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSkillsAndStars();
  }, []);

  useEffect(() => {
    let result = [...skills];

    if (search) {
      const lowerSearch = search.toLowerCase();
      result = result.filter(skill =>
        skill.name.toLowerCase().includes(lowerSearch) ||
        skill.description.toLowerCase().includes(lowerSearch)
      );
    }

    if (categoryFilter !== 'all') {
      result = result.filter(skill => skill.category === categoryFilter);
    }

    // Apply sorting
    if (sortBy === 'stars') {
      result = [...result].sort((a, b) => (stars[b.id] || 0) - (stars[a.id] || 0));
    } else if (sortBy === 'newest') {
      result = [...result].sort((a, b) => (b.date_added || '').localeCompare(a.date_added || ''));
    } else if (sortBy === 'az') {
      result = [...result].sort((a, b) => a.name.localeCompare(b.name));
    }

    setFilteredSkills(result);
  }, [search, categoryFilter, sortBy, skills, stars]);

  // Sort categories by count (most skills first), with 'uncategorized' at the end
  const categoryStats: CategoryStats = {};
  skills.forEach(skill => {
    categoryStats[skill.category] = (categoryStats[skill.category] || 0) + 1;
  });

  const categories = ['all', ...Object.keys(categoryStats)
    .filter(cat => cat !== 'uncategorized')
    .sort((a, b) => categoryStats[b] - categoryStats[a]),
    ...(categoryStats['uncategorized'] ? ['uncategorized'] : [])
  ];

  const handleSync = async () => {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await fetch('/api/refresh-skills');
      const data = await res.json();
      if (data.success) {
        if (data.upToDate) {
          setSyncMsg({ type: 'info', text: 'ℹ️ Skills are already up to date!' });
        } else {
          setSyncMsg({ type: 'success', text: `✅ Synced ${data.count} skills!` });
          // Reload skills data only when there are actual updates
          const freshRes = await fetch('/skills.json');
          const freshData = await freshRes.json();
          setSkills(freshData);
          setFilteredSkills(freshData);
        }
      } else {
        setSyncMsg({ type: 'error', text: `❌ ${data.error}` });
      }
    } catch (err) {
      setSyncMsg({ type: 'error', text: '❌ Network error' });
    } finally {
      setSyncing(false);
      setTimeout(() => setSyncMsg(null), 5000);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">Explore Skills</h1>
          <p className="text-slate-500 dark:text-slate-400">Discover {skills.length} agentic capabilities for your AI assistant.</p>
        </div>
        <div className="flex items-center gap-3">
          {syncMsg && (
            <span className={`text-sm font-medium px-3 py-1.5 rounded-full ${
              syncMsg.type === 'success'
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                : syncMsg.type === 'info'
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                  : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
            }`}>
              {syncMsg.text}
            </span>
          )}
          <button
            onClick={handleSync}
            disabled={syncing}
            className="flex items-center space-x-2 px-4 py-2.5 rounded-lg font-medium text-sm bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-wait transition-colors shadow-sm"
          >
            <RefreshCw className={`h-4 w-4 ${syncing ? 'animate-spin' : ''}`} />
            <span>{syncing ? 'Syncing...' : 'Sync Skills'}</span>
          </button>
        </div>
      </div>

      <div className="flex flex-col space-y-4 md:flex-row md:items-center md:space-x-4 md:space-y-0 bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm sticky top-20 z-40">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search skills (e.g., 'react', 'security', 'python')..."
            className="w-full rounded-md border border-slate-200 bg-slate-50 px-9 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
          <Filter className="h-4 w-4 text-slate-500 shrink-0" />
          <select
            className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[150px]"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat === 'all'
                  ? 'All Categories'
                  : `${cat.charAt(0).toUpperCase() + cat.slice(1)} (${categoryStats[cat] || 0})`
                }
              </option>
            ))}
          </select>
          <ArrowUpDown className="h-4 w-4 text-slate-500 shrink-0 ml-2" />
          <select
            className="h-9 rounded-md border border-slate-200 bg-slate-50 px-3 text-sm outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50 min-w-[130px]"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="default">Default</option>
            <option value="stars">⭐ Most Stars</option>
            <option value="newest">🆕 Newest</option>
            <option value="az">🔤 A → Z</option>
          </select>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <AnimatePresence>
          {loading ? (
            [...Array(8)].map((_, i) => (
              <div key={i} className="animate-pulse rounded-lg border border-slate-200 p-6 h-48 bg-slate-100 dark:border-slate-800 dark:bg-slate-900">
              </div>
            ))
          ) : filteredSkills.length === 0 ? (
            <div className="col-span-full py-12 text-center">
              <AlertCircle className="mx-auto h-12 w-12 text-slate-400" />
              <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">No skills found</h3>
              <p className="mt-2 text-slate-500 dark:text-slate-400">Try adjusting your search or filter.</p>
            </div>
          ) : (
            filteredSkills.map((skill) => (
              <motion.div
                key={skill.id}
                layout
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <Link
                  to={`/skill/${skill.id}`}
                  className="group flex flex-col h-full rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition-all hover:bg-slate-50 hover:shadow-md dark:border-slate-800 dark:bg-slate-900 dark:hover:border-indigo-500/50"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="p-2 bg-indigo-50 dark:bg-indigo-950/30 rounded-md">
                        <Book className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
                      </div>
                      <span className="text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                        {skill.category || 'Uncategorized'}
                      </span>
                    </div>
                    <SkillStarButton
                      skillId={skill.id}
                      initialCount={stars[skill.id] || 0}
                      variant="default"
                    />
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-50 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors mb-2 line-clamp-1">
                    @{skill.name}
                  </h3>

                  <p className="text-sm text-slate-500 dark:text-slate-400 line-clamp-3 mb-4 flex-grow">
                    {skill.description}
                  </p>

                  <div className="flex items-center justify-between text-xs text-slate-400 dark:text-slate-500 mb-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                    <span>Risk: <span className="font-semibold text-slate-600 dark:text-slate-300">{skill.risk || 'unknown'}</span></span>
                    {skill.date_added && (
                      <span className="ml-2">📅 {skill.date_added}</span>
                    )}
                  </div>

                  <div className="flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 pt-2 mt-auto group-hover:translate-x-1 transition-transform">
                    Read Skill <ArrowRight className="ml-1 h-4 w-4" />
                  </div>
                </Link>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default Home;
