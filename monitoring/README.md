# Monitoring & Observability - GrandFlow Dev Environment

This setup provides distributed tracing, metrics collection, and dashboard visualization for the GrandFlow microservices architecture.

## Components

### Jaeger - Distributed Tracing
- **URL**: http://localhost:16686
- **Purpose**: Trace requests across services, identify bottlenecks, debug async operations
- **Data**: End-to-end request flows, span timing, errors
- **Key Features**:
  - See the complete path a request takes through the system
  - Identify which service is slow
  - Detect blocking operations (like the RabbitMQ consumer issue we fixed!)
  - Trace database queries, HTTP calls, message publishing

### Prometheus - Metrics Collection
- **URL**: http://localhost:9090
- **Purpose**: Collect and query system metrics
- **Metrics Collected**:
  - FastAPI request latency, error rates
  - Database connection pool stats
  - RabbitMQ consumer metrics
  - JVM metrics
  - Custom application metrics

### Grafana - Dashboard & Visualization
- **URL**: http://localhost:3002
- **Credentials**: `admin:admin`
- **Purpose**: Beautiful dashboards for visualizing metrics over time
- **Pre-configured**:
  - Prometheus data source
  - Jaeger integration for traces

---

## Quick Start

### 1. Start Infrastructure
```bash
./dev.sh up
```

This starts:
- PostgreSQL
- Redis
- RabbitMQ
- Nginx proxy
- **Jaeger** (port 16686)
- **Prometheus** (port 9090)
- **Grafana** (port 3002)

### 2. Start Backend Services Locally
```bash
# Terminal 1: Users Service
cd services/users
alembic upgrade head
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Budget Service
cd services/budget
alembic upgrade head
python -m uvicorn main:app --reload --port 8001
```

Services will automatically send traces to Jaeger and metrics to Prometheus.

### 3. Generate Some Load
```bash
# Make requests to see traces
curl http://localhost:8001/docs

# Or run tests
cd services/budget && pytest
```

### 4. View the Data

#### Jaeger Tracing
1. Open http://localhost:16686
2. Select service: `budget-service` or `users-service`
3. View traces - each request shows:
   - Total latency
   - Service breakdown
   - Database queries
   - Event consumer processing

#### Prometheus Metrics
1. Open http://localhost:9090
2. Query examples:
   - `rate(http_requests_total[5m])` - Request rate
   - `histogram_quantile(0.99, http_request_duration_seconds)` - 99th percentile latency
   - `http_requests_total{service="budget-service", status="500"}` - Error requests

#### Grafana Dashboards
1. Open http://localhost:3002 (admin:admin)
2. Explore pre-built dashboards
3. Create custom dashboards by querying Prometheus

---

## Debugging with Observability Tools

### Finding Blocking Operations

**Problem**: App startup hangs (like the RabbitMQ consumer issue)

**How to debug with Jaeger**:
1. Add explicit span logging to startup:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    with tracer.start_as_current_span("app.startup"):
        logger.info("startup_begin")
        await init_consumer()
        logger.info("init_consumer_done")
        await start_consumer()
        logger.info("start_consumer_done")
    yield
```

2. Open Jaeger, select service, find the trace
3. Look for spans that take much longer than expected
4. Identify blocking calls that shouldn't be on the event loop

### Detecting Performance Issues

**Prometheus queries to find bottlenecks**:
```
# Slowest endpoints
topk(5, rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m]))

# Error rate by service
rate(http_requests_total{status=~"5.."}[5m])

# Database connection saturation
pg_stat_activity_count / max_connections
```

### Correlation Between Services

Jaeger shows how data flows:
- User API → Budget Service (via HTTP)
- Budget Service → Event Consumer (RabbitMQ)
- Event Consumer → User Cache (Redis)

Identify:
- Which service adds latency?
- Are microservices blocking each other?
- Are async operations actually async?

---

## Configuration

### Prometheus (`monitoring/prometheus.yml`)
- Scrapes metrics from services every 15s globally
- Users Service metrics: `http://host.docker.internal:8003/metrics`
- Budget Service metrics: `http://host.docker.internal:8002/metrics`
- RabbitMQ management API: `http://rabbitmq:15672/api/metrics`

### Jaeger (`docker-compose.dev.yml`)
- Listens on UDP 6831 for span data
- Stores traces in-memory (not persistent)
- Retention: ~72 hours
- UI: http://localhost:16686

### Grafana (`monitoring/grafana/provisioning/`)
- Data sources pre-configured (Prometheus, Jaeger)
- Auto-loads dashboards from `dashboards/` directory
- Can add custom Grafana dashboard JSON files here

---

## Adding Custom Metrics

### In FastAPI

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
request_counter = meter.create_counter("custom_requests_total")

@app.get("/api/endpoint")
async def my_endpoint():
    request_counter.add(1)
    return {"data": "..."}
```

### Querying in Prometheus

```
custom_requests_total{service="budget-service"}
```

---

## Production Notes

**This setup is for development only.** In production:
- Jaeger uses persistent storage (Elasticsearch, etc.)
- Prometheus uses persistent volumes
- Separate Grafana instance with SSO
- Tracing sampling (not 100% of requests)
- Metric retention policies

---

## Troubleshooting

### "No traces appearing in Jaeger"
- Check service is sending spans: `docker logs jaeger-dev`
- Verify Jaeger host/port in service config
- Check for `init_observability()` call in main.py

### "Prometheus shows no metrics"
- Check if services are running locally
- Verify `host.docker.internal:800X/metrics` is reachable
- Check prometheus.yml scrape configs

### "Grafana can't connect to Prometheus"
- Grafana uses DNS: verify `prometheus:9090` resolves
- Check both are on same Docker network (`grandflow`)
- Restart Grafana: `docker restart grafana-dev`

---

## Performance Tips

- **Sampling**: For high-traffic services, enable trace sampling to reduce overhead
- **Batch processing**: Prometheus batches metrics (default 64 spans)
- **Storage**: Jaeger in-memory for dev, but purges after 72 hours
- **Network**: Metrics are shipped asynchronously to avoid blocking requests
