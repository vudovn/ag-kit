import type { Locale } from "./locale-store";
import type { LandingDictionary } from "./landing-dictionaries";
import {
    landingEn,
    landingJa,
    landingVi,
    landingZh,
} from "./landing-dictionaries";

type Dict = {
    nav: {
        github: string;
        sponsored: string;
        donate: string;
    };
    search: {
        placeholder: string;
        inputPlaceholder: string;
        noResults: string;
        noResultsHint: string;
        navigate: string;
        select: string;
        close: string;
        groupGettingStarted: string;
        groupCoreConcepts: string;
        groupReference: string;
        introduction: string;
        installation: string;
        agents: string;
        skills: string;
        workflows: string;
        cliReference: string;
        commandsOptions: string;
    };
    footer: {
        product: string;
        resources: string;
        community: string;
        legal: string;
        documentation: string;
        agents: string;
        skills: string;
        workflows: string;
        installation: string;
        cliReference: string;
        examples: string;
        changelog: string;
        github: string;
        issues: string;
        discussions: string;
        contributing: string;
        license: string;
        privacy: string;
        terms: string;
        rights: string;
    };
    toc: {
        onThisPage: string;
        empty: string;
    };
    home: {
        tagline: string;
        github: string;
        documentation: string;
    };
    landing: LandingDictionary;
    docsHome: {
        title: string;
        welcomePre: string;
        welcomePost: string;
        whatIsPre: string;
        whatIsPost: string;
        whatIsP1: string;
        whatIsP2a: string;
        whatIsP2b: string;
        whatIsP2c: string;
        whatIsP2d: string;
        includedTitle: string;
        specialistAgents: string;
        specialistAgentsDesc: string;
        domainSkills: string;
        domainSkillsDesc: string;
        workflowsLabel: string;
        workflowsDesc: string;
        howToTitle: string;
        howToP: string;
        gettingStarted: string;
        gettingStartedDesc: string;
        coreConcepts: string;
        coreConceptsDesc: string;
        cliRef: string;
        cliRefDesc: string;
        sidebarHintPre: string;
        sidebarHintPost: string;
        nextStepsTitle: string;
        installationArrow: string;
        installationArrowDesc: string;
        learnCoreArrow: string;
        learnCoreArrowDesc: string;
        footerGettingStarted: string;
        footerInstallation: string;
    };
    agentsPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        whatTitle: string;
        whatP1: string;
        whatP2a: string;
        whatP2Strong: string;
        whatP2b: string;
        howTitle: string;
        howP1Strong: string;
        howP1b: string;
        howP2a: string;
        howP2Strong: string;
        howP2b: string;
        tipStrong: string;
        tipTextA: string;
        tipTextB: string;
        availableTitle: string;
        availablePa: string;
        availablePb: string;
        structureTitle: string;
        structureP: string;
        structureNoteA: string;
        structureNoteB: string;
        nextTitle: string;
        skillsArrow: string;
        skillsArrowDesc: string;
        workflowsArrow: string;
        workflowsArrowDesc: string;
        footerInstallation: string;
        footerSkills: string;
    };
    skillsPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        whatTitle: string;
        whatP1: string;
        whatP2a: string;
        whatP2Em: string;
        whatP2b: string;
        noteStrong: string;
        noteText: string;
        howTitle: string;
        howP: string;
        step1Title: string;
        step1Desc: string;
        step2Title: string;
        step2Desc: string;
        step3Title: string;
        step3Desc: string;
        categoriesTitle: string;
        categoriesPb: string;
        structureTitle: string;
        structureP: string;
        nextTitle: string;
        workflowsArrow: string;
        workflowsArrowDesc: string;
        cliArrow: string;
        cliArrowDesc: string;
        footerAgents: string;
        footerWorkflows: string;
    };
    workflowsPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        whatTitle: string;
        whatP1: string;
        whatP2: string;
        howTitle: string;
        howP: string;
        tipStrong: string;
        tipTextA: string;
        tipTextB: string;
        availableTitle: string;
        availablePa: string;
        availablePb: string;
        exampleUsage: string;
        customTitle: string;
        customPa: string;
        customPb: string;
        customNoteA: string;
        customNoteB: string;
        customNoteC: string;
        nextTitle: string;
        cliArrow: string;
        cliArrowDesc: string;
        backAgentsArrow: string;
        backAgentsArrowDesc: string;
        footerSkills: string;
        footerCli: string;
    };
    installPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        quickStartTitle: string;
        quickStartPa: string;
        quickStartPb: string;
        calloutNoteStrong: string;
        calloutNoteA: string;
        calloutNoteB: string;
        globalTitle: string;
        globalPa: string;
        globalPb: string;
        globalReadOtherA: string;
        globalReadOtherLink: string;
        globalReadOtherB: string;
        structureTitle: string;
        structureP: string;
        agentDirDesc: string;
        skillsDirDesc: string;
        workflowsDirDesc: string;
        rulesDirDescA: string;
        rulesDirDescB: string;
        requirementsTitle: string;
        req1: string;
        req2: string;
        req3: string;
        nextTitle: string;
        nextP: string;
        agentsArrow: string;
        agentsArrowDesc: string;
        skillsArrow: string;
        skillsArrowDesc: string;
        footerIntroduction: string;
        footerAgents: string;
    };
    cliPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        overviewTitle: string;
        overviewPa: string;
        overviewPb: string;
        commandsTitle: string;
        initDescA: string;
        initDescB: string;
        behaviorTitle: string;
        initBehavior1a: string;
        initBehavior1b: string;
        initBehavior2: string;
        initBehavior3a: string;
        initBehavior3b: string;
        initBehavior3c: string;
        updateDesc: string;
        updateWarningStrong: string;
        updateWarningA: string;
        updateWarningB: string;
        statusDesc: string;
        rollbackDesc: string;
        rollbackBehavior1: string;
        rollbackBehavior2: string;
        rollbackBehavior3: string;
        outputIncludesTitle: string;
        statusOut1: string;
        statusOut2: string;
        statusOut3: string;
        statusOut4a: string;
        statusOut4b: string;
        statusOut5: string;
        optionsTitle: string;
        optionsP: string;
        tableOption: string;
        tableDescription: string;
        optForceA: string;
        optForceB: string;
        optForceC: string;
        optPathDesc: string;
        optBranchDesc: string;
        optQuietDesc: string;
        optDryRunA: string;
        optDryRunB: string;
        optDryRunC: string;
        optStrategyDesc: string;
        optNoBackupDesc: string;
        optConflictReportDesc: string;
        examplesTitle: string;
        exForceReinstall: string;
        exInstallDir: string;
        exDevBranch: string;
        exSilentCI: string;
        exPreviewUpdate: string;
        exReplace: string;
        exRollbackLatest: string;
        nextTitle: string;
        installGuideArrow: string;
        installGuideDesc: string;
        viewGithubArrow: string;
        viewGithubDesc: string;
        footerWorkflows: string;
    };
    changelogPage: {
        breadcrumbDocs: string;
        breadcrumbCurrent: string;
        title: string;
        subtitle: string;
        added: string;
        changed: string;
        fixed: string;
        removed: string;
        fullOnGithub: string;
    };
};

export const dictionaries: Record<Locale, Dict> = {
    en: {
        nav: { github: "GitHub", sponsored: "Sponsored", donate: "Donate" },
        search: {
            placeholder: "Search docs...",
            inputPlaceholder: "Search documentation...",
            noResults: "No results found",
            noResultsHint: "Try searching for something else",
            navigate: "Navigate",
            select: "Select",
            close: "Close",
            groupGettingStarted: "Getting Started",
            groupCoreConcepts: "Core Concepts",
            groupReference: "Reference",
            introduction: "Introduction",
            installation: "Installation",
            agents: "Agents",
            skills: "Skills",
            workflows: "Workflows",
            cliReference: "CLI Reference",
            commandsOptions: "Commands & Options",
        },
        footer: {
            product: "Product",
            resources: "Resources",
            community: "Community",
            legal: "Legal",
            documentation: "Documentation",
            agents: "Agents",
            skills: "Skills",
            workflows: "Workflows",
            installation: "Installation",
            cliReference: "CLI Reference",
            examples: "Examples",
            changelog: "Changelog",
            github: "GitHub",
            issues: "Issues",
            discussions: "Discussions",
            contributing: "Contributing",
            license: "License",
            privacy: "Privacy Policy",
            terms: "Terms of Service",
            rights: "All rights reserved.",
        },
        toc: { onThisPage: "On This Page", empty: "No sections on this page." },
        changelogPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "Changelog",
            title: "Changelog",
            subtitle: "Notable changes to AG Kit, newest first.",
            added: "Added",
            changed: "Changed",
            fixed: "Fixed",
            removed: "Removed",
            fullOnGithub: "View the full changelog on GitHub",
        },
        home: {
            tagline: "AI agent templates with Skills, Agents, and Workflows for modern coding assistants.",
            github: "GitHub",
            documentation: "Documentation",
        },
        landing: landingEn,
        docsHome: {
            title: "Documentation",
            welcomePre: "Welcome to the ",
            welcomePost: " documentation.",
            whatIsPre: "What is ",
            whatIsPost: " ?",
            whatIsP1: " is a comprehensive collection of AI agent templates with Skills, Agents, and Workflows designed to supercharge modern coding assistants.",
            whatIsP2a: "Whether you're an individual developer or part of a larger team, AG Kit helps you build better software faster with ",
            whatIsP2b: "+ skills, ",
            whatIsP2c: "+ specialist agents, and ",
            whatIsP2d: "+ production-ready workflows.",
            includedTitle: "What's Included",
            specialistAgents: "Specialist Agents",
            specialistAgentsDesc: "Domain experts for frontend, backend, security, and more",
            domainSkills: "Domain Skills",
            domainSkillsDesc: "Knowledge modules for React, Next.js, testing, and more",
            workflowsLabel: "Workflows",
            workflowsDesc: "Slash command procedures for common dev tasks",
            howToTitle: "How to Use the Docs",
            howToP: "The docs are organized into 3 main sections:",
            gettingStarted: "Getting Started",
            gettingStartedDesc: "Quick installation and setup guide to get you started",
            coreConcepts: "Core Concepts",
            coreConceptsDesc: "Learn about Agents, Skills, and Workflows",
            cliRef: "CLI Reference",
            cliRefDesc: "Detailed command-line interface documentation",
            sidebarHintPre: "Use the sidebar to navigate through sections, or use ",
            sidebarHintPost: " to quickly search.",
            nextStepsTitle: "Next Steps",
            installationArrow: "Installation →",
            installationArrowDesc: "Get started with AG Kit in under a minute",
            learnCoreArrow: "Learn Core Concepts →",
            learnCoreArrowDesc: "Understand how Agents, Skills, and Workflows work",
            footerGettingStarted: "Getting Started",
            footerInstallation: "Installation",
        },
        agentsPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "Agents",
            title: "Agents",
            subtitle: "Specialist AI personas with deep expertise in specific domains.",
            whatTitle: "What are Agents?",
            whatP1: "Agents are specialist AI personas configured with domain-specific expertise, tools, and behavioral patterns. Each agent is designed to excel in a particular area of software development.",
            whatP2a: "When you make a request, AG Kit's ",
            whatP2Strong: "Intelligent Routing",
            whatP2b: " system automatically detects which agents are needed and activates them for you. You can also mention them by name to force a specific perspective.",
            howTitle: "How to Use Agents",
            howP1Strong: "No need to mention agents explicitly!",
            howP1b: " The system automatically detects and applies the right specialist(s) based on your request.",
            howP2a: "However, you ",
            howP2Strong: "can still override",
            howP2b: " this behavior by explicitly mentioning an agent name:",
            tipStrong: "Tip:",
            tipTextA: " Agents can work together! Use the ",
            tipTextB: " agent to coordinate multiple specialists on complex tasks.",
            availableTitle: "Available Agents",
            availablePa: "AG Kit includes ",
            availablePb: " specialist agents:",
            structureTitle: "Agent Structure",
            structureP: "Each agent is defined by a markdown file with YAML frontmatter:",
            structureNoteA: "The ",
            structureNoteB: " field determines which domain knowledge modules the agent can access.",
            nextTitle: "Next Steps",
            skillsArrow: "Skills →",
            skillsArrowDesc: "Learn about domain-specific knowledge modules",
            workflowsArrow: "Workflows →",
            workflowsArrowDesc: "Explore slash command procedures",
            footerInstallation: "Installation",
            footerSkills: "Skills",
        },
        skillsPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "Skills",
            title: "Skills",
            subtitle: "Domain-specific knowledge modules that agents load automatically.",
            whatTitle: "What are Skills?",
            whatP1: "Skills are modular knowledge packages that contain principles, patterns, and decision-making frameworks for specific domains. They're loaded automatically when an agent needs them.",
            whatP2a: "Unlike hard-coded templates, skills teach ",
            whatP2Em: "principles",
            whatP2b: " — enabling agents to make contextual decisions rather than copying patterns.",
            noteStrong: " Note:",
            noteText: " Skills are loaded on-demand based on task context. You don't need to configure anything manually.",
            howTitle: "How Skills Work",
            howP: "When you invoke an agent, it automatically loads relevant skills based on:",
            step1Title: "Agent Configuration",
            step1Desc: "Each agent specifies which skills it can access in its frontmatter",
            step2Title: "Task Context",
            step2Desc: "The AI reads skill descriptions and loads relevant ones",
            step3Title: "Selective Reading",
            step3Desc: "Only necessary sections are read to optimize context usage",
            categoriesTitle: "Skill Categories",
            categoriesPb: "+ skills organized by domain:",
            structureTitle: "Skill Structure",
            structureP: "Each skill contains:",
            nextTitle: "Next Steps",
            workflowsArrow: "Workflows →",
            workflowsArrowDesc: "Learn about slash command procedures",
            cliArrow: "CLI Reference →",
            cliArrowDesc: "Explore command-line tools",
            footerAgents: "Agents",
            footerWorkflows: "Workflows",
        },
        workflowsPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "Workflows",
            title: "Workflows",
            subtitle: "Slash command procedures for common development tasks.",
            whatTitle: "What are Workflows?",
            whatP1: "Workflows are well-defined, step-by-step procedures for achieving specific development tasks. They're invoked using slash commands and provide consistent, repeatable processes.",
            whatP2: "Each workflow contains specific instructions, decision points, and best practices for its domain.",
            howTitle: "How to Use Workflows",
            howP: "Simply type a slash command followed by your task description:",
            tipStrong: " Tip:",
            tipTextA: " Some workflows have a ",
            tipTextB: " annotation that allows auto-running safe commands without user approval.",
            availableTitle: "Available Workflows",
            availablePa: "",
            availablePb: " workflows covering common development scenarios:",
            exampleUsage: "Example Usage",
            customTitle: "Creating Custom Workflows",
            customPa: "You can create your own workflows by adding markdown files to ",
            customPb: ":",
            customNoteA: "Save as ",
            customNoteB: " and invoke with ",
            customNoteC: ".",
            nextTitle: "Next Steps",
            cliArrow: "CLI Reference →",
            cliArrowDesc: "Learn about command-line tools",
            backAgentsArrow: "Back to Agents →",
            backAgentsArrowDesc: "Review specialist agents",
            footerSkills: "Skills",
            footerCli: "CLI Reference",
        },
        installPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "Installation",
            title: "Installation",
            subtitle: "Get started with AG Kit in under a minute.",
            quickStartTitle: "Quick Start",
            quickStartPa: "The fastest way to install AG Kit is using ",
            quickStartPb: " in root project:",
            calloutNoteStrong: "Note:",
            calloutNoteA: " This command will create a ",
            calloutNoteB: " folder in your current directory containing all templates.",
            globalTitle: "Global Installation",
            globalPa: "Install the CLI globally to use ",
            globalPb: " command anywhere:",
            globalReadOtherA: "Read other commands in ",
            globalReadOtherLink: "CLI commands",
            globalReadOtherB: " documentation.",
            structureTitle: "What Gets Installed",
            structureP: "After running the installation command, you'll have the following structure:",
            agentDirDesc: "Contains 20 specialist AI agent configurations for different domains (frontend, backend, security, etc.)",
            skillsDirDesc: "48 domain-specific knowledge modules that agents can use",
            workflowsDirDesc: "13 slash command procedures for common development tasks",
            rulesDirDescA: "Workspace configuration including ",
            rulesDirDescB: " for behavior rules",
            requirementsTitle: "System Requirements",
            req1: "Node.js 18.0 or later",
            req2: "npm or yarn package manager",
            req3: "Git (for updates and version control)",
            nextTitle: "Next Steps",
            nextP: "Now that you have AG Kit installed, learn about the core concepts:",
            agentsArrow: "Agents →",
            agentsArrowDesc: "Learn about specialist AI agents",
            skillsArrow: "Skills →",
            skillsArrowDesc: "Discover 48 domain-specific skills",
            footerIntroduction: "Introduction",
            footerAgents: "Agents",
        },
        cliPage: {
            breadcrumbDocs: "Docs",
            breadcrumbCurrent: "CLI Reference",
            title: "CLI Reference",
            subtitle: "Command-line interface for managing AG Kit installations.",
            overviewTitle: "Overview",
            overviewPa: "The ",
            overviewPb: " CLI tool helps you manage AG Kit installations across your projects.",
            commandsTitle: "Commands",
            initDescA: "Initialize AG Kit in your project by installing the ",
            initDescB: " folder.",
            behaviorTitle: "Behavior",
            initBehavior1a: "Creates ",
            initBehavior1b: " directory in current folder",
            initBehavior2: "Downloads latest templates from GitHub",
            initBehavior3a: "Skips  if ",
            initBehavior3b: " already exists (use ",
            initBehavior3c: " to override)",
            updateDesc: "Update your existing AG Kit installation to the latest version.",
            updateWarningStrong: "Warning:",
            updateWarningA: " This will delete and replace your ",
            updateWarningB: " folder. Make sure to backup any custom changes.",
            statusDesc: "Check the current installation status and check npm for a newer release.",
            rollbackDesc: "Restore a pre-update backup of the managed tree. Defaults to the newest backup; pick one with --backup <id>.",
            rollbackBehavior1: "Lists available backups and restores the selected one",
            rollbackBehavior2: "Backs up the current tree first (disable with --no-keep-current)",
            rollbackBehavior3: "Preview which backup would be restored with --dry-run",
            outputIncludesTitle: "Output Includes",
            statusOut1: "CLI version",
            statusOut2: "Installation status (installed/not installed)",
            statusOut3: "Install path and last-modified time",
            statusOut4a: "Item count at the ",
            statusOut4b: " root",
            statusOut5: "Update notification if a newer version is available",
            optionsTitle: "Options",
            optionsP: "Customize CLI behavior with these options:",
            tableOption: "Option",
            tableDescription: "Description",
            optForceA: "Overwrite existing ",
            optForceB: " folder (on ",
            optForceC: ", skip the confirmation prompt)",
            optPathDesc: "Install in specific directory instead of current folder",
            optBranchDesc: "Use a specific Git branch (defaults to the repo default branch)",
            optQuietDesc: "Suppress output (useful for CI/CD pipelines)",
            optDryRunA: "Preview actions without executing (",
            optDryRunB: " / ",
            optDryRunC: ")",
            optStrategyDesc: "Update strategy: merge preserves local changes; replace restores the upstream tree",
            optNoBackupDesc: "Skip the automatic pre-update backup",
            optConflictReportDesc: "Write the update/conflict report to a custom path",
            examplesTitle: "Examples",
            exForceReinstall: "Force reinstall",
            exInstallDir: "Install in specific directory",
            exDevBranch: "Use development branch",
            exSilentCI: "Silent install for CI/CD",
            exPreviewUpdate: "Preview an update without applying it",
            exReplace: "Restore the pristine upstream tree",
            exRollbackLatest: "Roll back to the newest backup",
            nextTitle: "Next Steps",
            installGuideArrow: "Installation Guide →",
            installGuideDesc: "Full installation instructions",
            viewGithubArrow: "View on GitHub →",
            viewGithubDesc: "Source code and contribution guide",
            footerWorkflows: "Workflows",
        },
    },
    vi: {
        nav: { github: "GitHub", sponsored: "Tài trợ", donate: "Ủng hộ" },
        search: {
            placeholder: "Tìm tài liệu...",
            inputPlaceholder: "Tìm trong tài liệu...",
            noResults: "Không tìm thấy kết quả",
            noResultsHint: "Thử tìm từ khóa khác",
            navigate: "Di chuyển",
            select: "Chọn",
            close: "Đóng",
            groupGettingStarted: "Bắt đầu",
            groupCoreConcepts: "Khái niệm cốt lõi",
            groupReference: "Tham khảo",
            introduction: "Giới thiệu",
            installation: "Cài đặt",
            agents: "Agents",
            skills: "Kỹ năng",
            workflows: "Quy trình",
            cliReference: "Tài liệu CLI",
            commandsOptions: "Lệnh & Tùy chọn",
        },
        footer: {
            product: "Sản phẩm",
            resources: "Tài nguyên",
            community: "Cộng đồng",
            legal: "Pháp lý",
            documentation: "Tài liệu",
            agents: "Agents",
            skills: "Kỹ năng",
            workflows: "Quy trình",
            installation: "Cài đặt",
            cliReference: "Tài liệu CLI",
            examples: "Ví dụ",
            changelog: "Nhật ký thay đổi",
            github: "GitHub",
            issues: "Vấn đề",
            discussions: "Thảo luận",
            contributing: "Đóng góp",
            license: "Giấy phép",
            privacy: "Chính sách bảo mật",
            terms: "Điều khoản dịch vụ",
            rights: "Bảo lưu mọi quyền.",
        },
        toc: { onThisPage: "Trong trang này", empty: "Trang này không có mục nào." },
        changelogPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Nhật ký thay đổi",
            title: "Nhật ký thay đổi",
            subtitle: "Các thay đổi đáng chú ý của AG Kit, mới nhất ở trên.",
            added: "Thêm mới",
            changed: "Thay đổi",
            fixed: "Sửa lỗi",
            removed: "Gỡ bỏ",
            fullOnGithub: "Xem nhật ký đầy đủ trên GitHub",
        },
        home: {
            tagline: "Bộ mẫu AI agent với Skills, Agents và Workflows cho các trợ lý lập trình hiện đại.",
            github: "GitHub",
            documentation: "Tài liệu",
        },
        landing: landingVi,
        docsHome: {
            title: "Tài liệu",
            welcomePre: "Chào mừng bạn đến với tài liệu ",
            welcomePost: ".",
            whatIsPre: "",
            whatIsPost: " là gì?",
            whatIsP1: " là bộ sưu tập toàn diện các mẫu AI agent với Skills, Agents và Workflows, được thiết kế để tăng sức mạnh cho các trợ lý lập trình hiện đại.",
            whatIsP2a: "Dù bạn là lập trình viên cá nhân hay thành viên của một nhóm lớn, AG Kit giúp bạn xây dựng phần mềm tốt hơn và nhanh hơn với ",
            whatIsP2b: "+ kỹ năng, ",
            whatIsP2c: "+ agent chuyên biệt, và ",
            whatIsP2d: "+ quy trình sẵn sàng cho sản xuất.",
            includedTitle: "Bao gồm những gì",
            specialistAgents: "Agent chuyên biệt",
            specialistAgentsDesc: "Chuyên gia lĩnh vực cho frontend, backend, bảo mật và nhiều hơn nữa",
            domainSkills: "Kỹ năng theo lĩnh vực",
            domainSkillsDesc: "Mô-đun kiến thức cho React, Next.js, testing và nhiều hơn nữa",
            workflowsLabel: "Quy trình",
            workflowsDesc: "Các thủ tục lệnh gạch chéo cho những tác vụ phát triển thường gặp",
            howToTitle: "Cách sử dụng tài liệu",
            howToP: "Tài liệu được tổ chức thành 3 phần chính:",
            gettingStarted: "Bắt đầu",
            gettingStartedDesc: "Hướng dẫn cài đặt và thiết lập nhanh để bạn bắt đầu",
            coreConcepts: "Khái niệm cốt lõi",
            coreConceptsDesc: "Tìm hiểu về Agents, Skills và Workflows",
            cliRef: "Tài liệu CLI",
            cliRefDesc: "Tài liệu chi tiết về giao diện dòng lệnh",
            sidebarHintPre: "Dùng thanh bên để di chuyển qua các phần, hoặc nhấn ",
            sidebarHintPost: " để tìm kiếm nhanh.",
            nextStepsTitle: "Bước tiếp theo",
            installationArrow: "Cài đặt →",
            installationArrowDesc: "Bắt đầu với AG Kit trong chưa đầy một phút",
            learnCoreArrow: "Tìm hiểu khái niệm cốt lõi →",
            learnCoreArrowDesc: "Hiểu cách Agents, Skills và Workflows hoạt động",
            footerGettingStarted: "Bắt đầu",
            footerInstallation: "Cài đặt",
        },
        agentsPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Agents",
            title: "Agents",
            subtitle: "Những nhân cách AI chuyên biệt với chuyên môn sâu trong các lĩnh vực cụ thể.",
            whatTitle: "Agents là gì?",
            whatP1: "Agents là những nhân cách AI chuyên biệt được cấu hình với chuyên môn theo lĩnh vực, công cụ và các khuôn mẫu hành vi. Mỗi agent được thiết kế để xuất sắc trong một mảng cụ thể của phát triển phần mềm.",
            whatP2a: "Khi bạn đưa ra yêu cầu, hệ thống ",
            whatP2Strong: "Định tuyến thông minh",
            whatP2b: " của AG Kit tự động phát hiện cần những agent nào và kích hoạt chúng cho bạn. Bạn cũng có thể gọi tên chúng để buộc một góc nhìn cụ thể.",
            howTitle: "Cách sử dụng Agents",
            howP1Strong: "Không cần đề cập agent một cách rõ ràng!",
            howP1b: " Hệ thống tự động phát hiện và áp dụng (các) chuyên gia phù hợp dựa trên yêu cầu của bạn.",
            howP2a: "Tuy nhiên, bạn ",
            howP2Strong: "vẫn có thể ghi đè",
            howP2b: " hành vi này bằng cách đề cập rõ ràng tên một agent:",
            tipStrong: "Mẹo:",
            tipTextA: " Các agent có thể phối hợp với nhau! Dùng agent ",
            tipTextB: " để điều phối nhiều chuyên gia cho các tác vụ phức tạp.",
            availableTitle: "Các Agent có sẵn",
            availablePa: "AG Kit bao gồm ",
            availablePb: " agent chuyên biệt:",
            structureTitle: "Cấu trúc Agent",
            structureP: "Mỗi agent được định nghĩa bằng một tệp markdown với frontmatter YAML:",
            structureNoteA: "Trường ",
            structureNoteB: " xác định những mô-đun kiến thức theo lĩnh vực mà agent có thể truy cập.",
            nextTitle: "Bước tiếp theo",
            skillsArrow: "Kỹ năng →",
            skillsArrowDesc: "Tìm hiểu về các mô-đun kiến thức theo lĩnh vực",
            workflowsArrow: "Quy trình →",
            workflowsArrowDesc: "Khám phá các thủ tục lệnh gạch chéo",
            footerInstallation: "Cài đặt",
            footerSkills: "Kỹ năng",
        },
        skillsPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Kỹ năng",
            title: "Kỹ năng",
            subtitle: "Các mô-đun kiến thức theo lĩnh vực mà agent tải tự động.",
            whatTitle: "Kỹ năng là gì?",
            whatP1: "Kỹ năng là các gói kiến thức mô-đun chứa nguyên tắc, khuôn mẫu và khung ra quyết định cho những lĩnh vực cụ thể. Chúng được tải tự động khi một agent cần đến.",
            whatP2a: "Khác với các mẫu cứng nhắc, kỹ năng dạy ",
            whatP2Em: "nguyên tắc",
            whatP2b: " — giúp agent đưa ra quyết định theo ngữ cảnh thay vì sao chép khuôn mẫu.",
            noteStrong: " Lưu ý:",
            noteText: " Kỹ năng được tải theo nhu cầu dựa trên ngữ cảnh tác vụ. Bạn không cần cấu hình bất cứ điều gì thủ công.",
            howTitle: "Kỹ năng hoạt động thế nào",
            howP: "Khi bạn gọi một agent, nó tự động tải các kỹ năng liên quan dựa trên:",
            step1Title: "Cấu hình Agent",
            step1Desc: "Mỗi agent chỉ định những kỹ năng nó có thể truy cập trong frontmatter của mình",
            step2Title: "Ngữ cảnh tác vụ",
            step2Desc: "AI đọc mô tả kỹ năng và tải những kỹ năng liên quan",
            step3Title: "Đọc có chọn lọc",
            step3Desc: "Chỉ những phần cần thiết được đọc để tối ưu việc sử dụng ngữ cảnh",
            categoriesTitle: "Danh mục kỹ năng",
            categoriesPb: "+ kỹ năng được tổ chức theo lĩnh vực:",
            structureTitle: "Cấu trúc kỹ năng",
            structureP: "Mỗi kỹ năng chứa:",
            nextTitle: "Bước tiếp theo",
            workflowsArrow: "Quy trình →",
            workflowsArrowDesc: "Tìm hiểu về các thủ tục lệnh gạch chéo",
            cliArrow: "Tài liệu CLI →",
            cliArrowDesc: "Khám phá các công cụ dòng lệnh",
            footerAgents: "Agents",
            footerWorkflows: "Quy trình",
        },
        workflowsPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Quy trình",
            title: "Quy trình",
            subtitle: "Các thủ tục lệnh gạch chéo cho những tác vụ phát triển thường gặp.",
            whatTitle: "Quy trình là gì?",
            whatP1: "Quy trình là những thủ tục được xác định rõ ràng, theo từng bước để hoàn thành các tác vụ phát triển cụ thể. Chúng được gọi bằng lệnh gạch chéo và mang lại các quy trình nhất quán, có thể lặp lại.",
            whatP2: "Mỗi quy trình chứa các hướng dẫn cụ thể, điểm ra quyết định và thực hành tốt nhất cho lĩnh vực của nó.",
            howTitle: "Cách sử dụng Quy trình",
            howP: "Chỉ cần gõ một lệnh gạch chéo theo sau là mô tả tác vụ của bạn:",
            tipStrong: " Mẹo:",
            tipTextA: " Một số quy trình có chú thích ",
            tipTextB: " cho phép tự động chạy các lệnh an toàn mà không cần người dùng phê duyệt.",
            availableTitle: "Các Quy trình có sẵn",
            availablePa: "",
            availablePb: " quy trình bao quát các tình huống phát triển thường gặp:",
            exampleUsage: "Ví dụ sử dụng",
            customTitle: "Tạo Quy trình tùy chỉnh",
            customPa: "Bạn có thể tạo quy trình của riêng mình bằng cách thêm các tệp markdown vào ",
            customPb: ":",
            customNoteA: "Lưu thành ",
            customNoteB: " và gọi bằng ",
            customNoteC: ".",
            nextTitle: "Bước tiếp theo",
            cliArrow: "Tài liệu CLI →",
            cliArrowDesc: "Tìm hiểu về các công cụ dòng lệnh",
            backAgentsArrow: "Quay lại Agents →",
            backAgentsArrowDesc: "Xem lại các agent chuyên biệt",
            footerSkills: "Kỹ năng",
            footerCli: "Tài liệu CLI",
        },
        installPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Cài đặt",
            title: "Cài đặt",
            subtitle: "Bắt đầu với AG Kit trong chưa đầy một phút.",
            quickStartTitle: "Bắt đầu nhanh",
            quickStartPa: "Cách nhanh nhất để cài đặt AG Kit là dùng ",
            quickStartPb: " trong thư mục gốc của dự án:",
            calloutNoteStrong: "Lưu ý:",
            calloutNoteA: " Lệnh này sẽ tạo một thư mục ",
            calloutNoteB: " trong thư mục hiện tại của bạn chứa tất cả các mẫu.",
            globalTitle: "Cài đặt toàn cục",
            globalPa: "Cài đặt CLI toàn cục để dùng lệnh ",
            globalPb: " ở bất cứ đâu:",
            globalReadOtherA: "Đọc các lệnh khác trong tài liệu ",
            globalReadOtherLink: "lệnh CLI",
            globalReadOtherB: ".",
            structureTitle: "Những gì được cài đặt",
            structureP: "Sau khi chạy lệnh cài đặt, bạn sẽ có cấu trúc sau:",
            agentDirDesc: "Chứa 20 cấu hình AI agent chuyên biệt cho các lĩnh vực khác nhau (frontend, backend, bảo mật, v.v.)",
            skillsDirDesc: "48 mô-đun kiến thức theo lĩnh vực mà agent có thể sử dụng",
            workflowsDirDesc: "13 thủ tục lệnh gạch chéo cho những tác vụ phát triển thường gặp",
            rulesDirDescA: "Cấu hình workspace bao gồm ",
            rulesDirDescB: " cho các quy tắc hành vi",
            requirementsTitle: "Yêu cầu hệ thống",
            req1: "Node.js 18.0 trở lên",
            req2: "Trình quản lý gói npm hoặc yarn",
            req3: "Git (cho cập nhật và quản lý phiên bản)",
            nextTitle: "Bước tiếp theo",
            nextP: "Giờ bạn đã cài đặt AG Kit, hãy tìm hiểu về các khái niệm cốt lõi:",
            agentsArrow: "Agents →",
            agentsArrowDesc: "Tìm hiểu về các AI agent chuyên biệt",
            skillsArrow: "Kỹ năng →",
            skillsArrowDesc: "Khám phá 48 kỹ năng theo lĩnh vực",
            footerIntroduction: "Giới thiệu",
            footerAgents: "Agents",
        },
        cliPage: {
            breadcrumbDocs: "Tài liệu",
            breadcrumbCurrent: "Tài liệu CLI",
            title: "Tài liệu CLI",
            subtitle: "Giao diện dòng lệnh để quản lý các bản cài đặt AG Kit.",
            overviewTitle: "Tổng quan",
            overviewPa: "Công cụ CLI ",
            overviewPb: " giúp bạn quản lý các bản cài đặt AG Kit trên các dự án của mình.",
            commandsTitle: "Lệnh",
            initDescA: "Khởi tạo AG Kit trong dự án của bạn bằng cách cài đặt thư mục ",
            initDescB: ".",
            behaviorTitle: "Hành vi",
            initBehavior1a: "Tạo thư mục ",
            initBehavior1b: " trong thư mục hiện tại",
            initBehavior2: "Tải các mẫu mới nhất từ GitHub",
            initBehavior3a: "Bỏ qua nếu ",
            initBehavior3b: " đã tồn tại (dùng ",
            initBehavior3c: " để ghi đè)",
            updateDesc: "Cập nhật bản cài đặt AG Kit hiện có của bạn lên phiên bản mới nhất.",
            updateWarningStrong: "Cảnh báo:",
            updateWarningA: " Thao tác này sẽ xóa và thay thế thư mục ",
            updateWarningB: " của bạn. Hãy đảm bảo sao lưu mọi thay đổi tùy chỉnh.",
            statusDesc: "Kiểm tra trạng thái cài đặt hiện tại và kiểm tra npm xem có bản phát hành mới hơn không.",
            rollbackDesc: "Khôi phục bản sao lưu trước khi cập nhật của cây được quản lý. Mặc định dùng bản sao lưu mới nhất; chọn bản khác với --backup <id>.",
            rollbackBehavior1: "Liệt kê các bản sao lưu có sẵn và khôi phục bản được chọn",
            rollbackBehavior2: "Sao lưu cây hiện tại trước (tắt bằng --no-keep-current)",
            rollbackBehavior3: "Xem trước bản sao lưu sẽ được khôi phục với --dry-run",
            outputIncludesTitle: "Đầu ra bao gồm",
            statusOut1: "Phiên bản CLI",
            statusOut2: "Trạng thái cài đặt (đã cài/chưa cài)",
            statusOut3: "Đường dẫn cài đặt và thời gian sửa đổi gần nhất",
            statusOut4a: "Số lượng mục tại thư mục gốc ",
            statusOut4b: "",
            statusOut5: "Thông báo cập nhật nếu có phiên bản mới hơn",
            optionsTitle: "Tùy chọn",
            optionsP: "Tùy chỉnh hành vi của CLI với các tùy chọn sau:",
            tableOption: "Tùy chọn",
            tableDescription: "Mô tả",
            optForceA: "Ghi đè thư mục ",
            optForceB: " đang tồn tại (với ",
            optForceC: ", bỏ qua lời nhắc xác nhận)",
            optPathDesc: "Cài đặt vào thư mục cụ thể thay vì thư mục hiện tại",
            optBranchDesc: "Dùng một nhánh Git cụ thể (mặc định là nhánh mặc định của repo)",
            optQuietDesc: "Ẩn đầu ra (hữu ích cho các pipeline CI/CD)",
            optDryRunA: "Xem trước các hành động mà không thực thi (",
            optDryRunB: " / ",
            optDryRunC: ")",
            optStrategyDesc: "Chiến lược cập nhật: merge giữ thay đổi cục bộ; replace khôi phục cây upstream",
            optNoBackupDesc: "Bỏ qua sao lưu tự động trước khi cập nhật",
            optConflictReportDesc: "Ghi báo cáo cập nhật/xung đột vào đường dẫn tùy chỉnh",
            examplesTitle: "Ví dụ",
            exForceReinstall: "Cài đặt lại bắt buộc",
            exInstallDir: "Cài đặt vào thư mục cụ thể",
            exDevBranch: "Dùng nhánh phát triển",
            exSilentCI: "Cài đặt im lặng cho CI/CD",
            exPreviewUpdate: "Xem trước bản cập nhật mà không áp dụng",
            exReplace: "Khôi phục cây gốc từ upstream",
            exRollbackLatest: "Quay lại bản sao lưu mới nhất",
            nextTitle: "Bước tiếp theo",
            installGuideArrow: "Hướng dẫn cài đặt →",
            installGuideDesc: "Hướng dẫn cài đặt đầy đủ",
            viewGithubArrow: "Xem trên GitHub →",
            viewGithubDesc: "Mã nguồn và hướng dẫn đóng góp",
            footerWorkflows: "Quy trình",
        },
    },
    zh: {
        nav: { github: "GitHub", sponsored: "赞助", donate: "捐赠" },
        search: {
            placeholder: "搜索文档...",
            inputPlaceholder: "在文档中搜索...",
            noResults: "未找到结果",
            noResultsHint: "试试搜索其他内容",
            navigate: "导航",
            select: "选择",
            close: "关闭",
            groupGettingStarted: "入门",
            groupCoreConcepts: "核心概念",
            groupReference: "参考",
            introduction: "简介",
            installation: "安装",
            agents: "Agents",
            skills: "技能",
            workflows: "工作流",
            cliReference: "CLI 参考",
            commandsOptions: "命令与选项",
        },
        footer: {
            product: "产品",
            resources: "资源",
            community: "社区",
            legal: "法律",
            documentation: "文档",
            agents: "Agents",
            skills: "技能",
            workflows: "工作流",
            installation: "安装",
            cliReference: "CLI 参考",
            examples: "示例",
            changelog: "更新日志",
            github: "GitHub",
            issues: "问题",
            discussions: "讨论",
            contributing: "贡献",
            license: "许可证",
            privacy: "隐私政策",
            terms: "服务条款",
            rights: "保留所有权利。",
        },
        toc: { onThisPage: "本页内容", empty: "本页没有章节。" },
        changelogPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "更新日志",
            title: "更新日志",
            subtitle: "AG Kit 的重要变更，最新在前。",
            added: "新增",
            changed: "变更",
            fixed: "修复",
            removed: "移除",
            fullOnGithub: "在 GitHub 上查看完整更新日志",
        },
        home: {
            tagline: "面向现代编程助手的 AI agent 模板，内置 Skills、Agents 和 Workflows。",
            github: "GitHub",
            documentation: "文档",
        },
        landing: landingZh,
        docsHome: {
            title: "文档",
            welcomePre: "欢迎使用 ",
            welcomePost: " 文档。",
            whatIsPre: "",
            whatIsPost: " 是什么？",
            whatIsP1: " 是一套全面的 AI agent 模板集合，内置 Skills、Agents 和 Workflows，旨在为现代编程助手注入强劲动力。",
            whatIsP2a: "无论你是独立开发者还是大型团队的一员，AG Kit 都能帮你更快地构建更优质的软件，拥有 ",
            whatIsP2b: "+ 个技能、",
            whatIsP2c: "+ 个专业 agent，以及 ",
            whatIsP2d: "+ 个生产就绪的工作流。",
            includedTitle: "包含内容",
            specialistAgents: "专业 Agent",
            specialistAgentsDesc: "面向前端、后端、安全等领域的专家",
            domainSkills: "领域技能",
            domainSkillsDesc: "React、Next.js、测试等知识模块",
            workflowsLabel: "工作流",
            workflowsDesc: "用于常见开发任务的斜杠命令流程",
            howToTitle: "如何使用文档",
            howToP: "文档分为 3 个主要部分：",
            gettingStarted: "入门",
            gettingStartedDesc: "快速安装和设置指南，助你上手",
            coreConcepts: "核心概念",
            coreConceptsDesc: "了解 Agents、Skills 和 Workflows",
            cliRef: "CLI 参考",
            cliRefDesc: "详细的命令行界面文档",
            sidebarHintPre: "使用侧边栏浏览各部分，或使用 ",
            sidebarHintPost: " 快速搜索。",
            nextStepsTitle: "后续步骤",
            installationArrow: "安装 →",
            installationArrowDesc: "不到一分钟即可开始使用 AG Kit",
            learnCoreArrow: "了解核心概念 →",
            learnCoreArrowDesc: "理解 Agents、Skills 和 Workflows 如何运作",
            footerGettingStarted: "入门",
            footerInstallation: "安装",
        },
        agentsPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "Agents",
            title: "Agents",
            subtitle: "在特定领域拥有深厚专长的专业 AI 角色。",
            whatTitle: "Agents 是什么？",
            whatP1: "Agents 是配置了特定领域专长、工具和行为模式的专业 AI 角色。每个 agent 都旨在精通软件开发的某个特定领域。",
            whatP2a: "当你发出请求时，AG Kit 的 ",
            whatP2Strong: "智能路由",
            whatP2b: " 系统会自动检测需要哪些 agent 并为你激活它们。你也可以直接点名以强制使用某个特定视角。",
            howTitle: "如何使用 Agents",
            howP1Strong: "无需显式提及 agent！",
            howP1b: " 系统会根据你的请求自动检测并应用合适的专家。",
            howP2a: "不过，你 ",
            howP2Strong: "仍然可以覆盖",
            howP2b: " 这一行为，方法是显式提及某个 agent 名称：",
            tipStrong: "提示：",
            tipTextA: " Agent 可以协同工作！使用 ",
            tipTextB: " agent 来协调多个专家处理复杂任务。",
            availableTitle: "可用的 Agent",
            availablePa: "AG Kit 包含 ",
            availablePb: " 个专业 agent：",
            structureTitle: "Agent 结构",
            structureP: "每个 agent 由一个带 YAML frontmatter 的 markdown 文件定义：",
            structureNoteA: "该 ",
            structureNoteB: " 字段决定 agent 可以访问哪些领域知识模块。",
            nextTitle: "后续步骤",
            skillsArrow: "技能 →",
            skillsArrowDesc: "了解特定领域的知识模块",
            workflowsArrow: "工作流 →",
            workflowsArrowDesc: "探索斜杠命令流程",
            footerInstallation: "安装",
            footerSkills: "技能",
        },
        skillsPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "技能",
            title: "技能",
            subtitle: "agent 自动加载的特定领域知识模块。",
            whatTitle: "技能是什么？",
            whatP1: "技能是模块化的知识包，包含特定领域的原则、模式和决策框架。当 agent 需要时会自动加载它们。",
            whatP2a: "与硬编码的模板不同，技能传授 ",
            whatP2Em: "原则",
            whatP2b: " —— 让 agent 能够根据上下文做出决策，而不是照搬模式。",
            noteStrong: " 注意：",
            noteText: " 技能会根据任务上下文按需加载。你无需手动配置任何东西。",
            howTitle: "技能如何运作",
            howP: "当你调用一个 agent 时，它会根据以下因素自动加载相关技能：",
            step1Title: "Agent 配置",
            step1Desc: "每个 agent 在其 frontmatter 中指定可以访问哪些技能",
            step2Title: "任务上下文",
            step2Desc: "AI 读取技能描述并加载相关技能",
            step3Title: "选择性阅读",
            step3Desc: "只读取必要的部分以优化上下文使用",
            categoriesTitle: "技能分类",
            categoriesPb: "+ 个技能按领域组织：",
            structureTitle: "技能结构",
            structureP: "每个技能包含：",
            nextTitle: "后续步骤",
            workflowsArrow: "工作流 →",
            workflowsArrowDesc: "了解斜杠命令流程",
            cliArrow: "CLI 参考 →",
            cliArrowDesc: "探索命令行工具",
            footerAgents: "Agents",
            footerWorkflows: "工作流",
        },
        workflowsPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "工作流",
            title: "工作流",
            subtitle: "用于常见开发任务的斜杠命令流程。",
            whatTitle: "工作流是什么？",
            whatP1: "工作流是为完成特定开发任务而定义的、清晰的分步流程。它们通过斜杠命令调用，提供一致、可重复的过程。",
            whatP2: "每个工作流都包含其领域的具体指令、决策点和最佳实践。",
            howTitle: "如何使用工作流",
            howP: "只需键入斜杠命令，后跟你的任务描述：",
            tipStrong: " 提示：",
            tipTextA: " 有些工作流带有 ",
            tipTextB: " 注解，允许在无需用户批准的情况下自动运行安全命令。",
            availableTitle: "可用的工作流",
            availablePa: "",
            availablePb: " 个工作流，涵盖常见的开发场景：",
            exampleUsage: "用法示例",
            customTitle: "创建自定义工作流",
            customPa: "你可以通过将 markdown 文件添加到 ",
            customPb: " 来创建自己的工作流：",
            customNoteA: "保存为 ",
            customNoteB: " 并使用 ",
            customNoteC: " 调用。",
            nextTitle: "后续步骤",
            cliArrow: "CLI 参考 →",
            cliArrowDesc: "了解命令行工具",
            backAgentsArrow: "返回 Agents →",
            backAgentsArrowDesc: "回顾专业 agent",
            footerSkills: "技能",
            footerCli: "CLI 参考",
        },
        installPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "安装",
            title: "安装",
            subtitle: "不到一分钟即可开始使用 AG Kit。",
            quickStartTitle: "快速开始",
            quickStartPa: "安装 AG Kit 最快的方法是使用 ",
            quickStartPb: " ，在项目根目录中执行：",
            calloutNoteStrong: "注意：",
            calloutNoteA: " 此命令会在你当前目录中创建一个 ",
            calloutNoteB: " 文件夹，包含所有模板。",
            globalTitle: "全局安装",
            globalPa: "全局安装 CLI，即可在任何地方使用 ",
            globalPb: " 命令：",
            globalReadOtherA: "在 ",
            globalReadOtherLink: "CLI 命令",
            globalReadOtherB: " 文档中阅读其他命令。",
            structureTitle: "安装内容",
            structureP: "运行安装命令后，你将获得以下结构：",
            agentDirDesc: "包含 20 个面向不同领域（前端、后端、安全等）的专业 AI agent 配置",
            skillsDirDesc: "48 个 agent 可使用的特定领域知识模块",
            workflowsDirDesc: "13 个用于常见开发任务的斜杠命令流程",
            rulesDirDescA: "工作区配置，包含 ",
            rulesDirDescB: " 用于行为规则",
            requirementsTitle: "系统要求",
            req1: "Node.js 18.0 或更高版本",
            req2: "npm 或 yarn 包管理器",
            req3: "Git（用于更新和版本控制）",
            nextTitle: "后续步骤",
            nextP: "现在你已经安装了 AG Kit，来了解核心概念：",
            agentsArrow: "Agents →",
            agentsArrowDesc: "了解专业 AI agent",
            skillsArrow: "技能 →",
            skillsArrowDesc: "探索 48 个特定领域技能",
            footerIntroduction: "简介",
            footerAgents: "Agents",
        },
        cliPage: {
            breadcrumbDocs: "文档",
            breadcrumbCurrent: "CLI 参考",
            title: "CLI 参考",
            subtitle: "用于管理 AG Kit 安装的命令行界面。",
            overviewTitle: "概述",
            overviewPa: "",
            overviewPb: " CLI 工具可帮助你跨项目管理 AG Kit 安装。",
            commandsTitle: "命令",
            initDescA: "通过安装 ",
            initDescB: " 文件夹在你的项目中初始化 AG Kit。",
            behaviorTitle: "行为",
            initBehavior1a: "在当前文件夹中创建 ",
            initBehavior1b: " 目录",
            initBehavior2: "从 GitHub 下载最新模板",
            initBehavior3a: "如果 ",
            initBehavior3b: " 已存在则跳过（使用 ",
            initBehavior3c: " 覆盖）",
            updateDesc: "将你现有的 AG Kit 安装更新到最新版本。",
            updateWarningStrong: "警告：",
            updateWarningA: " 此操作将删除并替换你的 ",
            updateWarningB: " 文件夹。请务必备份任何自定义更改。",
            statusDesc: "检查当前安装状态，并查询 npm 是否有更新的版本。",
            rollbackDesc: "恢复更新前的托管目录备份。默认使用最新备份；可用 --backup <id> 指定。",
            rollbackBehavior1: "列出可用备份并恢复所选备份",
            rollbackBehavior2: "先备份当前目录（可用 --no-keep-current 关闭）",
            rollbackBehavior3: "使用 --dry-run 预览将恢复哪个备份",
            outputIncludesTitle: "输出包括",
            statusOut1: "CLI 版本",
            statusOut2: "安装状态（已安装/未安装）",
            statusOut3: "安装路径和最后修改时间",
            statusOut4a: "位于 ",
            statusOut4b: " 根目录的项目数量",
            statusOut5: "如果有更新的版本，则显示更新通知",
            optionsTitle: "选项",
            optionsP: "使用这些选项自定义 CLI 行为：",
            tableOption: "选项",
            tableDescription: "描述",
            optForceA: "覆盖现有的 ",
            optForceB: " 文件夹（在 ",
            optForceC: " 时跳过确认提示）",
            optPathDesc: "安装到指定目录而非当前文件夹",
            optBranchDesc: "使用特定的 Git 分支（默认为仓库的默认分支）",
            optQuietDesc: "抑制输出（对 CI/CD 流水线有用）",
            optDryRunA: "预览操作而不实际执行（",
            optDryRunB: " / ",
            optDryRunC: "）",
            optStrategyDesc: "更新策略：merge 保留本地更改；replace 恢复上游目录",
            optNoBackupDesc: "跳过更新前的自动备份",
            optConflictReportDesc: "将更新/冲突报告写入自定义路径",
            examplesTitle: "示例",
            exForceReinstall: "强制重新安装",
            exInstallDir: "安装到指定目录",
            exDevBranch: "使用开发分支",
            exSilentCI: "为 CI/CD 静默安装",
            exPreviewUpdate: "预览更新而不应用",
            exReplace: "恢复上游原始目录",
            exRollbackLatest: "回滚到最新备份",
            nextTitle: "后续步骤",
            installGuideArrow: "安装指南 →",
            installGuideDesc: "完整的安装说明",
            viewGithubArrow: "在 GitHub 上查看 →",
            viewGithubDesc: "源代码与贡献指南",
            footerWorkflows: "工作流",
        },
    },
    ja: {
        nav: { github: "GitHub", sponsored: "スポンサー", donate: "寄付" },
        search: {
            placeholder: "ドキュメントを検索...",
            inputPlaceholder: "ドキュメント内を検索...",
            noResults: "結果が見つかりません",
            noResultsHint: "別のキーワードで検索してみてください",
            navigate: "移動",
            select: "選択",
            close: "閉じる",
            groupGettingStarted: "はじめに",
            groupCoreConcepts: "コアコンセプト",
            groupReference: "リファレンス",
            introduction: "概要",
            installation: "インストール",
            agents: "Agents",
            skills: "スキル",
            workflows: "ワークフロー",
            cliReference: "CLI リファレンス",
            commandsOptions: "コマンドとオプション",
        },
        footer: {
            product: "製品",
            resources: "リソース",
            community: "コミュニティ",
            legal: "法的事項",
            documentation: "ドキュメント",
            agents: "Agents",
            skills: "スキル",
            workflows: "ワークフロー",
            installation: "インストール",
            cliReference: "CLI リファレンス",
            examples: "サンプル",
            changelog: "変更履歴",
            github: "GitHub",
            issues: "Issue",
            discussions: "ディスカッション",
            contributing: "コントリビュート",
            license: "ライセンス",
            privacy: "プライバシーポリシー",
            terms: "利用規約",
            rights: "無断複製・転載を禁じます。",
        },
        toc: { onThisPage: "このページの内容", empty: "このページにセクションはありません。" },
        changelogPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "変更履歴",
            title: "変更履歴",
            subtitle: "AG Kit の主な変更点（新しい順）。",
            added: "追加",
            changed: "変更",
            fixed: "修正",
            removed: "削除",
            fullOnGithub: "GitHub で完全な変更履歴を見る",
        },
        home: {
            tagline: "モダンなコーディングアシスタント向けの、Skills、Agents、Workflows を備えた AI agent テンプレート。",
            github: "GitHub",
            documentation: "ドキュメント",
        },
        landing: landingJa,
        docsHome: {
            title: "ドキュメント",
            welcomePre: "",
            welcomePost: " のドキュメントへようこそ。",
            whatIsPre: "",
            whatIsPost: " とは？",
            whatIsP1: " は、モダンなコーディングアシスタントを強化するために設計された、Skills、Agents、Workflows を備えた AI agent テンプレートの総合コレクションです。",
            whatIsP2a: "個人開発者であれ大規模チームの一員であれ、AG Kit は ",
            whatIsP2b: "+ のスキル、",
            whatIsP2c: "+ の専門 agent、そして ",
            whatIsP2d: "+ の本番対応ワークフローで、より優れたソフトウェアをより速く構築する手助けをします。",
            includedTitle: "含まれるもの",
            specialistAgents: "専門 Agent",
            specialistAgentsDesc: "フロントエンド、バックエンド、セキュリティなどの領域の専門家",
            domainSkills: "ドメインスキル",
            domainSkillsDesc: "React、Next.js、テストなどの知識モジュール",
            workflowsLabel: "ワークフロー",
            workflowsDesc: "よくある開発タスク向けのスラッシュコマンド手順",
            howToTitle: "ドキュメントの使い方",
            howToP: "ドキュメントは 3 つの主要セクションに分かれています：",
            gettingStarted: "はじめに",
            gettingStartedDesc: "すぐに始められるクイックインストールとセットアップガイド",
            coreConcepts: "コアコンセプト",
            coreConceptsDesc: "Agents、Skills、Workflows について学ぶ",
            cliRef: "CLI リファレンス",
            cliRefDesc: "詳細なコマンドラインインターフェースのドキュメント",
            sidebarHintPre: "サイドバーで各セクションを移動するか、",
            sidebarHintPost: " ですばやく検索できます。",
            nextStepsTitle: "次のステップ",
            installationArrow: "インストール →",
            installationArrowDesc: "1 分足らずで AG Kit を始められます",
            learnCoreArrow: "コアコンセプトを学ぶ →",
            learnCoreArrowDesc: "Agents、Skills、Workflows の仕組みを理解する",
            footerGettingStarted: "はじめに",
            footerInstallation: "インストール",
        },
        agentsPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "Agents",
            title: "Agents",
            subtitle: "特定領域に深い専門性を持つ専門 AI ペルソナ。",
            whatTitle: "Agents とは？",
            whatP1: "Agents は、ドメイン固有の専門知識、ツール、行動パターンが設定された専門 AI ペルソナです。各 agent はソフトウェア開発の特定分野で力を発揮するよう設計されています。",
            whatP2a: "リクエストを送信すると、AG Kit の ",
            whatP2Strong: "インテリジェントルーティング",
            whatP2b: " システムが必要な agent を自動的に検出して有効化します。名前を指定して特定の視点を強制することもできます。",
            howTitle: "Agents の使い方",
            howP1Strong: "agent を明示的に指定する必要はありません！",
            howP1b: " システムがリクエストに基づいて適切な専門家を自動的に検出して適用します。",
            howP2a: "ただし、",
            howP2Strong: "この動作を上書きする",
            howP2b: " ことも可能です。agent 名を明示的に指定してください：",
            tipStrong: "ヒント：",
            tipTextA: " agent は連携できます！複雑なタスクで複数の専門家を調整するには ",
            tipTextB: " agent を使用します。",
            availableTitle: "利用可能な Agent",
            availablePa: "AG Kit には ",
            availablePb: " 個の専門 agent が含まれます：",
            structureTitle: "Agent の構造",
            structureP: "各 agent は YAML frontmatter を持つ markdown ファイルで定義されます：",
            structureNoteA: "この ",
            structureNoteB: " フィールドは、agent がアクセスできるドメイン知識モジュールを決定します。",
            nextTitle: "次のステップ",
            skillsArrow: "スキル →",
            skillsArrowDesc: "ドメイン固有の知識モジュールについて学ぶ",
            workflowsArrow: "ワークフロー →",
            workflowsArrowDesc: "スラッシュコマンド手順を探索する",
            footerInstallation: "インストール",
            footerSkills: "スキル",
        },
        skillsPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "スキル",
            title: "スキル",
            subtitle: "agent が自動的に読み込むドメイン固有の知識モジュール。",
            whatTitle: "スキルとは？",
            whatP1: "スキルは、特定領域の原則、パターン、意思決定フレームワークを含むモジュール化された知識パッケージです。agent が必要とするときに自動的に読み込まれます。",
            whatP2a: "ハードコードされたテンプレートとは異なり、スキルは ",
            whatP2Em: "原則",
            whatP2b: " を教えます —— これにより agent はパターンをコピーするのではなく、文脈に応じた判断を下せます。",
            noteStrong: " 注意：",
            noteText: " スキルはタスクの文脈に基づいてオンデマンドで読み込まれます。手動で何かを設定する必要はありません。",
            howTitle: "スキルの仕組み",
            howP: "agent を呼び出すと、以下に基づいて関連するスキルを自動的に読み込みます：",
            step1Title: "Agent 設定",
            step1Desc: "各 agent は frontmatter でアクセスできるスキルを指定します",
            step2Title: "タスクの文脈",
            step2Desc: "AI がスキルの説明を読み、関連するものを読み込みます",
            step3Title: "選択的読み込み",
            step3Desc: "コンテキスト使用を最適化するため、必要なセクションのみを読み込みます",
            categoriesTitle: "スキルカテゴリ",
            categoriesPb: "+ のスキルをドメイン別に整理：",
            structureTitle: "スキルの構造",
            structureP: "各スキルに含まれるもの：",
            nextTitle: "次のステップ",
            workflowsArrow: "ワークフロー →",
            workflowsArrowDesc: "スラッシュコマンド手順について学ぶ",
            cliArrow: "CLI リファレンス →",
            cliArrowDesc: "コマンドラインツールを探索する",
            footerAgents: "Agents",
            footerWorkflows: "ワークフロー",
        },
        workflowsPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "ワークフロー",
            title: "ワークフロー",
            subtitle: "よくある開発タスク向けのスラッシュコマンド手順。",
            whatTitle: "ワークフローとは？",
            whatP1: "ワークフローは、特定の開発タスクを達成するための明確に定義された段階的な手順です。スラッシュコマンドで呼び出され、一貫した再現可能なプロセスを提供します。",
            whatP2: "各ワークフローには、その領域に固有の指示、判断ポイント、ベストプラクティスが含まれます。",
            howTitle: "ワークフローの使い方",
            howP: "スラッシュコマンドに続けてタスクの説明を入力するだけです：",
            tipStrong: " ヒント：",
            tipTextA: " 一部のワークフローには ",
            tipTextB: " アノテーションがあり、ユーザーの承認なしに安全なコマンドを自動実行できます。",
            availableTitle: "利用可能なワークフロー",
            availablePa: "",
            availablePb: " 個のワークフローが、よくある開発シナリオをカバーします：",
            exampleUsage: "使用例",
            customTitle: "カスタムワークフローの作成",
            customPa: "markdown ファイルを ",
            customPb: " に追加することで、独自のワークフローを作成できます：",
            customNoteA: "",
            customNoteB: " として保存し、",
            customNoteC: " で呼び出します。",
            nextTitle: "次のステップ",
            cliArrow: "CLI リファレンス →",
            cliArrowDesc: "コマンドラインツールについて学ぶ",
            backAgentsArrow: "Agents に戻る →",
            backAgentsArrowDesc: "専門 agent を確認する",
            footerSkills: "スキル",
            footerCli: "CLI リファレンス",
        },
        installPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "インストール",
            title: "インストール",
            subtitle: "1 分足らずで AG Kit を始められます。",
            quickStartTitle: "クイックスタート",
            quickStartPa: "AG Kit を最も速くインストールする方法は、",
            quickStartPb: " をプロジェクトルートで使うことです：",
            calloutNoteStrong: "注意：",
            calloutNoteA: " このコマンドは現在のディレクトリに ",
            calloutNoteB: " フォルダーを作成し、すべてのテンプレートが含まれます。",
            globalTitle: "グローバルインストール",
            globalPa: "CLI をグローバルにインストールすると、どこでも ",
            globalPb: " コマンドを使えます：",
            globalReadOtherA: "他のコマンドは ",
            globalReadOtherLink: "CLI コマンド",
            globalReadOtherB: " のドキュメントで確認できます。",
            structureTitle: "インストールされる内容",
            structureP: "インストールコマンドを実行すると、次の構造になります：",
            agentDirDesc: "さまざまな領域（フロントエンド、バックエンド、セキュリティなど）向けの 20 個の専門 AI agent 設定を含みます",
            skillsDirDesc: "agent が使用できる 48 個のドメイン固有の知識モジュール",
            workflowsDirDesc: "よくある開発タスク向けの 13 個のスラッシュコマンド手順",
            rulesDirDescA: "行動ルール用の ",
            rulesDirDescB: " を含むワークスペース設定",
            requirementsTitle: "システム要件",
            req1: "Node.js 18.0 以降",
            req2: "npm または yarn パッケージマネージャー",
            req3: "Git（更新とバージョン管理用）",
            nextTitle: "次のステップ",
            nextP: "AG Kit をインストールしたので、コアコンセプトについて学びましょう：",
            agentsArrow: "Agents →",
            agentsArrowDesc: "専門 AI agent について学ぶ",
            skillsArrow: "スキル →",
            skillsArrowDesc: "48 個のドメイン固有スキルを発見する",
            footerIntroduction: "概要",
            footerAgents: "Agents",
        },
        cliPage: {
            breadcrumbDocs: "ドキュメント",
            breadcrumbCurrent: "CLI リファレンス",
            title: "CLI リファレンス",
            subtitle: "AG Kit のインストールを管理するためのコマンドラインインターフェース。",
            overviewTitle: "概要",
            overviewPa: "",
            overviewPb: " CLI ツールは、プロジェクト全体で AG Kit のインストールを管理するのに役立ちます。",
            commandsTitle: "コマンド",
            initDescA: "",
            initDescB: " フォルダーをインストールして、プロジェクトに AG Kit を初期化します。",
            behaviorTitle: "動作",
            initBehavior1a: "現在のフォルダーに ",
            initBehavior1b: " ディレクトリを作成します",
            initBehavior2: "GitHub から最新のテンプレートをダウンロードします",
            initBehavior3a: "",
            initBehavior3b: " が既に存在する場合はスキップします（上書きするには ",
            initBehavior3c: " を使用）",
            updateDesc: "既存の AG Kit インストールを最新バージョンに更新します。",
            updateWarningStrong: "警告：",
            updateWarningA: " この操作はあなたの ",
            updateWarningB: " フォルダーを削除して置き換えます。カスタム変更は必ずバックアップしてください。",
            statusDesc: "現在のインストール状況を確認し、npm で新しいリリースがあるか確認します。",
            rollbackDesc: "更新前の管理ツリーのバックアップを復元します。デフォルトは最新のバックアップ。--backup <id> で選択できます。",
            rollbackBehavior1: "利用可能なバックアップを一覧表示し、選択したものを復元します",
            rollbackBehavior2: "先に現在のツリーをバックアップします（--no-keep-current で無効化）",
            rollbackBehavior3: "--dry-run でどのバックアップが復元されるかプレビューできます",
            outputIncludesTitle: "出力に含まれるもの",
            statusOut1: "CLI バージョン",
            statusOut2: "インストール状況（インストール済み/未インストール）",
            statusOut3: "インストールパスと最終更新時刻",
            statusOut4a: "",
            statusOut4b: " ルートの項目数",
            statusOut5: "新しいバージョンが利用可能な場合の更新通知",
            optionsTitle: "オプション",
            optionsP: "これらのオプションで CLI の動作をカスタマイズします：",
            tableOption: "オプション",
            tableDescription: "説明",
            optForceA: "既存の ",
            optForceB: " フォルダーを上書きします（",
            optForceC: " では確認プロンプトをスキップ）",
            optPathDesc: "現在のフォルダーではなく指定したディレクトリにインストールします",
            optBranchDesc: "特定の Git ブランチを使用します（デフォルトはリポジトリのデフォルトブランチ）",
            optQuietDesc: "出力を抑制します（CI/CD パイプラインに便利）",
            optDryRunA: "実行せずに操作をプレビューします（",
            optDryRunB: " / ",
            optDryRunC: "）",
            optStrategyDesc: "更新戦略：merge はローカル変更を保持、replace はアップストリームのツリーを復元",
            optNoBackupDesc: "更新前の自動バックアップをスキップ",
            optConflictReportDesc: "更新／競合レポートをカスタムパスに書き出し",
            examplesTitle: "例",
            exForceReinstall: "強制的に再インストール",
            exInstallDir: "指定したディレクトリにインストール",
            exDevBranch: "開発ブランチを使用",
            exSilentCI: "CI/CD 向けのサイレントインストール",
            exPreviewUpdate: "適用せずに更新をプレビュー",
            exReplace: "アップストリームの元のツリーを復元",
            exRollbackLatest: "最新のバックアップへロールバック",
            nextTitle: "次のステップ",
            installGuideArrow: "インストールガイド →",
            installGuideDesc: "完全なインストール手順",
            viewGithubArrow: "GitHub で見る →",
            viewGithubDesc: "ソースコードとコントリビュートガイド",
            footerWorkflows: "ワークフロー",
        },
    },
};

export type Dictionary = Dict;
