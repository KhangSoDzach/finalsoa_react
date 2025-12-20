# 🎯 SKYHOME SECURITY & SCALABILITY UPGRADE PLAN

## Master Implementation Roadmap (8 Weeks)

---

## 📋 PHASE 0: PREPARATION & BACKUP (Day 1-2)

### Prompt Template
CONTEXT: Dự án SkyHome apartment management, FastAPI + React, đang production.
TASK: Chuẩn bị môi trường để upgrade an toàn.
REQUIREMENTS:
- Tạo git branch mới từ main
- Backup database hiện tại
- Document current system state
- Setup testing environment
CONSTRAINTS:
- Không được chạm vào main branch
- Không được thay đổi production database
- Mọi thay đổi phải có rollback plan

### Checklist
- [ ] git checkout -b feature/security-upgrade
- [ ] pg_dump database → backup_YYYYMMDD.sql
- [ ] Document current endpoints trong CURRENT_STATE.md
- [ ] Setup .env.test cho testing
- [ ] Create tests/test_baseline.py để capture current behavior

---

## 🔴 PHASE 1: CRITICAL SECURITY FIXES (Week 1)

### 1.1 Password Hashing Migration (Day 1-2)
Prompt Template:
CONTEXT: backend/app/core/security.py đang dùng SHA256 thuần (unsafe).
TASK: Migrate sang bcrypt với backward compatibility.
FILES TO MODIFY/ADD: backend/app/core/security.py, backend/scripts/migrate_passwords_to_bcrypt.py, backend/requirements.txt, backend/tests/test_security_migration.py.
REQUIREMENTS:
1. Install passlib[bcrypt].
2. Dual-mode verify (legacy SHA256 + bcrypt).
3. Migration script để rehash passwords.
4. New passwords phải dùng bcrypt.
CONSTRAINTS: Không break existing users; phải có migration path; test với dummy data.
SUCCESS CRITERIA: Old users login OK; new passwords bcrypt; migration script chạy pass tests.

### 1.2 Rate Limiting Setup (Day 3)
Prompt Template:
CONTEXT: Không có rate limiting → dễ brute force/DDoS.
TASK: Implement SlowAPI rate limiting cho endpoints.
FILES: backend/requirements.txt (add slowapi), backend/app/main.py (middleware), backend/app/api/routes/auth.py (decorators), backend/app/core/rate_limiter.py.
LIMITS: login 5/min per IP; forgot-password 3/hour; register 10/hour.
REQUIREMENTS: Redis nếu có, fallback in-memory; custom error; exclude admin IP optional.
SUCCESS: 6th login attempt trả 429; headers hiện; tests pass.

### 1.3 Security Headers Middleware (Day 4)
Prompt Template:
CONTEXT: Thiếu security headers.
TASK: Add middleware với headers X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP, Referrer-Policy.
FILES: backend/app/main.py, backend/app/middleware/security_headers.py.
CONSTRAINT: CSP không chặn Chakra UI inline styles; middleware chạy trước CORS.
SUCCESS: securityheaders.com score A+; curl -I có đủ headers.

### 1.4 Environment Variables Security (Day 5)
Prompt Template:
CONTEXT: Hardcoded credentials trong backend/app/core/config.py.
TASK: Di chuyển sang env vars; validate bắt buộc.
FILES: backend/app/core/config.py, backend/.env.example, backend/.env (local, ignore git).
REQUIREMENTS: SECRET_KEY 32+ chars; DATABASE_URL từ env; fail fast nếu thiếu; .env.test cho pytest.
SUCCESS: App không start nếu thiếu env; local và CI đều chạy với env files.

---

## 🟡 PHASE 2: LOGGING & MONITORING (Week 2)

### 2.1 Structured Logging Setup (Day 1-2)
Prompt Template:
CONTEXT: Chưa có logging chuẩn.
TASK: Setup structlog JSON logging.
FILES: backend/app/core/logging_config.py, backend/app/middleware/request_logger.py, backend/app/main.py, backend/requirements.txt (add structlog, python-json-logger).
REQUIREMENTS: JSON output prod, pretty dev; include timestamp, request_id, user_id, endpoint; mask sensitive.
SUCCESS: Logs JSON; request_id consistent.

### 2.2 Audit Trail Implementation (Day 3-4)
Prompt Template:
CONTEXT: Cần audit actions (compliance/GDPR).
TASK: Tạo audit log system.
FILES: backend/app/models/audit_log.py, backend/app/services/audit_service.py, backend/app/api/routes/* (hook audit), backend/alembic/versions/xxx_add_audit_log_table.py.
EVENTS: login/logout, bill CRUD, payment, admin actions, data exports.
REQUIREMENTS: user_id, action, entity_type, entity_id, old_values, new_values, ip, ua, timestamp; immutable; retention 7 years; async/non-blocking; partition by month.
SUCCESS: Admin query được audit logs; overhead <5ms/request.

---

## 🟢 PHASE 3: DATABASE MIGRATIONS (Week 3)

### 3.1 Alembic Setup (Day 1-2)
Prompt Template:
CONTEXT: DB changes manual.
TASK: Setup Alembic baseline from current models.
FILES: backend/alembic/env.py, backend/alembic.ini, backend/alembic/versions/001_initial_schema.py.
COMMANDS: alembic init; alembic revision --autogenerate; alembic upgrade head.
CONSTRAINTS: Không đổi schema hiện tại; có rollback.
SUCCESS: upgrade/downgrade works; no data loss.

---

## 🔵 PHASE 4: TESTING INFRASTRUCTURE (Week 4)

### 4.1 Backend Unit Tests (Day 1-3)
Prompt Template:
CONTEXT: Coverage thấp (<10%).
TASK: Viết test cho auth, security, bills, users.
FILES: backend/tests/conftest.py, backend/tests/test_auth_comprehensive.py, backend/tests/test_security_comprehensive.py, backend/tests/test_bills_comprehensive.py.
REQUIREMENTS: pytest fixtures; SQLite in-memory; mock email; edge cases; runtime <30s.
SUCCESS: Coverage ≥80%; tests pass; CI green.

### 4.2 Frontend Tests (Day 4-5)
Prompt Template:
CONTEXT: Chưa có test FE.
TASK: Setup Vitest + React Testing Library.
FILES: src/tests/setup.ts, src/tests/Login.test.tsx, src/tests/api.test.ts.
REQUIREMENTS: Mock axios; test auth flow, validation, error handling; không cần backend chạy.
SUCCESS: npm test pass; coverage ≥60%.

---

## 🐳 PHASE 5: CONTAINERIZATION (Week 5)

### 5.1 Docker Setup (Day 1-3)
Prompt Template:
CONTEXT: Deployment không đồng nhất.
TASK: Tạo Dockerfile (backend, frontend) + docker-compose.
FILES: Dockerfile, Dockerfile.frontend, docker-compose.yml, docker-compose.dev.yml, .dockerignore.
SERVICES: backend (FastAPI), frontend (Nginx), postgres, redis, pgadmin (dev).
REQUIREMENTS: Multi-stage builds; non-root; health checks; dev volumes.
SUCCESS: docker-compose up chạy lần đầu thành công; services healthy; image <500MB.

---

## 🚀 PHASE 6: CI/CD PIPELINE (Week 6)

### 6.1 GitHub Actions Workflow (Day 1-3)
Prompt Template:
CONTEXT: Deploy manual.
TASK: Tạo CI/CD với GitHub Actions.
FILES: .github/workflows/ci.yml, deploy.yml, security-scan.yml.
PIPELINE: Lint (black, flake8, eslint) → Test (pytest, vitest) → Security (bandit, npm audit) → Build (docker) → Deploy (Vercel).
TRIGGERS: push/pr main; daily security scan.
SUCCESS: PR có green checks; auto-deploy chỉ khi tests pass; secrets trong GitHub Secrets.

---

## 📊 PHASE 7: GDPR COMPLIANCE (Week 7)

### 7.1 Data Export & Deletion (Day 1-3)
Prompt Template:
CONTEXT: GDPR Article 20/17.
TASK: Implement export và deletion request.
FILES: backend/app/api/routes/gdpr.py, backend/app/services/gdpr_service.py.
ENDPOINTS: POST /api/v1/users/me/export; POST /api/v1/users/me/delete-request; GET /api/v1/admin/gdpr/deletion-requests.
REQUIREMENTS: Export all user data; deletion = anonymize; retention 30 days then purge; email notify; financial records kept 7 years (anonymized).
SUCCESS: User nhận export; deleted account không login; audit trail giữ nguyên.

---

## ⚡ PHASE 8: PERFORMANCE OPTIMIZATION (Week 8)

### 8.1 Redis Caching (Day 1-2)
Prompt Template:
CONTEXT: Nhiều queries lặp.
TASK: Thêm Redis cache.
FILES: backend/app/core/cache.py; modify backend/app/api/routes/users.py, analytics.py.
STRATEGY: User stats TTL 5m; dashboard TTL 15m; invalidate on writes; graceful fallback nếu Redis down; key naming convention.
SUCCESS: Response time giảm ~50%; cache hit rate ≥70%.

---

## 📐 TASK EXECUTION PROMPT TEMPLATE

```
=== TASK EXECUTION PROMPT ===
PHASE: [Phase number & name]
TASK: [Task name]
OBJECTIVE: [Goal]

CURRENT STATE:
- Files affected: [list]
- Dependencies: [list]
- Tests to run: [list]

IMPLEMENTATION STEPS:
1. ...
2. ...
3. ...

VALIDATION CHECKLIST:
□ Code lints (black, flake8)
□ Tests pass (pytest -v / npm test)
□ No breaking changes
□ Documentation updated
□ Git commit with clear message

ROLLBACK PLAN:
If fails: [specific rollback steps]

NEXT TASK DEPENDENCIES:
This task blocks: [list]
This task requires: [list]
===========================
```

---

## 🎯 EXECUTION RULES

1) Luôn làm từng PHASE một.
2) Mỗi task có test riêng; chạy tests sau mỗi file đổi.
3) Git workflow: mỗi phase = 1 branch; commit rõ ràng; PR → review → merge.
4) Dependency graph:
- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → (Phase 7 || Phase 8)

---

## 🚨 ERROR PREVENTION CHECKLIST

Before starting any phase:
- Previous phase complete; tests pass; commit/push; backup DB; env files ok; deps installed.

During implementation:
- Work in feature branch; commit sau mỗi sub-task; run tests; không hardcode; giữ backward compatibility.

After completing phase:
- Run full suite: pytest && npm test
- Security: bandit -r backend/
- Lint: black backend/ && eslint src/
- Smoke: docker-compose up
- PR checklist; wait CI green; merge main.

---

## 📊 PROGRESS TRACKING TEMPLATE

```
# Implementation Status

## Phase 1: Critical Security
- [ ] 1.1 Password Hashing
- [ ] 1.2 Rate Limiting
- [ ] 1.3 Security Headers
- [ ] 1.4 Env Variables

## Phase 2: Logging & Monitoring
- [ ] 2.1 Structured Logging
- [ ] 2.2 Audit Trail

## Phase 3: Database Migrations
- [ ] 3.1 Alembic Setup

## Phase 4: Testing
- [ ] 4.1 Backend Tests
- [ ] 4.2 Frontend Tests

## Phase 5: Containerization
- [ ] 5.1 Docker Setup

## Phase 6: CI/CD
- [ ] 6.1 GitHub Actions

## Phase 7: GDPR
- [ ] 7.1 Data Export/Delete

## Phase 8: Performance
- [ ] 8.1 Redis Caching
```

---

## 📦 BRANCHING & MERGE STRATEGY
- Phase 1: feature/phase1-security
- Phase 2: feature/phase2-logging
- Phase 3: feature/phase3-migrations
- Phase 4: feature/phase4-testing
- Phase 5: feature/phase5-docker
- Phase 6: feature/phase6-cicd
- Phase 7: feature/phase7-gdpr
- Phase 8: feature/phase8-performance

---

## 🧪 TEST SUITES TO RUN PER PHASE
- Phase 1: pytest tests/test_security* tests/test_auth*; bandit
- Phase 2: pytest tests/test_logging*; manual log check
- Phase 3: alembic upgrade/downgrade; pytest DB tests
- Phase 4: pytest full; npm test
- Phase 5: docker-compose up --build; smoke API/UI
- Phase 6: CI pipeline dry-run; check artifacts
- Phase 7: GDPR endpoint tests; data export/delete flows
- Phase 8: Load test key endpoints; measure latency; cache hit metrics

---

## 🎛️ RISK & ROLLBACK
- Always keep latest DB backup.
- Use alembic downgrade for schema rollback.
- Feature flags for risky endpoints.
- If CI fails: revert PR or hotfix branch.

---

## ✅ NEXT ACTION
- Bắt đầu Phase 0: tạo branch feature/security-upgrade, backup DB, tạo CURRENT_STATE.md, thiết lập .env.test, thêm tests/test_baseline.py để lock hiện trạng.
