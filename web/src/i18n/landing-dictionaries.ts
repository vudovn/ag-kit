export type LandingDictionary = {
  nav: {
    benefits: string;
    features: string;
    workflows: string;
    testimonials: string;
    sponsored: string;
    contribute: string;
    faq: string;
    docs: string;
  };
  hero: {
    title: string;
    subtitle: string;
    getStarted: string;
    github: string;
  };
  stack: {
    title: string;
    items: [string, string, string, string, string, string];
  };
  benefits: {
    eyebrow: string;
    title: string;
    subtitle: string;
    items: { title: string; description: string }[];
  };
  features: {
    eyebrow: string;
    title: string;
    subtitle: string;
    items: { title: string; description: string }[];
  };
  workflows: {
    eyebrow: string;
    title: string;
    subtitle: string;
    core: string;
    browseAll: string;
    items: { title: string; description: string; highlight?: boolean }[];
  };
  testimonials: {
    title: string;
    subtitle: string;
    items: {
      name: string;
      role: string;
      comment: string;
      clamp: string;
      className?: string;
    }[];
  };
  sponsored: {
    eyebrow: string;
    title: string;
    subtitle: string;
    platinum: string;
    unikornBlurb: string;
    visitSponsor: string;
    becomeTitle: string;
    becomeDesc: string;
    talk: string;
    coffee: string;
    wantBrand: string;
    reachOut: string;
  };
  contribute: {
    eyebrow: string;
    title: string;
    subtitle: string;
    starLabel: string;
    guide: string;
    loading: string;
    empty: string;
    commits: string;
    viewAll: string;
  };
  faq: {
    eyebrow: string;
    title: string;
    items: { value: string; question: string; answer: string }[];
  };
  footer: {
    blurb: string;
    product: string;
    resources: string;
    community: string;
    legal: string;
    documentation: string;
    agents: string;
    skills: string;
    workflows: string;
    installation: string;
    cli: string;
    changelog: string;
    github: string;
    issues: string;
    discussions: string;
    license: string;
    security: string;
    credit: string;
  };
};

export const landingEn: LandingDictionary = {
  nav: {
    benefits: "Benefits",
    features: "Features",
    workflows: "Workflows",
    testimonials: "Testimonials",
    sponsored: "Sponsored",
    contribute: "Contribute",
    faq: "FAQ",
    docs: "Docs",
  },
  hero: {
    title: "Expand your AI coding agents with",
    subtitle:
      "48 skills, 20 specialist agents, and production workflows you can install in one command. Safe merge updates keep your local changes.",
    getStarted: "Get started",
    github: "GitHub",
  },
  stack: {
    title: "Everything in one toolkit",
    items: [
      "20 Agents",
      "48 Skills",
      "13 Workflows",
      "CLI",
      "Merge-safe",
      "Open source",
    ],
  },
  benefits: {
    eyebrow: "Benefits",
    title: "Your shortcut to production-ready agent work",
    subtitle:
      "AG Kit packages the playbooks, agents, and guardrails you need so AI coding assistants act like a coordinated team instead of a single chat window.",
    items: [
      {
        title: "Ship features faster",
        description:
          "Specialist agents and skills cover planning, coding, review, security, and deploy so you spend less time reinventing prompts.",
      },
      {
        title: "Safer updates",
        description:
          "Managed-file manifests, three-way conflict detection, and backups mean ag-kit update never silently wipes your local edits.",
      },
      {
        title: "Workflows that stick",
        description:
          "From /brainstorm to /deploy, repeatable command workflows keep teams aligned on the same process.",
      },
      {
        title: "Quality built in",
        description:
          "Lint, security, SEO, performance, and test checkers live next to the skills that teach agents how to use them.",
      },
    ],
  },
  features: {
    eyebrow: "Features",
    title: "What makes AG Kit different",
    subtitle:
      "A full agent capability pack, not a single prompt template - designed for real projects and safe upgrades over time.",
    items: [
      {
        title: "Specialist agents",
        description:
          "Frontend, backend, security, database, mobile, and more - each with a focused system prompt and skill set.",
      },
      {
        title: "Domain skills",
        description:
          "48 skills covering architecture, research, testing, i18n, SEO, GEO, deployment, and clean code standards.",
      },
      {
        title: "Guided workflows",
        description:
          "Slash commands for brainstorm, plan, create, debug, test, preview, status, orchestrate, and deploy.",
      },
      {
        title: "Simple CLI",
        description:
          "init, update, rollback, and status with dry-run, merge/replace strategies, and conflict reports.",
      },
      {
        title: "Merge-aware updates",
        description:
          "SHA-256 baselines detect clean files, local edits, and true three-way conflicts before writing.",
      },
      {
        title: "Docs that match the kit",
        description:
          "Installation guides, CLI reference, and localized examples stay in sync with the toolkit version.",
      },
    ],
  },
  workflows: {
    eyebrow: "Workflows",
    title: "Commands that run your process",
    subtitle: "Slash workflows turn tribal knowledge into repeatable agent sessions.",
    core: "Core",
    browseAll: "Browse all workflows",
    items: [
      {
        title: "/brainstorm",
        description:
          "Explore multiple approaches with pros, cons, and tradeoffs before writing code.",
      },
      {
        title: "/plan",
        description:
          "Break features into tasks, dependencies, and verification criteria.",
      },
      {
        title: "/create",
        description: "Scaffold full-stack apps from a natural-language request.",
      },
      {
        title: "/debug",
        description: "Systematic root-cause analysis with evidence-based fixes.",
      },
      {
        title: "/orchestrate",
        description:
          "Coordinate parallel specialist agents on complex multi-domain work.",
      },
      {
        title: "/deploy",
        description:
          "Production-minded release steps with rollback thinking built in.",
        highlight: true,
      },
    ],
  },
  testimonials: {
    title: "Testimonials",
    subtitle:
      "Real feedback from the community on GitHub.",
    items: [
      {
        name: "winniwoods",
        role: "GitHub · #38",
        comment:
          "First of all, thank you for this amazing project! I've been using the Antigravity Kit and really enjoy the workflow.",
        clamp: "line-clamp-3",
      },
      {
        name: "ghiemer",
        role: "GitHub · #23",
        comment:
          "Good work with antigravity-kit. Love it — Cheers.",
        clamp: "line-clamp-2",
      },
      {
        name: "AlexOptimizer",
        role: "GitHub · #66",
        comment:
          "The project architecture and settings are configured at the highest level, utilizing modern systemic prompting and modularity practices. The separation into specialized agents and pluggable skills prevents AI context overload.",
        clamp: "line-clamp-5",
      },
      {
        name: "DRYN07",
        role: "GitHub · #67",
        comment:
          "I have been using another skills repo so far, which has more skills, but yours seems quite well-organized, so I thought I'd give it a try.",
        clamp: "line-clamp-3",
        className: "hidden md:block",
      },
      {
        name: "kkkasio",
        role: "GitHub · #38",
        comment:
          "I support the idea — the tool is really quite robust for new environments like Node.",
        clamp: "line-clamp-2",
        className: "hidden md:block",
      },
      {
        name: "pragnyanramtha",
        role: "GitHub · #69",
        comment:
          "Antigravity now also supports .agents/ and it's the industry standard — helps in extensibility when I'm installing other skills.",
        clamp: "line-clamp-3",
        className: "hidden lg:block",
      },
    ],
  },
  sponsored: {
    eyebrow: "Sponsored",
    title: "Supported by partners who ship",
    subtitle:
      "Sponsorship keeps AG Kit free, maintained, and open for everyone. Thank you to the teams investing in the agent ecosystem.",
    platinum: "Platinum sponsor",
    unikornBlurb:
      "A platform to discover and share technology products built by Vietnamese makers, from AI tools and education apps to utilities, games, and developer tools.",
    visitSponsor: "Visit sponsor",
    becomeTitle: "Become a sponsor",
    becomeDesc:
      "Get logo placement here, shout-outs in releases, and direct influence on roadmap priorities that help your customers ship with AI agents.",
    talk: "Talk sponsorship",
    coffee: "Buy me a coffee",
    wantBrand: "Want your brand next to AG Kit?",
    reachOut: "Reach out",
  },
  contribute: {
    eyebrow: "Contribute",
    title: "Developers who build AG Kit",
    subtitle:
      "Thank you to everyone who has contributed code, docs, and ideas. Join them on GitHub.",
    starLabel: "Star on GitHub",
    guide: "Contributing guide",
    loading: "Loading contributors...",
    empty: "Could not load contributors right now. Visit the repo on GitHub.",
    commits: "commits",
    viewAll: "View all contributors",
  },
  faq: {
    eyebrow: "FAQ",
    title: "Common questions",
    items: [
      {
        value: "what",
        question: "What is AG Kit?",
        answer:
          "AG Kit is an open-source toolkit of AI agent skills, specialist agents, workflows, and a CLI that installs them into your project safely.",
      },
      {
        value: "install",
        question: "How do I install it?",
        answer:
          "Run npx @vudovn/ag-kit init in your project (or install the CLI globally). It downloads the toolkit into .agents and writes a managed-file manifest.",
      },
      {
        value: "update",
        question: "Will update overwrite my changes?",
        answer:
          "No. Default strategy is merge. Clean managed files update automatically; local edits are preserved; real conflicts write an incoming copy and a JSON report. You can also roll back from backups.",
      },
      {
        value: "works-with",
        question: "Which AI assistants work with AG Kit?",
        answer:
          "AG Kit targets modern coding agents that can load project skills and rules (for example Gemini CLI / Antigravity-style setups). The docs cover structure and workflows independent of a single vendor chat UI.",
      },
      {
        value: "license",
        question: "Is it free?",
        answer:
          "Yes. AG Kit is MIT-licensed. Use it commercially, fork it, and contribute improvements back if you like.",
      },
    ],
  },
  footer: {
    blurb:
      "AI agent templates - skills, agents, and workflows for modern coding assistants.",
    product: "Product",
    resources: "Resources",
    community: "Community",
    legal: "Legal",
    documentation: "Documentation",
    agents: "Agents",
    skills: "Skills",
    workflows: "Workflows",
    installation: "Installation",
    cli: "CLI reference",
    changelog: "Changelog",
    github: "GitHub",
    issues: "Issues",
    discussions: "Discussions",
    license: "MIT License",
    security: "Security",
    credit: "Landing layout adapted from",
  },
};

export const landingVi: LandingDictionary = {
  nav: {
    benefits: "Lợi ích",
    features: "Tính năng",
    workflows: "Quy trình",
    testimonials: "Đánh giá",
    sponsored: "Nhà tài trợ",
    contribute: "Đóng góp",
    faq: "Hỏi đáp",
    docs: "Tài liệu",
  },
  hero: {
    title: "Mở rộng AI coding agent của bạn với",
    subtitle:
      "48 kỹ năng, 20 agent chuyên biệt và các quy trình production cài chỉ bằng một lệnh. Cập nhật merge an toàn, giữ nguyên chỉnh sửa cục bộ của bạn.",
    getStarted: "Bắt đầu",
    github: "GitHub",
  },
  stack: {
    title: "Mọi thứ trong một bộ toolkit",
    items: [
      "20 Agent",
      "48 Kỹ năng",
      "13 Quy trình",
      "CLI",
      "Cập nhật an toàn",
      "Mã nguồn mở",
    ],
  },
  benefits: {
    eyebrow: "Lợi ích",
    title: "Lối tắt tới công việc agent sẵn sàng production",
    subtitle:
      "AG Kit đóng gói playbook, agent và hàng rào an toàn để trợ lý lập trình AI làm việc như một đội phối hợp, không chỉ một cửa sổ chat.",
    items: [
      {
        title: "Ship tính năng nhanh hơn",
        description:
          "Agent và skill chuyên biệt bao phủ lập kế hoạch, code, review, bảo mật và deploy - bớt thời gian viết lại prompt.",
      },
      {
        title: "Cập nhật an toàn hơn",
        description:
          "Manifest file được quản lý, phát hiện xung đột ba chiều và backup - ag-kit update không xóa im lặng chỉnh sửa cục bộ.",
      },
      {
        title: "Quy trình bám sát",
        description:
          "Từ /brainstorm đến /deploy, workflow lặp lại giúp cả đội thống nhất cùng một quy trình.",
      },
      {
        title: "Chất lượng tích hợp sẵn",
        description:
          "Lint, bảo mật, SEO, hiệu năng và checker kiểm thử nằm cạnh các skill hướng dẫn agent cách dùng.",
      },
    ],
  },
  features: {
    eyebrow: "Tính năng",
    title: "Điều làm AG Kit khác biệt",
    subtitle:
      "Gói năng lực agent đầy đủ, không chỉ một template prompt - thiết kế cho dự án thật và nâng cấp an toàn theo thời gian.",
    items: [
      {
        title: "Agent chuyên biệt",
        description:
          "Frontend, backend, bảo mật, database, mobile và nhiều hơn - mỗi agent có system prompt và bộ skill riêng.",
      },
      {
        title: "Skill theo domain",
        description:
          "48 skill gồm nghiên cứu, kiến trúc, testing, i18n, SEO, GEO, triển khai và chuẩn clean code.",
      },
      {
        title: "Workflow có hướng dẫn",
        description:
          "Lệnh slash cho brainstorm, plan, create, debug, test, preview, status, orchestrate và deploy.",
      },
      {
        title: "CLI đơn giản",
        description:
          "init, update, rollback và status với dry-run, chiến lược merge/replace và báo cáo xung đột.",
      },
      {
        title: "Cập nhật nhận biết merge",
        description:
          "Baseline SHA-256 phát hiện file sạch, chỉnh sửa cục bộ và xung đột ba chiều trước khi ghi.",
      },
      {
        title: "Tài liệu khớp toolkit",
        description:
          "Hướng dẫn cài đặt, tham chiếu CLI và ví dụ đa ngôn ngữ luôn đồng bộ phiên bản toolkit.",
      },
    ],
  },
  workflows: {
    eyebrow: "Quy trình",
    title: "Lệnh chạy đúng quy trình của bạn",
    subtitle:
      "Slash workflow biến kiến thức đội nhóm thành phiên agent có thể lặp lại.",
    core: "Cốt lõi",
    browseAll: "Xem tất cả quy trình",
    items: [
      {
        title: "/brainstorm",
        description:
          "Khám phá nhiều hướng tiếp cận với ưu, nhược điểm trước khi viết code.",
      },
      {
        title: "/plan",
        description:
          "Chia tính năng thành task, phụ thuộc và tiêu chí kiểm chứng.",
      },
      {
        title: "/create",
        description:
          "Scaffold ứng dụng full-stack từ yêu cầu ngôn ngữ tự nhiên.",
      },
      {
        title: "/debug",
        description:
          "Phân tích gốc rễ có hệ thống với các bản sửa dựa trên bằng chứng.",
      },
      {
        title: "/orchestrate",
        description:
          "Điều phối agent chuyên biệt song song cho công việc đa domain.",
      },
      {
        title: "/deploy",
        description:
          "Các bước release hướng production, có tư duy rollback sẵn.",
        highlight: true,
      },
    ],
  },
  testimonials: {
    title: "Đánh giá",
    subtitle:
      "Phản hồi thật từ cộng đồng trên GitHub.",
    items: [
      {
        name: "winniwoods",
        role: "GitHub · #38",
        comment:
          "First of all, thank you for this amazing project! I've been using the Antigravity Kit and really enjoy the workflow.",
        clamp: "line-clamp-3",
      },
      {
        name: "ghiemer",
        role: "GitHub · #23",
        comment:
          "Good work with antigravity-kit. Love it — Cheers.",
        clamp: "line-clamp-2",
      },
      {
        name: "AlexOptimizer",
        role: "GitHub · #66",
        comment:
          "The project architecture and settings are configured at the highest level, utilizing modern systemic prompting and modularity practices. The separation into specialized agents and pluggable skills prevents AI context overload.",
        clamp: "line-clamp-5",
      },
      {
        name: "DRYN07",
        role: "GitHub · #67",
        comment:
          "I have been using another skills repo so far, which has more skills, but yours seems quite well-organized, so I thought I'd give it a try.",
        clamp: "line-clamp-3",
        className: "hidden md:block",
      },
      {
        name: "kkkasio",
        role: "GitHub · #38",
        comment:
          "I support the idea — the tool is really quite robust for new environments like Node.",
        clamp: "line-clamp-2",
        className: "hidden md:block",
      },
      {
        name: "pragnyanramtha",
        role: "GitHub · #69",
        comment:
          "Antigravity now also supports .agents/ and it's the industry standard — helps in extensibility when I'm installing other skills.",
        clamp: "line-clamp-3",
        className: "hidden lg:block",
      },
    ],
  },
  sponsored: {
    eyebrow: "Nhà tài trợ",
    title: "Được hỗ trợ bởi các đối tác tin cậy",
    subtitle:
      "Tài trợ giúp AG Kit luôn miễn phí, được duy trì và mở cho mọi người. Cảm ơn các đội ngũ đang đầu tư vào hệ sinh thái AI agent.",
    platinum: "Nhà tài trợ chính",
    unikornBlurb:
      "Nền tảng khám phá và chia sẻ sản phẩm công nghệ do người Việt xây dựng, từ công cụ AI, ứng dụng giáo dục, tiện ích đến game và công cụ cho nhà phát triển.",
    visitSponsor: "Xem nhà tài trợ",
    becomeTitle: "Trở thành nhà tài trợ",
    becomeDesc:
      "Hiển thị logo tại đây, được nhắc trong các bản phát hành, và đóng góp định hướng roadmap để khách hàng của bạn triển khai AI agent tốt hơn.",
    talk: "Liên hệ tài trợ",
    coffee: "Mời tôi một ly cà phê",
    wantBrand: "Muốn thương hiệu của bạn xuất hiện cùng AG Kit?",
    reachOut: "Liên hệ ngay",
  },
  contribute: {
    eyebrow: "Đóng góp",
    title: "Các nhà phát triển đã đóng góp",
    subtitle:
      "Cảm ơn tất cả những ai đã đóng góp code, tài liệu và ý tưởng. Hãy tham gia cùng họ trên GitHub.",
    starLabel: "Star trên GitHub",
    guide: "Hướng dẫn đóng góp",
    loading: "Đang tải danh sách người đóng góp...",
    empty: "Không tải được danh sách lúc này. Xem repository trên GitHub.",
    commits: "commits",
    viewAll: "Xem tất cả người đóng góp",
  },
  faq: {
    eyebrow: "Hỏi đáp",
    title: "Câu hỏi thường gặp",
    items: [
      {
        value: "what",
        question: "AG Kit là gì?",
        answer:
          "AG Kit là toolkit mã nguồn mở gồm skill AI agent, agent chuyên biệt, workflow và CLI cài chúng vào dự án một cách an toàn.",
      },
      {
        value: "install",
        question: "Cài đặt thế nào?",
        answer:
          "Chạy npx @vudovn/ag-kit init trong dự án (hoặc cài CLI toàn cục). Toolkit được tải vào .agents và ghi managed-file manifest.",
      },
      {
        value: "update",
        question: "Update có ghi đè chỉnh sửa của tôi không?",
        answer:
          "Không. Chiến lược mặc định là merge. File managed sạch được cập nhật tự động; chỉnh sửa cục bộ được giữ; xung đột thật sẽ ghi bản incoming và báo cáo JSON. Bạn cũng có thể rollback từ backup.",
      },
      {
        value: "works-with",
        question: "AG Kit dùng với trợ lý AI nào?",
        answer:
          "AG Kit hướng tới coding agent hiện đại có thể nạp skill và rule dự án (ví dụ Gemini CLI / Antigravity). Tài liệu mô tả cấu trúc và workflow độc lập với một UI chat duy nhất.",
      },
      {
        value: "license",
        question: "Có miễn phí không?",
        answer:
          "Có. AG Kit theo giấy phép MIT. Dùng thương mại, fork, và đóng góp cải tiến nếu bạn muốn.",
      },
    ],
  },
  footer: {
    blurb:
      "Bộ mẫu AI agent - skill, agent và workflow cho trợ lý lập trình hiện đại.",
    product: "Sản phẩm",
    resources: "Tài nguyên",
    community: "Cộng đồng",
    legal: "Pháp lý",
    documentation: "Tài liệu",
    agents: "Agent",
    skills: "Kỹ năng",
    workflows: "Quy trình",
    installation: "Cài đặt",
    cli: "Tham chiếu CLI",
    changelog: "Nhật ký thay đổi",
    github: "GitHub",
    issues: "Issues",
    discussions: "Thảo luận",
    license: "Giấy phép MIT",
    security: "Bảo mật",
    credit: "Giao diện landing tham khảo từ",
  },
};

/** Chinese landing strings */
export const landingZh: LandingDictionary = {
  ...landingEn,
  nav: {
    benefits: "优势",
    features: "功能",
    workflows: "工作流",
    testimonials: "用户评价",
    sponsored: "赞助商",
    contribute: "贡献",
    faq: "常见问题",
    docs: "文档",
  },
  hero: {
    title: "用以下工具扩展你的 AI 编程助手",
    subtitle:
      "48 项技能、20 位专业 agent 与生产级工作流，一条命令即可安装。安全合并更新，保留你的本地修改。",
    getStarted: "开始使用",
    github: "GitHub",
  },
  stack: {
    title: "一站式工具包",
    items: ["20 个 Agent", "48 项技能", "13 个工作流", "CLI", "安全更新", "开源"],
  },
  sponsored: {
    ...landingEn.sponsored,
    eyebrow: "赞助商",
    title: "由可信伙伴支持",
    subtitle:
      "赞助让 AG Kit 保持免费、持续维护并对所有人开放。感谢投资 agent 生态的团队。",
    platinum: "首席赞助商",
    unikornBlurb:
      "发现并分享越南开发者打造的科技产品平台，涵盖 AI 工具、教育应用、实用程序、游戏和开发者工具。",
    visitSponsor: "访问赞助商",
    becomeTitle: "成为赞助商",
    becomeDesc:
      "在此展示 logo、在版本发布中获得提及，并直接影响路线图优先级，帮助客户用 AI agent 交付。",
    talk: "洽谈赞助",
    coffee: "请我喝杯咖啡",
    wantBrand: "希望你的品牌出现在 AG Kit 旁？",
    reachOut: "立即联系",
  },
  benefits: {
    eyebrow: "优势",
    title: "通往生产级 agent 工作的捷径",
    subtitle:
      "AG Kit 打包了所需的操作手册、agent 与防护措施，让 AI 编程助手像一支协调的团队，而不是单个聊天窗口。",
    items: [
      {
        title: "更快交付功能",
        description:
          "专业 agent 与技能覆盖规划、编码、评审、安全与部署，减少重复造 prompt 的时间。",
      },
      {
        title: "更安全的更新",
        description:
          "托管文件清单、三方冲突检测与备份，确保 ag-kit update 不会悄悄覆盖你的本地修改。",
      },
      {
        title: "可持续的工作流",
        description:
          "从 /brainstorm 到 /deploy，可复用的命令工作流让团队保持同一流程。",
      },
      {
        title: "内建质量保障",
        description:
          "Lint、安全、SEO、性能与测试检查器与技能一同提供，教会 agent 如何使用它们。",
      },
    ],
  },
  features: {
    eyebrow: "功能",
    title: "AG Kit 的不同之处",
    subtitle:
      "完整的 agent 能力包，而非单个 prompt 模板——为真实项目与长期安全升级而设计。",
    items: [
      {
        title: "专业 agent",
        description:
          "前端、后端、安全、数据库、移动端等——每个都有专注的系统提示与技能组合。",
      },
      {
        title: "领域技能",
        description:
          "48 项技能覆盖研究、架构、测试、i18n、SEO、GEO、部署与整洁代码标准。",
      },
      {
        title: "引导式工作流",
        description:
          "brainstorm、plan、create、debug、test、preview、status、orchestrate、deploy 等斜杠命令。",
      },
      {
        title: "简单的 CLI",
        description:
          "init、update、rollback、status，支持 dry-run、merge/replace 策略与冲突报告。",
      },
      {
        title: "感知合并的更新",
        description:
          "SHA-256 基线在写入前区分干净文件、本地修改与真正的三方冲突。",
      },
      {
        title: "与套件同步的文档",
        description:
          "安装指南、CLI 参考与本地化示例与工具包版本保持同步。",
      },
    ],
  },
  workflows: {
    eyebrow: "工作流",
    title: "运行你的流程的命令",
    subtitle: "斜杠工作流将团队经验变成可复用的 agent 会话。",
    core: "核心",
    browseAll: "浏览所有工作流",
    items: [
      {
        title: "/brainstorm",
        description: "在写代码前探索多种方案的优缺点与权衡。",
      },
      {
        title: "/plan",
        description: "把功能拆解为任务、依赖与验证标准。",
      },
      {
        title: "/create",
        description: "从自然语言请求搭建全栈应用。",
      },
      {
        title: "/debug",
        description: "系统化的根因分析与基于证据的修复。",
      },
      {
        title: "/orchestrate",
        description: "协调并行的专业 agent 处理复杂多领域工作。",
      },
      {
        title: "/deploy",
        description: "面向生产的发布步骤，内建回滚思维。",
        highlight: true,
      },
    ],
  },
  testimonials: {
    title: "用户评价",
    subtitle: "来自 GitHub 社区的真实反馈。",
    items: landingEn.testimonials.items,
  },
  contribute: {
    eyebrow: "贡献",
    title: "构建 AG Kit 的开发者",
    subtitle:
      "感谢每一位贡献代码、文档与想法的人。欢迎在 GitHub 上加入他们。",
    starLabel: "在 GitHub 上加星",
    guide: "贡献指南",
    loading: "正在加载贡献者...",
    empty: "暂时无法加载贡献者。请访问 GitHub 仓库。",
    commits: "次提交",
    viewAll: "查看所有贡献者",
  },
  faq: {
    eyebrow: "常见问题",
    title: "常见问题",
    items: [
      {
        value: "what",
        question: "AG Kit 是什么？",
        answer:
          "AG Kit 是一个开源工具包，包含 AI agent 技能、专业 agent、工作流，以及能将它们安全安装进项目的 CLI。",
      },
      {
        value: "install",
        question: "如何安装？",
        answer:
          "在项目中运行 npx @vudovn/ag-kit init（或全局安装 CLI）。它会把工具包下载到 .agents 并写入托管文件清单。",
      },
      {
        value: "update",
        question: "update 会覆盖我的修改吗？",
        answer:
          "不会。默认策略是 merge：干净的托管文件自动更新；本地修改被保留；真正的冲突会写入新副本与 JSON 报告，还可以从备份回滚。",
      },
      {
        value: "works-with",
        question: "哪些 AI 助手可以配合 AG Kit？",
        answer:
          "AG Kit 面向能加载项目技能与规则的现代编程 agent（例如 Gemini CLI / Antigravity 类环境）。文档独立于单一厂商的聊天界面。",
      },
      {
        value: "license",
        question: "免费吗？",
        answer:
          "是的。AG Kit 采用 MIT 许可，可商用、可 fork，欢迎回馈改进。",
      },
    ],
  },
  footer: {
    ...landingEn.footer,
    blurb: "面向现代编程助手的 AI agent 模板 - 技能、agent 与工作流。",
    product: "产品",
    resources: "资源",
    community: "社区",
    legal: "法律",
    documentation: "文档",
    agents: "Agents",
    skills: "技能",
    workflows: "工作流",
    installation: "安装",
    cli: "CLI 参考",
    changelog: "更新日志",
    discussions: "讨论",
    license: "MIT 许可",
    security: "安全",
    credit: "落地页布局参考自",
  },
};

/** Japanese landing strings */
export const landingJa: LandingDictionary = {
  ...landingEn,
  nav: {
    benefits: "メリット",
    features: "機能",
    workflows: "ワークフロー",
    testimonials: "お客様の声",
    sponsored: "スポンサー",
    contribute: "コントリビュート",
    faq: "FAQ",
    docs: "ドキュメント",
  },
  hero: {
    title: "AI コーディングエージェントを拡張",
    subtitle:
      "48 のスキル、20 の専門エージェント、本番向けワークフローを 1 コマンドで導入。安全なマージ更新でローカル変更を守ります。",
    getStarted: "はじめる",
    github: "GitHub",
  },
  stack: {
    title: "すべてが 1 つのツールキットに",
    items: [
      "20 Agents",
      "48 Skills",
      "13 Workflows",
      "CLI",
      "安全な更新",
      "オープンソース",
    ],
  },
  sponsored: {
    ...landingEn.sponsored,
    eyebrow: "スポンサー",
    title: "信頼できるパートナーに支えられています",
    subtitle:
      "スポンサーシップが AG Kit を無料・継続保守・誰でも使える状態に保ちます。",
    platinum: "プラチナスポンサー",
    unikornBlurb:
      "ベトナムの開発者が作ったテックプロダクトを発見・共有するプラットフォーム。AI ツール、教育アプリ、ユーティリティ、ゲーム、開発者ツールまで。",
    visitSponsor: "スポンサーを見る",
    becomeTitle: "スポンサーになる",
    becomeDesc:
      "ここにロゴ掲載、リリースでの紹介、ロードマップへの影響など、AI agent 導入を支援するメリットがあります。",
    talk: "スポンサー相談",
    coffee: "コーヒーをおごる",
    wantBrand: "ブランドを AG Kit の隣に置きたいですか？",
    reachOut: "連絡する",
  },
  benefits: {
    eyebrow: "メリット",
    title: "本番品質の agent ワークへの近道",
    subtitle:
      "AG Kit はプレイブック、agent、ガードレールをまとめて提供し、AI コーディングアシスタントを単なるチャット窓ではなく連携したチームのように動かします。",
    items: [
      {
        title: "機能をより速く出荷",
        description:
          "計画・実装・レビュー・セキュリティ・デプロイを専門 agent とスキルがカバーし、prompt の再発明を減らします。",
      },
      {
        title: "より安全な更新",
        description:
          "管理ファイルのマニフェスト、三方向の競合検出、バックアップにより、ag-kit update がローカル編集を静かに消すことはありません。",
      },
      {
        title: "定着するワークフロー",
        description:
          "/brainstorm から /deploy まで、再現可能なコマンドワークフローでチームの手順を統一します。",
      },
      {
        title: "品質を標準装備",
        description:
          "Lint・セキュリティ・SEO・パフォーマンス・テストのチェッカーが、使い方を教えるスキルと並んで付属します。",
      },
    ],
  },
  features: {
    eyebrow: "機能",
    title: "AG Kit の違い",
    subtitle:
      "単一の prompt テンプレートではなく、実プロジェクトと安全なアップグレードのために設計された完全な agent 能力パックです。",
    items: [
      {
        title: "専門 agent",
        description:
          "フロントエンド、バックエンド、セキュリティ、データベース、モバイルなど、それぞれ専用のシステムプロンプトとスキルを持ちます。",
      },
      {
        title: "ドメインスキル",
        description:
          "リサーチ、アーキテクチャ、テスト、i18n、SEO、GEO、デプロイ、クリーンコードを網羅する 48 のスキル。",
      },
      {
        title: "ガイド付きワークフロー",
        description:
          "brainstorm、plan、create、debug、test、preview、status、orchestrate、deploy のスラッシュコマンド。",
      },
      {
        title: "シンプルな CLI",
        description:
          "init・update・rollback・status。dry-run、merge/replace 戦略、競合レポートに対応。",
      },
      {
        title: "マージを理解する更新",
        description:
          "SHA-256 ベースラインが書き込み前にクリーンなファイル、ローカル編集、真の三方向競合を判別します。",
      },
      {
        title: "キットと同期したドキュメント",
        description:
          "インストールガイド、CLI リファレンス、ローカライズ済みの例がツールキットのバージョンと同期します。",
      },
    ],
  },
  workflows: {
    eyebrow: "ワークフロー",
    title: "プロセスを実行するコマンド",
    subtitle: "スラッシュワークフローが暗黙知を再現可能な agent セッションに変えます。",
    core: "コア",
    browseAll: "すべてのワークフローを見る",
    items: [
      {
        title: "/brainstorm",
        description: "コードを書く前に複数のアプローチを長所・短所とともに検討。",
      },
      {
        title: "/plan",
        description: "機能をタスク・依存関係・検証基準に分解。",
      },
      {
        title: "/create",
        description: "自然言語のリクエストからフルスタックアプリを scaffolding。",
      },
      {
        title: "/debug",
        description: "証拠に基づく修正を伴う体系的な根本原因分析。",
      },
      {
        title: "/orchestrate",
        description: "複雑な複数ドメインの作業で並列の専門 agent を調整。",
      },
      {
        title: "/deploy",
        description: "ロールバックを見据えた本番向けリリース手順。",
        highlight: true,
      },
    ],
  },
  testimonials: {
    title: "お客様の声",
    subtitle: "GitHub コミュニティからの実際のフィードバック。",
    items: landingEn.testimonials.items,
  },
  contribute: {
    eyebrow: "コントリビュート",
    title: "AG Kit を作る開発者たち",
    subtitle:
      "コード・ドキュメント・アイデアを提供してくれた皆さんに感謝します。GitHub で参加してください。",
    starLabel: "GitHub でスターを付ける",
    guide: "コントリビュートガイド",
    loading: "コントリビューターを読み込み中...",
    empty: "コントリビューターを読み込めませんでした。GitHub のリポジトリをご覧ください。",
    commits: "コミット",
    viewAll: "すべてのコントリビューターを見る",
  },
  faq: {
    eyebrow: "FAQ",
    title: "よくある質問",
    items: [
      {
        value: "what",
        question: "AG Kit とは？",
        answer:
          "AG Kit は AI agent スキル、専門 agent、ワークフロー、そしてそれらをプロジェクトに安全にインストールする CLI のオープンソースツールキットです。",
      },
      {
        value: "install",
        question: "インストール方法は？",
        answer:
          "プロジェクトで npx @vudovn/ag-kit init を実行します（CLI のグローバルインストールも可）。ツールキットが .agents にダウンロードされ、管理ファイルのマニフェストが書き込まれます。",
      },
      {
        value: "update",
        question: "update でローカルの変更は上書きされますか？",
        answer:
          "いいえ。デフォルトは merge 戦略です。クリーンな管理ファイルは自動更新、ローカル編集は保持、真の競合は新しいコピーと JSON レポートに書き出されます。バックアップからのロールバックも可能です。",
      },
      {
        value: "works-with",
        question: "どの AI アシスタントで使えますか？",
        answer:
          "AG Kit はプロジェクトのスキルとルールを読み込める最新のコーディング agent（Gemini CLI / Antigravity 系の環境など）を対象としています。ドキュメントは特定ベンダーのチャット UI に依存しません。",
      },
      {
        value: "license",
        question: "無料ですか？",
        answer:
          "はい。AG Kit は MIT ライセンスです。商用利用も fork も自由で、改善の還元を歓迎します。",
      },
    ],
  },
  footer: {
    ...landingEn.footer,
    blurb:
      "モダンなコーディングアシスタント向け AI agent テンプレート - スキル、エージェント、ワークフロー。",
    product: "プロダクト",
    resources: "リソース",
    community: "コミュニティ",
    legal: "法務",
    documentation: "ドキュメント",
    installation: "インストール",
    cli: "CLI リファレンス",
    changelog: "変更履歴",
    discussions: "ディスカッション",
    license: "MIT ライセンス",
    security: "セキュリティ",
    credit: "ランディングレイアウトの参考元",
  },
};
