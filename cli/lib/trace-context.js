import path from "node:path";
import { readJson, stateRoot } from "./project-state.js";

const TRACE_ENV = "AG_KIT_TRACE_ID";
const TRACE_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;

export const isValidTraceId = (value) => typeof value === "string" && TRACE_PATTERN.test(value);

export function currentTraceId(root = process.cwd()) {
    const explicit = process.env[TRACE_ENV];
    if (isValidTraceId(explicit)) return explicit;
    const session = readJson(path.join(stateRoot(root), "flow", "session.json"), null);
    if (session?.status !== "active") return null;
    const candidate = session.traceId || session.id;
    return isValidTraceId(candidate) ? candidate : null;
}

export function traceFields(root = process.cwd()) {
    const traceId = currentTraceId(root);
    return traceId ? { traceId } : {};
}

export function traceEnv(root = process.cwd(), extra = {}) {
    const traceId = currentTraceId(root);
    return { ...process.env, ...(traceId ? { [TRACE_ENV]: traceId } : {}), ...extra };
}
