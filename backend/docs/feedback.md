# Feedback API Documentation

## Base URL
`http://127.0.0.1:8000/api/feedback/`

## Overview
This API allows users to submit feedback for events, retrieve feedback, update their feedback, or delete it. Feedback is associated with events and users. Only authenticated users can access these endpoints.

## Authentication
All endpoints require the user to be authenticated. You must include an access token in the header of the request:
```
Authorization: Bearer <your_access_token>
```

## Endpoints

### 1. **List and Create Feedback for an Event**

**Endpoint:**
- `GET /api/feedback/event/<event_id>/`
- `POST /api/feedback/event/<event_id>/`

**Description:** 
- `GET` retrieves all feedback for a specific event.
- `POST` allows a user to submit feedback for an event.
  
**URL Parameters:**
- `event_id` (integer, required): The ID of the event for which feedback is being submitted or retrieved.

**Request Body for POST:**
```json
{
  "message": "Great event, really enjoyed it!"
}
```

**Response:**

GET Response:
```json
[
  {
    "id": 1,
    "event": 5,
    "user": 7,
    "message": "Great event, really enjoyed it!",
    "created_at": "2024-03-04T12:00:00Z",
    "user_details": {
      "username": "john_doe",
      "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/john_doe.jpg"
    }
  }
]
```

POST Response:
```json
{
  "id": 1,
  "event": 5,
  "user": 7,
  "message": "Great event, really enjoyed it!",
  "created_at": "2024-03-04T12:00:00Z",
  "user_details": {
    "username": "john_doe",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/john_doe.jpg"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing or invalid fields.
- `401 Unauthorized`: User is not authenticated.
- `403 Forbidden`: User is the organizer of the event and cannot submit feedback for their own event.

### 2. **Retrieve, Update, and Delete Feedback**

**Endpoint:**
- `GET /api/feedback/<feedback_id>/`
- `PUT /api/feedback/<feedback_id>/`
- `DELETE /api/feedback/<feedback_id>/`

**Description:**
- `GET` retrieves a specific feedback entry.
- `PUT` allows the user to update their own feedback.
- `DELETE` allows the user to delete their own feedback.

**URL Parameters:**
- `feedback_id` (integer, required): The ID of the feedback to retrieve, update, or delete.

**Response for GET:**
```json
{
  "id": 1,
  "event": 5,
  "user": 7,
  "message": "Great event, really enjoyed it!",
  "created_at": "2024-03-04T12:00:00Z",
  "user_details": {
    "username": "john_doe",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/john_doe.jpg"
  }
}
```

**Request Body for PUT (Update):**
```json
{
  "message": "It was an amazing event, would love to attend again!"
}
```

**Response for PUT (Update):**
```json
{
  "id": 1,
  "event": 5,
  "user": 7,
  "message": "It was an amazing event, would love to attend again!",
  "created_at": "2024-03-04T12:00:00Z",
  "user_details": {
    "username": "john_doe",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/john_doe.jpg"
  }
}
```

**Response for DELETE:**
```json
{
  "detail": "Feedback deleted successfully."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid fields.
- `401 Unauthorized`: User is not authenticated.
- `403 Forbidden`: User is not the owner of the feedback.
- `404 Not Found`: The requested feedback does not exist.