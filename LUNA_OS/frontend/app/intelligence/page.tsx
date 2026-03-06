"use client";

import { useState } from 'react';
import useSWR from 'swr';
import { motion } from 'framer-motion';
import type { IntelligenceProposal, EdgeCase, ClientIntelligence } from '@/types';
import {
  Brain,
  TrendingUp,
  Users,
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock,
  ThumbsUp,
  ThumbsDown,
  Sparkles,
  Target,
  MessageSquare,
  Lightbulb,
  RefreshCcw,
  ChevronRight,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

type Tab = 'proposals' | 'clients' | 'edge-cases'

function getCategoryColor(category: string) {
  const colors: Record<string, string> = {
    INTENT: 'bg-red-100 text-red-700',
    TONE: 'bg-orange-100 text-orange-700',
    INFORMATION: 'bg-yellow-100 text-yellow-700',
    FLOW: 'bg-blue-100 text-blue-700',
    ESCALATION: 'bg-purple-100 text-purple-700'
  };
  return colors[category] || 'bg-gray-100 text-gray-700';
}

function getStatusColor(status: string) {
  const colors: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
    new: 'bg-blue-100 text-blue-700',
    added_to_dojo: 'bg-green-100 text-green-700',
    dismissed: 'bg-gray-100 text-gray-700'
  };
  return colors[status] || 'bg-gray-100 text-gray-700';
}

export default function IntelligencePage() {
  const [activeTab, setActiveTab] = useState<Tab>('proposals');
  const [selectedClient, setSelectedClient] = useState<string>('');
  const [clientSearch, setClientSearch] = useState('');

  // Fetch proposals
  const { data: proposalsData, mutate: mutateProposals } = useSWR(
    '/api/dojo/proposals?status=pending&limit=50',
    fetcher,
    { refreshInterval: 30000 }
  );

  // Fetch edge cases
  const { data: edgeCasesData, mutate: mutateEdgeCases } = useSWR(
    '/api/dojo/edge-cases?status=new&limit=50',
    fetcher,
    { refreshInterval: 30000 }
  );

  // Fetch business insights
  const { data: insightsData } = useSWR(
    '/api/intelligence/insights?days=30&group_by=day',
    fetcher,
    { refreshInterval: 60000 }
  );

  // Fetch client intelligence
  const { data: clientData } = useSWR(
    clientSearch ? `/api/intelligence/client/${clientSearch}` : null,
    fetcher
  );

  const proposals: IntelligenceProposal[] = proposalsData?.proposals || [];
  const edgeCases: EdgeCase[] = edgeCasesData?.edge_cases || [];
  const insights = insightsData?.insights || [];
  const metrics = insightsData?.metrics || {};

  async function handleApprove(proposalId: string) {
    try {
      const res = await fetch(`/api/dojo/proposals/${proposalId}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approved_by: 'admin',
          apply_to_prompt: true
        })
      });

      if (res.ok) {
        mutateProposals();
        alert('✅ Proposal approved!');
      } else {
        alert('❌ Failed to approve');
      }
    } catch (e) {
      alert('Error: ' + e);
    }
  }

  async function handleReject(proposalId: string) {
    const reason = prompt('Reason for rejection:');
    if (!reason) return;

    try {
      const res = await fetch(`/api/dojo/proposals/${proposalId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rejected_by: 'admin',
          reason
        })
      });

      if (res.ok) {
        mutateProposals();
        alert('✅ Proposal rejected');
      } else {
        alert('❌ Failed to reject');
      }
    } catch (e) {
      alert('Error: ' + e);
    }
  }

  async function handleConvertEdgeCase(edgeCaseId: string) {
    const scenarioName = prompt('Scenario name:');
    if (!scenarioName) return;

    try {
      const res = await fetch(`/api/dojo/edge-cases/${edgeCaseId}/convert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_name: scenarioName,
          scenario_level: 'intermediate',
          expected_behavior: 'LUNA should resolve without handoff'
        })
      });

      if (res.ok) {
        mutateEdgeCases();
        alert('✅ Edge case converted to Dojo scenario!');
      } else {
        alert('❌ Failed to convert');
      }
    } catch (e) {
      alert('Error: ' + e);
    }
  }

  return (
    <div className="flex-1 overflow-y-auto bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="max-w-[1800px] mx-auto p-8 space-y-6">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-[2rem] p-8 text-white shadow-2xl shadow-indigo-500/30"
        >
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <Brain className="w-8 h-8 text-white/80" />
              <span className="text-sm font-black uppercase tracking-[0.3em] text-white/80">
                Intelligence Hub
              </span>
            </div>

            <h1 className="text-5xl font-black tracking-tighter mb-3">
              Business Intelligence
            </h1>

            <p className="text-lg text-white/80 font-medium max-w-2xl">
              Dojo Learning Cycle, Client Intelligence, and Edge Cases
            </p>
          </div>

          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-10 left-10 w-64 h-64 bg-white rounded-full blur-3xl" />
            <div className="absolute bottom-10 right-10 w-80 h-80 bg-white rounded-full blur-3xl" />
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex gap-2 border-b-2 border-gray-200">
          <button
            onClick={() => setActiveTab('proposals')}
            className={`px-6 py-3 font-bold uppercase tracking-wider transition-all ${activeTab === 'proposals'
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            <div className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5" />
              Dojo Proposals
              {proposals.length > 0 && (
                <span className="bg-indigo-600 text-white text-xs px-2 py-0.5 rounded-full">
                  {proposals.length}
                </span>
              )}
            </div>
          </button>

          <button
            onClick={() => setActiveTab('clients')}
            className={`px-6 py-3 font-bold uppercase tracking-wider transition-all ${activeTab === 'clients'
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              Client Intelligence
            </div>
          </button>

          <button
            onClick={() => setActiveTab('edge-cases')}
            className={`px-6 py-3 font-bold uppercase tracking-wider transition-all ${activeTab === 'edge-cases'
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Edge Cases
              {edgeCases.length > 0 && (
                <span className="bg-indigo-600 text-white text-xs px-2 py-0.5 rounded-full">
                  {edgeCases.length}
                </span>
              )}
            </div>
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'proposals' && (
          <div className="space-y-6">
            {/* Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <MetricCard
                title="Pending Proposals"
                value={proposals.length}
                icon={Lightbulb}
                color="indigo"
              />
              <MetricCard
                title="This Week"
                value={metrics.total_conversations || 0}
                icon={Clock}
                color="blue"
              />
              <MetricCard
                title="Avg Conversion"
                value={`${metrics.health_score || 0}%`}
                icon={TrendingUp}
                color="green"
              />
              <MetricCard
                title="Top Objection"
                value={metrics.top_objections?.[0]?.[0] || 'N/A'}
                icon={AlertCircle}
                color="orange"
              />
            </div>

            {/* Proposals List */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-2xl font-black text-gray-900 mb-6">
                Pending Proposals
              </h2>

              {proposals.length === 0 ? (
                <div className="text-center py-12">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <p className="text-gray-600 font-medium">
                    No pending proposals! All systems working well.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {proposals.map((proposal) => (
                    <ProposalCard
                      key={proposal.id}
                      proposal={proposal}
                      onApprove={() => handleApprove(proposal.id)}
                      onReject={() => handleReject(proposal.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'clients' && (
          <div className="space-y-6">
            {/* Search */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-2xl font-black text-gray-900 mb-4">
                Search Client
              </h2>

              <div className="flex gap-4">
                <input
                  type="text"
                  value={clientSearch}
                  onChange={(e) => setClientSearch(e.target.value)}
                  placeholder="Enter phone number (e.g., 5549991112233)"
                  className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:outline-none"
                />
                <button className="px-6 py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors">
                  Search
                </button>
              </div>
            </div>

            {/* Client Intelligence */}
            {clientData && (
              <ClientIntelligenceCard data={clientData} />
            )}
          </div>
        )}

        {activeTab === 'edge-cases' && (
          <div className="space-y-6">
            {/* Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <MetricCard
                title="New Edge Cases"
                value={edgeCases.length}
                icon={AlertCircle}
                color="red"
              />
              <MetricCard
                title="Converted to Dojo"
                value={edgeCases.filter(ec => ec.status === 'converted').length}
                icon={CheckCircle}
                color="green"
              />
              <MetricCard
                title="This Week"
                value={metrics.total_conversations || 0}
                icon={Clock}
                color="blue"
              />
            </div>

            {/* Edge Cases List */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-2xl font-black text-gray-900 mb-6">
                Edge Cases
              </h2>

              {edgeCases.length === 0 ? (
                <div className="text-center py-12">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <p className="text-gray-600 font-medium">
                    No edge cases! LUNA is handling all conversations well.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {edgeCases.map((edgeCase) => (
                    <EdgeCaseCard
                      key={edgeCase.id}
                      edgeCase={edgeCase}
                      onConvert={() => handleConvertEdgeCase(edgeCase.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Metric Card Component
function MetricCard({ title, value, icon: Icon, color }: any) {
  const colors: Record<string, string> = {
    indigo: 'from-indigo-500 to-purple-500',
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-green-500 to-emerald-500',
    orange: 'from-orange-500 to-red-500',
    red: 'from-red-500 to-pink-500'
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colors[color]} flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-1">
        {title}
      </p>
      <p className="text-3xl font-black text-gray-900">
        {value}
      </p>
    </div>
  );
}

// Proposal Card Component
function ProposalCard({ proposal, onApprove, onReject }: any) {
  return (
    <div className="border-2 border-gray-200 rounded-xl p-6 hover:border-indigo-300 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 rounded-full text-xs font-black uppercase ${getCategoryColor(proposal.failure_category)}`}>
            {proposal.failure_category}
          </span>
          <span className="text-sm text-gray-500 font-medium">
            {proposal.week_reference}
          </span>
        </div>
        <span className="text-xs text-gray-400 font-medium">
          {new Date(proposal.created_at).toLocaleDateString()}
        </span>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-2">
          Failure Count
        </p>
        <p className="text-2xl font-black text-gray-900">
          {proposal.failure_count} failures this week
        </p>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-2">
          Proposed Change
        </p>
        <div className="bg-indigo-50 rounded-lg p-4">
          <p className="text-gray-800 font-medium">
            {proposal.proposed_text || proposal.justification}
          </p>
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={onApprove}
          className="flex-1 px-4 py-3 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
        >
          <ThumbsUp className="w-5 h-5" />
          Approve
        </button>
        <button
          onClick={onReject}
          className="flex-1 px-4 py-3 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
        >
          <ThumbsDown className="w-5 h-5" />
          Reject
        </button>
      </div>
    </div>
  );
}

// Client Intelligence Card Component
function ClientIntelligenceCard({ data }: any) {
  const { client, intelligence } = data;

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <div className="flex items-center gap-4 mb-6">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white text-2xl font-black">
          {client.name?.[0] || client.phone?.slice(-2) || 'C'}
        </div>
        <div>
          <h2 className="text-2xl font-black text-gray-900">
            {client.name || 'Unknown Client'}
          </h2>
          <p className="text-gray-600 font-medium">{client.phone}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-indigo-50 rounded-xl p-4">
          <p className="text-sm text-indigo-600 font-bold uppercase tracking-wider mb-2">
            Emotional State
          </p>
          <p className="text-xl font-black text-gray-900">
            {intelligence.dominant_emotional_state || 'N/A'}
          </p>
        </div>

        <div className="bg-purple-50 rounded-xl p-4">
          <p className="text-sm text-purple-600 font-bold uppercase tracking-wider mb-2">
            Trust Level
          </p>
          <p className="text-xl font-black text-gray-900">
            {intelligence.trust_level || 'N/A'}
          </p>
        </div>

        <div className="bg-green-50 rounded-xl p-4">
          <p className="text-sm text-green-600 font-bold uppercase tracking-wider mb-2">
            Conversations
          </p>
          <p className="text-xl font-black text-gray-900">
            {intelligence.total_conversations || 0}
          </p>
        </div>

        <div className="bg-orange-50 rounded-xl p-4">
          <p className="text-sm text-orange-600 font-bold uppercase tracking-wider mb-2">
            Opportunities
          </p>
          <p className="text-xl font-black text-gray-900">
            {intelligence.opportunities?.length || 0}
          </p>
        </div>
      </div>

      {intelligence.opportunities?.length > 0 && (
        <div className="mb-6">
          <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-3">
            Upsell Opportunities
          </p>
          <div className="flex flex-wrap gap-2">
            {intelligence.opportunities.map((opp: string, i: number) => (
              <span key={i} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-bold">
                {opp}
              </span>
            ))}
          </div>
        </div>
      )}

      {intelligence.objections?.length > 0 && (
        <div>
          <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-3">
            Objections Raised
          </p>
          <div className="flex flex-wrap gap-2">
            {intelligence.objections.map((obj: string, i: number) => (
              <span key={i} className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-bold">
                {obj}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Edge Case Card Component
function EdgeCaseCard({ edgeCase, onConvert }: any) {
  return (
    <div className="border-2 border-gray-200 rounded-xl p-6 hover:border-red-300 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-red-500" />
          <span className={`px-3 py-1 rounded-full text-xs font-black uppercase ${getStatusColor(edgeCase.status)}`}>
            {edgeCase.status}
          </span>
        </div>
        <span className="text-xs text-gray-400 font-medium">
          {new Date(edgeCase.created_at).toLocaleDateString()}
        </span>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-2">
          Situation
        </p>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-gray-800 font-medium whitespace-pre-line">
            {edgeCase.situation_description}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-2">
            Why LUNA Failed
          </p>
          <p className="text-gray-700 font-medium">
            {edgeCase.why_luna_failed}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-600 font-bold uppercase tracking-wider mb-2">
            Expected Behavior
          </p>
          <p className="text-gray-700 font-medium">
            {edgeCase.expected_behavior}
          </p>
        </div>
      </div>

      {edgeCase.status === 'new' && (
        <button
          onClick={onConvert}
          className="w-full px-4 py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2"
        >
          <RefreshCcw className="w-5 h-5" />
          Convert to Dojo Scenario
        </button>
      )}
    </div>
  );
}
