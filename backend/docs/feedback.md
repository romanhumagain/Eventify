# Feedback API Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

## Endpoints

### 1. Submit Feedback for an Event
**Endpoint:**
```
POST /api/feedback/event/{event_id}/
```
**Description:**
User should be logged in to view the feedback
Allows an authenticated user to submit feedback for a specific event.

**Required Fields:**
- `rating` (integer, required): Rating value (1 to 5).
- `comment` (string, optional): Additional comments.

**Example Request:**
```json
{
  "rating": 5,
  "comment": "Great event! Very well organized."
}
```

**Response:**
```json
{
  "id": 1,
  "event": 3,
  "user": 7,
  "rating": 5,
  "comment": "Great event! Very well organized.",
  "created_at": "2024-03-04T12:00:00Z",
  "user_details": {
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": "http://yourdomain.com/media/profile.jpg",
    "username": "johndoe"
  }
}
```

### 2. Get All Feedback for an Event
**Endpoint:**
```
GET /api/feedback/event/{event_id}/
```
**Description:**
Retrieves all feedback related to a specific event.

**Response:**
```json
[
  {
    "id": 1,
    "event": 3,
    "user": 7,
    "rating": 5,
    "comment": "Great event!",
    "created_at": "2024-03-04T12:00:00Z",
    "user_details": {
      "first_name": "John",
      "last_name": "Doe",
      "profile_picture": "http://yourdomain.com/media/profile.jpg",
      "username": "johndoe"
    }
  },
  {
    "id": 2,
    "event": 3,
    "user": 8,
    "rating": 4,
    "comment": "Well planned event!",
    "created_at": "2024-03-04T13:00:00Z",
    "user_details": {
      "first_name": "Jane",
      "last_name": "Smith",
      "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/pp.jpg",
      "username": "janesmith"
    }
  }
]
```

### 3. Get, Update, or Delete a User's Feedback
**Endpoints:**
```
GET /api/feedback/{feedback_id}/
PUT /api/feedback/{feedback_id}/
DELETE /api/feedback/{feedback_id}/
```
**Description:**
- `GET`: Retrieves a specific feedback entry.
- `PUT`: Updates the feedback (only the owner can update).
- `DELETE`: Deletes the feedback (only the owner can delete).

**Required Fields for Update (PUT):**
- `rating` (integer, required): Updated rating value (1 to 5).
- `comment` (string, optional): Updated comment.

**Example Update Request:**
```json
{
  "rating": 4,
  "comment": "The event was good, but could be improved."
}
```

**Example Update Response:**
```json
{
  "id": 1,
  "event": 3,
  "user": 7,
  "rating": 4,
  "comment": "The event was good, but could be improved.",
  "created_at": "2024-03-04T12:00:00Z",
  "user_details": {
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/pp.jpg",
    "username": "johndoe"
  }
}
```

**Example Delete Response:**
```json
{
  "detail": "Feedback deleted successfully."
}
```

## Authentication
- All endpoints require authentication.
- Users must be logged in and provide an authentication token in the `Authorization` header:
```
Authorization: Bearer <your_access_token>
```

## Error Responses
- `400 Bad Request`: If required fields are missing or invalid.
- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the user does not have permission to perform the action.
- `404 Not Found`: If the event or feedback does not exist.

## Notes
- Users cannot submit feedback for their own events.
- Users can update or delete only their own feedback.
- Feedback is ordered by `created_at` in descending order.

