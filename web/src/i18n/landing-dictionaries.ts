export type LandingDictionary = {
  nav: { benefits: string; features: string; workflows: string; testimonials: string; sponsored: string; contribute: string; faq: string; docs: string };
  hero: { title: string; subtitle: string; getStarted: string; github: string };
  stack: { title: string; items: [string, string, string, string, string, string] };
  benefits: { eyebrow: string; title: string; subtitle: string; items: { title: string; description: string }[] };
  features: { eyebrow: string; title: string; subtitle: string; items: { title: string; description: string }[] };
  workflows: { eyebrow: string; title: string; subtitle: string; core: string; browseAll: string; items: { title: string; description: string; highlight?: boolean }[] };
  testimonials: { title: string; subtitle: string; items: { name: string; role: string; comment: string; clamp: string; className?: string }[] };
  sponsored: { eyebrow: string; title: string; subtitle: string; platinum: string; unikornBlurb: string; visitSponsor: string; becomeTitle: string; becomeDesc: string; talk: string; coffee: string; wantBrand: string; reachOut: string };
  contribute: { eyebrow: string; title: string; subtitle: string; starLabel: string; guide: string; loading: string; empty: string; commits: string; viewAll: string };
  faq: { eyebrow: string; title: string; items: { value: string; question: string; answer: string }[] };
  footer: { blurb: string; product: string; resources: string; community: string; legal: string; documentation: string; agents: string; skills: string; workflows: string; installation: string; cli: string; changelog: string; github: string; issues: string; discussions: string; license: string; security: string; credit: string };
};

type LandingOverrides = { [K in keyof LandingDictionary]?: Partial<LandingDictionary[K]> };

const testimonials = [
  { name: "winniwoods", role: "GitHub · #38", comment: "First of all, thank you for this amazing project! I've been using the Antigravity Kit and really enjoy the workflow.", clamp: "line-clamp-3" },
  { name: "ghiemer", role: "GitHub · #23", comment: "Good work with antigravity-kit. Love it — Cheers.", clamp: "line-clamp-2" },
  { name: "AlexOptimizer", role: "GitHub · #66", comment: "The separation into specialized agents and pluggable skills prevents AI context overload.", clamp: "line-clamp-3" },
  { name: "DRYN07", role: "GitHub · #67", comment: "Yours seems quite well-organized, so I thought I'd give it a try.", clamp: "line-clamp-2", className: "hidden md:block" },
  { name: "kkkasio", role: "GitHub · #38", comment: "I support the idea — the tool is really quite robust for new environments like Node.", clamp: "line-clamp-2", className: "hidden md:block" },
  { name: "pragnyanramtha", role: "GitHub · #69", comment: "Antigravity now also supports .agents/ and it helps extensibility when installing other skills.", clamp: "line-clamp-3", className: "hidden lg:block" },
];

export const landingEn: LandingDictionary = {
  nav: { benefits: "Benefits", features: "Features", workflows: "Flow", testimonials: "Testimonials", sponsored: "Sponsored", contribute: "Contribute", faq: "FAQ", docs: "Docs" },
  hero: { title: "Run AI coding agents with less context and more proof", subtitle: "A tiny shared core, 18 hot-loaded skills, four permanent agents, local-first memory, MCP, preflight gates, and read-only cross-audit across 16 runtime targets.", getStarted: "Get started", github: "GitHub" },
  stack: { title: "Small core. Wide runtime reach.", items: ["1 Core", "18 Skills", "4 Agents", "16 Runtimes", "MCP + Memory", "Open source"] },
  benefits: {
    eyebrow: "Benefits", title: "Less framework in context. More useful work.", subtitle: "AG Kit keeps permanent context intentionally small and loads behavior, domain knowledge, specialists, and verification only when the task needs them.",
    items: [
      { title: "Protect the context budget", description: "One tiny resident core replaces a pile of always-on personas and duplicated workflow instructions." },
      { title: "Use one brain across runtimes", description: "Shared behavior lives in one canonical source, while capability-aware adapters translate it for each supported runtime." },
      { title: "Keep memory local and readable", description: "Markdown remains canonical project memory; SQLite FTS5 is optional acceleration that can always be rebuilt." },
      { title: "Verify instead of guessing", description: "Preflight, runtime doctor, CI, and independent read-only cross-audit produce evidence and receipts." },
    ],
  },
  features: {
    eyebrow: "Features", title: "An operating layer, not a prompt warehouse", subtitle: "Behavior, knowledge, runtime adapters, project state, and verification stay separate so every layer remains small and testable.",
    items: [
      { title: "18 hot-loaded skills", description: "Capabilities load only when relevant instead of permanently occupying every session." },
      { title: "Four permanent agents", description: "Scout, architect, builder, and reviewer form the stable core; project specialists are generated only when needed." },
      { title: "One development spine", description: "QUICK, STANDARD, and DEEP modes share one flow with explicit gates instead of competing workflow engines." },
      { title: "16 runtime targets", description: "First-class, connected, and bridge tiers expose only surfaces AG Kit has actually verified." },
      { title: "Project-local MCP", description: "Memory, teams, runtime state, and audit capabilities can be shared without pretending every runtime has native parity." },
      { title: "Safe lifecycle", description: "Runtime install records ownership and backups; doctor verifies real wiring and uninstall preserves drift and project memory." },
    ],
  },
  workflows: {
    eyebrow: "Execution flow", title: "One spine, three levels of depth", subtitle: "The same operating model scales from a one-file fix to a multi-system migration.", core: "Core", browseAll: "Read the flow architecture",
    items: [
      { title: "QUICK", description: "Classify, load the minimum skill, build, run targeted verification, and return the result." },
      { title: "STANDARD", description: "Scout the codebase, define the plan, build, review independently, then verify acceptance criteria." },
      { title: "DEEP", description: "Map risks and dependencies, execute in waves, cross-audit where useful, then run release gates.", highlight: true },
      { title: "Project teams", description: "Generate temporary specialists from software, web, research, content, game, or operations archetypes." },
      { title: "Evolving memory", description: "Promote repeated project facts, supersede old decisions, retain temporal validity, and rebuild the warm index at any time." },
      { title: "Runtime doctor", description: "Distinguish live, standing-by, degraded, and untouched integrations from evidence on disk." },
    ],
  },
  testimonials: { title: "Community feedback", subtitle: "What developers have shared about AG Kit on GitHub.", items: testimonials },
  sponsored: { eyebrow: "Sponsored", title: "Supported by partners who ship", subtitle: "Sponsorship keeps AG Kit free, maintained, and open for everyone.", platinum: "Platinum sponsor", unikornBlurb: "A platform to discover and share technology products built by Vietnamese makers, from AI tools and education apps to utilities, games, and developer tools.", visitSponsor: "Visit sponsor", becomeTitle: "Become a sponsor", becomeDesc: "Support AG Kit maintenance and reach developers building with modern AI coding agents.", talk: "Talk sponsorship", coffee: "Buy me a coffee", wantBrand: "Want your brand next to AG Kit?", reachOut: "Reach out" },
  contribute: { eyebrow: "Contribute", title: "Developers who build AG Kit", subtitle: "Thank you to everyone contributing code, docs, runtime research, tests, and ideas.", starLabel: "Star on GitHub", guide: "Contributing guide", loading: "Loading contributors...", empty: "Could not load contributors right now. Visit the repo on GitHub.", commits: "commits", viewAll: "View all contributors" },
  faq: {
    eyebrow: "FAQ", title: "Common questions",
    items: [
      { value: "what", question: "What is AG Kit v2?", answer: "A lean multi-runtime operating layer combining a tiny shared core, hot-loaded skills, evolving local memory, runtime adapters, project teams, MCP, workflow gates, and executable verification." },
      { value: "runtimes", question: "Which runtimes are supported?", answer: "The capability matrix contains 16 targets across first-class, connected, and bridge tiers. Native surfaces are claimed only where verified." },
      { value: "memory", question: "Where is project memory stored?", answer: "Markdown under .ag-kit/memory is canonical. SQLite FTS5 is optional rebuildable acceleration, and memory survives runtime uninstall by default." },
      { value: "audit", question: "Can cross-audit modify my project?", answer: "No by design. Reviewer CLIs receive a snapshot or diff in a temporary workspace without a writable mount of the source project." },
      { value: "license", question: "Is AG Kit free?", answer: "Yes. AG Kit is MIT-licensed. You can use it commercially, fork it, and contribute improvements." },
    ],
  },
  footer: { blurb: "Lean multi-runtime operating layer for modern AI coding agents.", product: "Product", resources: "Resources", community: "Community", legal: "Legal", documentation: "Documentation", agents: "Agents", skills: "Skills", workflows: "Flow", installation: "Installation", cli: "CLI reference", changelog: "Changelog", github: "GitHub", issues: "Issues", discussions: "Discussions", license: "MIT License", security: "Security", credit: "Landing layout adapted from" },
};

const localized = (overrides: LandingOverrides): LandingDictionary => ({
  ...landingEn,
  nav: { ...landingEn.nav, ...overrides.nav },
  hero: { ...landingEn.hero, ...overrides.hero },
  stack: { ...landingEn.stack, ...overrides.stack },
  benefits: { ...landingEn.benefits, ...overrides.benefits },
  features: { ...landingEn.features, ...overrides.features },
  workflows: { ...landingEn.workflows, ...overrides.workflows },
  testimonials: { ...landingEn.testimonials, ...overrides.testimonials },
  sponsored: { ...landingEn.sponsored, ...overrides.sponsored },
  contribute: { ...landingEn.contribute, ...overrides.contribute },
  faq: { ...landingEn.faq, ...overrides.faq },
  footer: { ...landingEn.footer, ...overrides.footer },
});

export const landingVi: LandingDictionary = localized({
  nav: { benefits: "Lợi ích", features: "Tính năng", workflows: "Luồng", testimonials: "Đánh giá", sponsored: "Nhà tài trợ", contribute: "Đóng góp", faq: "Hỏi đáp", docs: "Tài liệu" },
  hero: { title: "Cho AI coding agent ít context hơn, nhiều bằng chứng hơn", subtitle: "Tiny shared core, 18 skill tải theo nhu cầu, bốn permanent agent, local-first memory, MCP, preflight gates và read-only cross-audit trên 16 runtime targets.", getStarted: "Bắt đầu", github: "GitHub" },
  stack: { title: "Core nhỏ. Phủ runtime rộng.", items: ["1 Core", "18 Skills", "4 Agents", "16 Runtimes", "MCP + Memory", "Mã nguồn mở"] },
  benefits: { eyebrow: "Lợi ích", title: "Ít framework trong context. Nhiều công việc hữu ích hơn.", subtitle: "AG Kit giữ permanent context thật nhỏ và chỉ tải behavior, domain knowledge, specialist và verification khi task cần." },
  features: { eyebrow: "Tính năng", title: "Operating layer, không phải kho prompt", subtitle: "Behavior, knowledge, runtime adapter, project state và verification được tách riêng để từng lớp đều nhỏ và test được." },
  workflows: { eyebrow: "Execution flow", title: "Một spine, ba mức độ sâu", subtitle: "Cùng một operating model chạy được từ fix một file đến migration nhiều hệ thống.", core: "Core", browseAll: "Xem kiến trúc flow" },
  testimonials: { title: "Phản hồi cộng đồng", subtitle: "Một số phản hồi developer đã chia sẻ về AG Kit trên GitHub." },
  sponsored: { eyebrow: "Nhà tài trợ", title: "Được hỗ trợ bởi những đội ngũ thích ship", subtitle: "Tài trợ giúp AG Kit tiếp tục miễn phí, được bảo trì và mở cho mọi người.", platinum: "Nhà tài trợ Platinum", visitSponsor: "Xem nhà tài trợ", becomeTitle: "Trở thành nhà tài trợ", becomeDesc: "Hỗ trợ việc bảo trì AG Kit và tiếp cận developer đang xây dựng với AI coding agents hiện đại.", talk: "Trao đổi tài trợ", coffee: "Mời mình một ly cà phê", wantBrand: "Muốn thương hiệu xuất hiện cùng AG Kit?", reachOut: "Liên hệ" },
  contribute: { eyebrow: "Đóng góp", title: "Những developer xây AG Kit", subtitle: "Cảm ơn mọi người đã đóng góp code, docs, runtime research, tests và ý tưởng.", starLabel: "Star trên GitHub", guide: "Hướng dẫn đóng góp", loading: "Đang tải contributor...", empty: "Hiện chưa tải được contributor. Hãy xem repository trên GitHub.", commits: "commit", viewAll: "Xem tất cả contributor" },
  faq: { eyebrow: "Hỏi đáp", title: "Câu hỏi thường gặp" },
  footer: { blurb: "Lean multi-runtime operating layer cho AI coding agents hiện đại.", product: "Sản phẩm", resources: "Tài nguyên", community: "Cộng đồng", legal: "Pháp lý", documentation: "Tài liệu", workflows: "Luồng", installation: "Cài đặt", cli: "CLI reference", security: "Bảo mật", credit: "Landing layout được điều chỉnh từ" },
});

export const landingZh: LandingDictionary = localized({
  nav: { benefits: "优势", features: "功能", workflows: "流程", testimonials: "用户评价", sponsored: "赞助", contribute: "贡献", faq: "常见问题", docs: "文档" },
  hero: { title: "用更少上下文运行 AI 编程代理，用更多证据验证结果", subtitle: "一个轻量共享核心、18 个按需技能、4 个常驻 agent、本地优先记忆、MCP、预检门禁，以及覆盖 16 个 runtime target 的只读交叉审计。", getStarted: "开始使用", github: "GitHub" },
  stack: { title: "核心更小，运行时覆盖更广。", items: ["1 Core", "18 Skills", "4 Agents", "16 Runtimes", "MCP + Memory", "开源"] },
  benefits: { eyebrow: "优势", title: "更少框架占用上下文，更多空间留给真正的工作。", subtitle: "AG Kit 将常驻上下文保持在最小，只在任务需要时加载行为、领域知识、专家与验证能力。" },
  features: { eyebrow: "功能", title: "这是运行层，不是 prompt 仓库", subtitle: "行为、知识、runtime adapter、项目状态和验证相互分离，因此每一层都能保持轻量和可测试。" },
  workflows: { eyebrow: "执行流程", title: "一条主干，三种深度", subtitle: "同一套运行模型可以覆盖单文件修复到多系统迁移。", core: "核心", browseAll: "查看流程架构" },
  testimonials: { title: "社区反馈", subtitle: "开发者在 GitHub 上分享的 AG Kit 使用反馈。" },
  contribute: { eyebrow: "贡献", title: "共同构建 AG Kit 的开发者", subtitle: "感谢所有贡献代码、文档、runtime 研究、测试和想法的人。", starLabel: "在 GitHub 上加星", guide: "贡献指南", loading: "正在加载贡献者...", empty: "暂时无法加载贡献者，请访问 GitHub 仓库。", commits: "次提交", viewAll: "查看所有贡献者" },
  faq: { eyebrow: "常见问题", title: "常见问题" },
  footer: { blurb: "面向现代 AI 编程 agent 的轻量多运行时 operating layer。", product: "产品", resources: "资源", community: "社区", legal: "法律", documentation: "文档", skills: "技能", workflows: "流程", installation: "安装", cli: "CLI 参考", changelog: "更新日志", discussions: "讨论", license: "MIT 许可", security: "安全", credit: "落地页布局参考" },
});

export const landingJa: LandingDictionary = localized({
  nav: { benefits: "メリット", features: "機能", workflows: "フロー", testimonials: "お客様の声", sponsored: "スポンサー", contribute: "コントリビュート", faq: "FAQ", docs: "ドキュメント" },
  hero: { title: "少ないコンテキストで AI coding agent を動かし、より多くの証拠で検証", subtitle: "小さな共有コア、オンデマンドの 18 スキル、4 つの常駐 agent、ローカル優先メモリ、MCP、preflight gate、16 runtime target にまたがる read-only cross-audit。", getStarted: "はじめる", github: "GitHub" },
  stack: { title: "小さなコア。広い runtime 対応。", items: ["1 Core", "18 Skills", "4 Agents", "16 Runtimes", "MCP + Memory", "オープンソース"] },
  benefits: { eyebrow: "メリット", title: "コンテキスト内の framework を減らし、実作業を増やす。", subtitle: "AG Kit は常駐コンテキストを意図的に小さく保ち、必要なときだけ behavior、domain knowledge、specialist、verification を読み込みます。" },
  features: { eyebrow: "機能", title: "prompt 倉庫ではなく operating layer", subtitle: "behavior、knowledge、runtime adapter、project state、verification を分離し、各レイヤーを小さくテスト可能に保ちます。" },
  workflows: { eyebrow: "実行フロー", title: "1 本の spine、3 段階の深さ", subtitle: "1 ファイルの修正から複数システムの migration まで同じ operating model で対応します。", core: "コア", browseAll: "フロー構成を見る" },
  testimonials: { title: "コミュニティの声", subtitle: "GitHub で共有された AG Kit へのフィードバック。" },
  contribute: { eyebrow: "コントリビュート", title: "AG Kit を作る開発者", subtitle: "コード、ドキュメント、runtime 調査、テスト、アイデアへの貢献に感謝します。", starLabel: "GitHub でスター", guide: "コントリビューションガイド", loading: "コントリビューターを読み込み中...", empty: "現在読み込めません。GitHub リポジトリをご覧ください。", commits: "commits", viewAll: "すべてのコントリビューターを見る" },
  faq: { eyebrow: "FAQ", title: "よくある質問" },
  footer: { blurb: "最新の AI coding agent 向け lean multi-runtime operating layer。", product: "製品", resources: "リソース", community: "コミュニティ", legal: "法務", documentation: "ドキュメント", workflows: "フロー", installation: "インストール", cli: "CLI リファレンス", changelog: "変更履歴", discussions: "ディスカッション", license: "MIT License", security: "セキュリティ", credit: "ランディング構成の参考" },
});
