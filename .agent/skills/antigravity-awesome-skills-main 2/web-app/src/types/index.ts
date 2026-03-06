/**
 * Skill data type from skills.json
 */
export interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  risk?: 'low' | 'medium' | 'high' | 'critical' | 'unknown';
  source?: string;
  date_added?: string;
  path: string;
}

/**
 * Star count data from Supabase
 */
export interface StarMap {
  [skillId: string]: number;
}

/**
 * Sync message type for UI feedback
 */
export interface SyncMessage {
  type: 'success' | 'error' | 'info';
  text: string;
}

/**
 * Category statistics
 */
export interface CategoryStats {
  [category: string]: number;
}
