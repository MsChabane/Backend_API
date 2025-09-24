# 🛡️ User Management System (FastAPI)

A **User Management System** built with **FastAPI** and **SQLModel**, featuring authentication, CRUD operations, email verification, JWT authentication, token revocation with Redis, and secure password reset with 2-factor token verification.

---

## ✨ Features

- 👤 User CRUD (create, read, update, delete)
- 🔐 Authentication with:
  - JWT **access** and **refresh** tokens
  - Token revocation with **Redis**
- 📧 Email features:
  - Send verification email on registration
  - Reset password with **URL-safe timed token**
- ✅ User attributes:
  - First name
  - Last name
  - Email (unique)
  - Password (hashed & secured)
  - IsVerified flag

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – modern, fast backend framework
- [SQLModel](https://sqlmodel.tiangolo.com/) – ORM with Pydantic + SQLAlchemy
- [PostgreSQL](https://www.postgresql.org/) – relational database
- [Redis](https://redis.io/) – token revocation
- [itsdangerous](https://pythonhosted.org/itsdangerous/) – password reset tokens
- [Docker](https://www.docker.com/) – containerization
- [SMTP](https://docs.python.org/3/library/smtplib.html) – email delivery

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory and configure:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHME=HS256

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com

SERILIZER_SECRET=your_serializer_secret

REDIS_URL=redis://localhost:6379
```
## 📓 Documentation :
- **Swagger UI**: /docs
- **Redoc** : /redoc

## 🚀 Run with Docker

You can pull the image directly from Docker Hub:

```bash
docker pull mschabane/user_management_fastapi:v1.0.0

docker run -d -p 8000:8000 --name user_management_api \
  --env DATABASE_URL=your_database_url \
  --env JWT_SECRET=your_jwt_secret \
  --env JWT_ALGORITHME=HS256 \
  --env MAIL_USERNAME=your_email_username \
  --env MAIL_PASSWORD=your_email_password \
  --env MAIL_FROM=your_email_address \
  --env SERILIZER_SECRET=your_serializer_secret \
  --env REDIS_URL=your_redis_url \
  mschabane/user_management_fastapi:v1.0.0
```


