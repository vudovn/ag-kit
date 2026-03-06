import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { Home } from '../Home';
import { renderWithRouter } from '../../utils/testUtils';
import { createMockSkills, createMockSkillsByCategory } from '../../factories/skill';
import type { Skill } from '../../types';

describe('Home', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('Rendering', () => {
    it('should show loading skeleton initially', async () => {
      // Mock fetch to never resolve (keep loading state)
      (global.fetch as Mock).mockImplementation(() => new Promise(() => {}));

      renderWithRouter(<Home />);

      // Should show pulse animation elements (skeletons)
      const skeletons = document.querySelectorAll('.animate-pulse');
      expect(skeletons.length).toBeGreaterThan(0);
    });

    it('should render skills after loading', async () => {
      const mockSkills = createMockSkills(3);

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@Test Skill 0')).toBeInTheDocument();
        expect(screen.getByText('@Test Skill 1')).toBeInTheDocument();
        expect(screen.getByText('@Test Skill 2')).toBeInTheDocument();
      });
    });

    it('should display correct skills count in header', async () => {
      const mockSkills = createMockSkills(5);

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText(/Discover 5 agentic capabilities/)).toBeInTheDocument();
      });
    });

    it('should show empty state when no skills match search', async () => {
      const mockSkills = createMockSkills(2);

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@Test Skill 0')).toBeInTheDocument();
      });

      // Search for non-existent skill
      const searchInput = screen.getByPlaceholderText(/Search skills/i);
      fireEvent.change(searchInput, { target: { value: 'nonexistent' } });

      await waitFor(() => {
        expect(screen.getByText(/No skills found/)).toBeInTheDocument();
        expect(screen.getByText(/Try adjusting your search or filter/)).toBeInTheDocument();
      });
    });
  });

  describe('Search functionality', () => {
    it('should filter skills by name', async () => {
      const mockSkills: Skill[] = [
        { id: '1', name: 'React Skill', description: 'React desc', category: 'frontend', path: 'skills/react/SKILL.md' },
        { id: '2', name: 'Python Skill', description: 'Python desc', category: 'backend', path: 'skills/python/SKILL.md' },
        { id: '3', name: 'Vue Skill', description: 'Vue desc', category: 'frontend', path: 'skills/vue/SKILL.md' },
      ];

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@React Skill')).toBeInTheDocument();
      });

      // Search for react
      const searchInput = screen.getByPlaceholderText(/Search skills/i);
      fireEvent.change(searchInput, { target: { value: 'react' } });

      await waitFor(() => {
        expect(screen.getByText('@React Skill')).toBeInTheDocument();
        expect(screen.queryByText('@Python Skill')).not.toBeInTheDocument();
        expect(screen.queryByText('@Vue Skill')).not.toBeInTheDocument();
      });
    });

    it('should filter skills by description', async () => {
      const mockSkills: Skill[] = [
        { id: '1', name: 'Skill One', description: 'Learn about React', category: 'frontend', path: 'skills/one/SKILL.md' },
        { id: '2', name: 'Skill Two', description: 'Learn about Python', category: 'backend', path: 'skills/two/SKILL.md' },
      ];

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@Skill One')).toBeInTheDocument();
      });

      // Search by description
      const searchInput = screen.getByPlaceholderText(/Search skills/i);
      fireEvent.change(searchInput, { target: { value: 'python' } });

      await waitFor(() => {
        expect(screen.queryByText('@Skill One')).not.toBeInTheDocument();
        expect(screen.getByText('@Skill Two')).toBeInTheDocument();
      });
    });

    it('should perform case-insensitive search', async () => {
      const mockSkills: Skill[] = [
        { id: '1', name: 'React Skill', description: 'Desc', category: 'frontend', path: 'skills/react/SKILL.md' },
      ];

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@React Skill')).toBeInTheDocument();
      });

      // Search with uppercase
      const searchInput = screen.getByPlaceholderText(/Search skills/i);
      fireEvent.change(searchInput, { target: { value: 'REACT' } });

      await waitFor(() => {
        expect(screen.getByText('@React Skill')).toBeInTheDocument();
      });
    });
  });

  describe('Category filter', () => {
    it('should filter skills by category', async () => {
      const mockSkills = createMockSkillsByCategory(['frontend', 'backend']);

      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => mockSkills,
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByText('@frontend Skill 0')).toBeInTheDocument();
      });

      // Select backend category using the select element by display value
      const categorySelect = screen.getByDisplayValue(/All Categories/i);
      fireEvent.change(categorySelect, { target: { value: 'backend' } });

      await waitFor(() => {
        // After filtering, frontend skills should not be visible
        const frontendSkills = screen.queryAllByText(/@frontend/);
        expect(frontendSkills.length).toBe(0);
      });
    });
  });

  describe('Sync button', () => {
    it('should show sync button', async () => {
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [],
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Sync Skills/i })).toBeInTheDocument();
      });
    });

    it('should show syncing state when clicked', async () => {
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => [],
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Sync Skills/i })).toBeInTheDocument();
      });

      const syncButton = screen.getByRole('button', { name: /Sync Skills/i });

      // Mock the sync API call
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => ({ success: true, upToDate: true }),
      });

      fireEvent.click(syncButton);

      await waitFor(() => {
        expect(screen.getByText(/Syncing/i)).toBeInTheDocument();
      });
    });
  });

  describe('Sorting', () => {
    it('should show sort options', async () => {
      (global.fetch as Mock).mockResolvedValueOnce({
        json: async () => createMockSkills(2),
      });

      renderWithRouter(<Home />);

      await waitFor(() => {
        const sortSelect = screen.getByDisplayValue(/Default/i);
        expect(sortSelect).toBeInTheDocument();
      });
    });
  });

  describe('Error handling', () => {
    it('should handle fetch errors gracefully', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      (global.fetch as Mock).mockRejectedValueOnce(new Error('Network error'));

      renderWithRouter(<Home />);

      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith('Failed to load skills', expect.any(Error));
      });

      // Should still show 0 skills
      expect(screen.getByText(/Discover 0 agentic capabilities/)).toBeInTheDocument();

      consoleSpy.mockRestore();
    });
  });
});
