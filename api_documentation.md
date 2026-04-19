# MechConnect API Documentation

All API responses are wrapped in a standard structure:
```json
{
  "data": { ... },
  "message": "Optional message string"
}
```

---

## 🔐 Authentication & Users

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/auth/register/` | POST | Create a new user account | `{"username": "john_doe", "email": "john@example.com", "password": "password123", "role": "ROLE_CUSTOMER"}` |
| `/auth/login/` | POST | Log in and receive a JWT token | `{"email": "john@example.com", "password": "password123"}` |
| `/users/me/` | GET | Get current logged-in user profile | (Authenticated with Bearer Token) |

---

## 🔧 Mechanics & Services

| Endpoint | Method | Description | Example / Parameters |
| :--- | :--- | :--- | :--- |
| `/mechanics/approved/` | GET | List all approved mechanics | |
| `/mechanics/search/` | GET | Search mechanics by name/location | `?query=engine` |
| `/mechanics/profile/` | PUT | Update mechanic profile details | `{"workshopName": "Super Mechs", "specialty": "Engines"}` |
| `/services/mechanic/{id}/` | GET | Get services offered by a mechanic | |
| `/services/my-services/` | GET | Get services offered by the current mechanic | |
| `/services/` | POST | Add a new service (Mechanic only) | `{"name": "Oil Change", "price": 50.0, "description": "Full oil change"}` |
| `/services/{id}/` | DELETE | Remove a service | |

---

## 🚗 Vehicles

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/vehicles/` | GET | List current user's vehicles | |
| `/vehicles/` | POST | Add a new vehicle | `{"type": "CAR", "brand": "Toyota", "model": "Camry", "registration_number": "ABC-123"}` |
| `/vehicles/{id}/` | DELETE | Remove a vehicle | |

---

## 📅 Bookings & Workflow

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/bookings/` | POST | Create a new booking | `{"mechanic_id": 1, "service_id": 2, "vehicle_id": 3, "booking_date": "2024-12-01T10:00:00", "pickup_required": true, "pickup_address": "123 Main St"}` |
| `/bookings/customer/` | GET | List customer's bookings | |
| `/bookings/mechanic/` | GET | List mechanic's bookings | |
| `/bookings/{id}/status/` | PATCH | Update booking status | `{"status": "ACCEPTED"}` (Statuses: REQUESTED, ACCEPTED, REJECTED, COMPLETED, etc.) |

---

## 📦 Pickups & Payments

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/pickups/request/` | POST | Request a pickup for a booking | `{"booking": 5, "pickup_location": "456 Oak Ave"}` |
| `/pickups/{id}/status/` | PATCH | Update pickup status | `{"status": "PICKED_UP"}` |
| `/payments/process/` | POST | Process a payment | `{"booking_id": 5, "amount": 150.0, "payment_method": "UPI", "transaction_id": "TRANS12345"}` |

---

## ⭐ Ratings & Feedback

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/ratings/` | POST | Submit a rating for a booking | `{"booking_id": 5, "score": 5, "comment": "Great service!"}` |
| `/ratings/check/{id}/` | GET | Check if a booking has been rated | |
| `/ratings/mechanic/{id}/` | GET | Get all ratings for a mechanic | |
| `/feedback/` | POST | Submit text feedback | `{"booking_id": 5, "content": "The mechanic was very professional."}` |

---

## 🛡️ Admin Panel

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/admin/customers/` | GET | List all registered customers |
| `/admin/mechanics/` | GET | List all mechanics (and their profiles) |
| `/admin/mechanics/pending/` | GET | List mechanics awaiting approval |
| `/admin/mechanics/{id}/approve/` | PATCH | Approve a mechanic |
| `/admin/mechanics/{id}/reject/` | PATCH | Reject/Unapprove a mechanic |
| `/admin/dashboard/stats/` | GET | Get overall system statistics |

---

## 💡 Testing Tip
You can access the **Interactive Swagger UI** at http://localhost:8005/docs while the server is running. It allows you to try out every endpoint directly from your browser!
