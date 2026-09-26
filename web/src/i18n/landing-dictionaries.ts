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
    workflows: "Flow",
    testimonials: "Testimonials",
    sponsored: "Sponsored",
    contribute: "Contribute",
    faq: "FAQ",
    docs: "Docs",
  },
  hero: {
    title: "Run AI coding agents with less context and more proof",
    subtitle:
      "A tiny shared core, 18 hot-loaded skills, four permanent agents, local-first memory, MCP, preflight gates, and read-only cross-audit across 12 runtime targets.",
    getStarted: "Get started",
    github: "GitHub",
  },
  stack: {
    title: "Small core. Wide runtime reach.",
    items: [
      "1 Core",
      "18 Skills",
      "4 Agents",
      "12 Runtimes",
      "MCP + Memory",
      "Open source",
    ],
  },
  benefits: {
    eyebrow: "Benefits",
    title: "Less framework in context. More useful work.",
    subtitle:
      "AG Kit keeps permanent context intentionally small and loads behavior, domain knowledge, specialists, and verification only when the task needs them.",
    items: [
      {
        title: "Protect the context budget",
        description:
          "One tiny resident core replaces a pile of always-on personas and duplicated workflow instructions.",
      },
      {
        title: "Use one brain across runtimes",
        description:
          "Shared behavior lives in one canonical source, while capability-aware adapters translate it for each supported runtime.",
      },
      {
        title: "Keep memory local and readable",
        description:
          "Markdown remains canonical project memory; SQLite FTS5 is optional acceleration that can always be rebuilt.",
      },
      {
        title: "Verify instead of guessing",
        description:
          "Preflight, native runtime checks, CI, and independent read-only cross-audit produce evidence and receipts.",
      },
    ],
  },
  features: {
    eyebrow: "Features",
    title: "An operating layer, not a prompt warehouse",
    subtitle:
      "The v2 architecture separates behavior, knowledge, runtime adapters, project state, and verification so each layer can stay small and testable.",
    items: [
      {
        title: "18 hot-loaded skills",
        description:
          "Capabilities load when relevant instead of permanently occupying every session.",
      },
      {
        title: "Four permanent agents",
        description:
          "Scout, architect, builder, and reviewer form the stable core; project specialists are generated only when needed.",
      },
      {
        title: "One development spine",
        description:
          "QUICK, STANDARD, and DEEP modes share one flow instead of many competing workflow engines.",
      },
      {
        title: "12 runtime targets",
        description:
          "First-class, connected, and bridge tiers expose only the surfaces AG Kit has actually verified.",
      },
      {
        title: "Project-local MCP",
        description:
          "Memory, team, runtime, and audit capabilities can be shared without pretending every runtime has the same native features.",
      },
      {
        title: "Safe cross-audit",
        description:
          "Independent reviewer CLIs inspect snapshots or diffs in temporary directories without a writable mount of your source tree.",
      },
    ],
  },
  workflows: {
    eyebrow: "Execution flow",
    title: "One spine, three levels of depth",
    subtitle:
      "The same operating model scales from a one-file fix to a multi-system migration.",
    core: "Core",
    browseAll: "Read the flow architecture",
    items: [
      {
        title: "QUICK",
        description:
          "Classify, load the minimum skill, build, run targeted verification, and return the result.",
      },
      {
        title: "STANDARD",
        description:
          "Scout the codebase, define the plan, build, review independently, then verify acceptance criteria.",
      },
      {
        title: "DEEP",
        description:
          "Map risks and dependencies, execute in waves, cross-audit where useful, then run release gates.",
        highlight: true,
      },
      {
        title: "Project teams",
        description:
          "Generate temporary specialists from software, web, research, content, game, or operations archetypes.",
      },
      {
        title: "Durable memory",
        description:
          "Write accepted decisions and conventions to human-readable project memory with rebuildable search acceleration.",
      },
      {
        title: "Preflight",
        description:
          "Block release-quality completion when architecture, projection, runtime, CLI, or web checks fail.",
      },
    ],
  },
  testimonials: {
    title: "Community feedback",
    subtitle: "What developers have shared about AG Kit on GitHub.",
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
        comment: "Good work with antigravity-kit. Love it — Cheers.",
        clamp: "line-clamp-2",
      },
      {
        name: "AlexOptimizer",
        role: "GitHub · #66",
        comment:
          "The separation into specialized agents and pluggable skills prevents AI context overload.",
        clamp: "line-clamp-3",
      },
      {
        name: "DRYN07",
        role: "GitHub · #67",
        comment:
          "Yours seems quite well-organized, so I thought I'd give it a try.",
        clamp: "line-clamp-2",
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
          "Antigravity now also supports .agents/ and it helps extensibility when installing other skills.",
        clamp: "line-clamp-3",
        className: "hidden lg:block",
      },
    ],
  },
  sponsored: {
    eyebrow: "Sponsored",
    title: "Supported by partners who ship",
    subtitle:
      "Sponsorship keeps AG Kit free, maintained, and open for everyone.",
    platinum: "Platinum sponsor",
    unikornBlurb:
      "A platform to discover and share technology products built by Vietnamese makers, from AI tools and education apps to utilities, games, and developer tools.",
    visitSponsor: "Visit sponsor",
    becomeTitle: "Become a sponsor",
    becomeDesc:
      "Support AG Kit maintenance and reach developers building with modern AI coding agents.",
    talk: "Talk sponsorship",
    coffee: "Buy me a coffee",
    wantBrand: "Want your brand next to AG Kit?",
    reachOut: "Reach out",
  },
  contribute: {
    eyebrow: "Contribute",
    title: "Developers who build AG Kit",
    subtitle:
      "Thank you to everyone contributing code, docs, runtime research, tests, and ideas.",
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
        question: "What is AG Kit v2?",
        answer:
          "AG Kit v2 is a lean multi-runtime operating layer for AI coding agents. It combines a tiny shared core, hot-loaded skills, local project memory, runtime adapters, specialist team assembly, MCP, and executable verification.",
      },
      {
        value: "runtimes",
        question: "Which runtimes are supported?",
        answer:
          "The current capability matrix contains 12 targets across first-class, connected, and bridge tiers. AG Kit only claims native surfaces that have been verified for that runtime.",
      },
      {
        value: "memory",
        question: "Where is project memory stored?",
        answer:
          "Markdown under .ag-kit/memory is canonical. SQLite FTS5 is an optional rebuildable warm index; recall falls back to Markdown if the index is unavailable.",
      },
      {
        value: "audit",
        question: "Can cross-audit modify my project?",
        answer:
          "No by design. Reviewer CLIs receive a snapshot or diff in a temporary workspace and do not get a writable mount of the source project.",
      },
      {
        value: "license",
        question: "Is AG Kit free?",
        answer:
          "Yes. AG Kit is MIT-licensed. You can use it commercially, fork it, and contribute improvements.",
      },
    ],
  },
  footer: {
    blurb:
      "Lean multi-runtime operating layer for modern AI coding agents.",
    product: "Product",
    resources: "Resources",
    community: "Community",
    legal: "Legal",
    documentation: "Documentation",
    agents: "Agents",
    skills: "Skills",
    workflows: "Flow",
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
    workflows: "Luồng",
    testimonials: "Đánh giá",
    sponsored: "Nhà tài trợ",
    contribute: "Đóng góp",
    faq: "Hỏi đáp",
    docs: "Tài liệu",
  },
  hero: {
    title: "Cho AI coding agent ít context hơn, nhiều bằng chứng hơn",
    subtitle:
      "Tiny shared core, 18 skill tải theo nhu cầu, bốn permanent agent, local-first memory, MCP, preflight gates và read-only cross-audit trên 12 runtime targets.",
    getStarted: "Bắt đầu",
    github: "GitHub",
  },
  stack: {
    title: "Core nhỏ. Phủ runtime rộng.",
    items: [
      "1 Core",
      "18 Skills",
      "4 Agents",
      "12 Runtimes",
      "MCP + Memory",
      "Mã nguồn mở",
    ],
  },
  benefits: {
    eyebrow: "Lợi ích",
    title: "Ít framework trong context. Nhiều công việc hữu ích hơn.",
    subtitle:
      "AG Kit giữ permanent context thật nhỏ và chỉ tải behavior, domain knowledge, specialist và verification khi task cần.",
    items: [
      {
        title: "Bảo vệ context budget",
        description:
          "Một tiny resident core thay cho hàng loạt persona và workflow instruction luôn bật.",
      },
      {
        title: "Một brain cho nhiều runtime",
        description:
          "Behavior canonical nằm ở một chỗ; adapter theo capability dịch nó sang từng runtime được hỗ trợ.",
      },
      {
        title: "Memory local và đọc được",
        description:
          "Markdown luôn là canonical project memory; SQLite FTS5 chỉ là lớp tăng tốc có thể rebuild.",
      },
      {
        title: "Verify thay vì đoán",
        description:
          "Preflight, native runtime checks, CI và read-only cross-audit tạo evidence và receipt thực thi được.",
      },
    ],
  },
  features: {
    eyebrow: "Tính năng",
    title: "Operating layer, không phải kho prompt",
    subtitle:
      "Kiến trúc v2 tách behavior, knowledge, runtime adapter, project state và verification để từng lớp đều nhỏ và test được.",
    items: [
      {
        title: "18 hot-loaded skills",
        description:
          "Capability chỉ vào context khi liên quan thay vì chiếm chỗ trong mọi session.",
      },
      {
        title: "Bốn permanent agents",
        description:
          "Scout, architect, builder và reviewer là core ổn định; specialist theo dự án chỉ sinh khi cần.",
      },
      {
        title: "Một development spine",
        description:
          "QUICK, STANDARD và DEEP dùng chung một flow thay cho nhiều workflow engine cạnh tranh nhau.",
      },
      {
        title: "12 runtime targets",
        description:
          "First-class, connected và bridge tiers chỉ bật surface AG Kit đã thực sự verify.",
      },
      {
        title: "Project-local MCP",
        description:
          "Memory, team, runtime và audit có thể dùng chung mà không giả vờ mọi runtime đều có cùng native feature.",
      },
      {
        title: "Cross-audit an toàn",
        description:
          "Reviewer CLI độc lập đọc snapshot hoặc diff trong temp directory, không được mount writable source tree.",
      },
    ],
  },
  workflows: {
    eyebrow: "Execution flow",
    title: "Một spine, ba mức độ sâu",
    subtitle:
      "Cùng một operating model chạy được từ fix một file đến migration nhiều hệ thống.",
    core: "Core",
    browseAll: "Xem kiến trúc flow",
    items: [
      {
        title: "QUICK",
        description:
          "Classify, tải skill tối thiểu, build, verify có mục tiêu rồi trả kết quả.",
      },
      {
        title: "STANDARD",
        description:
          "Scout codebase, chốt plan, build, review độc lập và verify acceptance criteria.",
      },
      {
        title: "DEEP",
        description:
          "Map risk/dependency, chạy theo waves, cross-audit khi cần rồi qua release gates.",
        highlight: true,
      },
      {
        title: "Project teams",
        description:
          "Sinh specialist tạm thời từ archetype software, web, research, content, game hoặc operations.",
      },
      {
        title: "Durable memory",
        description:
          "Lưu decision/convention đã chấp nhận vào project memory đọc được bằng mắt và index có thể rebuild.",
      },
      {
        title: "Preflight",
        description:
          "Không cho coi task release-quality là hoàn thành nếu architecture, projection, runtime, CLI hoặc web checks fail.",
      },
    ],
  },
  testimonials: {
    title: "Phản hồi cộng đồng",
    subtitle: "Một số phản hồi developer đã chia sẻ về AG Kit trên GitHub.",
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
        comment: "Good work with antigravity-kit. Love it — Cheers.",
        clamp: "line-clamp-2",
      },
      {
        name: "AlexOptimizer",
        role: "GitHub · #66",
        comment:
          "The separation into specialized agents and pluggable skills prevents AI context overload.",
        clamp: "line-clamp-3",
      },
      {
        name: "DRYN07",
        role: "GitHub · #67",
        comment:
          "Yours seems quite well-organized, so I thought I'd give it a try.",
        clamp: "line-clamp-2",
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
          "Antigravity now also supports .agents/ and it helps extensibility when installing other skills.",
        clamp: "line-clamp-3",
        className: "hidden lg:block",
      },
    ],
  },
  sponsored: {
    eyebrow: "Nhà tài trợ",
    title: "Được hỗ trợ bởi những đội ngũ thích ship",
    subtitle:
      "Tài trợ giúp AG Kit tiếp tục miễn phí, được bảo trì và mở cho mọi người.",
    platinum: "Nhà tài trợ Platinum",
    unikornBlurb:
      "Nền tảng khám phá và chia sẻ sản phẩm công nghệ do maker Việt Nam xây dựng, từ AI, giáo dục đến tiện ích, game và developer tools.",
    visitSponsor: "Xem nhà tài trợ",
    becomeTitle: "Trở thành nhà tài trợ",
    becomeDesc:
      "Hỗ trợ việc bảo trì AG Kit và tiếp cận developer đang xây dựng với AI coding agents hiện đại.",
    talk: "Trao đổi tài trợ",
    coffee: "Mời mình một ly cà phê",
    wantBrand: "Muốn thương hiệu xuất hiện cùng AG Kit?",
    reachOut: "Liên hệ",
  },
  contribute: {
    eyebrow: "Đóng góp",
    title: "Những developer xây AG Kit",
    subtitle:
      "Cảm ơn mọi người đã đóng góp code, docs, runtime research, tests và ý tưởng.",
    starLabel: "Star trên GitHub",
    guide: "Hướng dẫn đóng góp",
    loading: "Đang tải contributor...",
    empty: "Hiện chưa tải được contributor. Hãy xem repository trên GitHub.",
    commits: "commit",
    viewAll: "Xem tất cả contributor",
  },
  faq: {
    eyebrow: "Hỏi đáp",
    title: "Câu hỏi thường gặp",
    items: [
      {
        value: "what",
        question: "AG Kit v2 là gì?",
        answer:
          "AG Kit v2 là lớp vận hành multi-runtime gọn cho AI coding agents, kết hợp tiny shared core, hot-loaded skills, local project memory, runtime adapters, specialist team assembly, MCP và executable verification.",
      },
      {
        value: "runtimes",
        question: "Hỗ trợ những runtime nào?",
        answer:
          "Capability matrix hiện có 12 target thuộc các tier first-class, connected và bridge. AG Kit chỉ claim native surface đã được verify cho runtime đó.",
      },
      {
        value: "memory",
        question: "Project memory được lưu ở đâu?",
        answer:
          "Markdown dưới .ag-kit/memory là canonical. SQLite FTS5 là warm index tùy chọn có thể rebuild; recall tự fallback về Markdown nếu index không dùng được.",
      },
      {
        value: "audit",
        question: "Cross-audit có sửa project của tôi không?",
        answer:
          "Không theo thiết kế. Reviewer CLI chỉ nhận snapshot hoặc diff trong temp workspace và không có writable mount của source project.",
      },
      {
        value: "license",
        question: "AG Kit có miễn phí không?",
        answer:
          "Có. AG Kit dùng giấy phép MIT. Bạn có thể dùng thương mại, fork và đóng góp cải tiến.",
      },
    ],
  },
  footer: {
    blurb:
      "Lean multi-runtime operating layer cho AI coding agents hiện đại.",
    product: "Sản phẩm",
    resources: "Tài nguyên",
    community: "Cộng đồng",
    legal: "Pháp lý",
    documentation: "Tài liệu",
    agents: "Agents",
    skills: "Skills",
    workflows: "Flow",
    installation: "Cài đặt",
    cli: "CLI reference",
    changelog: "Changelog",
    github: "GitHub",
    issues: "Issues",
    discussions: "Discussions",
    license: "MIT License",
    security: "Bảo mật",
    credit: "Landing layout được điều chỉnh từ",
  },
};
