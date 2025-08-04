# Grandflow

**Grandflow** is an open-source microservices-based platform designed to simplify budgeting and financial reporting for NGOs and donors. It helps standardize budget formats, integrates with modern tools, and makes collaboration between organizations easier and more transparent.

## 🚀 Why Grandflow?

I’ve been a co-founder and part of the nonprofit world for nearly 20 years. Throughout this time, I’ve written and reviewed hundreds of budgets and financial reports, collaborating with dozens of donors and NGOs.

Yet, 99% of these budgets were managed in scattered Excel files — each with different versions, formats, and errors. The process was repetitive, inefficient, and often frustrating.

As a software engineer, I knew there had to be a better way. Grandflow is my attempt to bridge these two worlds: leveraging tech to simplify, unify, and modernize financial management for NGOs.

This open-source platform aims to:
- Provide standardized budget and report tools
- Help generate donor-compliant financial reports with ease
- Empower NGOs to focus more on their fieldwork, not on spreadsheets
- Leverage modern tools, including AI, for smarter budgeting

🚧 **Project Status:** _Grandflow is currently in early development._  
💡 **Contribute:** We welcome contributions from developers, designers, and domain experts.  
💰 **Support:** If you'd like to support this project financially, donations are greatly appreciated.


---

## 🚀 Features

- 🧑‍🤝‍🧑 User & Customer Management (NGOs, Donors)
- 💰 Budget & Donation Tracking (multi-currency support)
- 🔐 JWT-based Authentication and Refresh Tokens
- 🧱 Microservice Architecture using FastAPI
- 🐳 Docker + Docker Compose for local development
- 📦 Shared static libraries for common models and logic
- 📄 OpenAPI documentation available per service

---

## 🛠️ Stack

| Component     | Tech               |
|---------------|--------------------|
| Backend       | Python + FastAPI   |
| Auth          | JWT + Refresh Token|
| ORM           | SQLAlchemy         |
| DB (dev)      | SQLite             |
| Messaging     | (Planned: Redis or Kafka) |
| Search        | (Planned: Elasticsearch) |
| Deployment    | Docker + Compose   |
| Infra as Code | (Optional: Terraform) |

---

## 🧱 Services

| Service       | Description                        | Port  |
|---------------|------------------------------------|--------|
| users-service | Manages users, customers (NGOs, donors), auth | 8000 |
| budget-service| Manages budgets and budget lines   | 8001 |
| shared        | Shared Pydantic models & utils     | N/A    |

---

## 🔧 Local Development

### 🚩 Requirements

- Docker
- Docker Compose
- Python 3.11+
- `make` (optional for CLI shortcuts)

### 🐳 Quick Start

```bash
# Clone the repo
git clone https://github.com/<your-org>/grandflow.git
cd grandflow

# Build and run all services
docker-compose up --build
```

Each service will be available at:

- `http://localhost:8000/docs` → Users Service
- `http://localhost:8001/docs` → Budget Service

---

## 🧪 Debugging

Each service supports debugging via `debugpy` on port `5678` (or as defined in `launch.json` for VSCode).

Attach using the VSCode debugger and the correct path mapping:
```json
"remoteRoot": "/app",
"localRoot": "${workspaceFolder}/services/users"
```

---

## 🔐 Authentication

- Uses **JWT Bearer tokens** for protected endpoints
- Refresh tokens stored securely with expiration
- All inter-service communication uses tokens for validation

---

## 🗃️ Database

- SQLite for local development (stored per service)
- SQLAlchemy + Alembic for migrations
- DB per microservice recommended

---

## 📦 Project Structure

```
grandflow/
├── docker-compose.yml
├── shared/                  # Shared libraries (e.g. models, JWT utils)
├── services/
│   ├── users/               # User & auth service
│   └── budget/              # Budgeting logic
```

---

## 🧩 API Example

```http
# Get list of users
GET /users/

# Create a budget (requires token)
POST /budgets/
Authorization: Bearer <token>
```

---

## 👥 Contributing

1. Fork the repo
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request 🙌

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.

---

## 💬 Questions or Support?

Open an [issue](https://github.com/arutsh/grandflow/issues) or start a [discussion](https://github.com/arutsh/grandflow/discussions).

---

## 🌟 Star this repo if you find it useful!
