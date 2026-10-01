import fs from "node:fs";
import os from "node:os";
import path from "node:path";

export const resolveSafeProjectRoot = (root = process.cwd()) => {
    const resolved = path.resolve(root);
    if (resolved === path.parse(resolved).root) throw new Error("filesystem root cannot be used as an AG Kit project");
    if (resolved === path.resolve(os.homedir())) throw new Error("user home cannot be used as an AG Kit project");
    return resolved;
};
export const stateRoot = (root = process.cwd()) => path.join(resolveSafeProjectRoot(root), ".ag-kit");
export const ensureDir = (dir) => fs.mkdirSync(dir, { recursive: true });
export const readJson = (file, fallback = null) => {
    try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return fallback; }
};
export const writeJson = (file, value) => {
    ensureDir(path.dirname(file));
    fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
    return value;
};
export const appendJsonl = (file, value) => {
    ensureDir(path.dirname(file));
    fs.appendFileSync(file, `${JSON.stringify(value)}\n`);
    return value;
};
export const readJsonl = (file) => {
    if (!fs.existsSync(file)) return [];
    return fs.readFileSync(file, "utf8").split(/\r?\n/).filter(Boolean).flatMap((line) => {
        try { return [JSON.parse(line)]; } catch { return []; }
    });
};
export const writeJsonl = (file, rows) => {
    ensureDir(path.dirname(file));
    fs.writeFileSync(file, rows.length ? `${rows.map((row) => JSON.stringify(row)).join("\n")}\n` : "");
};
export const slugify = (value) => String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 64) || "item";
