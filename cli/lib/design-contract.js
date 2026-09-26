import fs from "node:fs";
import path from "node:path";

const templateRows = [
    ["graphite", "#0b0d10", "#f4f7fb", "#6ee7b7", "Inter / system-ui", "10px"],
    ["ivory", "#faf8f2", "#181713", "#8b5e34", "Source Serif 4 / Georgia", "6px"],
    ["ocean", "#071c2c", "#eef9ff", "#38bdf8", "Inter / system-ui", "12px"],
    ["forest", "#0d1f16", "#f1faF4", "#86efac", "Manrope / system-ui", "8px"],
    ["ember", "#22110d", "#fff7ed", "#fb923c", "Inter / system-ui", "8px"],
    ["violet", "#161127", "#faf5ff", "#c084fc", "Manrope / system-ui", "12px"],
    ["rose", "#241015", "#fff1f2", "#fb7185", "Inter / system-ui", "14px"],
    ["sand", "#f4ead7", "#2a2118", "#b7791f", "Source Sans 3 / system-ui", "4px"],
    ["terminal", "#050805", "#d1fae5", "#22c55e", "ui-monospace / SFMono-Regular", "2px"],
    ["editorial", "#fdfcf9", "#161616", "#dc2626", "Newsreader / Georgia", "0px"],
    ["neon", "#070711", "#f5f3ff", "#a3e635", "Space Grotesk / system-ui", "16px"],
    ["monochrome", "#ffffff", "#111111", "#111111", "Inter / system-ui", "0px"],
];
export const DESIGN_TEMPLATES = Object.fromEntries(templateRows.map(([name, background, foreground, accent, type, radius]) => [name, { name, background, foreground, accent, type, radius }]));
export const listDesignTemplates = () => Object.keys(DESIGN_TEMPLATES);
const fileFor = (root) => path.join(path.resolve(root), "DESIGN.md");

export function renderDesignContract({ template = "graphite", brand = "Project" } = {}) {
    const tokens = template === "blank" ? { name: "blank", background: "TBD", foreground: "TBD", accent: "TBD", type: "TBD", radius: "TBD" } : DESIGN_TEMPLATES[template];
    if (!tokens) throw new Error(`unknown design template: ${template}`);
    return `# DESIGN.md — ${brand}\n\nStatus: LOCKED until explicitly revised.\nTemplate: ${tokens.name}\n\n## 1. Brand intent\nDefine the product promise, audience, tone, and the one feeling the interface should create. Prefer concrete nouns and verbs over vague adjectives.\n\n## 2. Color system\n- Background: ${tokens.background}\n- Foreground: ${tokens.foreground}\n- Accent: ${tokens.accent}\n- Error/success/warning colors must meet contrast requirements and be semantic rather than decorative.\n\n## 3. Typography\n- Primary stack: ${tokens.type}\n- Use a deliberate type scale with no more than two font families.\n- Body copy must remain readable at narrow widths and browser zoom.\n\n## 4. Layout and spacing\nUse a consistent spacing scale, stable content widths, and explicit responsive breakpoints. Avoid arbitrary one-off spacing values when an existing token fits.\n\n## 5. Components\n- Default corner radius: ${tokens.radius}\n- Interactive states must include hover, focus-visible, disabled, loading, error, and success where relevant.\n- Reuse existing primitives before inventing a new component.\n\n## 6. Imagery and iconography\nUse one coherent visual language. Avoid stock-looking filler, fake engineering diagrams, and decorative imagery that competes with the task.\n\n## 7. Motion\nMotion explains state change; it never exists only to make the page feel busy. Respect reduced-motion preferences.\n\n## 8. Accessibility\nTarget WCAG 2.2 AA for contrast and interaction. Preserve semantic structure, keyboard access, visible focus, labels, and sensible reading order.\n\n## 9. Do / Don't\n**Do:** follow these tokens, reuse patterns, and verify responsive/accessibility behavior.\n\n**Don't:** invent new colors/type scales per screen, mix unrelated visual styles, or override this contract silently.\n`;
}

export function initDesignContract({ root = process.cwd(), template = "graphite", brand = "Project", force = false } = {}) {
    const file = fileFor(root);
    if (fs.existsSync(file) && !force) throw new Error("DESIGN.md already exists; use --force to replace it");
    fs.writeFileSync(file, renderDesignContract({ template, brand }));
    return { file: path.relative(root, file) || "DESIGN.md", template, brand };
}

export function checkDesignContract(root = process.cwd()) {
    const file = fileFor(root);
    if (!fs.existsSync(file)) return { exists: false, valid: false, missing: ["DESIGN.md"] };
    const text = fs.readFileSync(file, "utf8");
    const required = ["Brand intent", "Color system", "Typography", "Layout and spacing", "Components", "Imagery and iconography", "Motion", "Accessibility", "Do / Don't"];
    const missing = required.filter((heading) => !text.includes(heading));
    return { exists: true, valid: missing.length === 0, missing, file: "DESIGN.md" };
}
