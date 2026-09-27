const tokens = (value) => new Set(String(value || "").toLowerCase().match(/[a-z0-9_]{3,}/g) || []);

const similarity = (a, b) => {
    const left = tokens(`${a.title || ""} ${a.evidence || ""}`);
    const right = tokens(`${b.title || ""} ${b.evidence || ""}`);
    if (!left.size || !right.size) return 0;
    let shared = 0;
    for (const token of left) if (right.has(token)) shared += 1;
    return shared / (left.size + right.size - shared);
};

const severityRank = { optional: 1, important: 2, blocking: 3 };

export function dedupeFindings(findings, threshold = 0.78) {
    const merged = [];
    for (const finding of findings || []) {
        const normalized = {
            severity: ["blocking", "important", "optional"].includes(String(finding.severity).toLowerCase()) ? String(finding.severity).toLowerCase() : "important",
            title: String(finding.title || "Finding").trim(),
            evidence: String(finding.evidence || "").trim(),
        };
        let existing = merged.find((item) => similarity(item, normalized) >= threshold);
        if (!existing) {
            merged.push({ ...normalized, occurrences: 1 });
            continue;
        }
        existing.occurrences += 1;
        if ((severityRank[normalized.severity] || 0) > (severityRank[existing.severity] || 0)) existing.severity = normalized.severity;
        if (normalized.evidence.length > existing.evidence.length) existing.evidence = normalized.evidence;
    }
    return merged;
}

const chooseBoundary = (text, start, hardEnd) => {
    const window = text.slice(start, hardEnd);
    const floor = Math.floor(window.length * 0.65);
    for (const marker of ["\n\n", "\n", ". ", "; "]) {
        const index = window.lastIndexOf(marker);
        if (index >= floor) return start + index + marker.length;
    }
    return hardEnd;
};

export function chunkText(text, { maxChars = 32000, overlapChars = 2400 } = {}) {
    const source = String(text || "");
    const cap = Math.max(4000, Number(maxChars) || 32000);
    const overlap = Math.max(0, Math.min(Number(overlapChars) || 0, Math.floor(cap / 3)));
    if (source.length <= cap) return [{ index: 0, start: 0, end: source.length, text: source }];

    const chunks = [];
    let start = 0;
    while (start < source.length) {
        const hardEnd = Math.min(source.length, start + cap);
        const end = hardEnd === source.length ? hardEnd : chooseBoundary(source, start, hardEnd);
        chunks.push({ index: chunks.length, start, end, text: source.slice(start, end) });
        if (end >= source.length) break;
        start = Math.max(start + 1, end - overlap);
    }
    return chunks;
}
