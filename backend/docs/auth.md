# Authentication API Documentation

This document describes the authentication API that includes user login, user creation, update, and delete (soft delete).

- **Required fields while registering a user:** `first_name`, `last_name`, `username`, `email`, and `password`.
- **Optional fields:** `profile_picture`, `phone_number`, `address`, `is_organizer` (can be updated later from the profile).

## **BASE URL:**
`http://127.0.0.1:8000/api`

---

## **Endpoints**

### **1. User Login**
- **Endpoint:** `POST /user/login/`
- **Request Body:**
  ```json
  {
    "email": "example@gmail.com",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "detail": "User logged in successfully.",
    "refresh_token": "<refresh_token>",
    "access_token": "<access_token>",
    "is_organizer": false
  }
  ```

---

### **2. User Registration**
- **Endpoint:** `POST /user/register/`
- **Request Body:**
  ```json
  {
    "first_name": "first",
    "last_name": "last",
    "username": "username",
    "email": "example@gmail.com",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "detail": "User registered successfully.",
    "refresh_token": "<refresh_token>",
    "access_token": "<access_token>",
    "is_organizer": false
  }
  ```

---

### **3. Update User Profile**
- **Endpoint:** `PUT /user/profile/`
- **Request Body:**
  - Only provided fields will be updated.
  - Use `form-data` in the body.
  ```json
  {
    "first_name": "First",
    "last_name": "Last",
    "address": "address",
    "is_organizer": true
  }
  ```

---

### **4. Delete User Profile**
- **Endpoint:** `DELETE /user/profile/`
- **Response:**
  ```json
  {
    "detail": "User profile deleted successfully."
  }
  ```

---

### **5. Token Refresh**
- **Endpoint:** `POST /token/refresh/`
- **Request Body:**
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
- **Response:**
  ```json
  {
    "access": "<new_access_token>",
    "refresh": "<new_refresh_token>"
  }
  ```

---

## **Notes:**
- Always pass the JWT token in the `Authorization` header for secured API requests.
- The refresh token is used to generate a new access token when expired.
