import React from 'react';
import { Star } from 'lucide-react';
import { useSkillStars } from '../hooks/useSkillStars';

interface SkillStarButtonProps {
  skillId: string;
  initialCount?: number;
  onStarClick?: () => void;
  variant?: 'default' | 'compact';
}

/**
 * Star button component for skills
 * Uses useSkillStars hook for state management
 */
export function SkillStarButton({
  skillId,
  initialCount = 0,
  onStarClick,
  variant = 'default'
}: SkillStarButtonProps): React.ReactElement {
  const { starCount, hasStarred, handleStarClick, isLoading } = useSkillStars(skillId);

  // Use optimistic count from hook, fall back to initial
  const displayCount = starCount || initialCount;

  const handleClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (hasStarred || isLoading) return;

    await handleStarClick();
    onStarClick?.();
  };

  if (variant === 'compact') {
    return (
      <button
        onClick={handleClick}
        className="flex items-center space-x-1.5 px-3 py-1 bg-yellow-50 dark:bg-yellow-900/10 hover:bg-yellow-100 dark:hover:bg-yellow-900/30 text-yellow-700 dark:text-yellow-500 rounded-full text-xs font-bold border border-yellow-200 dark:border-yellow-700/50 transition-colors disabled:opacity-50"
        disabled={hasStarred || isLoading}
        title={hasStarred ? 'You already upvoted' : 'Upvote skill'}
      >
        <Star className={`h-3.5 w-3.5 ${hasStarred ? 'fill-yellow-500 stroke-yellow-500' : ''}`} />
        <span>{displayCount} Upvotes</span>
      </button>
    );
  }

  return (
    <button
      onClick={handleClick}
      className="flex items-center space-x-1 px-2 py-1 rounded-md bg-slate-50 dark:bg-slate-800/50 hover:bg-yellow-50 dark:hover:bg-yellow-900/20 text-slate-500 hover:text-yellow-600 dark:hover:text-yellow-500 transition-colors border border-slate-200 dark:border-slate-800 z-10 disabled:opacity-50"
      disabled={hasStarred || isLoading}
      title={hasStarred ? 'You already upvoted' : 'Upvote skill'}
    >
      <Star className={`h-4 w-4 ${hasStarred ? 'fill-yellow-400 stroke-yellow-400' : ''} ${isLoading ? 'animate-pulse' : ''}`} />
      <span className="text-xs font-semibold">{displayCount}</span>
    </button>
  );
}

export default SkillStarButton;
