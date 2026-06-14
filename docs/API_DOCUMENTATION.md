# SwedeAccounting API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
TBD - JWT authentication to be implemented

## Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login

### Invoices
- `GET /invoices/` - Get all invoices
- `GET /invoices/{id}` - Get specific invoice
- `POST /invoices/` - Create new invoice
- `PUT /invoices/{id}` - Update invoice
- `DELETE /invoices/{id}` - Delete invoice

### Bookkeeping
- `GET /bookkeeping/accounts` - Get all accounts
- `POST /bookkeeping/accounts` - Create new account
- `GET /bookkeeping/transactions` - Get all transactions
- `POST /bookkeeping/transactions` - Create new transaction

### Reporting
- `GET /reporting/balance-sheet` - Generate balance sheet
- `GET /reporting/income-statement` - Generate income statement

## Response Format
All responses are in JSON format.

### Success Response
```json
{
  "data": {...},
  "message": "Success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "code": 400
}
```
