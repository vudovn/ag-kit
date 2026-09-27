import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { compactMarkdown, compressArtifact, createHandoff, readHandoff } from "../lib/context-artifacts.js";

test("markdown compaction preserves fenced code while reducing prose whitespace", () => {
  const input = "# Title\n\nThis is   a line\nthat continues.\n\n\n```js\nconst x =  1;\n```\n";
  const output = compactMarkdown(input);
  assert.match(output, /This is a line that continues\./);
  assert.match(output, /```js\nconst x =  1;\n```/);
  assert.ok(Buffer.byteLength(output) < Buffer.byteLength(input));
});

test("compression defaults to a new file and measures real byte reduction", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-compress-"));
  try {
    fs.writeFileSync(path.join(root, "notes.md"), "# Notes\n\nAlpha    beta\ncontinues here.\n\n\n");
    const result = compressArtifact({ root, file: "notes.md" });
    assert.equal(result.source, "notes.md");
    assert.equal(result.destination, "notes.md.compressed.md");
    assert.ok(result.bytesSaved > 0);
    assert.ok(fs.existsSync(path.join(root, result.destination)));
    assert.match(fs.readFileSync(path.join(root, "notes.md"), "utf8"), /Alpha    beta/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("compression refuses a symlink-parent escape", { skip: process.platform === "win32" }, () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-contained-"));
  const outside = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-outside-"));
  try {
    fs.writeFileSync(path.join(root, "notes.md"), "alpha  beta\n");
    fs.symlinkSync(outside, path.join(root, "escape"), "dir");
    assert.throws(() => compressArtifact({ root, file: "notes.md", output: "escape/out.md" }), /inside the project root/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
    fs.rmSync(outside, { recursive: true, force: true });
  }
});

test("handoff creates a compact continuity artifact and archives the previous handoff", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "ag-kit-handoff-"));
  try {
    createHandoff({ root, goal: "Ship v2", state: "Core is green", decisions: ["Keep Markdown canonical"], evidence: ["npm test passed"], risks: ["Web audit pending"], next: "Run CI" });
    const first = readHandoff(root);
    assert.equal(first.exists, true);
    assert.match(first.content, /Ship v2/);
    assert.match(first.content, /Keep Markdown canonical/);
    createHandoff({ root, state: "CI rerun" });
    const archiveDir = path.join(root, ".ag-kit", "handoffs");
    assert.equal(fs.existsSync(archiveDir), true);
    assert.ok(fs.readdirSync(archiveDir).some((name) => name.endsWith(".md")));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
