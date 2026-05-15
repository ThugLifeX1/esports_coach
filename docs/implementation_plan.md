# خطة التنفيذ (Implementation Plan)
# ESports Coach — مدرب الرياضات الإلكترونية
**الإصدار:** 1.0.0 | **التاريخ:** 2026-05-03

---

## Phase 0 — Project Setup & Infrastructure
**الهدف:** بيئة العمل، Monorepo، Docker، CI/CD

- [ ] تهيئة Turborepo Monorepo (`apps/web`, `apps/api`, `packages/`)
- [ ] إعداد TypeScript shared config
- [ ] إنشاء `packages/shared-types` لـ Types المشتركة
- [ ] إنشاء `packages/game-configs` لخرائط وإعدادات الألعاب
- [ ] إعداد Docker Compose (PostgreSQL 16, Redis 7, MinIO)
- [ ] إعداد Drizzle ORM + كتابة كامل schema قاعدة البيانات
- [ ] تشغيل أول migration وتأكيد الاتصال
- [ ] إعداد Fastify app هيكل أساسي (plugins, routes, error handler)
- [ ] إعداد Next.js 15 App Router + TypeScript + Tailwind 4
- [ ] إعداد ESLint + Prettier + Husky pre-commit hooks
- [ ] كتابة Health Check endpoint: `GET /api/v1/health`
- [ ] إعداد environment variables template (`.env.example`)
- [ ] إعداد Nginx reverse proxy config (dev + prod)
- [ ] إعداد GitHub Actions: lint + type-check على كل PR

---

## Phase 1 — Authentication & Multi-Tenancy
**الهدف:** نظام مصادقة كامل، إدارة المنظمات والفرق

- [ ] تنفيذ `POST /api/v1/auth/login` (JWT Access + Refresh Token)
- [ ] تنفيذ `POST /api/v1/auth/refresh` (httpOnly cookie)
- [ ] تنفيذ `POST /api/v1/auth/logout` (Redis token blacklist)
- [ ] تنفيذ `POST /api/v1/auth/forgot-password` + `reset-password`
- [ ] تنفيذ `GET /api/v1/auth/me`
- [ ] Middleware: JWT Verify → Tenant Resolver → Permission Guard
- [ ] Rate limiting على auth endpoints (5 req/min)
- [ ] CRUD كامل للمنظمات (Platform Admin فقط)
- [ ] CRUD كامل للفرق داخل المنظمة
- [ ] CRUD أعضاء الفريق + نظام الأدوار الـ 8
- [ ] نظام Granular Permissions (JSON array per member)
- [ ] Row Level Security في PostgreSQL (`org_id` isolation)
- [ ] صفحة Login (Next.js) مع validation
- [ ] صفحة إنشاء حساب / دعوة عضو
- [ ] Protected Routes middleware (Next.js middleware.ts)
- [ ] اختبارات: unit tests للـ auth module

---

## Phase 2 — Landing Page & Subscription System
**الهدف:** صفحة الهبوط العامة، نظام الاشتراكات

- [ ] تصميم نظام الألوان: Dark Gaming (Space Black + Electric Blue + Neon)
- [ ] إعداد Tailwind design tokens + Google Fonts (Rajdhani, Inter, Tajawal)
- [ ] مكونات UI الأساسية: Button, Card, Modal, Input, Badge, Toast
- [ ] بناء Header مع تبديل اللغة AR/EN وDark/Light
- [ ] بناء Footer
- [ ] بناء Landing Page:
  - [ ] Hero Section (animation + CTA)
  - [ ] Supported Games Section (logos)
  - [ ] Features Overview (AI Agents, Simulation, Analytics)
  - [ ] How It Works (steps)
  - [ ] Pricing Section (3 plans comparison table)
  - [ ] Testimonials Slider
  - [ ] FAQ Accordion
- [ ] صفحة Pricing مستقلة
- [ ] تكامل Stripe: Checkout + Webhook handler
- [ ] جداول `subscriptions` + منطق الـ plan limits
- [ ] صفحة إدارة الاشتراك (ترقية / إلغاء)
- [ ] i18n كامل: next-intl + ملفات ترجمة AR/EN
- [ ] SEO: meta tags, OpenGraph لكل صفحة
- [ ] PWA: manifest.json + service worker أساسي

---

## Phase 3 — Coach Dashboard (Core)
**الهدف:** لوحة الإدارة الفنية — الهيكل والأقسام الأساسية

- [ ] بناء Coach Layout: Sidebar + Top Bar + Breadcrumbs
- [ ] Sidebar navigation (collapsible, responsive)
- [ ] Dashboard Overview Page:
  - [ ] إحصائيات سريعة (فرق، لاعبون، مباريات، وكلاء)
  - [ ] آخر النشاطات
  - [ ] المباريات القادمة
- [ ] صفحة إدارة الفريق:
  - [ ] عرض قائمة الأعضاء + أدوارهم
  - [ ] إضافة/تعديل/حذف عضو
  - [ ] تعديل الصلاحيات
- [ ] صفحة ملف اللاعب الشخصي:
  - [ ] معلومات اللاعب + In-Game Name
  - [ ] ملخص الإحصائيات الشخصية
  - [ ] سجل المباريات
- [ ] إدارة المباريات:
  - [ ] إضافة مباراة يدوياً
  - [ ] استيراد من API اللعبة
  - [ ] عرض نتائج وإحصائيات المباراة

---

## Phase 4 — AI Agents System
**الهدف:** نظام وكلاء AI الكامل (إنشاء، تنفيذ، مهارات)

- [ ] تصميم AI Orchestrator Layer (LangChain.js + LangGraph)
- [ ] تنفيذ AI Provider adapters:
  - [ ] OpenAI adapter (GPT-4o)
  - [ ] Google Gemini adapter
  - [ ] Anthropic Claude adapter
  - [ ] Ollama adapter (local LLM)
- [ ] نظام تشفير AI API Keys (AES-256-GCM)
- [ ] CRUD وكلاء AI (Platform + Org-level)
- [ ] نظام المهارات (Skills):
  - [ ] 8 مهارات محددة مسبقاً (Predefined)
  - [ ] واجهة بناء مهارة مخصصة (Custom Skill Builder)
  - [ ] ربط مهارات بوكيل (Skill Assignment)
- [ ] `POST /api/v1/agents/:id/execute` (تنفيذ وكيل)
- [ ] حفظ تاريخ المحادثات (`agent_executions` table)
- [ ] واجهة الوكلاء في Coach Panel:
  - [ ] قائمة الوكلاء المتاحة
  - [ ] واجهة محادثة مع الوكيل (Chat-like UI)
  - [ ] عرض نتائج التحليل
- [ ] واجهة Agent Builder في Admin Panel:
  - [ ] إنشاء وكيل جديد (wizard)
  - [ ] إضافة/ربط مهارات
  - [ ] اختبار الوكيل
  - [ ] مشاركة الوكيل بين فرق المنظمة

---

## Phase 5 — Map Simulation & Video Analysis
**الهدف:** لوحة المحاكاة التفاعلية + تحليل الفيديو

- [ ] تجهيز خرائط الألعاب (WebP مضغوطة، إحداثيات موحدة)
- [ ] بناء SimulationCanvas (Konva.js):
  - [ ] MapLayer (خلفية الخريطة)
  - [ ] PlayersLayer (لاعبون قابلون للسحب)
  - [ ] PathsLayer (رسم مسارات متحركة)
  - [ ] ZonesLayer (دوائر الحصار، مناطق التحكم)
  - [ ] EventsLayer (أحداث المباراة)
  - [ ] AnnotationsLayer (تعليقات نصية)
- [ ] Simulation Controls (Play, Pause, Rewind, Speed)
- [ ] Timeline bar تفاعلي
- [ ] أدوات الرسم (Draw, Select, Delete, Color Picker)
- [ ] حفظ واسترجاع السيناريوهات (canvas_data JSON)
- [ ] مكتبة السيناريوهات (Templates قابلة لإعادة الاستخدام)
- [ ] **تحليل الفيديو:**
  - [ ] رفع فيديو → S3
  - [ ] Bull Queue Job: FFmpeg frame extraction
  - [ ] AI Vision: استخراج أحداث + مواضع اللاعبين
  - [ ] تحويل تلقائي لـ canvas_data
  - [ ] واجهة مراجعة وتعديل النتائج
  - [ ] SSE endpoint لمتابعة تقدم المعالجة
- [ ] **خيار 3D:** Three.js layer فوق الـ 2D (toggle)
- [ ] AI تحليل السيناريو: `POST /scenarios/:id/analyze`

---

## Phase 6 — Analytics & Statistics
**الهدف:** لوحة التحليلات والإحصائيات الشاملة

- [ ] إحصائيات اللاعع الفردي:
  - [ ] K/D Ratio, Accuracy, Damage, Survival Rate
  - [ ] Recharts: Line Chart (تطور عبر الزمن)
  - [ ] Radar Chart (مقارنة مهارات اللاعب)
- [ ] إحصائيات الفريق:
  - [ ] Win Rate, Placement avg, Team Fight Stats
  - [ ] Bar Chart + Pie Chart
- [ ] Heatmap تفاعلي على الخريطة (مناطق التواجد والاشتباك)
- [ ] مقارنة اللاعبين (Player Comparison Tool)
- [ ] مقارنة أداء الفريق بين الأدوار المختلفة
- [ ] تصدير التقارير (PDF / CSV)
- [ ] AI Report Generator: تقرير أداء تلقائي

---

## Phase 7 — Tournaments Management
**الهدف:** إدارة البطولات الداخلية والخارجية

- [ ] CRUD البطولات
- [ ] دعم أشكال البطولات: Round Robin, Single/Double Elimination, Swiss
- [ ] واجهة Bracket تفاعلية (رسم الأقواس)
- [ ] جدولة المباريات داخل البطولة
- [ ] تسجيل النتائج وتحديث الترتيب تلقائياً
- [ ] **بطولات خارجية:**
  - [ ] استيراد من API رسمي (PUBG, Valorant APIs)
  - [ ] استخراج نتائج من فيديو (OCR + AI)
  - [ ] إدخال يدوي مع Scraper helper
- [ ] إشعارات المباريات القادمة (24h, 1h قبل المباراة)
- [ ] صفحة عرض البطولة العامة (للمشاركين)

---

## Phase 8 — Real-time Communication
**الهدف:** Chat + Voice + Video داخل التطبيق + Discord

- [ ] Socket.IO server setup (namespaces: chat, voice, notifications)
- [ ] **Chat:**
  - [ ] قنوات الفريق (Team Channels)
  - [ ] Direct Messages
  - [ ] Coaching Sessions (مدرب ↔ لاعب)
  - [ ] Typing indicators, Read receipts
  - [ ] رفع ملفات/صور في الشات
- [ ] **Voice/Video:**
  - [ ] WebRTC Peer-to-Peer (مجموعات صغيرة ≤4)
  - [ ] mediasoup SFU (مجموعات أكبر)
  - [ ] غرف صوتية دائمة للفريق
  - [ ] Mute/Unmute/Camera controls
- [ ] **Discord Integration:**
  - [ ] Webhook إشعارات للـ Discord server
  - [ ] Bot commands أساسية (نتائج, مواعيد)
- [ ] **Email Notifications:** Nodemailer + Queue
- [ ] **Push Notifications:** Web Push API (PWA)
- [ ] إعدادات تفضيلات الإشعارات per user

---

## Phase 9 — Admin Control Panel
**الهدف:** لوحة تحكم المنصة الكاملة

- [ ] بناء Admin Layout منفصل
- [ ] **إدارة المنصة:**
  - [ ] إدارة المنظمات (CRUD + تفعيل/تعطيل)
  - [ ] إدارة المستخدمين على مستوى المنصة
  - [ ] إدارة الاشتراكات (ترقية، تعديل حدود)
  - [ ] Platform Agents & Skills الافتراضية
- [ ] **Analytics Dashboard:**
  - [ ] إجمالي المنظمات/الفرق/المستخدمين
  - [ ] نمو الاشتراكات (رسوم بيانية)
  - [ ] استخدام وكلاء AI
  - [ ] أكثر الألعاب استخداماً
- [ ] Audit Log viewer (فلترة + بحث)
- [ ] System Settings (إعدادات المنصة العامة)
- [ ] إدارة إعدادات AI المحركات الافتراضية
- [ ] إدارة الألعاب المدعومة والخرائط

---

## Phase 10 — Polish, Security & Performance
**الهدف:** الصقل النهائي، الأمان، الأداء

- [ ] **Animations & UX:**
  - [ ] Framer Motion: page transitions, scroll reveal
  - [ ] Loading Skeletons لكل قسم
  - [ ] Micro-interactions على الأزرار والبطاقات
  - [ ] Empty States تصميم جذاب
  - [ ] Error Boundaries + Error Pages
- [ ] **Security Hardening:**
  - [ ] Helmet.js headers
  - [ ] CSRF protection
  - [ ] Input sanitization (DOMPurify)
  - [ ] File upload validation (type, size, virus scan)
  - [ ] SQL Injection prevention audit
  - [ ] Penetration testing checklist
- [ ] **Performance:**
  - [ ] Next.js Image optimization (WebP, lazy loading)
  - [ ] Code splitting + dynamic imports
  - [ ] Redis caching audit + optimization
  - [ ] Database query optimization + indexes audit
  - [ ] Lighthouse score > 90 (Performance, Accessibility)
- [ ] **Testing:**
  - [ ] Unit tests: auth, agents, permissions (>70% coverage)
  - [ ] Integration tests: API endpoints
  - [ ] E2E tests: Playwright (login, simulation, agent execution)
- [ ] **Deployment:**
  - [ ] Docker Compose production config
  - [ ] Zero-downtime deployment script
  - [ ] Environment secrets management
  - [ ] Backup strategy (PostgreSQL + S3)
  - [ ] Monitoring: uptime + error tracking (Sentry)
- [ ] **i18n Final Review:** مراجعة كل الترجمات AR/EN
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## ملخص الجدول الزمني المقترح

| Phase | المدة المقدرة |
|-------|--------------|
| Phase 0 — Setup | أسبوع 1 |
| Phase 1 — Auth & Tenancy | أسبوع 2-3 |
| Phase 2 — Landing & Subscriptions | أسبوع 4-5 |
| Phase 3 — Coach Dashboard Core | أسبوع 6-7 |
| Phase 4 — AI Agents | أسبوع 8-10 |
| Phase 5 — Simulation & Video | أسبوع 11-13 |
| Phase 6 — Analytics | أسبوع 14-15 |
| Phase 7 — Tournaments | أسبوع 16-17 |
| Phase 8 — Communication | أسبوع 18-19 |
| Phase 9 — Admin Panel | أسبوع 20-21 |
| Phase 10 — Polish & Security | أسبوع 22-24 |

**الإجمالي المقدر:** ~24 أسبوع (6 أشهر) للإصدار الأول الكامل
