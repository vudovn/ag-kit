import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Markdown from 'react-markdown';
import { ArrowLeft, Copy, Check, FileCode, AlertTriangle } from 'lucide-react';
import { SkillStarButton } from '../components/SkillStarButton';
import type { Skill } from '../types';

interface RouteParams {
  id: string;
}

export function SkillDetail(): React.ReactElement {
  const { id } = useParams<keyof RouteParams>() as RouteParams;
  const [skill, setSkill] = useState<Skill | null>(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [copiedFull, setCopiedFull] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [customContext, setCustomContext] = useState('');
  const [initialStarCount] = useState(0);

  useEffect(() => {
    // Fetch index and stars in parallel when possible
    const loadData = async () => {
      try {
        // 1. Fetch index to get skill metadata and path
        const res = await fetch('/skills.json');
        const skills: Skill[] = await res.json();
        const foundSkill = skills.find(s => s.id === id);

        if (foundSkill) {
          setSkill(foundSkill);

          // 2. Fetch the actual markdown content
          const cleanPath = foundSkill.path.startsWith('skills/')
            ? foundSkill.path.replace('skills/', '')
            : foundSkill.path;

          const mdRes = await fetch(`/skills/${cleanPath}/SKILL.md`);
          if (!mdRes.ok) throw new Error('Skill file not found');

          const text = await mdRes.text();
          setContent(text);
        } else {
          setError('Skill not found in registry.');
        }
      } catch (err) {
        console.error('Failed to load skill data', err);
        setError(err instanceof Error ? err.message : 'Could not load skill content.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [id]);

  const copyToClipboard = () => {
    if (!skill) return;

    const basePrompt = `Use @${skill.name}`;
    const finalPrompt = customContext.trim()
      ? `${basePrompt}\n\nContext:\n${customContext}`
      : basePrompt;

    navigator.clipboard.writeText(finalPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const copyFullToClipboard = () => {
    const finalPrompt = customContext.trim()
      ? `${content}\n\nContext:\n${customContext}`
      : content;

    navigator.clipboard.writeText(finalPrompt);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !skill) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Error Loading Skill</h2>
        <p className="text-slate-500 mt-2">{error}</p>
        <Link to="/" className="mt-8 inline-flex items-center text-indigo-600 font-medium hover:underline">
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <Link to="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 dark:hover:text-slate-200 mb-6 transition-colors">
        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Catalog
      </Link>

      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="p-6 sm:p-8 border-b border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/50">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center space-x-3 mb-2 flex-wrap gap-2">
                <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-400 uppercase tracking-wide">
                  {skill.category}
                </span>
                {skill.source && (
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                    {skill.source}
                  </span>
                )}
                {skill.date_added && (
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400">
                    📅 Added {skill.date_added}
                  </span>
                )}
                <SkillStarButton
                  skillId={skill.id}
                  initialCount={initialStarCount}
                  variant="compact"
                />
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-slate-50 tracking-tight">
                @{skill.name}
              </h1>
              <p className="mt-2 text-lg text-slate-600 dark:text-slate-300">
                {skill.description}
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-2">
              <button
                onClick={copyToClipboard}
                className="flex items-center justify-center space-x-2 bg-slate-100 hover:bg-slate-200 text-slate-900 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700 px-4 py-2.5 rounded-lg font-medium transition-colors min-w-[140px] border border-slate-200 dark:border-slate-700"
              >
                {copied ? <Check className="h-4 w-4 text-green-600 dark:text-green-400" /> : <Copy className="h-4 w-4" />}
                <span>{copied ? 'Copied!' : 'Copy @Skill'}</span>
              </button>
              <button
                onClick={copyFullToClipboard}
                className="flex items-center justify-center space-x-2 bg-slate-900 hover:bg-slate-800 text-white dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200 px-4 py-2.5 rounded-lg font-medium transition-colors min-w-[140px]"
              >
                {copiedFull ? <Check className="h-4 w-4 text-green-400" /> : <FileCode className="h-4 w-4" />}
                <span>{copiedFull ? 'Copied Content!' : 'Copy Full Content'}</span>
              </button>
            </div>
          </div>

          <div className="mt-6 border-t border-slate-200 dark:border-slate-800 pt-6">
            <label htmlFor="context" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Interactive Prompt Builder (Optional)
            </label>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Add specific details below (e.g. &quot;Use React 19 and Tailwind&quot;). The &quot;Copy Prompt&quot; button will automatically attach your context.
            </p>
            <textarea
              id="context"
              rows={3}
              className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all resize-y"
              placeholder="Type your specific task requirements here..."
              value={customContext}
              onChange={(e) => setCustomContext(e.target.value)}
            />
          </div>
        </div>

        <div className="p-6 sm:p-8">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <Markdown>{content}</Markdown>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SkillDetail;
