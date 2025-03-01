# Authentication API Documentation
This document describes the authentication API that includes user login and create, update and delete (soft delete) user

- Required fields while registering user are (first_name, last_name, username, email and password )
- Optional fields (profile_picture, phone_number, address, is_organizer)  which can be later updated from profile


- **BASE URL :** `http://127.0.0.1:8000/api` 
## Endpoints


### 1. ---------- User Login ---------
- **Endpoint:** `POST /user/login/`
- **Request Body:**
  ```json
  {
    "email": "example@gmail.com",
    "password": "password123"
  }
- **Response:**
  ```json
  {
    "detail": "User logged in successfully.",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzQxODU2OSwiaWF0IjoxNzQwODI2NTY5LCJqdGkiOiI4NjY3ZjQzMWY5NWE0MzI5OTIxZjIzOWU2MmZkNjZiYyIsInVzZXJfaWQiOjl9.NPpJ4rzGwPauW738UrEymeeRxleybuTuYX6NB5omAuk",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNDMxMzY5LCJpYXQiOjE3NDA4MjY1NjksImp0aSI6IjI3ZTUzZmY3NTUyZjQ3ZmFiYTJhNzViZWNjZTljMjA1IiwidXNlcl9pZCI6OX0.pZkxvG52ZhuhU6O4WFJmCCxFL_M5PpGLZQkGXH7pVLE",
    "is_organizer": false
  }




### 2. ------------ User Registration ------------
- **Endpoint:** `POST /user/register/`
- **Request Body:**
- Required fields are (first_name, last_name, email and username)
  ```json
  {
    "first_name":"first",
    "last_name":"last",
    "username" :"username",
    "email":"example@gmai.com",
    "password":"password123"
  }
  ```
- **Response:**
  ```json
  {
    "detail": "User registered successfully.",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzQxMTQyMCwiaWF0IjoxNzQwODE5NDIwLCJqdGkiOiI1YzdjYjVhY2Y1NGI0YzU1OWQ0YjJhYjZmMTY3YzM5OSIsInVzZXJfaWQiOjl9.SNpC9647U-PknV7i7k8Sp4bAjWvfmYQTLT1prtgFnKA",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNDI0MjIwLCJpYXQiOjE3NDA4MTk0MjAsImp0aSI6IjMwNmYxZDRhZjdkNzRkOGJhMjljYjA5OWE4OWQyNjE2IiwidXNlcl9pZCI6OX0.drLlUMUUj13ghF1cLgfucLHn3AAbjYgRLW7HSiV3W7Y",
    "is_organizer": false
  }
  ```


### 3.----------  Update User Profile  ----------
- **Endpoint:** `PUT /user/profile/`
- **Request Body:**
- Only provided fields will be updated 
- Use form-data in body 
  ```json
  {
    "first_name": "First",
    "last_name": "Last",
    "address": "address",
    "is_organizer": true
  }




### 4. -------- Delete User Profile --------
- **Endpoint:** `DELETE /user/profile/`
- **Response:**
- ```json
  {
    "detail": "User profile deleted successfully."
  } 



### 5. ---------  Token Refresh ---------------- 
- **Endpoint:** `POST /token/refresh/`
- **Request Body:**
  ```json
  {
    "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzQxODUxNSwiaWF0IjoxNzQwODI2NTE1LCJqdGkiOiIxYjJiNTdmMGNhODE0NWI3YTMyZGNiMzY0NjY4Nzc5ZCIsInVzZXJfaWQiOjl9.KrTRhx9ptfsd3RJ4pl9KZGFKxNapyH-hXN5OrdVXC5c"
  }
  ```
- **Response:**
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNDMxODQxLCJpYXQiOjE3NDA4MjcwMjUsImp0aSI6IjZhMzAzYjRjMTg1YjRiYTU5ZjExNDEzYTNkNzk4ODRjIiwidXNlcl9pZCI6OX0.SwnDlhI9DVQsA3MUFw1jZxdNIoyg354ClesqDTc9hBA",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzQxOTA0MSwiaWF0IjoxNzQwODI3MDQxLCJqdGkiOiIwMzYyMjVkYjk1MDU0ZDM5YmNiYWFlNzNkN2UwNGU4ZiIsInVzZXJfaWQiOjl9.bKRHSUOPOTg-GIOoSP4rTaUKLWzsQ5Mly9l-Jn4MBbw"
  }
  ``` 


### Notes:
- Always pass the JWT token in the `Authorization` header for secured API requests.
- The refresh token is used to generate a new access token when expired.


