---
name: mcp-builder
description: MCP (Model Context Protocol) server and client engineering. Protocol design, schemas, transports, extensions, security, and migration.
when_to_use: "When building or reviewing MCP servers or clients, designing MCP tools/resources/prompts, migrating protocol versions, or validating MCP security and interoperability."
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# MCP Builder

> Build interoperable MCP implementations against the stable **2026-07-28** specification. Treat extensions as negotiated, opt-in capabilities rather than core protocol guarantees.

---

## 1. Stable baseline and compatibility

- The authoritative stable baseline is MCP **2026-07-28**.
- Core requests are stateless and self-contained. Do not infer protocol version, client capabilities, identity, conversation, or task state from a transport connection or process lifetime.
- Put cross-request state behind explicit identifiers supplied on every relevant request.
- Negotiate the protocol version and capabilities; do not assume that a client or server implements every optional feature.
- Preserve compatibility with earlier peers where the specification requires it, including accepting legacy resource-not-found error code `-32002` while emitting `-32602` for invalid parameters in the current protocol.

### Core versus extensions

| Layer | Status | Engineering rule |
| --- | --- | --- |
| Base protocol, versioning, message patterns | Stable core | Required for every implementation |
| Resources, prompts, tools, elicitation | Optional core features | Advertise and check capabilities before use |
| Tasks, Skills over MCP, MCP Apps | Extensions | Opt-in; require explicit support from both peers |
| Draft or vendor extensions | Experimental/vendor-specific | Isolate behind adapters and feature flags |

Never label an extension as stable merely because one SDK or host supports it. Check the extension's own official status and version.

---

## 2. Architecture

MCP uses JSON-RPC 2.0 between hosts, clients, and servers.

```text
host application
  └─ MCP client / runtime adapter
       ├─ stdio transport
       └─ Streamable HTTP transport
            └─ MCP server
                 ├─ resources
                 ├─ prompts
                 └─ tools
```

### Stateless request model

Every request must carry the protocol metadata required by the negotiated version. For 2026-07-28 this includes per-request protocol version and client capability metadata under reserved `_meta` keys.

Servers must implement `server/discover` for protocol-version and capability discovery. Clients may call it before normal requests or use it as a backward-compatibility probe for stdio peers.

Do not:

- use a stdio process as a conversation or session boundary;
- depend on request ordering to establish capabilities or identity;
- keep hidden mutable state without an explicit handle;
- use self-reported client/server information for authorization decisions.

Do:

- make task, thread, workspace, or subscription handles explicit;
- validate every request independently;
- tolerate interleaved requests from unrelated tasks;
- document lifecycle, expiry, and cleanup for durable handles.

---

## 3. Transports and authentication

| Transport | Typical use | Security baseline |
| --- | --- | --- |
| `stdio` | Local process integration | Read credentials from the environment; constrain process and filesystem access |
| Streamable HTTP | Remote or shared service | Use the MCP HTTP authorization framework, validate origins where applicable, and enforce network boundaries |

WebSocket is not a standard MCP transport unless defined by a separately negotiated extension or vendor adapter.

Transport concerns must not leak into protocol semantics. Reconnection or process replacement must not destroy logical state that is represented by an explicit durable handle.

---

## 4. Schema design and validation

MCP defaults to **JSON Schema 2020-12** when `$schema` is absent. Implementations must support that dialect and should document any additional dialects.

### Tool input schemas

- Use an object root for tool arguments.
- Give every property a clear, action-oriented description.
- Declare required fields explicitly.
- Prefer narrow enums, bounds, formats, and `additionalProperties: false` where forward compatibility does not require open objects.
- Validate both the schema and each invocation payload.

### Tool output schemas

Use structured content and `outputSchema` when consumers need typed, predictable results. Keep human-readable text concise and ensure structured output remains the source of truth for automation.

### `$ref` and validator safety

- Never dereference network `$ref` values automatically.
- If remote dereferencing is explicitly enabled, use a host allowlist; reject loopback, link-local, and private addresses; apply timeouts and response-size limits; and log resolved URIs without secrets.
- Reject schemas with unresolved external references instead of treating them as permissive.
- Bound schema depth, total subschemas, and validation time to prevent denial-of-service through composition keywords or recursive references.

---

## 5. Tool, resource, and prompt design

### Tools

- Use clear action names and a single responsibility.
- Mark read-only, destructive, idempotent, or open-world behavior with annotations when useful, but treat annotations as untrusted hints unless the server itself is trusted.
- Require explicit user approval for consequential actions.
- Return stable machine-readable errors without internal stack traces or secrets.

### Resources

- Use stable URIs and MIME types.
- Separate discovery metadata from resource content.
- Apply authorization per resource, not only per server connection.
- Avoid silently forwarding resource data to another server or model without user consent.

### Prompts

- Treat prompts as user-visible templates, not hidden authority.
- Keep tool permissions and policy enforcement outside prompt text.
- Validate prompt arguments and clearly identify any data sources included in generated messages.

---

## 6. Security requirements

1. **Consent and least privilege** — expose only required data and obtain explicit approval before tool execution or data sharing.
2. **Untrusted metadata** — do not use tool descriptions, annotations, client info, server info, or model-produced arguments as authorization evidence.
3. **Input and output validation** — validate schemas, arguments, structured results, URIs, and content types at trust boundaries.
4. **Secret handling** — load credentials from environment or a secret manager; never place real keys in repository configuration, logs, traces, prompts, or error payloads.
5. **Network controls** — defend remote schema/resource fetching against SSRF, redirect abuse, oversized responses, and slow responses.
6. **Execution isolation** — sandbox subprocesses and filesystem access; use explicit path grants and reject archive or symlink escapes.
7. **Auditability** — record security-relevant decisions, approvals, tool identity, and result status without storing sensitive payloads unnecessarily.

---

## 7. Extensions

Extensions are negotiated independently from the core protocol.

| Extension | Use | Guardrail |
| --- | --- | --- |
| Tasks | Long-running work, polling, durable handles, mid-flight input | Do not use the older experimental task API; negotiate the extension |
| Skills over MCP | Discoverable structured agent instructions | Treat skill content as untrusted input and apply host policy |
| MCP Apps | Interactive UI rendered in conversations | Constrain origins, content, data access, and action permissions |

An adapter must fail gracefully when an extension is absent. Never silently downgrade a security requirement to preserve feature parity.

---

## 8. Deprecated features and migration

The 2026-07-28 specification deprecates legacy roots, sampling, and logging shapes while keeping a compatibility window. Do not remove compatibility abruptly, but avoid designing new architecture around deprecated forms.

### Migration checklist from 2025-era implementations

- [ ] Replace connection-scoped sessions and the `initialize` handshake with stateless per-request metadata.
- [ ] Implement or consume `server/discover` for version and capability selection.
- [ ] Move durable state behind explicit task, thread, workspace, or application handles.
- [ ] Send and validate negotiated protocol version and client capabilities on every request.
- [ ] Upgrade schema validation to JSON Schema 2020-12 by default.
- [ ] Disable network `$ref` resolution by default and add validation resource limits.
- [ ] Move experimental Tasks usage to the negotiated Tasks extension.
- [ ] Accept legacy `-32002` resource-not-found responses, but emit current error semantics.
- [ ] Treat a missing `resultType` from older servers as `"complete"`; require it for current-version results.
- [ ] Audit roots, sampling, and logging integrations for their documented replacements and deprecation timeline.
- [ ] Add interoperability tests against at least one older peer and one 2026-07-28 peer.

---

## 9. Testing matrix

| Test | Expected evidence |
| --- | --- |
| Contract | Invalid JSON-RPC, missing metadata, unsupported version/capability, schema dialect handling |
| Statelessness | Interleaved requests, reconnects, process reuse, explicit-handle recovery |
| Schema security | External `$ref`, recursive/composed schemas, depth/count/time limits |
| Authorization | Denied resource/tool access, approval gates, credential isolation |
| Extension negotiation | Extension absent, version mismatch, feature enabled, graceful fallback |
| Compatibility | Current peer plus supported older protocol revision |
| Failure handling | Timeouts, cancellation, partial results, structured errors, no secret leakage |

---

## 10. Review checklist

- [ ] Stable protocol version and extension status are documented.
- [ ] Requests are stateless; cross-request state uses explicit handles.
- [ ] Capabilities are negotiated and checked before optional operations.
- [ ] JSON Schema 2020-12 is supported and validator resource use is bounded.
- [ ] Network `$ref` resolution is disabled by default.
- [ ] Tool annotations are not trusted as authorization.
- [ ] User approval, least privilege, secret handling, and execution isolation are enforced outside prompts.
- [ ] Deprecated features have a compatibility and migration plan.
- [ ] Contract, security, extension, and cross-version tests pass.
