# user authentication API Documentation

## Base URL
`http://127.0.0.1:8000`

## Endpoints Overview

| Endpoint            | Method | Description |
|--------------------|--------|-------------|
| `/api/user/register/` | POST | Register a new user or organizer |
| `/api/user/login/` | POST | Login a user and obtain user authentication tokens |
| `/api/user/profile/` | GET | Retrieve the userenticated user's profile |
| `/api/user/profile/` | PATCH | Update the userenticated user's profile |
| `/api/user/profile/` | DELETE | Deactivate the userenticated user's account |

---

## User Registration

### Endpoint
`POST /api/user/register/`

### Request Body

| Field          | Type    | Required | Description |
|--------------|--------|----------|-------------|
| `username`    | string | Yes      | Unique username |
| `email`       | string | Yes      | Unique email address |
| `password`    | string | Yes      | Must be at least 8 characters long |
| `is_organizer` | boolean | No      | `true` for organizers, `false` for normal users |

### Example Request
```json
{
  "username": "john_doe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "is_organizer": false
}
```



### Response
```json
{
  "detail": "User registered successfully.",
  "refresh_token": "<refresh_token>",
  "access_token": "<access_token>",
  "is_organizer": false
}
```

### Error Responses
If a user tries to register with an already existing username or email, the server will respond with a 400 Bad Request status code, along with the following error message:
```json
{
  "username": [
    "user with this username already exists."
  ],
  "email": [
    "user with this email already exists."
  ]
}
```


---

## User Login

### Endpoint
`POST /api/user/login/`

### Request Body

| Field     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `email`    | string | Yes      | Registered email address |
| `password` | string | Yes      | User password |

### Example Request
```json
{
  "email": "johndoe@example.com",
  "password": "securepassword"
}
```

### Response
```json
{
  "detail": "User logged in successfully.",
  "refresh_token": "<refresh_token>",
  "access_token": "<access_token>",
  "is_organizer": false
}
```
### Error Responses for login
1. If the provided email does not exist in the system, the server will respond with a 400 Bad Request status code and the following error message:
```json
{
  "detail": "User with this email does not exist."
}
```

2. If the credentials provided (email/password) are invalid, the server will respond with a 400 Bad Request status code and the following error message:
```json
{
  "detail": "Invalid credentials."
}
```


---

## Retrieve User Profile

### Endpoint
`GET /api/user/profile/`

### Headers
| Key           | Value |
|--------------|-------|
| Authorization | Bearer `<access_token>` |

### Response
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "email": "johndoe@example.com",
  "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/image.jpg",
  "phone_number": "1234567890",
  "address": "123 Main St",
  "is_organizer": false
}
```

---

## Update User Profile

### Endpoint
`PATCH /api/user/profile/`

### Headers
| Key           | Value |
|--------------|-------|
| Authorization | Bearer `<access_token>` |

### Request Body (Partial Updates Allowed)

| Field           | Type    | Required | Description |
|---------------|--------|----------|-------------|
| `first_name`    | string | No      | First name |
| `last_name`     | string | No      | Last name |
| `profile_picture` | file | No      | Upload profile image |
| `phone_number`  | string | No      | Phone number |
| `address`       | string | No      | Address |

### Example Request
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "9876543210"
}
```

### Response
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "email": "johndoe@example.com",
  "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/image.jpg",
  "phone_number": "9876543210",
  "address": "123 Main St",
  "is_organizer": false
}
```

---

## Delete User Account

### Endpoint
`DELETE /api/user/profile/`

### Headers
| Key           | Value |
|--------------|-------|
| Authorization | Bearer `<access_token>` |

### Response
```json
{
  "message": "User profile deleted successfully."
}
```

> **Note:** This is a soft delete. The user's account will be deactivated but not permanently deleted.

---

## user authentication Notes
- Tokens (access & refresh) must be included in the `Authorization` header for protected routes.
- Profile updates allow partial updates (i.e., sending only the fields that need to be modified).
- Deleting a user account does not permanently remove it but marks it as inactive.

---

