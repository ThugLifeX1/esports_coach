# وثيقة تصميم النظام (SDD)
# ESports Coach — مدرب الرياضات الإلكترونية
**الإصدار:** 1.0.0  
**التاريخ:** 2026-05-03  
**الحالة:** مسودة أولى

---

## 1. المعمارية العامة (System Architecture)

### 1.1 نمط المعمارية
نظام **Modular Monolith** مع إمكانية الانتقال إلى Microservices في المستقبل:
- **Frontend:** Next.js 15 (App Router) — SSR + CSR Hybrid
- **Backend:** Node.js + Fastify (أسرع من Express) — RESTful API + WebSocket
- **AI Orchestration Layer:** طبقة منفصلة لإدارة وكلاء AI
- **Background Jobs:** Bull Queue مع Redis
- **Database:** PostgreSQL (Supabase-compatible)
- **Cache:** Redis
- **Storage:** S3-Compatible (MinIO self-hosted / AWS S3)
- **Real-time:** Socket.IO

```
┌─────────────────────────────────────────────────────┐
│                   CLIENTS                            │
│     Browser (Next.js PWA)  ·  Mobile (PWA)          │
└────────────────┬────────────────────────────────────┘
                 │ HTTPS / WSS
┌────────────────▼────────────────────────────────────┐
│              API GATEWAY (Nginx / Caddy)             │
│         Rate Limiting · SSL · Load Balancing         │
└──────┬────────────────┬───────────────┬─────────────┘
       │                │               │
┌──────▼──────┐  ┌──────▼──────┐ ┌─────▼──────────────┐
│ Next.js App │  │  Fastify    │ │  AI Orchestrator   │
│  (Frontend) │  │  (API)      │ │  (Agent Engine)    │
└─────────────┘  └──────┬──────┘ └─────┬──────────────┘
                        │              │
        ┌───────────────┼──────────────┤
        │               │              │
┌───────▼───┐   ┌───────▼──┐  ┌───────▼──────┐
│ PostgreSQL│   │  Redis   │  │  S3 Storage  │
│  (Main DB)│   │(Cache+MQ)│  │  (Files/Vid) │
└───────────┘   └──────────┘  └──────────────┘
```

### 1.2 مبدأ Multi-Tenancy
- كل **Organization** مستأجر مستقل (Tenant)
- عزل البيانات على مستوى `org_id` في كل جدول
- Row Level Security (RLS) في PostgreSQL
- الفرق داخل نفس المنظمة يمكنها مشاركة موارد محددة (Shared Agents)

---

## 2. Stack التقني المختار

### 2.1 Frontend
| التقنية | الإصدار | الغرض |
|---------|---------|--------|
| Next.js | 15+ | Framework رئيسي (App Router) |
| React | 19+ | UI Library |
| TypeScript | 5+ | Type Safety |
| Tailwind CSS | 4+ | Styling |
| Framer Motion | 11+ | Animations |
| next-intl | 3+ | i18n (AR/EN/قابل للتوسع) |
| Zustand | 5+ | Client State Management |
| TanStack Query | 5+ | Server State + Caching |
| Socket.IO Client | 4+ | Real-time Communication |
| Konva.js | 9+ | 2D Map Canvas (محاكاة الخريطة) |
| Three.js + React Three Fiber | latest | 3D Map (اختياري) |
| React Hook Form + Zod | latest | Forms + Validation |
| Recharts | latest | Charts + Graphs |
| Lucide React | latest | Icons |

### 2.2 Backend
| التقنية | الإصدار | الغرض |
|---------|---------|--------|
| Node.js | 22 LTS | Runtime |
| Fastify | 4+ | HTTP Framework |
| TypeScript | 5+ | Type Safety |
| PostgreSQL | 16+ | Main Database |
| Drizzle ORM | latest | ORM + Migrations |
| Redis | 7+ | Cache + Message Queue |
| Bull Queue | 4+ | Background Jobs |
| Socket.IO | 4+ | Real-time (Chat, Voice Signaling) |
| Zod | 3+ | Input Validation |
| bcrypt | latest | Password Hashing |
| JWT (jose) | latest | Authentication |
| Multer / Fastify-Multipart | latest | File Upload |
| FFmpeg (via fluent-ffmpeg) | latest | Video Processing |
| Nodemailer | latest | Email |
| discord.js | latest | Discord Integration |

### 2.3 AI Layer
| التقنية | الغرض |
|---------|--------|
| LangChain.js | AI Agent Orchestration |
| OpenAI SDK | GPT-4o Integration |
| Google Generative AI SDK | Gemini Integration |
| Anthropic SDK | Claude Integration |
| Ollama Client | Local LLM Support |
| LangGraph.js | Multi-step Agent Workflows |

### 2.4 Infrastructure
| التقنية | الغرض |
|---------|--------|
| Docker + Docker Compose | Containerization |
| Nginx / Caddy | Reverse Proxy + SSL |
| MinIO | S3-Compatible Object Storage |
| Supabase (Optional) | Managed PostgreSQL + Auth |

---

## 3. هيكل المشروع (Project Structure)

```
esports-coach/
├── apps/
│   ├── web/                    # Next.js Frontend
│   │   ├── app/
│   │   │   ├── [locale]/
│   │   │   │   ├── (public)/   # صفحات عامة
│   │   │   │   │   ├── page.tsx           # Landing Page
│   │   │   │   │   ├── pricing/
│   │   │   │   │   └── auth/
│   │   │   │   ├── (coach)/    # لوحة الإدارة الفنية
│   │   │   │   │   ├── dashboard/
│   │   │   │   │   ├── analysis/
│   │   │   │   │   ├── simulation/
│   │   │   │   │   ├── agents/
│   │   │   │   │   ├── tournaments/
│   │   │   │   │   ├── team/
│   │   │   │   │   └── communication/
│   │   │   │   └── (admin)/    # لوحة تحكم الإدارة
│   │   │   │       ├── platform/
│   │   │   │       ├── organizations/
│   │   │   │       ├── subscriptions/
│   │   │   │       ├── agents-builder/
│   │   │   │       └── settings/
│   │   ├── components/
│   │   │   ├── ui/             # Base UI Components
│   │   │   ├── map/            # Map Simulation Components
│   │   │   ├── agents/         # AI Agent Components
│   │   │   ├── charts/         # Analytics Charts
│   │   │   └── shared/
│   │   └── lib/
│   │       ├── api/
│   │       ├── store/
│   │       └── utils/
│   │
│   └── api/                    # Fastify Backend
│       ├── src/
│       │   ├── modules/
│       │   │   ├── auth/
│       │   │   ├── organizations/
│       │   │   ├── teams/
│       │   │   ├── players/
│       │   │   ├── agents/
│       │   │   ├── analysis/
│       │   │   ├── simulation/
│       │   │   ├── tournaments/
│       │   │   ├── communication/
│       │   │   ├── subscriptions/
│       │   │   ├── notifications/
│       │   │   └── admin/
│       │   ├── ai/
│       │   │   ├── orchestrator/
│       │   │   ├── skills/
│       │   │   ├── providers/
│       │   │   └── video-analyzer/
│       │   ├── jobs/
│       │   ├── db/
│       │   │   ├── schema/
│       │   │   └── migrations/
│       │   └── lib/
│       │       ├── socket/
│       │       ├── storage/
│       │       └── notifications/
│
├── packages/
│   ├── shared-types/           # Shared TypeScript Types
│   ├── game-configs/           # خرائط وإعدادات الألعاب
│   └── ui-kit/                 # Shared UI Components
│
├── docker-compose.yml
├── docker-compose.prod.yml
└── turbo.json                  # Turborepo Monorepo Config
```

---

## 4. مخطط قاعدة البيانات (Database Schema)

### 4.1 الجداول الرئيسية

#### `organizations` (المنظمات)
```sql
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
name            TEXT NOT NULL
slug            TEXT UNIQUE NOT NULL
logo_url        TEXT
subscription_id UUID FK subscriptions
settings        JSONB DEFAULT '{}'
created_at      TIMESTAMPTZ DEFAULT NOW()
updated_at      TIMESTAMPTZ DEFAULT NOW()
```

#### `teams` (الفرق)
```sql
id              UUID PK
org_id          UUID FK organizations (NOT NULL)
name            TEXT NOT NULL
game            TEXT NOT NULL  -- pubg_mobile | free_fire | valorant | ...
logo_url        TEXT
region          TEXT
is_active       BOOLEAN DEFAULT true
settings        JSONB DEFAULT '{}'
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `users` (المستخدمون)
```sql
id              UUID PK
email           TEXT UNIQUE NOT NULL
password_hash   TEXT NOT NULL
full_name       TEXT NOT NULL
full_name_ar    TEXT
avatar_url      TEXT
system_role     TEXT  -- platform_admin | org_owner | staff | player
org_id          UUID FK organizations (NULLABLE)
is_active       BOOLEAN DEFAULT true
last_login      TIMESTAMPTZ
preferences     JSONB  -- language, theme, notifications
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `team_members` (أعضاء الفرق)
```sql
id              UUID PK
team_id         UUID FK teams
user_id         UUID FK users
role            TEXT  -- head_coach | asst_coach | lead_analyst | asst_analyst
                       -- team_manager | player | substitute
in_game_name    TEXT  -- الاسم داخل اللعبة
jersey_number   INTEGER
permissions     JSONB  -- granular permissions array
joined_at       TIMESTAMPTZ
left_at         TIMESTAMPTZ (NULLABLE)
is_active       BOOLEAN DEFAULT true
```

#### `ai_agents` (وكلاء AI)
```sql
id              UUID PK
org_id          UUID FK organizations (NULLABLE - null = platform agent)
team_id         UUID FK teams (NULLABLE - null = org-wide)
name_en         TEXT NOT NULL
name_ar         TEXT NOT NULL
description_en  TEXT
description_ar  TEXT
agent_type      TEXT  -- analyst | coach | scout | custom
ai_provider     TEXT  -- openai | gemini | claude | ollama
ai_model        TEXT  -- gpt-4o | gemini-1.5-pro | claude-3-5-sonnet | ...
system_prompt   TEXT
skills          JSONB  -- array of skill IDs
game_contexts   TEXT[]  -- which games this agent supports
is_shared       BOOLEAN DEFAULT false  -- shared across org teams
is_active       BOOLEAN DEFAULT true
created_by      UUID FK users
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `agent_skills` (مهارات الوكلاء)
```sql
id              UUID PK
name_en         TEXT NOT NULL
name_ar         TEXT NOT NULL
description_en  TEXT
description_ar  TEXT
skill_type      TEXT  -- predefined | custom
category        TEXT  -- analysis | coaching | scouting | video | reporting
prompt_template TEXT
input_schema    JSONB  -- JSON Schema for skill inputs
output_schema   JSONB  -- JSON Schema for skill outputs
org_id          UUID (NULLABLE - null = platform skill)
is_active       BOOLEAN DEFAULT true
created_at      TIMESTAMPTZ
```

#### `matches` (المباريات)
```sql
id              UUID PK
team_id         UUID FK teams
tournament_id   UUID FK tournaments (NULLABLE)
game            TEXT NOT NULL
map_name        TEXT
match_date      TIMESTAMPTZ
opponent_team   TEXT
result          TEXT  -- win | loss | draw
score           JSONB  -- {"team": 3, "opponent": 1}
placement       INTEGER  -- للألعاب Battle Royale
match_data      JSONB  -- raw game data from API
video_url       TEXT
source          TEXT  -- api | manual | video_extracted
created_at      TIMESTAMPTZ
```

#### `scenarios` (السيناريوهات)
```sql
id              UUID PK
team_id         UUID FK teams
match_id        UUID FK matches (NULLABLE)
name            TEXT NOT NULL
game            TEXT NOT NULL
map_name        TEXT NOT NULL
description     TEXT
canvas_data     JSONB  -- كامل بيانات المحاكاة (positions, paths, zones)
tags            TEXT[]
created_by      UUID FK users
is_template     BOOLEAN DEFAULT false
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `player_stats` (إحصائيات اللاعبين)
```sql
id              UUID PK
player_id       UUID FK team_members
match_id        UUID FK matches
game            TEXT NOT NULL
kills           INTEGER
deaths          INTEGER
assists         INTEGER
damage_dealt    NUMERIC
accuracy        NUMERIC
survival_time   INTEGER  -- seconds
placement       INTEGER
extra_stats     JSONB  -- game-specific stats
recorded_at     TIMESTAMPTZ
```

#### `tournaments` (البطولات)
```sql
id              UUID PK
org_id          UUID FK organizations (NULLABLE - external)
name            TEXT NOT NULL
game            TEXT NOT NULL
type            TEXT  -- internal | external
format          TEXT  -- round_robin | single_elim | double_elim | swiss
status          TEXT  -- draft | registration | ongoing | completed
start_date      DATE
end_date        DATE
external_source TEXT  -- URL or API source
bracket_data    JSONB  -- tournament bracket structure
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `subscriptions` (الاشتراكات)
```sql
id              UUID PK
org_id          UUID FK organizations
plan_type       TEXT  -- free | pro | enterprise
status          TEXT  -- active | past_due | cancelled | trialing
current_period_start  DATE
current_period_end    DATE
payment_provider      TEXT  -- stripe | paypal
external_sub_id       TEXT  -- Stripe Subscription ID
limits          JSONB  -- {teams: 5, players: 15, agents: 3, storage_gb: 20}
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
```

#### `notifications` (الإشعارات)
```sql
id              UUID PK
user_id         UUID FK users
type            TEXT  -- match_reminder | agent_report | team_update | system
title_en        TEXT
title_ar        TEXT
body_en         TEXT
body_ar         TEXT
channels        TEXT[]  -- in_app | email | discord | push
is_read         BOOLEAN DEFAULT false
link            TEXT
metadata        JSONB
created_at      TIMESTAMPTZ
```

#### `audit_log` (سجل التدقيق)
```sql
id              UUID PK
user_id         UUID FK users
org_id          UUID FK organizations (NULLABLE)
action          TEXT NOT NULL
entity_type     TEXT
entity_id       UUID
details         JSONB
ip_address      INET
created_at      TIMESTAMPTZ
```

---

## 5. واجهات API الرئيسية

### 5.1 المصادقة
```
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/me
```

### 5.2 المنظمات والفرق
```
GET    /api/v1/organizations/:orgId
PUT    /api/v1/organizations/:orgId
GET    /api/v1/organizations/:orgId/teams
POST   /api/v1/organizations/:orgId/teams
GET    /api/v1/teams/:teamId
PUT    /api/v1/teams/:teamId
GET    /api/v1/teams/:teamId/members
POST   /api/v1/teams/:teamId/members
PUT    /api/v1/teams/:teamId/members/:memberId
DELETE /api/v1/teams/:teamId/members/:memberId
```

### 5.3 وكلاء AI
```
GET    /api/v1/agents                     # list accessible agents
POST   /api/v1/agents                     # create agent
GET    /api/v1/agents/:agentId
PUT    /api/v1/agents/:agentId
DELETE /api/v1/agents/:agentId
POST   /api/v1/agents/:agentId/execute    # run agent with input
GET    /api/v1/agents/:agentId/history    # conversation history
GET    /api/v1/skills                     # list all skills
POST   /api/v1/skills                     # create custom skill
PUT    /api/v1/skills/:skillId
DELETE /api/v1/skills/:skillId
```

### 5.4 التحليل والمحاكاة
```
GET    /api/v1/scenarios
POST   /api/v1/scenarios
GET    /api/v1/scenarios/:id
PUT    /api/v1/scenarios/:id
DELETE /api/v1/scenarios/:id
POST   /api/v1/scenarios/:id/analyze      # AI analyze scenario
POST   /api/v1/video/upload               # upload video for analysis
GET    /api/v1/video/:jobId/status        # video processing status
POST   /api/v1/video/:jobId/to-scenario   # convert to simulation
```

### 5.5 الإحصائيات والمباريات
```
GET    /api/v1/matches
POST   /api/v1/matches
GET    /api/v1/matches/:id
PUT    /api/v1/matches/:id
GET    /api/v1/players/:playerId/stats
GET    /api/v1/teams/:teamId/stats
GET    /api/v1/teams/:teamId/heatmap
```

### 5.6 البطولات
```
GET    /api/v1/tournaments
POST   /api/v1/tournaments
GET    /api/v1/tournaments/:id
PUT    /api/v1/tournaments/:id
POST   /api/v1/tournaments/:id/matches
PUT    /api/v1/tournaments/:id/matches/:matchId/result
GET    /api/v1/tournaments/:id/bracket
POST   /api/v1/tournaments/:id/import     # import from external
```

### 5.7 التواصل
```
GET    /api/v1/channels                   # list team channels
POST   /api/v1/channels
GET    /api/v1/channels/:id/messages
POST   /api/v1/channels/:id/messages
WS     /ws/chat                           # real-time chat
WS     /ws/voice                          # WebRTC signaling for voice/video
```

### 5.8 الإشعارات
```
GET    /api/v1/notifications
PUT    /api/v1/notifications/:id/read
PUT    /api/v1/notifications/read-all
PUT    /api/v1/notification-preferences
```

### 5.9 Admin Platform
```
GET    /api/v1/admin/organizations
POST   /api/v1/admin/organizations
GET    /api/v1/admin/organizations/:id
PUT    /api/v1/admin/organizations/:id
DELETE /api/v1/admin/organizations/:id
GET    /api/v1/admin/users
GET    /api/v1/admin/subscriptions
PUT    /api/v1/admin/subscriptions/:id
GET    /api/v1/admin/analytics/overview
GET    /api/v1/admin/platform-agents      # manage shared agents
GET    /api/v1/admin/platform-skills      # manage shared skills
GET    /api/v1/admin/audit-log
```

---

## 6. نظام وكلاء AI — التصميم التقني

### 6.1 دورة حياة تنفيذ الوكيل
```
User Input
    │
    ▼
Agent Orchestrator (LangGraph)
    │
    ├── Load Agent Config (skills, provider, system prompt)
    ├── Resolve AI Provider (OpenAI / Gemini / Claude / Ollama)
    ├── Build Context (team data, match history, game context)
    │
    ▼
Skill Executor
    │
    ├── Parse Input against skill.input_schema
    ├── Inject data into skill.prompt_template
    ├── Call AI Provider API
    │
    ▼
Output Processor
    │
    ├── Validate output against skill.output_schema
    ├── Store result (agent_executions table)
    ├── Trigger follow-up actions (simulation, report, notification)
    │
    ▼
Return to User
```

### 6.2 تحليل الفيديو — السير التقني
```
Upload Video → S3 Storage
    │
    ▼
Bull Queue Job: video-analysis
    │
    ├── FFmpeg: Extract frames at key intervals
    ├── Computer Vision (AI): Detect players, positions, events
    ├── Game Event Extraction: kills, zones, rotations
    │
    ▼
Scenario Builder
    │
    ├── Map player positions to game map coordinates
    ├── Generate canvas_data (Konva.js format)
    ├── Create Scenario record in DB
    │
    ▼
Notify User → Ready for review/edit in Simulation Panel
```

---

## 7. نظام المحاكاة على الخريطة

### 7.1 بنية Konva.js Canvas
```
SimulationCanvas
├── MapLayer          # خلفية الخريطة (صورة مضغوطة)
├── ZonesLayer        # مناطق الخطر/الحصار
├── PathsLayer        # مسارات الحركة (Animated Lines)
├── PlayersLayer      # أيقونات اللاعبين (Draggable Circles)
├── EventsLayer       # أحداث (Kills, Loot, etc.)
├── AnnotationsLayer  # تعليقات نصية وصوتية
└── UILayer           # أدوات التحكم (Timeline, Tools)
```

### 7.2 تنسيق بيانات السيناريو (canvas_data)
```json
{
  "version": "1.0",
  "game": "pubg_mobile",
  "map": "erangel",
  "duration": 300,
  "players": [
    {
      "id": "p1",
      "name": "Player1",
      "team": "team_a",
      "color": "#3B82F6",
      "keyframes": [
        {"time": 0, "x": 0.35, "y": 0.42},
        {"time": 30, "x": 0.38, "y": 0.40}
      ]
    }
  ],
  "zones": [
    {"time": 60, "cx": 0.5, "cy": 0.5, "r": 0.3, "type": "safe"}
  ],
  "events": [
    {"time": 45, "type": "kill", "actor": "p1", "target": "enemy1", "x": 0.37, "y": 0.41}
  ],
  "annotations": [
    {"time": 30, "type": "text", "text": "Rotate now!", "x": 0.4, "y": 0.45}
  ]
}
```

---

## 8. نظام التواصل الفوري

### 8.1 Chat (Socket.IO)
```
Client connects → authenticate via JWT → join room(s)
    │
    ├── team:{teamId}           # Team channel
    ├── direct:{userId}         # Direct message
    └── coaching:{sessionId}    # Live coaching session
```

### 8.2 Voice/Video (WebRTC)
- **Signaling:** Socket.IO لتبادل SDP و ICE Candidates
- **Media:** WebRTC Peer-to-Peer (للمجموعات الصغيرة)
- **Fallback:** SFU (Selective Forwarding Unit) عبر mediasoup للمجموعات الكبيرة

---

## 9. نظام الإشعارات

### 9.1 معالج الإشعارات
```
Notification Event Trigger
    │
    ▼
Notification Router
    │
    ├── Check user preferences (channels: in_app, email, discord, push)
    ├── In-App: Store in notifications table → Socket.IO push
    ├── Email: Bull Queue → Nodemailer
    ├── Discord: Bull Queue → discord.js Webhook
    └── Push: Web Push API (PWA)
```

---

## 10. الأمان والتفويض

### 10.1 تدفق JWT
```
Login → Access Token (15min) + Refresh Token (7 days, httpOnly cookie)
Request → Bearer {access_token} in Authorization header
Refresh → POST /auth/refresh with httpOnly cookie
Logout → Revoke refresh token (Redis blacklist)
```

### 10.2 Middleware Stack (Fastify)
```
1. Rate Limiter (fastify-rate-limit)
2. CORS (fastify-cors)
3. Helmet (fastify-helmet)
4. JWT Verify (fastify-jwt)
5. Tenant Resolver (extract org_id from token)
6. Permission Guard (check user role + permissions)
7. Route Handler
8. Input Validation (Zod schema)
```

### 10.3 تشفير مفاتيح AI
- مفاتيح AI API مشفرة في قاعدة البيانات (AES-256-GCM)
- Master encryption key مخزن في Environment Variables
- لا تُعاد المفاتيح أبداً عبر API responses

---

## 11. إعداد البيئة والنشر

### 11.1 المتغيرات البيئية الرئيسية
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/esports_coach

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=...
JWT_REFRESH_SECRET=...
ENCRYPTION_KEY=...  # for AI API keys

# Storage
S3_ENDPOINT=...
S3_BUCKET=esports-coach
S3_ACCESS_KEY=...
S3_SECRET_KEY=...

# AI Providers (Platform defaults - orgs add their own)
OPENAI_API_KEY=...
GOOGLE_AI_KEY=...

# Email
SMTP_HOST=...
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...

# Discord
DISCORD_BOT_TOKEN=...

# Stripe
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
```

### 11.2 Docker Compose (Development)
```yaml
services:
  web:
    build: ./apps/web
    ports: ["3000:3000"]
  api:
    build: ./apps/api
    ports: ["4000:4000"]
    depends_on: [postgres, redis]
  postgres:
    image: postgres:16-alpine
    volumes: [pgdata:/var/lib/postgresql/data]
  redis:
    image: redis:7-alpine
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports: ["9000:9000", "9001:9001"]
```

---

## 12. اعتبارات الأداء

### 12.1 استراتيجية Caching
| البيانات | استراتيجية | TTL |
|----------|------------|-----|
| Game Maps / Configs | Redis + CDN | 24h |
| Player Stats | Redis | 5min |
| Tournament Brackets | Redis | 1min |
| AI Agent Config | Redis | 30min |
| Session Data | Redis | 15min |

### 12.2 تحسينات الخريطة والفيديو
- خرائط الألعاب: صور WebP مضغوطة، تحميل Lazy
- فيديو: معالجة في الخلفية (Bull Queue)، Streaming للنتائج عبر SSE
- Canvas: فقط الـ layers المتغيرة تُعاد رسمها (requestAnimationFrame)
