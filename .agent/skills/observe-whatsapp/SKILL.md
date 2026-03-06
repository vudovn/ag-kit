---
name: observe-whatsapp
description: "Observe and troubleshoot WhatsApp in Kapso: debug message delivery, inspect webhook deliveries/retries, triage API errors, and run health checks. Use when investigating production issues, message f..."
risk: safe
source: "https://github.com/gokapso/agent-skills/tree/master/skills/observe-whatsapp"
date_added: "2026-02-27"
---

# Observe WhatsApp

## When to use

Use this skill for operational diagnostics: message delivery investigation, webhook delivery debugging, error triage, and WhatsApp health checks.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`

## How to

### Investigate message delivery

1. List messages: `node scripts/messages.js --phone-number-id <id>`
2. Inspect message: `node scripts/message-details.js --message-id <id>`
3. Find conversation: `node scripts/lookup-conversation.js --phone-number <e164>`

### Triage errors

1. Message errors: `node scripts/errors.js`
2. API logs: `node scripts/api-logs.js`
3. Webhook deliveries: `node scripts/webhook-deliveries.js`

### Run health checks

1. Project overview: `node scripts/overview.js`
2. Phone number health: `node scripts/whatsapp-health.js --phone-number-id <id>`

## Scripts

### Messages

| Script | Purpose |
|--------|---------|
| `messages.js` | List messages |
| `message-details.js` | Get message details |
| `lookup-conversation.js` | Find conversation by phone or ID |

### Errors and logs

| Script | Purpose |
|--------|---------|
| `errors.js` | List message errors |
| `api-logs.js` | List external API logs |
| `webhook-deliveries.js` | List webhook delivery attempts |

### Health

| Script | Purpose |
|--------|---------|
| `overview.js` | Project overview |
| `whatsapp-health.js` | Phone number health check |

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
node scripts/openapi-explore.mjs --spec platform search "webhook deliveries"
node scripts/openapi-explore.mjs --spec platform op listWebhookDeliveries
node scripts/openapi-explore.mjs --spec platform schema WebhookDelivery
```

## Notes

- For webhook setup (create/update/delete, signature verification, event types), use `integrate-whatsapp`.

## References

- references/message-debugging-reference.md - Message debugging guide
- references/triage-reference.md - Error triage guide
- references/health-reference.md - Health check guide

## Related skills

- `integrate-whatsapp` - Onboarding, webhooks, messaging, templates, flows
- `automate-whatsapp` - Workflows, agents, and automations

<!-- FILEMAP:BEGIN -->
```text
[observe-whatsapp file map]|root: .
|.:{package.json,SKILL.md}
|assets:{health-example.json,message-debugging-example.json,triage-example.json}
|references:{health-reference.md,message-debugging-reference.md,triage-reference.md}
|scripts:{api-logs.js,errors.js,lookup-conversation.js,message-details.js,messages.js,openapi-explore.mjs,overview.js,webhook-deliveries.js,whatsapp-health.js}
|scripts/lib/messages:{args.js,kapso-api.js}
|scripts/lib/status:{args.js,kapso-api.js}
|scripts/lib/triage:{args.js,kapso-api.js}
```
<!-- FILEMAP:END -->

