# Performance

> Deep-dive reference for Go performance profiling and optimization. Load when user needs to profile or optimize Go code.

## Profiling First (Measure, Don't Guess)

```
Tools:
├── go tool pprof      → CPU, memory, goroutine profiling
├── go test -bench     → Micro-benchmarks
├── go test -benchmem  → Memory allocation counts
├── runtime/trace      → Execution tracer
├── expvar / metrics   → Runtime metrics endpoint
└── go build -gcflags="-m" → Escape analysis

Common optimizations (ONLY after profiling):
├── Reduce allocations (sync.Pool, pre-allocate slices)
├── Use strings.Builder for string concatenation
├── Avoid interface{}/any in hot paths
├── Use struct embedding to reduce pointer chasing
├── Pre-size maps and slices: make([]T, 0, expectedCap)
├── Use io.Reader/Writer for streaming (avoid loading all into memory)
└── Consider msgpack/protobuf over JSON for internal services
```

## Memory Layout

```
Struct field ordering matters:
├── Group same-size fields together
├── Larger fields first, smaller fields last
├── Reduces padding, saves memory
├── Use fieldalignment linter to detect issues
└── ONLY matters at scale (millions of structs)
```

## Escape Analysis

```
Understanding heap vs stack:
├── go build -gcflags="-m" shows escape decisions
├── Variables that escape to heap = allocation = GC pressure
├── Returning pointer to local variable → escapes
├── Interface conversion → may escape
├── Closures capturing variables → may escape
└── Reducing escapes = reducing GC pauses
```

## Benchmark Patterns

```
Writing benchmarks:
├── func BenchmarkXxx(b *testing.B) { for i := 0; i < b.N; i++ { ... } }
├── Use b.ResetTimer() after setup
├── Use b.ReportAllocs() for allocation tracking
├── Compare with benchstat for statistical significance
├── Run: go test -bench=. -benchmem -count=10
└── Profile: go test -bench=. -cpuprofile=cpu.prof
```

## GC Tuning

```
├── GOGC=100 (default) — collect when heap doubles
├── GOMEMLIMIT (Go 1.19+) — set soft memory limit
├── Monitor with runtime.ReadMemStats()
├── Reduce allocations > tuning GC
└── Use sync.Pool for frequently allocated objects
```
