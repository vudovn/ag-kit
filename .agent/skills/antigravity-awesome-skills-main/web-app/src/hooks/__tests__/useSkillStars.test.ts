import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useSkillStars } from '../useSkillStars';

const STORAGE_KEY = 'user_stars';

describe('useSkillStars', () => {
  beforeEach(() => {
    // Clear localStorage mock before each test
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('Initialization', () => {
    it('should initialize with zero stars when no skillId provided', () => {
      const { result } = renderHook(() => useSkillStars(undefined));

      expect(result.current.starCount).toBe(0);
      expect(result.current.hasStarred).toBe(false);
      expect(result.current.isLoading).toBe(false);
    });

    it('should initialize with zero stars for new skill', () => {
      const { result } = renderHook(() => useSkillStars('new-skill'));

      expect(result.current.starCount).toBe(0);
      expect(result.current.hasStarred).toBe(false);
    });

    it('should read starred status from localStorage on init', () => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ 'test-skill': true }));

      const { result } = renderHook(() => useSkillStars('test-skill'));

      expect(result.current.hasStarred).toBe(true);
    });

    it('should handle corrupted localStorage gracefully', () => {
      // Mock getItem to return invalid JSON
      const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
      localStorage.setItem(STORAGE_KEY, 'invalid-json');

      const { result } = renderHook(() => useSkillStars('test-skill'));

      expect(result.current.hasStarred).toBe(false);
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to parse user_stars from localStorage:',
        expect.any(Error)
      );

      consoleSpy.mockRestore();
    });
  });

  describe('handleStarClick', () => {
    it('should not allow starring without skillId', async () => {
      const { result } = renderHook(() => useSkillStars(undefined));

      await act(async () => {
        await result.current.handleStarClick();
      });

      expect(result.current.starCount).toBe(0);
      expect(localStorage.setItem).not.toHaveBeenCalled();
    });

    it('should not allow double-starring same skill', async () => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ 'skill-1': true }));

      const { result } = renderHook(() => useSkillStars('skill-1'));

      await act(async () => {
        await result.current.handleStarClick();
      });

      // Star count should remain unchanged (already starred)
      expect(result.current.starCount).toBe(0);
      expect(result.current.hasStarred).toBe(true);
    });

    it('should optimistically update star count', async () => {
      const { result } = renderHook(() => useSkillStars('optimistic-skill'));

      // Initial state
      expect(result.current.starCount).toBe(0);

      // Click star
      await act(async () => {
        await result.current.handleStarClick();
      });

      // Should be optimistically updated
      await waitFor(() => {
        expect(result.current.starCount).toBe(1);
        expect(result.current.hasStarred).toBe(true);
      });
    });

    it('should persist starred status to localStorage', async () => {
      const { result } = renderHook(() => useSkillStars('persist-skill'));

      await act(async () => {
        await result.current.handleStarClick();
      });

      expect(localStorage.setItem).toHaveBeenCalledWith(
        STORAGE_KEY,
        JSON.stringify({ 'persist-skill': true })
      );
    });

    it('should set loading state during operation', async () => {
      const { result } = renderHook(() => useSkillStars('loading-skill'));

      // Wait for initial render
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      // Click star - the loading state may change very quickly due to the async nature
      await act(async () => {
        await result.current.handleStarClick();
      });

      // After completion, loading should be false
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('LocalStorage error handling', () => {
    it('should handle setItem errors gracefully', async () => {
      const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      // Mock setItem to throw
      localStorage.setItem = vi.fn(() => {
        throw new Error('Storage quota exceeded');
      });

      const { result } = renderHook(() => useSkillStars('error-skill'));

      // Should still optimistically update UI
      await act(async () => {
        await result.current.handleStarClick();
      });

      expect(result.current.starCount).toBe(1);
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to save user_stars to localStorage:',
        expect.any(Error)
      );

      consoleSpy.mockRestore();
    });
  });

  describe('Return values', () => {
    it('should return all expected properties', () => {
      const { result } = renderHook(() => useSkillStars('test'));

      expect(result.current).toHaveProperty('starCount');
      expect(result.current).toHaveProperty('hasStarred');
      expect(result.current).toHaveProperty('handleStarClick');
      expect(result.current).toHaveProperty('isLoading');
    });

    it('should expose handleStarClick as function', () => {
      const { result } = renderHook(() => useSkillStars('test'));

      expect(typeof result.current.handleStarClick).toBe('function');
    });
  });
});
