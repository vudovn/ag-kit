# Concurrency Patterns

> Deep-dive reference for Go concurrency. Load when user works with goroutines, channels, or parallel processing.

## When to Use What

| Pattern | Use When |
|---------|----------|
| `goroutine + channel` | Fan-out/fan-in, pipelines |
| `sync.WaitGroup` | Wait for N goroutines to complete |
| `errgroup.Group` | Wait + collect first error + cancel others |
| `sync.Mutex/RWMutex` | Protect shared state |
| `sync.Once` | One-time initialization |
| `context.Context` | Cancellation, timeout, request-scoped values |

## The Golden Rules

```
Concurrency rules:
├── Always pass context.Context as first parameter
├── Never start a goroutine without knowing how it will stop
├── Use errgroup for concurrent operations that can fail
├── Prefer channels for communication, mutexes for state
├── Don't communicate by sharing memory—share memory by communicating
├── Always handle context cancellation
└── Use sync.Pool for frequently allocated objects (measure first!)

Context propagation:
├── Accept ctx in every function that does I/O
├── Pass ctx to downstream calls
├── Check ctx.Err() in long loops
├── Use context.WithTimeout for external calls
└── NEVER store context in a struct
```

## Goroutine Lifecycle

```
ALWAYS ensure goroutine cleanup:
├── Use context for cancellation
├── Use done channels for signaling
├── Defer cleanup in goroutines
├── Prevent goroutine leaks
└── Log goroutine lifecycle in debug mode
```

## Common Patterns

### Fan-Out / Fan-In
```
Use when: Processing N items concurrently, collecting results
├── Spawn N goroutines (fan-out)
├── Collect results via channel (fan-in)
├── Use errgroup to handle errors
└── Limit concurrency with semaphore channel
```

### Pipeline
```
Use when: Multi-stage data processing
├── Each stage: goroutine reading from input channel
├── Process → send to output channel
├── Close output channel when input is exhausted
└── Cancel pipeline via context
```

### Worker Pool
```
Use when: Rate-limiting concurrent work
├── Fixed number of goroutines reading from job channel
├── Results sent to result channel
├── Backpressure via buffered channels
└── Graceful shutdown via context cancellation
```
