"use client";

import { useState, useMemo } from 'react';
import useSWR from 'swr';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Brain,
    Zap,
    Target,
    Smile,
    AlertCircle,
    CheckCircle,
    ChevronRight,
    Trophy,
    TrendingUp,
    ShieldCheck,
    Sparkles,
    Flame,
    Award,
    Activity,
    Play,
    RotateCcw,
    Star,
    MessageSquare,
    User,
    ScrollText,
    Lightbulb,
    ThumbsUp,
    ThumbsDown,
    Swords,
    Gem
} from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

interface Scenario {
    id: string;
    name: string;
    level: string;
    description: string;
    sample_message: string;
    points: number;
}

interface Persona {
    id: string;
    name: string;
    mood: string;
    emoji: string;
    description: string;
    difficulty: number;
}

interface TestResult {
    scenario_name: string;
    persona_name: string;
    user_message: string;
    luna_response: string;
    intent_detected: string;
    confidence_score: number;
    processing_time_ms: number;
    metrics: {
        empathy_score: number;
        clarity_score: number;
        actionability_score: number;
        overall_success: boolean;
        criteria_met: string[];
        criteria_missing: string[];
    };
    success: boolean;
    points_earned: number;
}

// Mood emojis com gradientes
const moodEmojis: any = {
    happy: { emoji: "😊", gradient: "from-yellow-400 to-orange-400", bg: "bg-yellow-50" },
    frustrated: { emoji: "😤", gradient: "from-red-500 to-pink-500", bg: "bg-red-50" },
    hurry: { emoji: "🔥", gradient: "from-orange-500 to-red-600", bg: "bg-orange-50" },
    hesitant: { emoji: "🤔", gradient: "from-purple-400 to-indigo-400", bg: "bg-purple-50" },
    unknown: { emoji: "😶", gradient: "from-gray-400 to-slate-400", bg: "bg-gray-50" },
    aggressive: { emoji: "😡", gradient: "from-red-600 to-rose-700", bg: "bg-red-50" },
    needy: { emoji: "🥺", gradient: "from-blue-300 to-cyan-300", bg: "bg-blue-50" },
};

const levelColors: any = {
    beginner: { bg: 'bg-emerald-500', text: 'text-emerald-600', border: 'border-emerald-200', gradient: 'from-emerald-500 to-teal-500' },
    intermediate: { bg: 'bg-amber-500', text: 'text-amber-600', border: 'border-amber-200', gradient: 'from-amber-500 to-orange-500' },
    advanced: { bg: 'bg-rose-500', text: 'text-rose-600', border: 'border-rose-200', gradient: 'from-rose-500 to-red-600' },
    expert: { bg: 'bg-purple-500', text: 'text-purple-600', border: 'border-purple-200', gradient: 'from-purple-500 to-pink-500' },
};

export default function DojoArena() {
    const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
    const [selectedPersona, setSelectedPersona] = useState<string | null>(null);
    const [customMessage, setCustomMessage] = useState("");
    const [lastResult, setLastResult] = useState<TestResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [testHistory, setTestHistory] = useState<TestResult[]>([]);

    const { data: scenariosData } = useSWR('/api/dojo/scenarios', fetcher);
    const { data: personasData } = useSWR('/api/dojo/personas', fetcher);
    const { data: summary } = useSWR('/api/dojo/metrics/summary', fetcher);

    const scenarios = scenariosData?.scenarios || [];
    const personas = personasData?.personas || [];

    const selectedScenarioData = useMemo(() => 
        scenarios.find((s: Scenario) => s.id === selectedScenario),
        [scenarios, selectedScenario]
    );

    const selectedPersonaData = useMemo(() => 
        personas.find((p: Persona) => p.id === selectedPersona),
        [personas, selectedPersona]
    );

    async function runTest() {
        setLoading(true);
        try {
            const res = await fetch('/api/dojo/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    scenario_id: selectedScenario,
                    persona_id: selectedPersona,
                    message: customMessage || selectedScenarioData?.sample_message || "Oi!"
                })
            });
            const result = await res.json();
            setLastResult(result);
            setTestHistory(prev => [result, ...prev].slice(0, 10));
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    }

    async function submitFeedback(rating: number) {
        if (!lastResult) return;

        await fetch('/api/dojo/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scenario_id: selectedScenario || '',
                persona_id: selectedPersona || '',
                message: lastResult.user_message,
                response: lastResult.luna_response,
                success: lastResult.success,
                rating,
                metrics: lastResult.metrics
            })
        });
    }

    return (
        <div className="flex-1 overflow-y-auto bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
            <div className="max-w-[1800px] mx-auto p-8 space-y-6">

                {/* Header Hero Section */}
                <motion.div 
                    initial={{ opacity: 0, y: -30 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-[2rem] p-8 text-white shadow-2xl shadow-indigo-500/30"
                >
                    {/* Background Pattern */}
                    <div className="absolute inset-0 opacity-10">
                        <div className="absolute top-10 left-10 w-64 h-64 bg-white rounded-full blur-3xl" />
                        <div className="absolute bottom-10 right-10 w-80 h-80 bg-white rounded-full blur-3xl" />
                    </div>

                    <div className="relative z-10">
                        <div className="flex items-start justify-between mb-6">
                            <div>
                                <motion.div 
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.1 }}
                                    className="flex items-center gap-2 mb-3"
                                >
                                    <Swords className="w-5 h-5 text-white/80" />
                                    <span className="text-xs font-black uppercase tracking-[0.3em] text-white/80">
                                        Training Arena
                                    </span>
                                </motion.div>
                                
                                <motion.h1 
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 }}
                                    className="text-5xl font-black tracking-tighter mb-3"
                                >
                                    Dojo Arena <span className="text-6xl">🥋</span>
                                </motion.h1>
                                
                                <motion.p 
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.3 }}
                                    className="text-lg text-white/80 font-medium max-w-xl"
                                >
                                    Teste e aprimore a LUNA em cenários controlados com personas realistas
                                </motion.p>
                            </div>

                            {/* Quick Stats */}
                            <div className="flex gap-3">
                                <QuickStat 
                                    icon={Target} 
                                    value={summary?.total_tests || 0} 
                                    label="Testes"
                                    delay={0.2}
                                />
                                <QuickStat 
                                    icon={Trophy} 
                                    value={summary?.total_points || 0} 
                                    label="Pontos"
                                    delay={0.3}
                                />
                                <QuickStat 
                                    icon={TrendingUp} 
                                    value={`${summary?.success_rate || 0}%`} 
                                    label="Sucesso"
                                    trend={summary?.success_rate > 70 ? 'up' : 'down'}
                                    delay={0.4}
                                />
                            </div>
                        </div>

                        {/* Maturity Score Bar */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 }}
                            className="bg-white/10 backdrop-blur-sm rounded-2xl p-5 border border-white/20"
                        >
                            <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                                        <ShieldCheck className="w-6 h-6 text-white" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-bold text-white/80">Maturity Score</p>
                                        <p className="text-xs text-white/60">Prontidão para produção</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-4xl font-black">{summary?.maturity_score?.score || 0}</p>
                                    <p className="text-xs text-white/60">de 100 pontos</p>
                                </div>
                            </div>
                            
                            {/* Progress Bar */}
                            <div className="relative h-4 bg-white/10 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${summary?.maturity_score?.score || 0}%` }}
                                    transition={{ duration: 1, delay: 0.7 }}
                                    className="absolute inset-y-0 left-0 bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 rounded-full"
                                />
                                {/* Animated shine effect */}
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
                            </div>

                            {/* Recommendation */}
                            <div className="mt-3 flex items-center gap-2">
                                {summary?.maturity_score?.score >= 75 ? (
                                    <span className="inline-flex items-center gap-2 bg-green-500/20 text-green-300 px-3 py-1.5 rounded-full text-xs font-bold border border-green-500/30">
                                        <CheckCircle className="w-3.5 h-3.5" />
                                        {summary.maturity_score.recommendation}
                                    </span>
                                ) : (
                                    <span className="inline-flex items-center gap-2 bg-amber-500/20 text-amber-300 px-3 py-1.5 rounded-full text-xs font-bold border border-amber-500/30">
                                        <Activity className="w-3.5 h-3.5" />
                                        {summary?.maturity_score?.recommendation || "Continue treinando"}
                                    </span>
                                )}
                            </div>
                        </motion.div>
                    </div>
                </motion.div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                    {/* Left Column: Scenarios */}
                    <div className="lg:col-span-1 space-y-4">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="flex items-center gap-2 mb-2"
                        >
                            <ScrollText className="w-5 h-5 text-indigo-600" />
                            <h2 className="text-xl font-black text-gray-900">Cenários</h2>
                            <span className="ml-auto text-xs font-bold text-gray-400 bg-gray-100 px-2 py-1 rounded-full">
                                {scenarios.length} disponíveis
                            </span>
                        </motion.div>

                        <div className="space-y-3">
                            {scenarios.slice(0, 6).map((scenario: Scenario, idx: number) => (
                                <ScenarioCard
                                    key={scenario.id}
                                    scenario={scenario}
                                    selected={selectedScenario === scenario.id}
                                    onSelect={() => setSelectedScenario(scenario.id)}
                                    levelColors={levelColors}
                                    index={idx}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Middle Column: Personas */}
                    <div className="lg:col-span-1 space-y-4">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.1 }}
                            className="flex items-center gap-2 mb-2"
                        >
                            <User className="w-5 h-5 text-purple-600" />
                            <h2 className="text-xl font-black text-gray-900">Personas</h2>
                            <span className="ml-auto text-xs font-bold text-gray-400 bg-gray-100 px-2 py-1 rounded-full">
                                {personas.length} disponíveis
                            </span>
                        </motion.div>

                        <div className="space-y-3">
                            {personas.slice(0, 6).map((persona: Persona, idx: number) => (
                                <PersonaCard
                                    key={persona.id}
                                    persona={persona}
                                    selected={selectedPersona === persona.id}
                                    onSelect={() => setSelectedPersona(persona.id)}
                                    moodEmojis={moodEmojis}
                                    index={idx}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Right Column: Test Area & Results */}
                    <div className="lg:col-span-1 space-y-6">
                        
                        {/* Test Area */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.2 }}
                            className="bg-white rounded-3xl p-6 border-2 border-gray-200 shadow-xl shadow-gray-200/50"
                        >
                            <div className="flex items-center gap-3 mb-4">
                                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
                                    <Brain className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="text-lg font-black text-gray-900">Área de Teste</h3>
                                    <p className="text-xs text-gray-500">Configure e execute testes</p>
                                </div>
                            </div>

                            {/* Selected Info */}
                            {(selectedScenarioData || selectedPersonaData) && (
                                <div className="mb-4 p-4 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl border border-indigo-100">
                                    {selectedScenarioData && (
                                        <div className="mb-3">
                                            <div className="flex items-center gap-2 text-xs font-bold text-indigo-600 mb-1">
                                                <ScrollText className="w-3.5 h-3.5" />
                                                Cenário
                                            </div>
                                            <p className="text-sm font-bold text-gray-900">{selectedScenarioData.name}</p>
                                        </div>
                                    )}
                                    {selectedPersonaData && (
                                        <div>
                                            <div className="flex items-center gap-2 text-xs font-bold text-purple-600 mb-1">
                                                <User className="w-3.5 h-3.5" />
                                                Persona
                                            </div>
                                            <p className="text-sm font-bold text-gray-900">{selectedPersonaData.name}</p>
                                        </div>
                                    )}
                                </div>
                            )}

                            <textarea
                                value={customMessage}
                                onChange={(e) => setCustomMessage(e.target.value)}
                                placeholder={selectedScenarioData?.sample_message || "Digite uma mensagem de teste..."}
                                className="w-full h-32 p-4 bg-gray-50 border-2 border-gray-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-sm font-medium"
                            />

                            <button
                                onClick={runTest}
                                disabled={loading || (!selectedScenario && !customMessage)}
                                className="mt-4 w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-black hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 transition-all shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 active:scale-[0.98]"
                            >
                                {loading ? (
                                    <>
                                        <Zap className="w-5 h-5 animate-spin" />
                                        Processando...
                                    </>
                                ) : (
                                    <>
                                        <Play className="w-5 h-5" />
                                        Executar Teste
                                    </>
                                )}
                            </button>
                        </motion.div>

                        {/* Test History */}
                        {testHistory.length > 0 && (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="bg-white rounded-3xl p-6 border-2 border-gray-200 shadow-xl shadow-gray-200/50"
                            >
                                <div className="flex items-center gap-3 mb-4">
                                    <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg shadow-amber-500/30">
                                        <Activity className="w-5 h-5 text-white" />
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-black text-gray-900">Histórico</h3>
                                        <p className="text-xs text-gray-500">Últimos {testHistory.length} testes</p>
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    {testHistory.slice(0, 5).map((result: TestResult, idx: number) => (
                                        <div
                                            key={idx}
                                            className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100"
                                        >
                                            <div className={`w-2 h-2 rounded-full ${result.success ? 'bg-green-500' : 'bg-red-500'}`} />
                                            <div className="flex-1 min-w-0">
                                                <p className="text-xs font-bold text-gray-900 truncate">{result.scenario_name}</p>
                                                <p className="text-[10px] text-gray-500">{result.persona_name}</p>
                                            </div>
                                            <span className={`text-xs font-black px-2 py-1 rounded-full ${result.success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                                +{result.points_earned} pts
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        )}
                    </div>
                </div>

                {/* Results Section */}
                <AnimatePresence mode="wait">
                    {lastResult && (
                        <motion.div
                            initial={{ opacity: 0, y: 40 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -40 }}
                            className="bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900 rounded-[2rem] p-8 text-white shadow-2xl shadow-gray-900/50 border border-white/10"
                        >
                            {/* Header */}
                            <div className="flex items-center justify-between mb-8">
                                <div className="flex items-center gap-4">
                                    <div className={`w-16 h-16 rounded-3xl flex items-center justify-center ${lastResult.success ? 'bg-gradient-to-br from-green-500 to-emerald-600' : 'bg-gradient-to-br from-red-500 to-rose-600'} shadow-2xl`}>
                                        {lastResult.success ? (
                                            <CheckCircle className="w-8 h-8 text-white" />
                                        ) : (
                                            <AlertCircle className="w-8 h-8 text-white" />
                                        )}
                                    </div>
                                    <div>
                                        <h3 className="text-2xl font-black mb-1">
                                            {lastResult.success ? 'Teste Aprovado!' : 'Precisa Melhorar'}
                                        </h3>
                                        <p className="text-sm text-gray-400">
                                            {lastResult.scenario_name} • {lastResult.persona_name}
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    <div className="text-right">
                                        <p className="text-xs text-gray-400 font-bold mb-1">Pontos Ganhos</p>
                                        <p className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                                            +{lastResult.points_earned}
                                        </p>
                                    </div>
                                    <Gem className="w-12 h-12 text-indigo-400" />
                                </div>
                            </div>

                            {/* Response Display */}
                            <div className="mb-8">
                                <div className="flex items-center gap-2 mb-3">
                                    <MessageSquare className="w-5 h-5 text-indigo-400" />
                                    <p className="text-sm font-bold text-gray-400">Resposta da LUNA:</p>
                                </div>
                                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
                                    <p className="text-base leading-relaxed">{lastResult.luna_response}</p>
                                </div>
                            </div>

                            {/* Quick Stats Grid */}
                            <div className="grid grid-cols-4 gap-4 mb-8">
                                <QuickStatCard
                                    icon={Zap}
                                    label="Tempo"
                                    value={`${lastResult.processing_time_ms}ms`}
                                    color="text-yellow-400"
                                    bg="bg-yellow-500/10"
                                />
                                <QuickStatCard
                                    icon={Brain}
                                    label="Intent"
                                    value={lastResult.intent_detected}
                                    color="text-blue-400"
                                    bg="bg-blue-500/10"
                                />
                                <QuickStatCard
                                    icon={Target}
                                    label="Confiança"
                                    value={`${(lastResult.confidence_score * 100).toFixed(0)}%`}
                                    color="text-green-400"
                                    bg="bg-green-500/10"
                                />
                                <QuickStatCard
                                    icon={Star}
                                    label="Pontos"
                                    value={lastResult.points_earned}
                                    color="text-purple-400"
                                    bg="bg-purple-500/10"
                                />
                            </div>

                            {/* Detailed Metrics */}
                            <div className="grid grid-cols-3 gap-6 mb-8">
                                <MetricCard
                                    label="Empatia"
                                    value={lastResult.metrics.empathy_score}
                                    max={100}
                                    color="from-pink-500 to-rose-500"
                                    icon={Smile}
                                />
                                <MetricCard
                                    label="Clareza"
                                    value={lastResult.metrics.clarity_score}
                                    max={100}
                                    color="from-blue-500 to-cyan-500"
                                    icon={Sparkles}
                                />
                                <MetricCard
                                    label="Acionabilidade"
                                    value={lastResult.metrics.actionability_score}
                                    max={100}
                                    color="from-green-500 to-emerald-500"
                                    icon={CheckCircle}
                                />
                            </div>

                            {/* Criteria */}
                            <div className="grid grid-cols-2 gap-6 mb-8">
                                <div className="bg-green-500/10 rounded-2xl p-6 border border-green-500/20">
                                    <div className="flex items-center gap-2 mb-4">
                                        <CheckCircle className="w-5 h-5 text-green-400" />
                                        <p className="text-sm font-bold text-green-400">Critérios Atendidos</p>
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                        {lastResult.metrics.criteria_met.map((criterion, idx) => (
                                            <span
                                                key={idx}
                                                className="px-3 py-1.5 bg-green-500/20 text-green-300 rounded-full text-xs font-bold border border-green-500/30"
                                            >
                                                {criterion}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div className="bg-red-500/10 rounded-2xl p-6 border border-red-500/20">
                                    <div className="flex items-center gap-2 mb-4">
                                        <AlertCircle className="w-5 h-5 text-red-400" />
                                        <p className="text-sm font-bold text-red-400">Critérios Faltando</p>
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                        {lastResult.metrics.criteria_missing.map((criterion, idx) => (
                                            <span
                                                key={idx}
                                                className="px-3 py-1.5 bg-red-500/20 text-red-300 rounded-full text-xs font-bold border border-red-500/30"
                                            >
                                                {criterion}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Feedback Section */}
                            <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
                                <div className="flex items-center gap-3 mb-4">
                                    <Award className="w-5 h-5 text-amber-400" />
                                    <p className="text-sm font-bold text-gray-400">Sua Avaliação:</p>
                                </div>
                                <div className="flex gap-3">
                                    {[1, 2, 3, 4, 5].map((rating) => (
                                        <motion.button
                                            key={rating}
                                            whileHover={{ scale: 1.1 }}
                                            whileTap={{ scale: 0.95 }}
                                            onClick={() => submitFeedback(rating)}
                                            className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 transition-all font-black text-lg flex items-center justify-center shadow-lg shadow-indigo-500/30"
                                        >
                                            {rating}
                                        </motion.button>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

            </div>
        </div>
    );
}

// Components

function QuickStat({ icon: Icon, value, label, trend, delay }: any) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay }}
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 min-w-[120px]"
        >
            <div className="flex items-center gap-2 mb-2">
                <Icon className="w-4 h-4 text-white/80" />
                {trend && (
                    <TrendingUp className={`w-3.5 h-3.5 ${trend === 'up' ? 'text-green-300' : 'text-red-300'}`} />
                )}
            </div>
            <p className="text-2xl font-black">{value}</p>
            <p className="text-xs text-white/60 font-bold">{label}</p>
        </motion.div>
    );
}

function ScenarioCard({ scenario, selected, onSelect, levelColors, index }: any) {
    const level = levelColors[scenario.level] || levelColors.beginner;

    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onSelect}
            className={`p-5 rounded-2xl border-2 cursor-pointer transition-all shadow-sm hover:shadow-md ${
                selected
                    ? 'border-indigo-500 bg-gradient-to-br from-indigo-50 to-purple-50 shadow-indigo-200'
                    : 'border-gray-200 bg-white hover:border-indigo-300'
            }`}
        >
            <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                        <p className="font-bold text-gray-900">{scenario.name}</p>
                        <span className={`w-2 h-2 rounded-full bg-gradient-to-r ${level.gradient}`} />
                    </div>
                    <p className="text-sm text-gray-500">{scenario.description}</p>
                </div>
                <div className="flex flex-col items-end gap-2">
                    <span className="text-xs font-black text-indigo-600 bg-indigo-50 px-2 py-1 rounded-full">
                        +{scenario.points} pts
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r ${level.gradient} text-white`}>
                        {scenario.level === 'beginner' ? 'Iniciante' :
                         scenario.level === 'intermediate' ? 'Intermediário' :
                         scenario.level === 'advanced' ? 'Avançado' : 'Expert'}
                    </span>
                </div>
            </div>
        </motion.div>
    );
}

function PersonaCard({ persona, selected, onSelect, moodEmojis, index }: any) {
    const moodData = moodEmojis[persona.mood] || moodEmojis.unknown;

    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 + 0.1 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onSelect}
            className={`p-5 rounded-2xl border-2 cursor-pointer transition-all shadow-sm hover:shadow-md ${
                selected
                    ? 'border-purple-500 bg-gradient-to-br from-purple-50 to-pink-50 shadow-purple-200'
                    : 'border-gray-200 bg-white hover:border-purple-300'
            }`}
        >
            <div className="flex items-center gap-4">
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${moodData.gradient} flex items-center justify-center text-3xl shadow-lg`}>
                    {moodData.emoji}
                </div>
                <div className="flex-1">
                    <p className="font-bold text-gray-900">{persona.name}</p>
                    <p className="text-sm text-gray-500">{persona.description}</p>
                </div>
                <div className="flex items-center gap-1">
                    {[...Array(5)].map((_, i) => (
                        <Flame
                            key={i}
                            className={`w-4 h-4 ${i < persona.difficulty ? 'text-orange-500 fill-orange-500' : 'text-gray-300'}`}
                        />
                    ))}
                </div>
            </div>
        </motion.div>
    );
}

function QuickStatCard({ icon: Icon, label, value, color, bg }: any) {
    return (
        <div className={`${bg} rounded-2xl p-4 border border-white/10`}>
            <div className="flex items-center gap-2 mb-2">
                <Icon className={`w-4 h-4 ${color}`} />
                <span className="text-[10px] font-bold text-gray-400 uppercase">{label}</span>
            </div>
            <p className="text-xl font-black text-white">{value}</p>
        </div>
    );
}

function MetricCard({ label, value, max, color, icon: Icon }: any) {
    const percentage = (value / max) * 100;

    return (
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center shadow-lg`}>
                        <Icon className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-sm font-bold text-gray-400">{label}</span>
                </div>
                <span className="text-2xl font-black text-white">{value}</span>
            </div>

            {/* Progress Bar */}
            <div className="relative h-3 bg-white/10 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className={`absolute inset-y-0 left-0 bg-gradient-to-r ${color} rounded-full`}
                />
            </div>

            <div className="mt-2 text-right">
                <span className="text-xs font-bold text-gray-400">{percentage.toFixed(0)}% de {max}</span>
            </div>
        </div>
    );
}
