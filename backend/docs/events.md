# Event Management System API Documentation

This document provides detailed information about the Event Management System API endpoints, request/response formats, and usage guidelines for frontend integration.

## Base URL

All endpoints are prefixed with: `/api/events/`

## Authentication

## Table of Contents

- [Important Notes for Frontend Integration](#important-notes-for-frontend-integration)

## API Endpoints Overview

| Endpoint                          | Method | Description                                    | Authentication Required |
|-----------------------------------|--------|------------------------------------------------|------------------------|
| `/api/events/categories/`         | GET    | List all event categories                      | No                     |
| `/api/events/`                    | GET    | List all approved events with filtering options| No                     |
| `/api/events/`                    | POST   | Create a new event                             | Yes                    |
| `/api/events/{event_id}/`               | GET    | Retrieve detailed information about an event   | No                     |
| `/api/events/{event_id}/`               | PUT    | Update an event                                | Yes (Owner only)       |
| `/api/events/{event_id}/`               | DELETE | Delete an event                                | Yes (Owner only)       |
| `/api/events/my-events/`          | GET    | List events created by the authenticated user  | Yes                    |
| `/api/events/my-bookings/`        | GET    | List events booked by the authenticated user   | Yes                    |
| `/api/events/saved/`              | GET    | List events saved by the authenticated user    | Yes                    |
| `/api/events/toggle-save/{event_id}/`   | POST   | Save or unsave an event                   | Yes                    |
| `/api/events/send-invitation/`          |POST    | Send invitation                           | YES                      |


### Request Body for `/api/events/send-invitation/`

```json
{
  "event_id": 17,
  "email": [
    "email1@gmail.com",
    "email2@gmail.com",
    "email3@gmail.com"
  ]
}



## Event Categories

### List All Categories

Retrieves a list of all event categories.

- **URL**: `/api/events/categories/`
- **Method**: `GET`
- **Authentication Required**: No

#### Response

```json
[
  {
    "id": 1,
    "name": "Conference"
  },
  {
    "id": 2,
    "name": "Workshop"
  },
  {
    "id": 3,
    "name": "Networking Event"
  }
]
```

## Events

### List All Events

Retrieves a list of all approved events with filtering options.

- **URL**: `/api/events/`
- **Method**: `GET`
- **Authentication Required**: No

#### Query Parameters
- GET /api/events/?search=conference&category=Workshop&date=today&event_type=remote&is_free=true&venue=Kathmandu&status=upcoming

| Parameter  | Description                                          | Example Value            |
|------------|------------------------------------------------------|--------------------------|
| search     | Search for events by title                           | conference               |
| category   | Filter events by category name                       | Workshop                 |
| date       | Filter events by date                                | today, tomorrow, this_week, next_week, this_month |
| event_type | Filter events by type                                | remote, physical         |
| is_free    | Filter events by whether they are free               | true, false              |
| venue      | Filter events by venue                               | Kathmandu                 |
| status     | Filter events by status                              | upcoming, active, expired|

#### Response

```json
[
  {
    "id": 1,
    "banner": "http://example.com/media/events-banner/event1.jpg",
    "title": "Tech Conference 2025",
    "subtitle": "Future of AI",
    "event_type": "physical",
    "is_free": false,
    "ticket_price": "50.00",
    "start_date": "2025-03-20T10:00:00Z",
    "end_date": "2025-03-20T18:00:00Z",
    "booking_deadline": "2025-03-19T23:59:59Z",
    "venue": "Convention Center, New York",
    "category_details": {
      "id": 1,
      "name": "Conference"
    },
    "tickets_available": 150,
    "created_at": "2025-02-15T14:30:00Z",
    "updated_at": "2025-02-15T14:30:00Z",
    "organizer": {
      "id": 5,
      "profile_picture": "http://example.com/media/profile_pics/user5.jpg",
      "username": "event_organizer"
    },
    "is_upcoming": true,
    "is_active": false,
    "is_expired": false,
    "attendees_count": 0,
    "is_saved": false
  }
]
```

## My Events

### List My Events

Retrieves events created by the authenticated user.

- **URL**: `/api/events/my-events/`
- **Method**: `GET`
- **Authentication Required**: Yes

#### Query Parameters

| Parameter  | Description                       | Example Value |
|------------|-----------------------------------|---------------|
| is_approved| Filter by approval status         | true, false   |

#### Response

```json
[
  {
    "id": 1,
    "banner": "http://example.com/media/events-banner/event1.jpg",
    "title": "Tech Conference 2025",
    "subtitle": "Future of AI",
    "event_type": "physical",
    "is_free": false,
    "ticket_price": "50.00",
    "start_date": "2025-03-20T10:00:00Z",
    "end_date": "2025-03-20T18:00:00Z",
    "booking_deadline": "2025-03-19T23:59:59Z",
    "venue": "Convention Center, New York",
    "category_details": {
      "id": 1,
      "name": "Conference"
    },
    "tickets_available": 150,
    "created_at": "2025-02-15T14:30:00Z",
    "updated_at": "2025-02-15T14:30:00Z",
    "organizer": {
      "id": 5,
      "profile_picture": "http://example.com/media/profile_pics/user5.jpg",
      "username": "event_organizer"
    },
    "is_upcoming": true,
    "is_active": false,
    "is_expired": false,
    "attendees_count": 50,
    "is_saved": false
  }
]
```
## View Event Details
Retrieve detailed information about an event

### As an Organizer
- If you are the organizer of this event, you can view attendees.
- You cannot view the attendees of other events.

### As a User
- If you have previously booked this event, you can view your bookings.
- You cannot view bookings of other users.

- **URL**: `/api/events/{event_id}/`
- **Method**: `GET`
- **Authentication Required**: Yes

#### Response

``` json
{
    "id": 17,
    "banner": "http://127.0.0.1:8000/media/events/Screenshot_459_7JuuuiC.png",
    "title": "Django & React Workshop IV",
    "subtitle": "Learn to build full-stack applications",
    "details": "Join us for an exciting workshop on building web apps with Django and React.",
    "event_type": "physical",
    "is_free": true,
    "ticket_price": "0.00",
    "start_date": "2025-03-15T10:00:00Z",
    "end_date": "2025-03-18T14:00:00Z",
    "booking_deadline": "2025-04-18T14:00:00Z",
    "venue": "Kathmandu",
    "category_details": {
        "id": 6,
        "name": "Technology"
    },
    "total_tickets": 100,
    "tickets_available": 93,
    "created_at": "2025-03-08T10:36:13.337326Z",
    "updated_at": "2025-03-10T17:01:50.269641Z",
    "organizer": {
        "id": 15,
        "profile_picture": null,
        "username": "johnny"
    },
    "is_upcoming": true,
    "is_active": false,
    "is_expired": false,
    "attendees": {
        "attendees_count": 20,
        "attendees_detail": [
            {
                "user_id": 16,
                "username": "romanhumagain",
                "ticket_count": 5,
                "is_checked_in": false
            },
            {
                "user_id": 16,
                "username": "romanhumagain",
                "ticket_count": 10,
                "is_checked_in": true
            },
            {
                "user_id": 16,
                "username": "romanhumagain",
                "ticket_count": 5,
                "is_checked_in": true
            }
        ]
    },
    "is_saved": true,
    "feedbacks": [],
    "bookings": [
        {
            "booking_id": 24,
            "qr_code_data": "6cc00d29eba5b21592749998640a9b679ae2fe0fdf20ba0a16c55b86c7459c49",
            "booked_at": "2025-03-10T20:05:04.585550Z",
            "is_checked_in": false
        }
    ]
}

```


## Saved Events

### List Saved Events

Retrieves events saved by the authenticated user.

- **URL**: `/api/events/saved/`
- **Method**: `GET`
- **Authentication Required**: Yes

#### Query Parameters

Supports all the same filtering options as the main event list endpoint.

#### Response

```json
[
  {
    "id": 1,
    "saved_at": "2025-03-10T15:45:00Z",
    "event_details": {
      "id": 3,
      "banner": "http://example.com/media/events-banner/event3.jpg",
      "title": "Data Science Summit",
      "subtitle": "Big Data Analytics",
      "event_type": "remote",
      "is_free": true,
      "ticket_price": "0.00",
      "start_date": "2025-04-15T09:00:00Z",
      "end_date": "2025-04-15T17:00:00Z",
      "booking_deadline": "2025-04-14T23:59:59Z",
      "venue": "Online",
      "category_details": {
        "id": 2,
        "name": "Webinar"
      },
      "tickets_available": 500,
      "created_at": "2025-03-01T10:00:00Z",
      "updated_at": "2025-03-01T10:00:00Z",
      "organizer": {
        "id": 7,
        "profile_picture": "http://example.com/media/profile_pics/user7.jpg",
        "username": "data_scientist"
      },
      "is_upcoming": true,
      "is_active": false,
      "is_expired": false,
      "attendees_count": 0,
      "is_saved": true
    }
  }
]
```

### Toggle Save Event

Save or unsave an event for the authenticated user.

- **URL**: `/api/events/toggle-save/{event_id}/`
- **Method**: `POST`
- **Authentication Required**: Yes

#### Response (When Saving)

```json
{
  "detail": "Event saved successfully."
}
```

#### Response (When Unsaving)

```json
{
  "detail": "Event unsaved successfully."
}
```

## My Bookings

### List My Bookings

Retrieves events booked by the authenticated user.

- **URL**: `/api/events/my-bookings/`
- **Method**: `GET`
- **Authentication Required**: Yes

#### Response

```json
[
  {
    "id": 2,
    "banner": "http://example.com/media/events-banner/event2.jpg",
    "title": "Python Workshop",
    "subtitle": "Advanced Django",
    "event_type": "physical",
    "is_free": false,
    "ticket_price": "30.00",
    "start_date": "2025-03-25T13:00:00Z",
    "end_date": "2025-03-25T17:00:00Z",
    "booking_deadline": "2025-03-24T23:59:59Z",
    "venue": "Tech Hub, San Francisco",
    "category_details": {
      "id": 3,
      "name": "Workshop"
    },
    "tickets_available": 40,
    "created_at": "2025-02-20T09:15:00Z",
    "updated_at": "2025-02-20T09:15:00Z",
    "organizer": {
      "id": 6,
      "profile_picture": "http://example.com/media/profile_pics/user6.jpg",
      "username": "django_expert"
    },
    "is_upcoming": true,
    "is_active": false,
    "is_expired": false,
    "attendees_count": 0,
    "is_saved": false
  }
]
```


## Data Models

### Event Model Fields

| Field            | Type                | Description                             | Required | Default |
|------------------|---------------------|-----------------------------------------|----------|---------|
| organizer        | ForeignKey (User)   | User who created the event             | Yes      | -       |
| category         | ForeignKey          | Event category                         | No       | null    |
| banner           | ImageField          | Event banner image                     | Yes      | -       |
| title            | CharField           | Event title                            | Yes      | -       |
| subtitle         | CharField           | Event subtitle                         | Yes      | -       |
| details          | TextField           | Detailed description                   | No       | null    |
| event_type       | CharField           | Physical or Remote                     | Yes      | -       |
| venue            | CharField           | Event location (required for physical) | No       | null    |
| start_date       | DateTimeField       | Event start date and time              | Yes      | -       |
| end_date         | DateTimeField       | Event end date and time                | Yes      | -       |
| booking_deadline | DateTimeField       | Deadline for booking tickets           | No       | end_date|
| total_tickets    | PositiveIntegerField| Total number of available tickets      | No       | null    |
| is_free          | BooleanField        | Whether the event is free              | No       | false   |
| ticket_price     | DecimalField        | Price per ticket                       | No       | 0.00    |
| is_approved      | BooleanField        | Whether the event is approved          | No       | false   |
| created_at       | DateTimeField       | When the event was created             | Auto     | now     |
| updated_at       | DateTimeField       | When the event was last updated        | Auto     | now     |

## Important Notes for Frontend Integration

1. **Event Creation**:
   - All new events start with `is_approved` set to `false`
   - Only approved events appear in the main event listing
   - Event creators can see their unapproved events in the "My Events" list with the filter `is_approved=false`

2. **Dates and Timezones**:
   - All dates are in ISO 8601 format with UTC timezone (e.g., `2025-03-20T10:00:00Z`)
   - Frontend should handle proper display based on user's local timezone

3. **Image Handling**:
   - Banner images must be sent as files using `multipart/form-data`
   - Use form data for creating and updating events with images

4. **Event Status**:
   - `is_upcoming`: Event start date is in the future
   - `is_active`: Current time is between start and end dates
   - `is_expired`: Event end date is in the past

5. **Validation Rules**:
   - End date must be after start date
   - Booking deadline must be before end date
   - Events with the same title, start date, and event type for the same organizer are not allowed

6. **Deletion Restrictions**:
   - Events cannot be deleted if they have been booked by users

7. **Permissions**:
   - Only event owners can update or delete their events
   - Only superusers can manage event categories
   - Authentication is required for creating events, saving events, and viewing bookings