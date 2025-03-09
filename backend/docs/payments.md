# Payment API Integration Documentation

This document outlines the integration requirements for the payment processing feature. It details API endpoints, request/response formats, and the payment flow to guide frontend developers with implementation.


## Overview
The payment system supports both free tickets (directly issued) and paid tickets (processed through Stripe). Authentication is required for all endpoints, and the system handles ticket reservations, payment processing, and QR code generation.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/payments/create-payment-intent/` | POST | Create payment intent and redirect to Stripe |
| `/api/payments/verify/` | POST | Verify payment completion |
| `/api/payments/cancel/` | POST | Cancel a reserved ticket |


## API Reference

### Create Payment Intent
Creates a payment intent for paid events or directly issues tickets for free events.

**Endpoint:** `http://127.0.0.1:8000/api/payments/create-payment-intent/`

**Method:** POST

**Authentication:** Required (JWT Token <access_token>)
**Note:**  We dont need to provide the total_amount as backend automatically handle 
**Request Body:**
```json
{
    "event_id": 15,
    "quantity": 10
}
```

**Response (Paid Event):**
```json
{
    "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_a1rlWLd6nBr9ZkAV70h2BnbvOFRTmDfnVLgnaPGUclFX3LbWVkoXDuQUEn#fidkdWxOYHwnPyd1blpxYHZxWjA0VHxmRDY1MEY9SmJmcjE2QldEdGlkM0Nwd1RCMEtoV3FiX3V9XXNDVHVCSDNOb0hySHR0SmN9R0pDd2JMf0NoZE10PDVKZmJIYDZBUXdyfTRHVXBVTVJQNTVSVU1JT2ZURCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
    "session_id": "cs_test_a1rlWLd6nBr9ZkAV70h2BnbvOFRTmDfnVLgnaPGUclFX3LbWVkoXDuQUEn",
    "ticket_id": 31,
    "ticket_code": "6e40a178-b56f-42e2-8264-77af31d21c3d"
}
```

**Response (Free Event):**
```json
{
    "detail": "Successfully purchased tickets",
    "qr_code_data": "[Base64 encoded QR code data]",
    "ticket_id": 30,
    "ticket_code": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
}
```

**Error Responses:**
- 400 Bad Request: When not enough tickets are available
- 404 Not Found: When event doesn't exist
- 400 Bad Request: When Stripe payment fails
- 500 Internal Server Error: For unexpected errors

### Verify Payment
Verifies payment completion after successful Stripe checkout.

**Endpoint:** `http://127.0.0.1:8000/api/payments/verify/`

**Method:** POST

**Authentication:** Required (JWT Token)

**Request Body:**
```json
{
    "session_id": "cs_test_a1rlWLd6nBr9ZkAV70h2BnbvOFRTmDfnVLgnaPGUclFX3LbWVkoXDuQUEn",
    "ticket_id": 31
}
```

**Response (Success):**
```json
{
    "detail": "Payment successful",
    "qr_code_data": "[Base64 encoded QR code data]",
    "ticket_id": 31,
    "ticket_code": "6e40a178-b56f-42e2-8264-77af31d21c3d"
}
```

**Error Responses:**
- 400 Bad Request: Missing parameters or payment not completed
- 403 Forbidden: Unauthorized access to ticket
- 404 Not Found: Ticket or payment not found
- 500 Internal Server Error: For unexpected errors

### Cancel Payment
Cancels a reserved ticket if payment was not completed.

**Endpoint:** `http://127.0.0.1:8000/api/payments/cancel/`

**Method:** POST

**Authentication:** Required (JWT Token)

**Request Body:**
```json
{
    "ticket_id": 31
}
```

**Response (Success):**
```json
{
    "detail": "Payment cancelled"
}
```

**Error Responses:**
- 400 Bad Request: Missing ticket_id or ticket already processed
- 403 Forbidden: Unauthorized access to ticket
- 404 Not Found: Ticket not found
- 500 Internal Server Error: For unexpected errors

## Frontend Implementation Guide

### Creating a Payment

1. Collect event_id and quantity from the user
2. Make a POST request to `/api/payments/create-payment-intent/`
3. For paid events:
   - Redirect the user to the `checkout_url` from the response
   - Store `ticket_id` and `session_id` in local storage or state
4. For free events:
   - Display success message and QR code directly

### After Stripe Checkout

1. When redirected to `http://localhost:5173/payment/success?session_id={SESSION_ID}&ticket_id={TICKET_ID}`:
   - Extract `session_id` and `ticket_id` from URL parameters
   - Call the verification endpoint with these parameters
   - Display the QR code to the user from the response

2. If user cancels or payment fails:
   - User will be redirected to `http://localhost:5173/payment/cancel?ticket_id={TICKET_ID}`
   - Extract `ticket_id` from URL parameters
   - Call the cancel endpoint to release the ticket reservation

