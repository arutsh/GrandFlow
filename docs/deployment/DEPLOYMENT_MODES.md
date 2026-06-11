# GrandFlow Deployment Modes

GrandFlow supports three deployment modes to suit different use cases and deployment targets:

## 1. 🚀 DEV MODE (Development)

**Use case:** Local development with hot-reload capabilities.

**What runs:**
- ✅ PostgreSQL (Docker)
- ✅ Redis (Docker)
- ✅ API Gateway (Docker)
- ✅ Nginx Proxy (Docker)
- ❌ Frontend (runs locally)
- ❌ Users Service (runs locally)
- ❌ Budget Service (runs locally)

**Benefits:**
- Hot-reload for backend code changes
- Frontend assets compiled in real-time
- Faster local development iteration
- Reduced Docker container overhead

### Quick Start

```bash
# Start infrastructure
./dev.sh up

# In separate terminals, start local services:
cd services/users && python -m uvicorn main:app --reload
cd services/budget && python -m uvicorn main:app --reload
cd frontend-typescript && npm run dev
```

### Available Commands

```bash
./dev.sh up           # Start infrastructure
./dev.sh down         # Stop infrastructure
./dev.sh logs         # View logs
./dev.sh status       # Show container status
./dev.sh rebuild      # Rebuild containers without cache
./dev.sh clean        # Stop and remove volumes
```

### Endpoints (Dev Mode)

| Service | URL |
|---------|-----|
| Database | localhost:5432 |
| Redis | localhost:6379 |
| API Gateway | http://localhost:8080 |
| Nginx Proxy | http://localhost:8082 |
| Users Service | http://localhost:8000 |
| Budget Service | http://localhost:8001 |
| Frontend | http://localhost:3000 |

---

## 2. 🏠 LOCAL MODE (Production-like Local)

**Use case:** Complete local testing, demo for non-technical users, CI/CD testing.

**What runs:**
- ✅ PostgreSQL (Docker)
- ✅ Redis (Docker)
- ✅ API Gateway (Docker)
- ✅ Nginx Proxy (Docker)
- ✅ Frontend (Docker)
- ✅ Users Service (Docker)
- ✅ Budget Service (Docker)

**Benefits:**
- Everything runs in Docker
- No local dependencies required
- Production-like environment
- Perfect for demos and non-technical users
- Easy to share and reproduce

### Quick Start

```bash
# Start everything
./local.sh up

# Open browser
open http://localhost:3000
```

### Available Commands

```bash
./local.sh up              # Start all services
./local.sh down            # Stop all services
./local.sh logs [SERVICE]  # View logs (optional: specific service)
./local.sh status          # Show container status
./local.sh rebuild         # Rebuild containers without cache
./local.sh clean           # Stop and remove volumes
./local.sh shell [SERVICE] # Open shell in container
```

### Endpoints (Local Mode)

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Nginx Proxy | http://localhost:8082 |
| API Gateway | http://localhost:8080 |
| Users Service | http://localhost:8000 |
| Budget Service | http://localhost:8001 |
| Database | localhost:5432 |

### Database Access (Local Mode)

```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Databases: 
  - grandflow_users
  - grandflow_budget
```

---

## 3. ☁️ CLOUD MODE (SaaS - Future)

**Use case:** Scalable cloud deployment (AWS, Azure, GCP, etc.).

**What runs:**
- Kubernetes or orchestration platform
- Managed databases
- Load-balanced services
- Auto-scaling replicas
- CDN & monitoring

**Status:** 🚧 Under development

### Show Architecture Info

```bash
./cloud.sh info
```

### Future Implementation

The codebase is designed to support cloud deployment:
- ✅ Environment-based configuration
- ✅ Health checks implemented
- ✅ Stateless services
- ✅ Database migrations automated
- 🔄 Kubernetes manifests (TODO)
- 🔄 CI/CD pipelines (TODO)
- 🔄 Infrastructure-as-Code (TODO)

---

## Switching Between Modes

### Dev → Local

```bash
# Stop dev infrastructure
./dev.sh down

# Start local mode
./local.sh up
```

### Local → Dev

```bash
# Stop local stack
./local.sh down

# Start dev infrastructure
./dev.sh up
```

---

## Performance & Caching

All modes use Docker BuildKit with persistent cache mounts for faster builds:

```bash
DOCKER_BUILDKIT=1 docker compose build
```

**Benefits:**
- Python packages cached between builds
- No re-downloading of pip dependencies
- Builds ~10x faster on subsequent runs

---

## Troubleshooting

### Services won't start (Dev Mode)

**Problem:** Services exit immediately

**Solution:**
```bash
# Check logs
./dev.sh logs

# Make sure DB is healthy
docker compose -f docker-compose.dev.yml exec grandflow-db pg_isready
```

### Port already in use

**Solution:**
```bash
# Find service using port
lsof -i :8000

# Or use different dev file
docker compose -f docker-compose.dev.yml down
```

### Rebuild without cache

All modes support clean rebuild:

```bash
# Dev mode
./dev.sh rebuild

# Local mode
./local.sh rebuild
```

### Reset everything

```bash
# Dev mode
./dev.sh clean

# Local mode
./local.sh clean
```

---

## Default Environment Files

Each mode uses environment files for configuration:

- **Dev Mode:** `.env.*.dev` files
- **Local Mode:** `.env.*.dev` files
- **Cloud Mode:** To be defined per cloud provider

Example:
```
./services/users/.env.users.dev
./services/budget/.env.budget.private.dev
./api-gateway/.env.gateway.dev
```

---

## Architecture Comparison

| Feature | Dev | Local | Cloud |
|---------|-----|-------|-------|
| Hot-reload | ✅ | ❌ | ❌ |
| Docker only | ❌ | ✅ | ✅* |
| Local deps | ✅ | ❌ | ❌ |
| Scale-ready | ❌ | ❌ | ✅ |
| Non-tech user | ❌ | ✅ | ✅ |
| Dev speed | ⚡⚡ | ⚡ | 🔄 |

*Cloud mode requires cloud provider setup

---

## For Maintainers

### Modifying Docker Compose Files

1. **Dev mode:** `docker-compose.dev.yml`
2. **Local mode:** `docker-compose.local.yml`
3. **Cloud mode:** Define `docker-compose.cloud.yml` or K8s manifests

### Adding New Services

If adding a new service:
1. Add to `docker-compose.dev.yml` for dev testing
2. Add to `docker-compose.local.yml` for production-like local
3. Keep services stateless for cloud portability

### Environment Variables

Use `env_file` directive in compose files:
```yaml
env_file:
  - ./services/users/.env.users.dev
```

Keep `.env` files in `.gitignore` and provide `.env.example` templates.

---

## Quick Reference

```bash
# Start developing
./dev.sh up

# Run services locally (in separate terminals)
cd services/users && python -m uvicorn main:app --reload
cd services/budget && python -m uvicorn main:app --reload
cd frontend-typescript && npm run dev

# Test local mode
./local.sh up

# Check cloud readiness
./cloud.sh info
```
