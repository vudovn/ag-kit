# Evidence ledger schema

Save one UTF-8 JSON object:

```json
{
  "question": "What is being investigated?",
  "searched_at": "2026-08-20",
  "providers": ["runtime_web_search", "runtime_page_reader"],
  "unavailable_providers": [],
  "sources": [
    {
      "id": "s1",
      "url": "https://example.org/primary-document",
      "publisher": "Example Institute",
      "source_type": "primary"
    }
  ],
  "claims": [
    {
      "id": "c1",
      "text": "One bounded, checkable proposition.",
      "kind": "sourced",
      "confidence": "low",
      "source_ids": ["s1"],
      "independent_source_count": 1,
      "conflict": false
    }
  ],
  "gaps": ["Independent replication is unavailable."]
}
```

Rules:

- `providers` contains at least two unique capability names. Repeated queries to one capability still count once.
- Source IDs and URLs are unique. `source_type` is `primary`, `secondary`, or `aggregator`.
- Claims reference existing source IDs and use `kind` of `sourced` or `inference`.
- High confidence needs at least three independent sources, medium needs two, and low needs one.
- A conflicting claim cannot be high confidence.
- Every source supports at least one claim. Record every known evidence gap explicitly.

The validator does not fetch URLs, assess credibility, identify hidden shared provenance,
or prove that claims are true.

