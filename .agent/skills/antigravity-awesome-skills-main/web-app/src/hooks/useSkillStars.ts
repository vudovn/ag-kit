import { useState, useEffect, useCallback } from 'react';
import { supabase } from '../lib/supabase';

const STORAGE_KEY = 'user_stars';

interface UserStars {
  [skillId: string]: boolean;
}

interface UseSkillStarsReturn {
  starCount: number;
  hasStarred: boolean;
  handleStarClick: () => Promise<void>;
  isLoading: boolean;
}

/**
 * Safely parse localStorage data with error handling
 */
function getUserStarsFromStorage(): UserStars {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return {};
    const parsed = JSON.parse(stored);
    return typeof parsed === 'object' && parsed !== null ? parsed : {};
  } catch (error) {
    console.warn('Failed to parse user_stars from localStorage:', error);
    return {};
  }
}

/**
 * Safely save to localStorage with error handling
 */
function saveUserStarsToStorage(stars: UserStars): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stars));
  } catch (error) {
    console.warn('Failed to save user_stars to localStorage:', error);
  }
}

/**
 * Hook to manage skill starring functionality
 * Handles localStorage persistence, optimistic UI updates, and Supabase sync
 */
export function useSkillStars(skillId: string | undefined): UseSkillStarsReturn {
  const [starCount, setStarCount] = useState<number>(0);
  const [hasStarred, setHasStarred] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Initialize star count from Supabase and check if user has starred
  useEffect(() => {
    if (!skillId) return;

    const initializeStars = async () => {
      // Check localStorage for user's starred status
      const userStars = getUserStarsFromStorage();
      setHasStarred(!!userStars[skillId]);

      // Fetch star count from Supabase if available
      if (supabase) {
        try {
          const { data, error } = await supabase
            .from('skill_stars')
            .select('star_count')
            .eq('skill_id', skillId)
            .single();

          if (!error && data) {
            setStarCount(data.star_count);
          }
        } catch (err) {
          console.warn('Failed to fetch star count:', err);
        }
      }
    };

    initializeStars();
  }, [skillId]);

  /**
   * Handle star button click
   * Prevents double-starring, updates optimistically, syncs to Supabase
   */
  const handleStarClick = useCallback(async () => {
    if (!skillId || isLoading) return;

    // Check if user has already starred (prevent spam)
    const userStars = getUserStarsFromStorage();
    if (userStars[skillId]) return;

    setIsLoading(true);

    try {
      // Optimistically update UI
      setStarCount(prev => prev + 1);
      setHasStarred(true);

      // Persist to localStorage
      const updatedStars = { ...userStars, [skillId]: true };
      saveUserStarsToStorage(updatedStars);

      // Sync to Supabase if available
      if (supabase) {
        const { data: existingData, error: fetchError } = await supabase
          .from('skill_stars')
          .select('star_count')
          .eq('skill_id', skillId)
          .single();

        if (fetchError && fetchError.code !== 'PGRST116') {
          // PGRST116 = not found, which is expected for new skills
          console.warn('Failed to fetch existing star count:', fetchError);
        }

        if (existingData) {
          // Update existing record
          const { error: updateError } = await supabase
            .from('skill_stars')
            .update({ star_count: existingData.star_count + 1 })
            .eq('skill_id', skillId);

          if (updateError) {
            console.warn('Failed to update star count:', updateError);
          }
        } else {
          // Insert new record
          const { error: insertError } = await supabase
            .from('skill_stars')
            .insert({ skill_id: skillId, star_count: 1 });

          if (insertError) {
            console.warn('Failed to insert star count:', insertError);
          }
        }
      }
    } catch (error) {
      // Rollback optimistic update on error
      console.error('Failed to star skill:', error);
      setStarCount(prev => Math.max(0, prev - 1));
      setHasStarred(false);

      // Remove from localStorage on error
      const userStars = getUserStarsFromStorage();
      if (userStars[skillId]) {
        const { [skillId]: _, ...rest } = userStars;
        saveUserStarsToStorage(rest);
      }
    } finally {
      setIsLoading(false);
    }
  }, [skillId, isLoading]);

  return {
    starCount,
    hasStarred,
    handleStarClick,
    isLoading
  };
}

export default useSkillStars;
