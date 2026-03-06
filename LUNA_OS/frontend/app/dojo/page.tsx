"use client";

import { useState, useCallback } from 'react';
import useSWR from 'swr';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  Target, 
  CheckCircle, 
  AlertCircle,
  Play,
  RefreshCcw,
  MessageSquare,
  TrendingUp,
  ShieldCheck,
  Swords,
  User,
  ScrollText
} from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

interface TestScenario {
  id: string;
  name: string;
  category: 'atendimento' | 'vendas' | 'suporte' | 'emergencia';
  message: string;
  expected_intent: string;
}

interface TestResult {
  scenario_id: string;
  intent_detected: string;
  confidence: number;
  response_time_ms: number;
  success: boolean;
  response: string;
}

const SCENARIOS: TestScenario[] = [
  {
    id: '1',
    name: 'Agendamento de Horário',
    category: 'atendimento',
    message: 'Quero agendar um horário para fazer as unhas amanhã às 14h',
    expected_intent: 'schedule_appointment'
  },
  {
    id: '2',
    name: 'Consulta de Preços',
    category: 'vendas',
    message: 'Qual o preço da escova progressiva?',
    expected_intent: 'price_inquiry'
  },
  {
    id: '3',
    name: 'Cancelamento',
    category: 'atendimento',
    message: 'Preciso cancelar meu horário de amanhã',
    expected_intent: 'cancel_appointment'
  },
  {
    id: '4',
    name: 'Reclamação',
    category: 'suporte',
    message: 'Estou insatisfeita com o atendimento de ontem',
    expected_intent: 'complaint'
  },
  {
    id: '5',
    name: 'Emergência',
    category: 'emergencia',
    message: 'Preciso de atendimento urgente para hoje!',
    expected_intent: 'urgent_request'
  },
  {
    id: '6',
    name: 'Dúvida sobre Serviços',
    category: 'vendas',
    message: 'Vocês fazem alongamento de cílios?',
    expected_intent: 'service_inquiry'
  }
];

const CATEGORY_COLORS: Record<string, string> = {
  atendimento: 'bg-blue-500',
  vendas: 'bg-green-500',
  suporte: 'bg-orange-500',
  emergencia: 'bg-red-500'
};

export default function DojoArena() {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const { data: metrics } = useSWR('/api/dojo/metrics/summary', fetcher, {
    refreshInterval: 10000
  });

  const runTest = useCallback(async (scenarioId: string) => {
    setIsRunning(true);
    try {
      const scenario = SCENARIOS.find(s => s.id === scenarioId);
      if (!scenario) return;

      const response = await fetch('/api/brain/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: scenario.message,
          name: 'Test User',
          phone: '5549900000000'
        })
      });

      const result = await response.json();
      
      const testResult: TestResult = {
        scenario_id: scenarioId,
        intent_detected: result.intent || 'unknown',
        confidence: result.intent_confidence || 0,
        response_time_ms: result.processing_ms || 0,
        success: result.intent === scenario.expected_intent,
        response: result.response || ''
      };

      setTestResults(prev => [testResult, ...prev].slice(0, 10));
    } catch (error) {
      console.error('Test failed:', error);
    } finally {
      setIsRunning(false);
    }
  }, []);

  const runAllTests = useCallback(async () => {
    setIsRunning(true);
    for (const scenario of SCENARIOS) {
      await runTest(scenario.id);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    setIsRunning(false);
  }, [runTest]);

  const successRate = testResults.length > 0
    ? (testResults.filter(r => r.success).length / testResults.length * 100).toFixed(0)
    : 0;

  const avgResponseTime = testResults.length > 0
    ? Math.round(testResults.reduce((acc, r) => acc + r.response_time_ms, 0) / testResults.length)
    : 0;

  return (
    <div className="flex-1 overflow-y-auto bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-8">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-3xl p-8 text-white shadow-2xl">
          <div className="flex items-start justify-between mb-6">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Swords className="w-5 h-5 text-white/80" />
                <span className="text-xs font-black uppercase tracking-[0.3em] text-white/80">
                  AI Training Arena
                </span>
              </div>
              <h1 className="text-4xl font-black tracking-tighter mb-2">
                Dojo Arena <span className="text-5xl">🥋</span>
              </h1>
              <p className="text-lg text-white/80 font-medium">
                Teste e aprimore a LUNA em cenários do mundo real
              </p>
            </div>

            <button
              onClick={runAllTests}
              disabled={isRunning}
              className="flex items-center gap-3 bg-white/20 backdrop-blur-sm hover:bg-white/30 disabled:opacity-50 px-6 py-4 rounded-2xl font-bold transition-all"
            >
              {isRunning ? (
                <>
                  <RefreshCcw className="w-5 h-5 animate-spin" />
                  Testando...
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" />
                  Rodar Todos Testes
                </>
              )}
            </button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              icon={Target}
              value={testResults.length}
              label="Testes Rodados"
              color="bg-white/20"
            />
            <StatCard
              icon={CheckCircle}
              value={`${successRate}%`}
              label="Taxa de Acerto"
              color="bg-green-500/30"
            />
            <StatCard
              icon={Zap}
              value={`${avgResponseTime}ms`}
              label="Tempo Médio"
              color="bg-yellow-500/30"
            />
            <StatCard
              icon={ShieldCheck}
              value={metrics?.maturity_score?.score || 0}
              label="Maturity Score"
              color="bg-purple-500/30"
            />
          </div>
        </div>

        {/* Test Scenarios */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Scenarios List */}
          <div className="bg-white rounded-3xl p-6 shadow-xl border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <ScrollText className="w-6 h-6 text-indigo-600" />
              <h2 className="text-xl font-black text-gray-900">Cenários de Teste</h2>
              <span className="ml-auto text-xs font-bold text-gray-400 bg-gray-100 px-3 py-1 rounded-full">
                {SCENARIOS.length} disponíveis
              </span>
            </div>

            <div className="space-y-3">
              {SCENARIOS.map((scenario) => (
                <div
                  key={scenario.id}
                  className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
                    selectedScenario === scenario.id
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-indigo-300'
                  }`}
                  onClick={() => setSelectedScenario(scenario.id)}
                >
                  <div className="flex items-start gap-3">
                    <span className={`w-3 h-3 rounded-full mt-1.5 ${CATEGORY_COLORS[scenario.category]}`} />
                    <div className="flex-1">
                      <p className="font-bold text-gray-900">{scenario.name}</p>
                      <p className="text-sm text-gray-500 mt-1">{scenario.message}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 bg-gray-100 px-2 py-0.5 rounded">
                          {scenario.category}
                        </span>
                        <span className="text-[10px] text-gray-400">
                          Esperado: {scenario.expected_intent}
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        runTest(scenario.id);
                      }}
                      disabled={isRunning}
                      className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg disabled:opacity-50"
                    >
                      <Play className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Results */}
          <div className="bg-white rounded-3xl p-6 shadow-xl border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-6 h-6 text-purple-600" />
              <h2 className="text-xl font-black text-gray-900">Resultados Recentes</h2>
              {testResults.length > 0 && (
                <button
                  onClick={() => setTestResults([])}
                  className="ml-auto text-xs text-gray-400 hover:text-gray-600"
                >
                  Limpar
                </button>
              )}
            </div>

            {testResults.length === 0 ? (
              <div className="h-64 flex flex-col items-center justify-center text-center text-gray-400">
                <Brain className="w-16 h-16 mb-4 opacity-20" />
                <p className="font-semibold">Nenhum teste rodado ainda</p>
                <p className="text-sm mt-1">Selecione um cenário e clique em testar</p>
              </div>
            ) : (
              <div className="space-y-3">
                {testResults.map((result, idx) => {
                  const scenario = SCENARIOS.find(s => s.id === result.scenario_id);
                  return (
                    <div
                      key={idx}
                      className={`p-4 rounded-2xl border-l-4 ${
                        result.success
                          ? 'bg-green-50 border-green-500'
                          : 'bg-red-50 border-red-500'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            {result.success ? (
                              <CheckCircle className="w-4 h-4 text-green-600" />
                            ) : (
                              <AlertCircle className="w-4 h-4 text-red-600" />
                            )}
                            <span className="font-bold text-gray-900">
                              {scenario?.name || `Teste ${result.scenario_id}`}
                            </span>
                          </div>
                          <div className="mt-2 text-sm text-gray-600">
                            <p><span className="font-semibold">Detectado:</span> {result.intent_detected} ({(result.confidence * 100).toFixed(0)}%)</p>
                            <p><span className="font-semibold">Tempo:</span> {result.response_time_ms}ms</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, value, label, color }: any) {
  return (
    <div className={`${color} backdrop-blur-sm rounded-2xl p-4`}>
      <div className="flex items-center gap-2 mb-2">
        <Icon className="w-4 h-4 text-white/80" />
      </div>
      <p className="text-2xl font-black text-white">{value}</p>
      <p className="text-xs text-white/80 font-bold">{label}</p>
    </div>
  );
}
