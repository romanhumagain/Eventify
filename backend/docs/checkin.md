# Ticket Check-In API

## Endpoint
`POST api/tickets/booking/check-in/`

## Description
This API is used by event organizers to validate and check-in users' tickets using QR code data.

## Permissions
- **Organizer Permission**: Only event organizers can access this endpoint. Users without the `is_organizer` flag will receive a **403 Forbidden** response.

## Request Data
The request body should contain the following data:
```json
{
  "qr_code_data": "<QR_CODE_DATA>"
}


Response
OK (Success)

{
  "detail": "Ticket successfully checked in",
  "ticket_info": {
    "event_name": "Event Title",
    "ticket_code": "<TICKET_CODE>",
    "ticket_quantity": 10,
    "ticket_status": "paid",
    "purchase_date": "<PURCHASE_DATE>",
    "attendee_name": "username",
    "check_in_time": "<CHECK_IN_TIME>"
  }
}


Bad Request (Invalid QR Code)
{
  "detail": "Invalid QR code"
}


Bad Request (QR Code Data Missing)
{
  "detail": "QR code data is required"
}


Bad Request (Event Date Passed)
{
  "detail": "This event has already passed"
}


Bad Request (Ticket Already Checked In)
{
  "detail": "Ticket already checked in",
  "checked_in_time": "<CHECK_IN_TIME>"
}


Bad Request (Ticket Status Invalid for Check-In)
{
  "detail": "Ticket status is <TICKET_STATUS>, which is not valid for check-in",
  "valid_statuses": ["paid"]
}

Forbidden (User is not Organizer of the Event)
{
  "detail": "You do not have permission for ticket verification"
}


Forbidden (Organizer does not match the Event's Organizer)
{
  "detail": "You do not have permission to verify this ticket."
}


How it Works:
Authentication: The user must be logged in as an organizer.
QR Code Validation: The qr_code_data sent in the request is validated against the BookedTicket model.
Event Validation: The event associated with the ticket is checked to ensure it has not already passed.
Ticket Status Check: Only tickets with a "paid" status can be checked in.
Check-In: If all validations pass, the ticket is marked as checked in, and the check-in time is recorded.
Response: A detailed response containing ticket information and check-in time is returned.