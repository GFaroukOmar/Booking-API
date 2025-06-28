# 🧐 Booking API – FastAPI + MySQL + JWT Auth

This project is a **complete backend Booking API** built with **FastAPI**, **SQLAlchemy**, and **MySQL**. It includes:

* ✅ JWT-based authentication
* ✅ Role-based access control (Admin & User)
* ✅ Service and slot management
* ✅ Booking system with real-time availability
* ✅ Swagger UI for API testing

---

## 🚀 Features

* **User Registration & Login**
* **JWT Authentication**
* **Admin Role** with full user/service/slot CRUD access
* **Service & Slot Management**
* **Book/Cancel Slots**
* **Protected Routes & Role Checks**
* **Swagger UI** (`/docs`) for easy testing

---

## 📦 Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-username/booking-api.git
cd booking-api
```

### 2. Install dependencies

Make sure you have Python 3.10+ and pip installed:

```bash
pip install -r requirements.txt
```

### 3. Configure database

In `app/database.py`, edit the following line with your own DB settings:

```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/booking_db"
```

> ⚠️ No `.env` used — DB config is hardcoded.

### 4. Create tables

Run this once to create all necessary tables in your MySQL DB:

```bash
python app/models.py
```

(If `models.py` doesn’t run directly, create a new `init_db.py` with `Base.metadata.create_all()` and run that.)

### 5. Run the app

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🥪 API Overview

| Method | Endpoint          | Description          | Access        |
| ------ | ----------------- | -------------------- | ------------- |
| POST   | `/users/register` | Register a new user  | Public        |
| POST   | `/users/login`    | Get JWT token        | Public        |
| GET    | `/users/`         | List all users       | Admin         |
| DELETE | `/users/{id}`     | Delete a user        | Admin         |
| POST   | `/services/`      | Create a service     | Admin         |
| GET    | `/services/`      | List services        | Public        |
| PUT    | `/services/{id}`  | Update a service     | Admin         |
| DELETE | `/services/{id}`  | Delete a service     | Admin         |
| POST   | `/slots/`         | Create a slot        | Admin         |
| GET    | `/slots/`         | List available slots | Public        |
| PUT    | `/slots/{id}`     | Update a slot        | Admin         |
| DELETE | `/slots/{id}`     | Delete a slot        | Admin         |
| POST   | `/bookings/`      | Book a slot          | Authenticated |
| GET    | `/bookings/`      | List my bookings     | Authenticated |
| DELETE | `/bookings/{id}`  | Cancel a booking     | Authenticated |
| GET    | `/bookings/all`   | List all bookings    | Admin         |

---

## 💡 Tech Stack

* **FastAPI** – web framework
* **SQLAlchemy** – ORM for MySQL
* **MySQL** – relational database
* **JWT** – secure token-based auth
* **Pydantic** – schema validation
* **Swagger UI** – built-in docs

---

## 🤑 Developer Notes

* Designed to be **frontend-ready** (React, Vue, mobile, etc.)
* Can easily be extended with:

  * Payment logic
  * Availability calendar
  * Email confirmations
  * Admin dashboards

---

## 📥 Contact

Need help building your custom API or app?
**I’m available for freelance work on Upwork.**

🔗 [See my Upwork profile](https://www.upwork.com/freelancers/~01eaf709db878e0c02)

---

## 📖 License

This project is open-source and available under the MIT License.
