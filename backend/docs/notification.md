# Notifications API Documentation

This documentation provides details on how the frontend can integrate the Notifications API. It includes endpoints, required fields, response structures, and authentication requirements.

# Notification API Documentation

## Endpoints Overview

| Endpoint                                      | Method | Description                                                   |
|-----------------------------------------------|--------|---------------------------------------------------------------|
| `/api/notifications/`                         | GET    | Retrieve all notifications for the authenticated user with latest details at first.        |
| `/api/notifications/mark-all-as-read/`        | PUT    | Mark all unread notifications as read for the authenticated user. |
| `/api/notifications/mark-as-read/<id>/`       | PUT    | Mark a specific notification as read for the authenticated user by providing notification id. |

---

## Retrieve Notifications

### Endpoint
`GET /api/notifications/`


`GET /api/notifications/?is_read=false` **Note:** This endpoint will provide all the notification for the user which are not read. This helps to count the unread notification. 

### Query Parameters
| Parameter  | Type    | Required | Description                               |
|------------|---------|----------|-------------------------------------------|
| `is_read`  | boolean | No       | Filter notifications by read status (`true` or `false`) |

### Headers
| Key           | Value                         |
|---------------|-------------------------------|
| Authorization | Bearer `<access_token>`        |

### Response
```json
[
  {
    "id": 1,
    "event": 10,  
    "message": "Your event 'Tech Conference' is starting soon.",
    "is_read": false,
    "created_at": "2025-03-08T10:30:00Z",
    "event_details": {
            "banner": "http://127.0.0.1:8000/media/events/Screenshot_459_6hZ2a2D.png",
            "title": "Event Title"
        }
  },
  {
    "id": 2,
    "event": 11,
    "message": "New ticket assigned to you for 'Project Update'.",
    "is_read": true,
    "created_at": "2025-03-08T09:00:00Z",
    "event_details": {
            "banner": "http://127.0.0.1:8000/media/events/Screenshot_459_6hZ2a2D.png",
            "title": "Event Title"
        }
  }
]


