---
name: api-testing
description: Comprehensive API testing strategies — contract testing with Pact, load testing with k6, integration tests with Supertest, and OpenAPI schema validation. Load when testing or verifying any API.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# API Testing Skill

> An API without tests is a promise without proof.

---

## Testing Pyramid for APIs

```
         /\
        /E2E\        ← Playwright / Postman collections
       /------\
      /  Integ \     ← Supertest / Jest / Vitest
     /----------\
    /  Contract  \   ← Pact (consumer-driven)
   /--------------\
  /    Unit Tests  \ ← Pure function tests (validators, transformers)
 /------------------\
```

---

## Integration Tests with Supertest

```typescript
// auth.test.ts
import request from 'supertest';
import { app } from '../app';
import { db } from '../lib/db';

describe('POST /api/auth/login', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  afterAll(async () => {
    await db.destroy();
  });

  it('returns 200 with valid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@test.com', password: 'correct-password' })
      .expect(200);

    expect(res.body).toMatchObject({
      token: expect.any(String),
      user: { email: 'user@test.com' }
    });
  });

  it('returns 401 with invalid credentials', async () => {
    await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@test.com', password: 'wrong' })
      .expect(401);
  });

  it('returns 400 with missing fields', async () => {
    await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@test.com' }) // missing password
      .expect(400);
  });
});
```

---

## Contract Testing with Pact

```typescript
// consumer.pact.test.ts
import { Pact } from '@pact-foundation/pact';

const provider = new Pact({
  consumer: 'FrontendApp',
  provider: 'UserAPI',
  port: 4000,
});

describe('User API Contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('gets user by id', async () => {
    await provider.addInteraction({
      state: 'user 1 exists',
      uponReceiving: 'a request for user 1',
      withRequest: { method: 'GET', path: '/users/1' },
      willRespondWith: {
        status: 200,
        body: { id: 1, email: 'user@test.com', name: 'Test User' }
      }
    });

    const user = await fetchUser(1);
    expect(user.id).toBe(1);
    await provider.verify();
  });
});
```

---

## Load Testing with k6

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up
    { duration: '1m',  target: 100 },  // stay at peak
    { duration: '30s', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],   // 95% under 500ms
    http_req_failed: ['rate<0.01'],     // <1% error rate
  },
};

export default function () {
  const res = http.get('https://api.example.com/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

---

## OpenAPI Validation

```typescript
// Use zod-to-openapi or @anatine/zod-openapi
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  name: z.string().min(1),
});

// Auto-generate OpenAPI spec and validate responses against it
// Use jest-openapi for response validation:
// expect(response).toSatisfyApiSpec();
```

---

## API Test Checklist

For every endpoint, test:

- [ ] Success (200/201) with valid data
- [ ] Missing required field (400)
- [ ] Invalid data type (422)
- [ ] Unauthorized (401) without token
- [ ] Forbidden (403) with wrong role
- [ ] Not found (404) for non-existent resource
- [ ] Rate limiting (429) when applicable
- [ ] Server error (500) handled gracefully
