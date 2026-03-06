import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { SkillDetail } from '../SkillDetail';
import { renderWithRouter } from '../../utils/testUtils';
import { createMockSkill } from '../../factories/skill';
import type { Skill } from '../../types';

// Mock the SkillStarButton component
vi.mock('../../components/SkillStarButton', () => ({
  SkillStarButton: ({ skillId, initialCount }: { skillId: string; initialCount?: number }) => (
    <button data-testid="star-button" data-skill-id={skillId} data-count={initialCount}>
      {initialCount || 0} Upvotes
    </button>
  ),
}));

describe('SkillDetail', () => {
  beforeEach(() => {
    localStorage.clear();
    // Reset and setup fresh fetch mock for each test
    const mockFetch = vi.fn();
    global.fetch = mockFetch;
  });

  describe('Loading state', () => {
    it('should show loading spinner initially', async () => {
      // Create a promise that never resolves
      const neverResolvingPromise = new Promise(() => {});
      (global.fetch as Mock).mockReturnValue(neverResolvingPromise);

      renderWithRouter(<SkillDetail />, { route: '/skill/test-skill' });

      expect(document.querySelector('.animate-spin')).toBeInTheDocument();
    });
  });

  describe('Skill rendering', () => {
    it('should render skill details correctly', async () => {
      const mockSkill = createMockSkill({
        id: 'react-patterns',
        name: 'react-patterns',
        description: 'React design patterns and best practices',
        category: 'frontend',
        source: 'official',
        date_added: '2024-01-15',
      });

      // Mock first fetch for skills.json
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      // Mock second fetch for markdown content
      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => '# React Patterns\n\nThis is the skill content.',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/react-patterns' });

      await waitFor(() => {
        expect(screen.getByText('@react-patterns')).toBeInTheDocument();
        expect(screen.getByText('React design patterns and best practices')).toBeInTheDocument();
        expect(screen.getByText(/frontend/i)).toBeInTheDocument();
      });
    });

    it('should show skill not found when id does not exist', async () => {
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [],
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/nonexistent' });

      await waitFor(() => {
        expect(screen.getByText(/Error Loading Skill/i)).toBeInTheDocument();
        expect(screen.getByText(/Skill not found in registry/i)).toBeInTheDocument();
      });
    });
  });

  describe('Copy functionality', () => {
    it('should have copy buttons', async () => {
      const mockSkill = createMockSkill({ id: 'copy-test', name: 'copy-test' });

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/copy-test' });

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Copy @Skill/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Copy Full Content/i })).toBeInTheDocument();
      });
    });

    it('should copy skill name to clipboard when clicked', async () => {
      const mockSkill = createMockSkill({ id: 'click-test', name: 'click-test' });

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/click-test' });

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Copy @Skill/i })).toBeInTheDocument();
      });

      const copyButton = screen.getByRole('button', { name: /Copy @Skill/i });
      fireEvent.click(copyButton);

      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Use @click-test');
    });
  });

  describe('Prompt builder', () => {
    it('should have interactive prompt builder textarea', async () => {
      const mockSkill = createMockSkill({ id: 'prompt-test' });

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/prompt-test' });

      await waitFor(() => {
        expect(screen.getByLabelText(/Interactive Prompt Builder/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/Type your specific task requirements/i)).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    it('should have back to catalog link', async () => {
      const mockSkill = createMockSkill({ id: 'nav-test' });

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/nav-test' });

      await waitFor(() => {
        expect(screen.getByText(/Back to Catalog/i)).toBeInTheDocument();
      });
    });
  });

  describe('Star button integration', () => {
    it('should render star button component', async () => {
      const mockSkill = createMockSkill({ id: 'star-integration' });

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [mockSkill],
      });

      (global.fetch as Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => 'Content',
      });

      renderWithRouter(<SkillDetail />, { route: '/skill/star-integration' });

      await waitFor(() => {
        expect(screen.getByTestId('star-button')).toBeInTheDocument();
      });
    });
  });
});
