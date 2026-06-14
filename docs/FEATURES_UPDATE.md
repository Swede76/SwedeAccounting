# SwedeAccounting - Features Update

## New Features Added

### 1. Customer Management
- Create, read, update, delete customers
- Store customer details: name, contact info, address, tax ID
- Track active/inactive customers
- **Endpoints:**
  - `GET /api/invoices/customers` - List all customers
  - `POST /api/invoices/customers` - Create customer
  - `GET /api/invoices/customers/{id}` - Get customer details
  - `PUT /api/invoices/customers/{id}` - Update customer
  - `DELETE /api/invoices/customers/{id}` - Deactivate customer

### 2. Payroll Management
- Employee management (hire, track, manage)
- Time entry tracking (hours worked, overtime)
- Automated payslip generation
- Salary calculations with tax and deductions
- Payslip approval and payment workflow
- **Endpoints:**
  - `GET /api/invoices/payroll/employees` - List employees
  - `POST /api/invoices/payroll/employees` - Add employee
  - `POST /api/invoices/payroll/time-entries` - Record time
  - `POST /api/invoices/payroll/payslips` - Generate payslip
  - `POST /api/invoices/payroll/payslips/{id}/approve` - Approve payslip
  - `POST /api/invoices/payroll/payslips/{id}/pay` - Pay employee

### 3. Bank Reconciliation
- Multiple bank account management
- Record debit and credit transactions
- Mark transactions as reconciled
- Track unreconciled transactions
- Automatic balance updates
- **Endpoints:**
  - `GET /api/invoices/bank/accounts` - List bank accounts
  - `POST /api/invoices/bank/accounts` - Add bank account
  - `POST /api/invoices/bank/transactions` - Record transaction
  - `POST /api/invoices/bank/reconcile/{id}` - Mark as reconciled
  - `GET /api/invoices/bank/accounts/{id}/unreconciled` - Unreconciled items

### 4. Project Management
- Create and track projects
- Budget management and tracking
- Cost allocation by type (labor, material, equipment)
- Attach invoices to projects
- Project status tracking
- **Endpoints:**
  - `GET /api/invoices/projects` - List projects
  - `POST /api/invoices/projects` - Create project
  - `GET /api/invoices/projects/{id}` - Get project details
  - `POST /api/invoices/projects/{id}/costs` - Add cost
  - `POST /api/invoices/projects/{id}/attach-invoice/{invoice_id}` - Link invoice

### 5. Tax & VAT Management
- VAT rate configuration
- VAT return generation
- Track VAT on sales and purchases
- Calculate net VAT liability
- VAT return submission workflow
- **Endpoints:**
  - `GET /api/invoices/tax/vat-rates` - List VAT rates
  - `POST /api/invoices/tax/vat-rates` - Add VAT rate
  - `POST /api/invoices/tax/vat-returns` - Create VAT return
  - `GET /api/invoices/tax/vat-returns` - List VAT returns
  - `POST /api/invoices/tax/vat-returns/{id}/submit` - Submit return

### 6. JWT Authentication
- Token-based authentication
- Protected route decorator
- User identity verification
- Claims support
- **Features:**
  - Secure API endpoints
  - Token generation and validation
  - User context in requests

### 7. Audit Logging
- Track all user actions
- Log resource changes (old and new values)
- Store IP address and user agent
- Comprehensive audit trail
- **Tracked Actions:**
  - Create, Update, Delete operations
  - User login/logout
  - Sensitive operations

## Database Schema

New tables added:
- `customers` - Customer information
- `employees` - Employee data
- `time_entries` - Time tracking
- `payslips` - Payroll records
- `bank_accounts` - Bank account details
- `bank_transactions` - Bank transaction records
- `projects` - Project information
- `project_costs` - Project cost tracking
- `project_invoices` - Invoice-to-project mapping
- `vat_rates` - VAT rate configuration
- `vat_returns` - VAT return filings
- `audit_logs` - Audit trail

## Next Steps

1. Implement JWT token generation in auth routes
2. Add request validation with Pydantic
3. Create comprehensive error handling
4. Add email notifications
5. Implement report export (PDF, Excel)
6. Add file upload for receipts and invoices
7. Create webhooks for integrations
8. Add API rate limiting
9. Implement data backup and recovery
10. Add multi-currency support
