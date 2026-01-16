# InvoiceFlow

## Overview

InvoiceFlow is a Django-based invoicing and financial management application designed for small businesses and freelancers. It provides functionality for creating and managing invoices, tracking clients, processing payments through multiple providers (Stripe and Paystack), and monitoring sales and expenses. The application includes user authentication, role-based access control, automated payment reminders, and PDF invoice generation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Django 5.2+**: The application is built on Django, using its MVT (Model-View-Template) architecture
- **Python**: Primary backend language with standard Django project structure

### Application Structure
The project is organized into multiple Django apps, each handling a specific domain:

| App | Purpose |
|-----|---------|
| `accounts` | User authentication, registration, role-based access (admin/standard users) |
| `invoices` | Invoice and client management, PDF generation |
| `payments` | Payment processing, webhook handling, user payment settings |
| `sales` | Sales tracking and analytics |
| `expenses` | Expense tracking and analytics |
| `dashboard` | Dashboard views and aggregated data display |
| `settings` | Application settings management |
| `core` | Main Django project configuration |

### Database Models
- **User**: Extended Django AbstractUser with role-based permissions (admin/standard)
- **Client**: Customer information linked to users
- **Invoice**: Invoice records with status tracking (draft/sent/paid/overdue)
- **InvoiceItem**: Line items for invoices with quantity and pricing
- **Payment**: Payment transaction records from Stripe/Paystack
- **UserPaymentSettings**: Per-user payment gateway credentials and bank details
- **Sale**: Sales transaction records
- **Expense**: Expense records

### Authentication & Authorization
- Django's built-in authentication system with custom User model
- Role-based access using custom `admin_required` decorator
- Password reset functionality via Django's auth views
- Session-based authentication

### Frontend Architecture
- Server-rendered templates using Django's template engine
- Light/dark theme toggle with localStorage persistence
- Chart.js for data visualization in dashboards
- Custom CSS with CSS variables for theming
- Static files served via WhiteNoise

## External Dependencies

### Payment Gateways
- **Stripe**: Credit card payment processing with checkout sessions and webhooks
- **Paystack**: Alternative payment provider (popular in Africa) with webhook support

### Email Service
- **SendGrid**: Transactional email delivery for invoices, reminders, and confirmations

### PDF Generation
- **xhtml2pdf**: HTML to PDF conversion for invoice documents (referenced in utils but not in requirements)

### Database
- **PostgreSQL**: Primary database via psycopg2-binary and dj-database-url
- Database URL configuration through environment variables

### Environment Configuration
Required environment variables:
- `DJANGO_SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode flag
- `DJANGO_ALLOWED_HOSTS`: Comma-separated allowed hosts
- `DATABASE_URL`: PostgreSQL connection string
- `STRIPE_SECRET_KEY`: Stripe API key
- `SENDGRID_API_KEY`: SendGrid API key

### Production Dependencies
- **Gunicorn**: WSGI HTTP server for production
- **WhiteNoise**: Static file serving for production
- **python-dotenv**: Environment variable loading from .env files