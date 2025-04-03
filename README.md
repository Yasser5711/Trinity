# 🛒 E-Commerce Backend

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Dockerized](https://img.shields.io/badge/docker-ready-blue)
![Alt](https://repobeats.axiom.co/api/embed/540ac2fa615fe9dc532e07149de658bc8d7f7dd8.svg "Repobeats analytics image")

This project is a fully-featured **e-commerce backend** written in **FastAPI** 🚀 with a focus on **DevOps principles**, **clean architecture**, and **modular design**. It supports user authentication, role-based access control, stock and product management, PayPal integration for payments, and much more.

## 📦 Features

- ✅ **User Management**  
  Register, login, JWT-based auth, password reset, role assignment

- 🛡 **Role-Based Access Control**  
  Admin-only endpoints, dynamic role linking

- 📦 **Stock & Inventory Management**  
  CRUD operations on products, stock updates on checkout

- 🛒 **Cart & Checkout**  
  Cart with multiple items, item quantity tracking

- 💳 **PayPal Integration**  
  Create and capture PayPal orders via API

- 📊 **Reports & KPIs**  
  Generate downloadable PDF reports

- 🔐 **Token Blacklisting**  
  Secure logout with token blacklisting

- 🧪 **Full Test Coverage**  
  Unit + integration tests with `pytest`, `factory_boy`, and SQLite in-memory DB

- 🐳 **Dockerized Setup**  
  Clean service separation using Docker Compose (dev-ready)

---

## 🚀 Tech Stack

| Layer    | Technology          |
| -------- | ------------------- |
| API      | FastAPI             |
| Auth     | JWT, PassLib        |
| DB       | PostgreSQL          |
| ORM      | SQLAlchemy          |
| Payments | PayPal REST API     |
| Docs     | Swagger/OpenAPI     |
| Testing  | Pytest, Factory Boy |
| DevOps   | Docker, Compose     |

---

## 📂 Project Structure

- [back/](.\T-DEV-701-Devops\back)
  - [api/](.\T-DEV-701-Devops\back\api)
    - [controllers/](.\T-DEV-701-Devops\back\api\controllers)
  - [core/](.\T-DEV-701-Devops\back\core)
    - [helpers/](.\T-DEV-701-Devops\back\core\helpers)
    - [config.py](.\T-DEV-701-Devops\back\core\config.py)
    - [logger.py](.\T-DEV-701-Devops\back\core\logger.py)
  - [db/](.\T-DEV-701-Devops\back\db)
    - [models/](.\T-DEV-701-Devops\back\db\models)
    - [schemas/](.\T-DEV-701-Devops\back\db\schemas)
    - [scripts_db/](.\T-DEV-701-Devops\back\db\scripts_db)
    - [events.py](.\T-DEV-701-Devops\back\db\events.py)
    - [seed.py](.\T-DEV-701-Devops\back\db\seed.py)
    - [session.py](.\T-DEV-701-Devops\back\db\session.py)
  - [external/](.\T-DEV-701-Devops\back\external)
    - [paypal_client.py](.\T-DEV-701-Devops\back\external\paypal_client.py)
  - [fonts/](.\T-DEV-701-Devops\back\fonts)
  - [repositories/](.\T-DEV-701-Devops\back\repositories)
  - [services/](.\T-DEV-701-Devops\back\services)
  - [tests/](.\T-DEV-701-Devops\back\tests)
    - [factories/](.\T-DEV-701-Devops\back\tests\factories)
    - [integration/](.\T-DEV-701-Devops\back\tests\integration)
    - [unit/](.\T-DEV-701-Devops\back\tests\unit)
    - [utils/](.\T-DEV-701-Devops\back\tests\utils)
    - [conftest.py](.\T-DEV-701-Devops\back\tests\conftest.py)
  - [main.py](.\T-DEV-701-Devops\back\main.py)
- [docker/](.\T-DEV-701-Devops\docker)
  - [back/](.\T-DEV-701-Devops\docker\back)
    - [compose-dev.yml](.\T-DEV-701-Devops\docker\back\compose-dev.yml)
    - [compose-prod.yml](.\T-DEV-701-Devops\docker\back\compose-prod.yml)
  - [db/](.\T-DEV-701-Devops\docker\db)
    - [compose-dev.yml](.\T-DEV-701-Devops\docker\db\compose-dev.yml)
    - [compose-prod.yml](.\T-DEV-701-Devops\docker\db\compose-prod.yml)
  - [tools/](.\T-DEV-701-Devops\docker\tools)
    - [pgadmin/](.\T-DEV-701-Devops\docker\tools\pgadmin)
    - [compose-dev.yml](.\T-DEV-701-Devops\docker\tools\compose-dev.yml)
- [.env.template](.\T-DEV-701-Devops.env.template)
- [docker-compose-dev.yml](.\T-DEV-701-Devops\docker-compose-dev.yml)
- [docker-compose-prod.yml](.\T-DEV-701-Devops\docker-compose-prod.yml)
- [README.md](.\T-DEV-701-Devops\README.md)
- [script_fixture_product.py](.\T-DEV-701-Devops\script_fixture_product.py)

---

## 🧰 Getting Started

### 1. 📄 Set up your `.env` file

```bash
cp .env.template .env
```

---

### 2. 🐳 Start the Development Environment

Make sure Docker is running, then:

```bash
docker-compose -f docker-compose-dev.yml --profile back --env-file .env up -d
```

This spins up:

- PostgreSQL database
- FastAPI app (with hot reload)
- Optional: pgAdmin (if tools profile is used)

## 🔄 To stop everything

```bash
docker-compose down
```

### 3. 🧪 Run Tests

```bash
docker exec -it back bash -c "pytest"
```

## 📈 Example Endpoints

| Method | Endpoint                    | Description                 |
| ------ | --------------------------- | --------------------------- |
| POST   | `/auth/register`            | Register new user           |
| POST   | `/auth/login`               | Login and receive JWT       |
| GET    | `/users`                    | List all users (admin only) |
| POST   | `/stocks`                   | Add new stock (admin only)  |
| POST   | `/create-paypal-order`      | Create PayPal order (auth)  |
| POST   | `/capture-paypal-order/:id` | Capture PayPal payment      |
| GET    | `/reports`                  | Download PDF report (admin) |

## 🧠 License

This project is educational and open-source. Feel free to adapt it for your own use. Contributions welcome!
