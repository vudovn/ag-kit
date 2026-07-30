from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_kit = load_module("agkit_validate_kit", SCRIPTS / "validate_kit.py")
component_registry = sys.modules["component_registry"]
dependency_graph = sys.modules["dependency_graph"]
security_scan = load_module("agkit_security_scan", TOOLKIT / "skills/vulnerability-scanner/scripts/security_scan.py")
dependency_analyzer = load_module("agkit_dependency_analyzer", TOOLKIT / "skills/vulnerability-scanner/scripts/dependency_analyzer.py")
bundle_analyzer = load_module("agkit_bundle_analyzer", TOOLKIT / "skills/performance-profiling/scripts/bundle_analyzer.py")
validation_runner = load_module("agkit_validation_runner", SCRIPTS / "validation_runner.py")
geo_checker = load_module("agkit_geo_checker", TOOLKIT / "skills/geo-fundamentals/scripts/geo_checker.py")
react_performance = load_module(
    "agkit_react_performance",
    TOOLKIT / "skills/nextjs-react-expert/scripts/react_performance_checker.py",
)


class ToolkitRegressionTests(unittest.TestCase):
    def test_toolkit_self_validation_passes(self):
        findings = validate_kit.validate(TOOLKIT)
        errors = [item for item in findings if item.severity == "error"]
        self.assertEqual([], errors)

    def test_mcp_config_is_valid_json(self):
        data = json.loads((TOOLKIT / "mcp_config.json").read_text("utf-8"))
        self.assertIn("mcpServers", data)

    def test_security_scanner_ignores_patterns_inside_strings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.py").write_text("PATTERN = r'eval\\s*\\('
TOKEN = 'YOUR_API_KEY'
", "utf-8")
            report = security_scan.run_full_scan(str(root), "all")
            self.assertEqual(0, report["summary"]["critical"])
            self.assertEqual(0, report["summary"]["high"])

    def test_security_scanner_detects_executable_eval_and_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.py").write_text("api_key = 'sk_live_12345678901234567890'
eval(user_input)
", "utf-8")  # agkit: allow-secret
            report = security_scan.run_full_scan(str(root), "all")
            self.assertGreaterEqual(report["summary"]["critical"], 1)
            self.assertGreaterEqual(report["summary"]["high"], 1)
            self.assertTrue(security_scan._should_fail(report, "high"))

    def test_security_scanner_detects_nested_nextjs_header_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"private":true}', "utf-8")
            web = root / "web"
            web.mkdir()
            (web / "next.config.ts").write_text(
                'const headers = [{ key: "Content-Security-Policy", value: "frame-ancestors \'none\'" }];',
                "utf-8",
            )
            report = security_scan.run_full_scan(str(root), "config")
            config = report["scans"]["configuration"]
            self.assertTrue(config["checks"]["security_headers_config"])
            self.assertFalse(any("security-header" in item.get("issue", "") for item in config["findings"]))

    def test_dependency_analyzer_flags_missing_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"dependencies":{"demo":"latest"}}', "utf-8")
            report = dependency_analyzer.analyze(root)
            issues = {item["issue"] for item in report["findings"]}
            self.assertIn("Missing JavaScript lock file", issues)
            self.assertIn("Unbounded dependency version", issues)

    def test_bundle_analyzer_flags_oversized_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "dist" / "app.js"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"x" * 2048)
            report = bundle_analyzer.analyze(root, file_warn_kib=1, file_fail_kib=2, total_fail_kib=100)
            self.assertTrue(report["findings"])
            self.assertEqual("high", report["findings"][0]["severity"])

    def test_geo_checker_follows_localized_mdx_and_skips_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            route = root / "web" / "src" / "app" / "docs" / "demo"
            route.mkdir(parents=True)
            (route / "page.tsx").write_text(
                'import En from "./content.en.mdx";\n'
                'import Vi from "./content.vi.mdx";\n'
                'export default function Page(){ return <En />; }\n',
                "utf-8",
            )
            (route / "content.en.mdx").write_text(
                "# Demo\n\n## Overview\nText.\n\n## Usage\nText.\n",
                "utf-8",
            )
            (route / "content.vi.mdx").write_text(
                "# Trình diễn\n\n## Tổng quan\nNội dung.\n\n## Sử dụng\nNội dung.\n",
                "utf-8",
            )
            (route.parent / "layout.tsx").write_text(
                "export default function Layout({children}){return <div>{children}</div>}\n",
                "utf-8",
            )

            pages = geo_checker.find_web_pages(root)
            self.assertEqual([route / "page.tsx"], pages)
            result = geo_checker.check_page(route / "page.tsx", root)
            self.assertGreaterEqual(result["score"], 60)
            self.assertFalse(any("Multiple H1" in issue for issue in result["issues"]))

    def test_react_checker_ignores_generated_next_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            web = root / "web"
            source = web / "src" / "app"
            generated = web / ".next" / "types"
            source.mkdir(parents=True)
            generated.mkdir(parents=True)
            (web / "package.json").write_text(
                '{"dependencies":{"next":"16.2.10","react":"19.2.3"}}',
                "utf-8",
            )
            (source / "page.tsx").write_text(
                "export default function Page(){return <main><h1>Safe</h1></main>}\n",
                "utf-8",
            )
            (generated / "page.ts").write_text(
                "async function generated(){await one();\nawait two();}\n",
                "utf-8",
            )

            checker = react_performance.PerformanceChecker(str(root))
            # Resolve paths: macOS temp dirs use /var -> /private/var symlinks.
            scanned = {path.resolve() for path in checker._iter_files(["ts", "tsx"])}
            self.assertIn((source / "page.tsx").resolve(), scanned)
            self.assertNotIn((generated / "page.ts").resolve(), scanned)
            self.assertTrue(checker.run())
            self.assertEqual([], checker.issues)

    def test_runner_finds_embedded_toolkit_for_external_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            located = validation_runner.locate_toolkit_root(project, str(SCRIPTS / "checklist.py"))
            self.assertEqual(TOOLKIT, located)

    def test_all_components_use_strict_semver(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        for group in ("agents", "skills", "workflows", "rules"):
            with self.subTest(group=group):
                invalid = {
                    name: data["version"]
                    for name, data in manifest[group].items()
                    if not component_registry.is_semver(data["version"])
                }
                self.assertEqual({}, invalid)

    def test_component_registry_and_lock_are_synchronized(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        lock = component_registry.build_lock(TOOLKIT, manifest)
        self.assertEqual(manifest, json.loads((TOOLKIT / "manifest.json").read_text("utf-8")))
        self.assertEqual(lock, json.loads((TOOLKIT / "manifest.lock.json").read_text("utf-8")))

    def test_dependency_graph_is_synchronized(self):
        expected = dependency_graph.render(TOOLKIT)
        self.assertEqual(expected, (TOOLKIT / "DEPENDENCY_GRAPH.md").read_text("utf-8"))

    def test_workflow_dependencies_resolve(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        agents = set(manifest["agents"])
        skills = set(manifest["skills"])
        for name, workflow in manifest["workflows"].items():
            with self.subTest(workflow=name):
                self.assertLessEqual(set(workflow["requires"]["agents"]), agents)
                self.assertLessEqual(set(workflow["requires"]["skills"]), skills)
                self.assertTrue(workflow["artifactOutputs"])

    def test_orchestration_guidance_is_antigravity_first_and_bounded(self):
        orchestrator = (TOOLKIT / "agent/orchestrator.md").read_text("utf-8")
        parallel = (TOOLKIT / "skills/parallel-agents/SKILL.md").read_text("utf-8")
        combined = orchestrator + "\n" + parallel

        self.assertNotIn("Claude Code's native Agent Tool", combined)
        self.assertNotIn("Claude orchestrates autonomously", combined)
        self.assertNotIn("**Explore** | Haiku", combined)
        self.assertNotIn("**Plan** | Sonnet", combined)
        self.assertIn("Google Antigravity is the primary production runtime", combined)
        self.assertIn("max_delegation_depth", combined)
        self.assertIn("Never allow an open-ended ReAct", combined)
        self.assertIn("isolated worktree", combined)
        self.assertIn("untrusted data", combined)

    def test_caret_semver_resolution(self):
        self.assertTrue(component_registry.version_satisfies("1.4.2", "^1.2.0"))
        self.assertFalse(component_registry.version_satisfies("2.0.0", "^1.2.0"))
        self.assertTrue(component_registry.version_satisfies("0.3.5", "^0.3.1"))
        self.assertFalse(component_registry.version_satisfies("0.4.0", "^0.3.1"))

    def test_memory_topics_are_present(self):
        topics = {
            "project-conventions.md",
            "user-preferences.md",
            "tech-decisions.md",
            "feedback-history.md",
        }
        self.assertLessEqual(topics, {path.name for path in (TOOLKIT / "memory").glob("*.md")})
        self.assertLessEqual(len((TOOLKIT / "memory/MEMORY.md").read_text("utf-8").splitlines()), 200)


if __name__ == "__main__":
    unittest.main()
