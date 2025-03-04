# RSVP API Documentation

## Overview
The RSVP API allows users to manage event attendance by confirming, declining, or keeping RSVP status as pending. Users can only manage their own RSVPs, and an email notification is sent upon status change.


## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication
All endpoints require authentication via a valid token.

## Endpoints

### 1. Get User's RSVPs
**Endpoint:** `GET /rsvp/`

**Description:** Retrieves all RSVPs for the authenticated user.

**Response:**
```json
[
    {
        "id": 1,
        "event": 5,
        "user": 3,
        "status": "Confirmed",
        "created_at": "2024-03-01T12:00:00Z"
    }
]
```

### 2. Create RSVP
**Endpoint:** `POST /rsvp/`

**Description:** Creates an RSVP for an event.

**Request:**
```json
{
    "event": 5,
    "status": "Confirmed"
}
```

**Response:**
```json
{
    "id": 1,
    "event": 5,
    "user": 3,
    "status": "Confirmed",
    "created_at": "2024-03-01T12:00:00Z"
}
```

### 3. Update RSVP
**Endpoint:** `PUT /rsvp/{id}/`

**Description:** Updates an existing RSVP.

**Request:**
```json
{
    "status": "Declined"
}
```

**Response:**
```json
{
    "id": 1,
    "event": 5,
    "user": 3,
    "status": "Declined",
    "created_at": "2024-03-01T12:00:00Z"
}
```

### 4. Delete RSVP
**Endpoint:** `DELETE /rsvp/{id}/`

**Description:** Deletes an RSVP.

**Response:**
```json
{
    "detail": "RSVP deleted successfully."
}
```

## RSVP Status Options
- **Confirmed**: The user has confirmed attendance.
- **Pending**: The RSVP is pending.
- **Declined**: The user has declined the invitation.

## Email Notifications
When a user confirms their RSVP, an email notification is automatically sent to them as a reminder.

## Notes
- Each user can RSVP to an event only once.
- Users can only modify their own RSVPs.
- The API follows standard REST principles.

---
This document serves as a reference for integrating the RSVP API into your application.