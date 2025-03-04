# Notifications API Documentation

This documentation provides details on how the frontend can integrate the Notifications API. It includes endpoints, required fields, response structures, and authentication requirements.

## Base URL
```
/api/notifications/
```

## Authentication
All endpoints require authentication using a valid JWT token in the `Authorization` header.

### Headers:
```json
{
  "Authorization": "Bearer <your_access_token>"
}
```

---

## Endpoints

### 1. Get All Notifications
**Endpoint:**
```
GET /api/notifications/
```

**Description:**
Fetches all notifications for the authenticated user, ordered by the latest.

**Response:**
```json
[
  {
    "id": 1,
    "message": "Your event has been approved!",
    "is_read": false,
    "created_at": "2024-03-04T10:15:30Z"
  },
  {
    "id": 2,
    "message": "New comment on your post!",
    "is_read": true,
    "created_at": "2024-03-03T08:45:00Z"
  }
]
```

---

### 2. Mark a Notification as Read
**Endpoint:**
```
PUT /api/notifications/mark-as-read/{id}/
```

**Description:**
Marks a specific notification as read.

**Request Example:**
```
PUT /api/notifications/mark-as-read/1/
```

**Response:**
```json
{
  "detail": "Notification marked as read."
}
```

**Error Response:**
```json
{
  "detail": "Notification not found."
}
```

---

### 3. Mark All Notifications as Read
**Endpoint:**
```
PUT /api/notifications/mark-all-as-read/
```

**Description:**
Marks all unread notifications for the authenticated user as read.

**Response:**
```json
{
  "detail": "All notifications marked as read."
}
```

---

## Field Descriptions

| Field       | Type    | Description |
|-------------|---------|-------------|
| `id`        | Integer | Unique ID of the notification |
| `message`   | String  | Notification message |
| `is_read`   | Boolean | Status of the notification (read/unread) |
| `created_at`| String  | Timestamp when the notification was created |

---

## Notes
- All endpoints require authentication.
- Notifications are user-specific; users can only access their own notifications.
- `is_read` status helps in distinguishing between read and unread notifications.
- The `mark-all-as-read` endpoint updates all unread notifications in bulk.

This documentation should assist the frontend developer in seamlessly integrating the Notifications API into their application.

