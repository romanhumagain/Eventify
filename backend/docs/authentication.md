# user authentication API Documentation


## Endpoints Overview

| Endpoint            | Method | Description |
|--------------------|--------|-------------|
| `/api/user/register/` | POST | Register a new user or organizer |
| `/api/user/login/` | POST | Login a user and obtain userentication tokens |
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

---

## Retrieve User Profile

### Endpoint
`GET /api/user/profile/`

### Headers
| Key           | Value |
|--------------|-------|
| userorization | Bearer `<access_token>` |

### Response
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "email": "johndoe@example.com",
  "profile_picture": "<profile_picture_url>",
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
| userorization | Bearer `<access_token>` |

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
  "profile_picture": "<profile_picture_url>",
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
| userorization | Bearer `<access_token>` |

### Response
```json
{
  "message": "User profile deleted successfully."
}
```

> **Note:** This is a soft delete. The user's account will be deactivated but not permanently deleted.

---

## userentication Notes
- Tokens (access & refresh) must be included in the `userorization` header for protected routes.
- Profile updates allow partial updates (i.e., sending only the fields that need to be modified).
- Deleting a user account does not permanently remove it but marks it as inactive.

---

