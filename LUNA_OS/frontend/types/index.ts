// ============================================================================
// LUNA OS - Shared Type Definitions
// ============================================================================

// ----------------------------------------------------------------------------
// API Response Types
// ----------------------------------------------------------------------------
export interface ApiResponse<T = unknown> {
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

// ----------------------------------------------------------------------------
// Dashboard & Analytics Types
// ----------------------------------------------------------------------------
export interface DashboardData {
  period_days: number
  conversations?: {
    total: number
    converted: number
    abandoned: number
    conversion_rate: number
  }
  messages?: {
    total: number
    avg_response_time_ms: number
  }
  appointments?: {
    total: number
    completed: number
  }
  resumo?: {
    total_conversas: number
    total_mensagens: number
    human_hours_saved: number
  }
  conversao?: {
    fechadas: number
    perdidas: number
    taxa_conversao: number
  }
}

export interface SentimentDistribution {
  positive: number
  negative: number
  neutral: number
}

export interface SentimentData {
  distribution: SentimentDistribution
  period_days: number
}

export interface MaturityData {
  score: number
  recommendation?: string
}

// ----------------------------------------------------------------------------
// Conversation Types
// ----------------------------------------------------------------------------
export interface Conversation {
  id: string
  phone: string
  contact_name?: string
  last_message_at: string
  messages_count: number
  status: 'active' | 'closed' | 'abandoned'
  assigned_to?: string
  tags?: string[]
}

export interface Message {
  id: string
  conversation_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  meta?: {
    intent?: string
    confidence?: number
    model?: string
    processing_time_ms?: number
  }
}

// ----------------------------------------------------------------------------
// Client Types
// ----------------------------------------------------------------------------
export interface Client {
  id: string
  name: string
  phone: string
  email?: string
  created_at: string
  last_contact_at: string
  total_conversations: number
  total_appointments: number
  lifetime_value: number
  tags?: string[]
  notes?: string
}

export interface ClientActivity {
  type: 'conversation' | 'appointment' | 'payment'
  timestamp: string
  description: string
  metadata?: Record<string, unknown>
}

// ----------------------------------------------------------------------------
// Service & Professional Types
// ----------------------------------------------------------------------------
export interface Service {
  id: string
  name: string
  description?: string
  duration_minutes: number
  price: number
  category: string
  active: boolean
  created_at: string
  updated_at: string
}

export interface Professional {
  id: string
  name: string
  role: string
  avatar_url?: string
  active: boolean
  specialties?: string[]
  schedule?: {
    day_of_week: number
    start_time: string
    end_time: string
  }[]
}

export interface Package {
  id: string
  name: string
  description: string
  services: string[]
  price: number
  discount_percentage: number
  active: boolean
}

// ----------------------------------------------------------------------------
// Campaign Types
// ----------------------------------------------------------------------------
export type CampaignType = 'reativacao' | 'aniversario' | 'promocao' | 'lembrete'
export type CampaignSegment = 'todos' | 'ativos' | 'inativos' | 'vip'
export type CampaignStatus = 'draft' | 'scheduled' | 'active' | 'completed' | 'cancelled'

export interface Campaign {
  id: string
  name: string
  type: CampaignType
  segment: CampaignSegment
  objective: string
  insights?: string
  start_date?: string
  end_date?: string
  status: CampaignStatus
  created_at: string
  updated_at: string
  messages_sent?: number
  messages_delivered?: number
  conversion_rate?: number
}

export interface CampaignCreateInput {
  name: string
  type: CampaignType
  segment: CampaignSegment
  objective: string
  insights?: string
  start_date?: string
  end_date?: string
}

// ----------------------------------------------------------------------------
// Knowledge Base Types (Brain)
// ----------------------------------------------------------------------------
export type KnowledgeCategory = 'business' | 'services' | 'faq' | 'insights' | 'prompts'
export type KnowledgeSource = 'manual' | 'auto'
export type SaveStatus = 'idle' | 'saving' | 'saved' | 'error'

export interface KnowledgeItem {
  id: string
  category: KnowledgeCategory
  key: string
  data: KnowledgeData | string
  source?: KnowledgeSource
  created_at: string
  updated_at: string
}

export interface KnowledgeData {
  content: string
  metadata?: Record<string, unknown>
}

export interface BusinessInfo {
  name: string
  hours: string
  address: string
}

// ----------------------------------------------------------------------------
// Dojo (Testing Arena) Types
// ----------------------------------------------------------------------------
export type ScenarioLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert'
export type PersonaMood = 'happy' | 'frustrated' | 'hurry' | 'hesitant' | 'unknown' | 'aggressive' | 'needy'

export interface Scenario {
  id: string
  name: string
  level: ScenarioLevel
  description: string
  sample_message: string
  points: number
  success_criteria?: string[]
}

export interface Persona {
  id: string
  name: string
  mood: PersonaMood
  emoji: string
  description: string
  difficulty: number
  background?: string
}

export interface TestMetrics {
  empathy_score: number
  clarity_score: number
  actionability_score: number
  overall_success: boolean
  criteria_met: string[]
  criteria_missing: string[]
}

export interface TestResult {
  scenario_name: string
  persona_name: string
  user_message: string
  luna_response: string
  intent_detected: string
  confidence_score: number
  processing_time_ms: number
  metrics: TestMetrics
  success: boolean
  points_earned: number
}

export interface DojoMetrics {
  total_tests: number
  total_points: number
  success_rate: number
  maturity_score?: {
    score: number
    recommendation: string
  }
}

// ----------------------------------------------------------------------------
// Intelligence Types
// ----------------------------------------------------------------------------
export interface IntelligenceProposal {
  id: string
  client_id: string
  client_name: string
  type: 'upsell' | 'reactivation' | 'retention'
  description: string
  expected_impact: number
  confidence: number
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
}

export interface EdgeCase {
  id: string
  conversation_id: string
  description: string
  category: 'ambiguous' | 'out_of_scope' | 'technical_error' | 'escalation'
  suggested_action: string
  status: 'pending' | 'resolved' | 'converted'
  created_at: string
}

export interface ClientIntelligence {
  client_id: string
  client_name: string
  satisfaction_score: number
  churn_risk: 'low' | 'medium' | 'high'
  lifetime_value: number
  preferred_services: string[]
  last_interaction: string
}

// ----------------------------------------------------------------------------
// Settings & Configuration Types
// ----------------------------------------------------------------------------
export interface BotSettings {
  name: string
  greeting: string
  fallback: string
  personality?: string
  max_tokens?: number
  temperature?: number
}

export interface BusinessSettings {
  name: string
  hours: string
  address: string
  phone: string
  email?: string
  timezone: string
}

export interface IntegrationSettings {
  whatsapp_connected: boolean
  supabase_connected: boolean
  openrouter_connected: boolean
  webhook_url?: string
}

export interface AppSettings {
  bot: BotSettings
  business: BusinessSettings
  integrations: IntegrationSettings
}

// ----------------------------------------------------------------------------
// UI Component Types
// ----------------------------------------------------------------------------
export interface NavItem {
  name: string
  href: string
  icon: React.ElementType
  badge?: string
}

export interface KPICardProps {
  title: string
  value: string | number
  sub?: string
  icon: React.ElementType
  accent: string
  trend?: 'up' | 'down' | null
  href?: string
  index: number
}

export interface SectionProps {
  icon: React.ElementType
  title: string
  children: React.ReactNode
}

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

// ----------------------------------------------------------------------------
// Utility Types
// ----------------------------------------------------------------------------
export type Optional<T, K extends keyof T> = Pick<Partial<T>, K> & Omit<T, K>

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = Pick<
  T,
  Exclude<keyof T, Keys>
> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
  }[Keys]

export type Nullable<T> = T | null

export interface DateRange {
  start: Date
  end: Date
}

export interface PaginationParams {
  page: number
  per_page: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

// ----------------------------------------------------------------------------
// Mood & Level Configuration (Dojo specific)
// ----------------------------------------------------------------------------
export interface MoodConfig {
  emoji: string
  gradient: string
  bg: string
}

export interface LevelConfig {
  bg: string
  text: string
  border: string
  gradient: string
}

export const MOOD_EMOJIS: Record<PersonaMood, MoodConfig> = {
  happy: { emoji: '😊', gradient: 'from-yellow-400 to-orange-400', bg: 'bg-yellow-50' },
  frustrated: { emoji: '😤', gradient: 'from-red-500 to-pink-500', bg: 'bg-red-50' },
  hurry: { emoji: '🔥', gradient: 'from-orange-500 to-red-600', bg: 'bg-orange-50' },
  hesitant: { emoji: '🤔', gradient: 'from-purple-400 to-indigo-400', bg: 'bg-purple-50' },
  unknown: { emoji: '😶', gradient: 'from-gray-400 to-slate-400', bg: 'bg-gray-50' },
  aggressive: { emoji: '😡', gradient: 'from-red-600 to-rose-700', bg: 'bg-red-50' },
  needy: { emoji: '🥺', gradient: 'from-blue-300 to-cyan-300', bg: 'bg-blue-50' },
}

export const LEVEL_COLORS: Record<ScenarioLevel, LevelConfig> = {
  beginner: { bg: 'bg-emerald-500', text: 'text-emerald-600', border: 'border-emerald-200', gradient: 'from-emerald-500 to-teal-500' },
  intermediate: { bg: 'bg-amber-500', text: 'text-amber-600', border: 'border-amber-200', gradient: 'from-amber-500 to-orange-500' },
  advanced: { bg: 'bg-rose-500', text: 'text-rose-600', border: 'border-rose-200', gradient: 'from-rose-500 to-red-600' },
  expert: { bg: 'bg-purple-500', text: 'text-purple-600', border: 'border-purple-200', gradient: 'from-purple-500 to-pink-500' },
}

// ----------------------------------------------------------------------------
// Export type aliases (avoid conflicts)
// ----------------------------------------------------------------------------
export type {
  Client as ClientType,
  Service as ServiceType,
  Professional as ProfessionalType
}
