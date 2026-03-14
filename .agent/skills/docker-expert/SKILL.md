---
name: docker-expert
description: Docker and containerization expertise for reliable builds, secure images, and efficient deployment pipelines.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Docker Expert

Use this skill for Dockerfiles, image optimization, container runtime hardening, and CI/CD image workflows.

## Core Rules

1. Use multi-stage builds to keep runtime images small.
2. Pin base image major versions and keep them updated.
3. Run as non-root in production containers.
4. Copy only required files and use `.dockerignore` aggressively.

## Build and Security Checklist

- Keep dependency install layers cache-friendly.
- Avoid baking secrets into image layers.
- Set explicit `NODE_ENV=production` (or equivalent runtime env).
- Expose only required ports.
- Validate startup command and health behavior for orchestrators.

## Performance Practices

- Minimize context size and invalidating layers.
- Cache dependency installs by copying lockfiles first.
- Keep runtime stage free of build tooling and source artifacts.
