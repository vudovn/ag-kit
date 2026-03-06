import { createClient, SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = (import.meta as ImportMeta & { env: Record<string, string> }).env.VITE_SUPABASE_URL
const supabaseAnonKey = (import.meta as ImportMeta & { env: Record<string, string> }).env.VITE_SUPABASE_ANON_KEY

// Create a single supabase client for interacting with your database
// Returns null if credentials are not configured (graceful degradation)
export const supabase: SupabaseClient | null =
  supabaseUrl && supabaseAnonKey
    ? createClient(supabaseUrl, supabaseAnonKey)
    : null

// Type for star data in the database
export interface SkillStarData {
  skill_id: string
  star_count: number
}
