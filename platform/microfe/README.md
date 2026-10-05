# MicroFE Platform Contract

This directory defines the platform-level contracts shared by independently deployed Micro Frontends.

## Scope

- Authentication boundary: Secure, HttpOnly browser session cookie.
- API boundary: stable edge-facing /api routes.
- WebSocket boundary: one browser connection with channel subscriptions.
- Domain events: tce.*, stock.*, media.*.

## Non-goals

- No shared business state.
- No shared domain components.
- No Supabase Auth.
- No Supabase Realtime.
- No bearer token in a WebSocket URL.

## Browser contract

The browser JavaScript runtime must not need to read long-lived access or refresh credentials. Authentication is established through the auth service and a Secure + HttpOnly cookie.

WebSocket clients connect through the ws endpoint and authenticate from the established session boundary.
