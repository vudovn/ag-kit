---
name: automate-whatsapp
description: "Build WhatsApp automations with Kapso workflows: configure WhatsApp triggers, edit workflow graphs, manage executions, deploy functions, and use databases/integrations for state. Use when automatin..."
risk: safe
source: "https://github.com/gokapso/agent-skills/tree/master/skills/automate-whatsapp"
date_added: "2026-02-27"
---

# Automate WhatsApp

## When to use

Use this skill to build and run WhatsApp automations: workflow CRUD, graph edits, triggers, executions, function management, app integrations, and D1 database operations.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`

## How to

### Edit a workflow graph

1. Fetch graph: `node scripts/get-graph.js <workflow_id>` (note the `lock_version`)
2. Edit the JSON (see graph rules below)
3. Validate: `node scripts/validate-graph.js --definition-file <path>`
4. Update: `node scripts/update-graph.js <workflow_id> --expected-lock-version <n> --definition-file <path>`
5. Re-fetch to confirm

For small edits, use `edit-graph.js` with `--old-file` and `--new-file` instead.

If you get a lock_version conflict: re-fetch, re-apply changes, retry with new lock_version.

### Manage triggers

1. List: `node scripts/list-triggers.js <workflow_id>`
2. Create: `node scripts/create-trigger.js <workflow_id> --trigger-type <type> --phone-number-id <id>`
3. Toggle: `node scripts/update-trigger.js --trigger-id <id> --active true|false`
4. Delete: `node scripts/delete-trigger.js --trigger-id <id>`

For inbound_message triggers, first run `node scripts/list-whatsapp-phone-numbers.js` to get `phone_number_id`.

### Debug executions

1. List: `node scripts/list-executions.js <workflow_id>`
2. Inspect: `node scripts/get-execution.js <execution-id>`
3. Get value: `node scripts/get-context-value.js <execution-id> --variable-path vars.foo`
4. Events: `node scripts/list-execution-events.js <execution-id>`

### Create and deploy a function

1. Write code with handler signature (see function rules below)
2. Create: `node scripts/create-function.js --name <name> --code-file <path>`
3. Deploy: `node scripts/deploy-function.js --function-id <id>`
4. Verify: `node scripts/get-function.js --function-id <id>`

### Set up agent node with app integrations

1. Find model: `node scripts/list-provider-models.js`
2. Find account: `node scripts/list-accounts.js --app-slug <slug>` (use `pipedream_account_id`)
3. Find action: `node scripts/search-actions.js --query <word> --app-slug <slug>` (action_id = key)
4. Create integration: `node scripts/create-integration.js --action-id <id> --app-slug <slug> --account-id <id> --configured-props <json>`
5. Add tools to agent node via `flow_agent_app_integration_tools`

### Database CRUD

1. List tables: `node scripts/list-tables.js`
2. Query: `node scripts/query-rows.js --table <name> --filters <json>`
3. Create/update/delete with row scripts

## Graph rules

- Exactly one start node with `id` = `start`
- Never change existing node IDs
- Use `{node_type}_{timestamp_ms}` for new node IDs
- Non-decide nodes have 0 or 1 outgoing `next` edge
- Decide edge labels must match `conditions[].label`
- Edge keys are `source`/`target`/`label` (not `from`/`to`)

For full schema details, see `references/graph-contract.md`.

## Function rules

```js
async function handler(request, env) {
  // Parse input
  const body = await request.json();
  // Use env.KV and env.DB as needed
  return new Response(JSON.stringify({ result: "ok" }));
}
```

- Do NOT use `export`, `export default`, or arrow functions
- Return a `Response` object

## Execution context

Always use this structure:
- `vars` - user-defined variables
- `system` - system variables
- `context` - channel data
- `metadata` - request metadata

## Scripts

### Workflows

| Script | Purpose |
|--------|---------|
| `list-workflows.js` | List workflows (metadata only) |
| `get-workflow.js` | Get workflow metadata |
| `create-workflow.js` | Create a workflow |
| `update-workflow-settings.js` | Update workflow settings |

### Graph

| Script | Purpose |
|--------|---------|
| `get-graph.js` | Get workflow graph + lock_version |
| `edit-graph.js` | Patch graph via string replacement |
| `update-graph.js` | Replace entire graph |
| `validate-graph.js` | Validate graph structure locally |

### Triggers

| Script | Purpose |
|--------|---------|
| `list-triggers.js` | List triggers for a workflow |
| `create-trigger.js` | Create a trigger |
| `update-trigger.js` | Enable/disable a trigger |
| `delete-trigger.js` | Delete a trigger |
| `list-whatsapp-phone-numbers.js` | List phone numbers for trigger setup |

### Executions

| Script | Purpose |
|--------|---------|
| `list-executions.js` | List executions |
| `get-execution.js` | Get execution details |
| `get-context-value.js` | Read value from execution context |
| `update-execution-status.js` | Force execution state |
| `resume-execution.js` | Resume waiting execution |
| `list-execution-events.js` | List execution events |

### Functions

| Script | Purpose |
|--------|---------|
| `list-functions.js` | List project functions |
| `get-function.js` | Get function details + code |
| `create-function.js` | Create a function |
| `update-function.js` | Update function code |
| `deploy-function.js` | Deploy function to runtime |
| `invoke-function.js` | Invoke function with payload |
| `list-function-invocations.js` | List function invocations |

### App integrations

| Script | Purpose |
|--------|---------|
| `list-apps.js` | Search integration apps |
| `search-actions.js` | Search actions (action_id = key) |
| `get-action-schema.js` | Get action JSON schema |
| `list-accounts.js` | List connected accounts |
| `create-connect-token.js` | Create OAuth connect link |
| `configure-prop.js` | Resolve remote_options for a prop |
| `reload-props.js` | Reload dynamic props |
| `list-integrations.js` | List saved integrations |
| `create-integration.js` | Create an integration |
| `update-integration.js` | Update an integration |
| `delete-integration.js` | Delete an integration |

### Databases

| Script | Purpose |
|--------|---------|
| `list-tables.js` | List D1 tables |
| `get-table.js` | Get table schema + sample rows |
| `query-rows.js` | Query rows with filters |
| `create-row.js` | Create a row |
| `update-row.js` | Update rows |
| `upsert-row.js` | Upsert a row |
| `delete-row.js` | Delete rows |

### OpenAPI

| Script | Purpose |
|--------|---------|
| `openapi-explore.mjs` | Explore OpenAPI (search/op/schema/where) |

Install deps (once):
```bash
npm i
```

Examples:
```bash
node scripts/openapi-explore.mjs --spec workflows search "variables"
node scripts/openapi-explore.mjs --spec workflows op getWorkflowVariables
node scripts/openapi-explore.mjs --spec platform op queryDatabaseRows
```

## Notes

- Prefer file paths over inline JSON (`--definition-file`, `--code-file`)
- `action_id` is the same as `key` from `search-actions`
- `--account-id` uses `pipedream_account_id` from `list-accounts`
- Variable CRUD (`variables-set.js`, `variables-delete.js`) is blocked - Platform API doesn't support it
- Raw SQL execution is not supported via Platform API

## References

Read before editing:
- references/graph-contract.md - Graph schema, computed vs editable fields, lock_version
- references/node-types.md - Node types and config shapes
- references/workflow-overview.md - Execution flow and states

Other references:
- references/execution-context.md - Context structure and variable substitution
- references/triggers.md - Trigger types and setup
- references/app-integrations.md - App integration and variable_definitions
- references/functions-reference.md - Function management
- references/functions-payloads.md - Payload shapes for functions
- references/databases-reference.md - Database operations

## Assets

| File | Description |
|------|-------------|
| `workflow-linear.json` | Minimal linear workflow |
| `workflow-decision.json` | Minimal branching workflow |
| `workflow-agent-simple.json` | Minimal agent workflow |
| `workflow-customer-support-intake-agent.json` | Customer support intake |
| `workflow-interactive-buttons-decide-function.json` | Interactive buttons + decide (function) |
| `workflow-interactive-buttons-decide-ai.json` | Interactive buttons + decide (AI) |
| `workflow-api-template-wait-agent.json` | API trigger + template + agent |
| `function-decide-route-interactive-buttons.json` | Function for button routing |
| `agent-app-integration-example.json` | Agent node with app integrations |

## Related skills

- `integrate-whatsapp` - Onboarding, webhooks, messaging, templates, flows
- `observe-whatsapp` - Debugging, logs, health checks

<!-- FILEMAP:BEGIN -->
```text
[automate-whatsapp file map]|root: .
|.:{package.json,SKILL.md}
|assets:{agent-app-integration-example.json,databases-example.json,function-decide-route-interactive-buttons.json,functions-example.json,workflow-agent-simple.json,workflow-api-template-wait-agent.json,workflow-customer-support-intake-agent.json,workflow-decision.json,workflow-interactive-buttons-decide-ai.json,workflow-interactive-buttons-decide-function.json,workflow-linear.json}
|references:{app-integrations.md,databases-reference.md,execution-context.md,function-contracts.md,functions-payloads.md,functions-reference.md,graph-contract.md,node-types.md,triggers.md,workflow-overview.md,workflow-reference.md}
|scripts:{configure-prop.js,create-connect-token.js,create-function.js,create-integration.js,create-row.js,create-trigger.js,create-workflow.js,delete-integration.js,delete-row.js,delete-trigger.js,deploy-function.js,edit-graph.js,get-action-schema.js,get-context-value.js,get-execution-event.js,get-execution.js,get-function.js,get-graph.js,get-table.js,get-workflow.js,invoke-function.js,list-accounts.js,list-apps.js,list-execution-events.js,list-executions.js,list-function-invocations.js,list-functions.js,list-integrations.js,list-provider-models.js,list-tables.js,list-triggers.js,list-whatsapp-phone-numbers.js,list-workflows.js,openapi-explore.mjs,query-rows.js,reload-props.js,resume-execution.js,search-actions.js,update-execution-status.js,update-function.js,update-graph.js,update-integration.js,update-row.js,update-trigger.js,update-workflow-settings.js,upsert-row.js,validate-graph.js,variables-delete.js,variables-list.js,variables-set.js}
|scripts/lib/databases:{args.js,filters.js,kapso-api.js}
|scripts/lib/functions:{args.js,kapso-api.js}
|scripts/lib/workflows:{args.js,kapso-api.js,result.js}
```
<!-- FILEMAP:END -->

