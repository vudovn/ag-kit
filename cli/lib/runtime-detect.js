import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { RUNTIME_TARGETS } from "./runtime-registry.js";

const definitions = {
  antigravity: { bins: ["antigravity", "agy"], markers: [".agents"] },
  claude: { bins: ["claude"], markers: [".claude"] },
  codex: { bins: ["codex"], markers: [".codex", ".codex-plugin"] },
  gemini: { bins: ["gemini"], markers: [".gemini"] },
  qwen: { bins: ["qwen"], markers: [".qwen"] },
  kimi: { bins: ["kimi"], markers: [".kimi", ".kimi-code"] },
  cline: { bins: [], markers: [".cline"] },
  cursor: { bins: ["cursor"], markers: [".cursor"] },
  windsurf: { bins: ["windsurf"], markers: [".windsurf", ".windsurfrules"] },
  copilot: { bins: ["copilot"], markers: [".github/copilot-instructions.md", ".vscode/mcp.json"] },
  opencode: { bins: ["opencode"], markers: ["opencode.json", ".opencode"] },
  openclaw: { bins: ["openclaw"], markers: [".openclaw"] },
  aider: { bins: ["aider"], markers: [".aider.conf.yml", "CONVENTIONS.md"] },
  wayland: { bins: ["wayland"], markers: [".wayland"] },
  hermes: { bins: ["hermes"], markers: [".hermes"] },
  pi: { bins: ["pi"], markers: [".pi"] },
};

const executableExtensions = () => process.platform === "win32"
  ? (process.env.PATHEXT || ".EXE;.CMD;.BAT;.COM").split(";").filter(Boolean)
  : [""];

const isExecutable = (file) => {
  try {
    fs.accessSync(file, process.platform === "win32" ? fs.constants.F_OK : fs.constants.X_OK);
    return fs.statSync(file).isFile();
  } catch { return false; }
};

export function findBinary(name, envPath = process.env.PATH || "") {
  const extensions = executableExtensions();
  for (const dir of envPath.split(path.delimiter).filter(Boolean)) {
    for (const ext of extensions) {
      const candidate = path.join(dir, process.platform === "win32" ? `${name}${ext}` : name);
      if (isExecutable(candidate)) return candidate;
    }
  }
  return null;
}

const homeMarkers = {
  claude: [".claude"], codex: [".codex"], gemini: [".gemini"], qwen: [".qwen"], kimi: [".kimi", ".kimi-code"],
  cursor: [".cursor"], windsurf: [".codeium/windsurf"], opencode: [".config/opencode"], openclaw: [".openclaw"],
  aider: [".aider.conf.yml"], wayland: [".wayland"], hermes: [".hermes"], pi: [".pi"],
};

export function detectRuntimes({ root = process.cwd(), includeHome = true } = {}) {
  const project = path.resolve(root);
  const home = os.homedir();
  return RUNTIME_TARGETS.map((runtime) => {
    const def = definitions[runtime] || { bins: [], markers: [] };
    const binaries = def.bins.flatMap((bin) => {
      const found = findBinary(bin);
      return found ? [{ bin, path: found }] : [];
    });
    const projectMarkers = def.markers.filter((marker) => fs.existsSync(path.join(project, marker)));
    const userMarkers = includeHome ? (homeMarkers[runtime] || []).filter((marker) => fs.existsSync(path.join(home, marker))) : [];
    const lifecycle = fs.existsSync(path.join(project, ".ag-kit", "runtime-installs", `${runtime}.json`));
    const detected = lifecycle || binaries.length > 0 || projectMarkers.length > 0 || userMarkers.length > 0;
    const evidence = [
      ...binaries.map((item) => `bin:${item.bin}`),
      ...projectMarkers.map((item) => `project:${item}`),
      ...userMarkers.map((item) => `home:${item}`),
      ...(lifecycle ? ["ag-kit:lifecycle"] : []),
    ];
    return { runtime, detected, lifecycle, binaries, projectMarkers, userMarkers, evidence };
  });
}

export function detectedRuntimeNames(options = {}) {
  return detectRuntimes(options).filter((item) => item.detected).map((item) => item.runtime);
}
