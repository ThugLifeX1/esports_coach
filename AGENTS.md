# ESports Coach — Developer Guide

## Project Status
**Early planning phase.** No source code yet — only design docs (`docs/PRD.md`, `docs/SDD.md`, `docs/implementation_plan.md`) and domain skills (`skills/`).

## Architecture (Planned)
```
esports-coach/
├── apps/
│   ├── web/          # Next.js 15 (App Router), Arabic/English i18n
│   └── api/          # Fastify (Node.js 22), REST + WebSocket
├── packages/
│   ├── shared-types/ # Shared TypeScript types
│   ├── game-configs/ # Game maps and config
│   └── ui-kit/       # Shared UI components
├── docker-compose.yml
└── turbo.json        # Turborepo
```

## Key Conventions
- **i18n:** Arabic (RTL primary) + English; use `next-intl`; text keys in code
- **Theme:** Dark Gaming aesthetic — Deep Space Black + Electric Blue + Neon accents; Rajdhani/Bebas Neue for headings
- **AI Layer:** LangChain.js + LangGraph for agent orchestration; multiple providers (OpenAI, Gemini, Claude, Ollama)
- **Multi-tenancy:** Row-level security via `org_id` on every table
- **Auth:** JWT (15min access) + httpOnly refresh cookie (7 days); RBAC with 8 team roles
- **Database:** PostgreSQL 16 + Drizzle ORM + Redis 7 for cache/queue
- **Background jobs:** Bull Queue with Redis
- **Real-time:** Socket.IO; WebRTC signaling for voice/video

## Working with Skills
Domain skills live in `skills/esports-division/<role>/`. Each skill is self-contained with:
- `SKILL.md` — role definition and workflow
- `references/*.md` — supporting documents (templates, checklists)
- `scripts/*.py` — automation scripts

## Important Design Decisions (from SDD.md)
- Map simulation uses **Konva.js** for 2D canvas with canvas_data as JSON
- Video analysis: upload → S3 → Bull Queue (FFmpeg) → AI extraction → Scenario
- AI API keys encrypted at rest (AES-256-GCM)
- API versioning: `/api/v1/...`

## First Steps for New Features
1. Check `docs/implementation_plan.md` for phase context
2. Verify proposed structure against `docs/SDD.md` schema/APIs
3. For UI work: check design tokens in `docs/PRD.md` (Section 10.4)
4. Use `docs/` as source of truth over memory

## No Code Yet
Do not attempt to run/build/test — nothing is implemented. Focus on documentation improvements or creating new skill definitions.