# Design Document

## Overview

The inventory management backend is a FastAPI-based REST API that provides secure, role-based access to inventory and order management functionality. The system integrates with Supabase PostgreSQL for data persistence and implements JWT-based authentication with bcrypt password hashing.

The backend serves as a complete replacement for the current localStorage-based data management in the React frontend, providing proper data persistence, security, and multi-user support.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    HTTP/JSON     ┌─────────────────┐    SQL/TCP    ┌─────────────────┐
│   React Client  │ ◄──────────────► │  FastAPI Server │ ◄────────────► │ Supabase PostgreSQL │
│   (Frontend)    │                  │   (Backend)     │                │   (Database)    │
└─────────────────┘                  └─────────────────┘                └─────────────────┘
```

### Technology Stack

- **API Framework**: FastAPI (Python 3.9+)
- **Database**: Supabase PostgreSQL
- **Authentication**: JWT tokens with bcrypt password hashing
- **Database Client**: Supabase Python client
- **Validation**: Pydantic models
- **CORS**: FastAPI CORS middleware for React frontend integration

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration and environment variables
│   ├── database.py            # Supabase connection and utilities
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py     # JWT token creation and validation
│   │   ├── password.py        # Password hashing utilities
│   │   └── dependencies.py    # Authentication dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User Pydantic models
│   │   ├── inventory.py      # Inventory Pydantic models
│   │   └── order.py          # Order Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── users.py          # User management endpoints
│   │   ├── inventory.py      # Inventory management endpoints
│   │   └── orders.py         # Order management endpoints
│   └── utils/
│       ├── __init__.py
│       └── validators.py     # Input validation utilities
├── migrations/
│   ├── 001_create_tables.sql # Database schema creation
│   └── 002_seed_data.sql     # Default admin user creation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # Setup and deployment instructions
```

## Components and Interfaces

### 1. Authentication System

**JWT Handler (`auth/jwt_handler.py`)**
- Creates JWT tokens containing user_id and role
- Validates and decodes JWT tokens
- Handles token expiration (24-hour default)

**Password Manager (`auth/password.py`)**
- Hashes passwords using bcrypt with salt rounds
- Verifies passwords against stored hashes
- Enforces password complexity requirements

**Auth Dependencies (`auth/dependencies.py`)**
- `get_current_user()`: Extracts user from JWT token
- `require_admin()`: Ensures admin role access
- `require_warehouse_manager_or_admin()`: Ensures warehouse/admin access
- `require_salesperson()`: Ensures salesperson access

### 2. Database Layer

**Supabase Connection (`database.py`)**
- Initializes Supabase client with project URL and service key
- Provides connection health checks
- Handles connection pooling and error recovery

**Database Schema**
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    phone_number VARCHAR(20),
    emergency_contact_number VARCHAR(20),
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'salesperson', 'warehouse_manager')),
    status VARCHAR(20) NOT NULL DEFAULT 'invited' CHECK (status IN ('invited', 'active')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inventory items table
CREATE TABLE inventory_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stock_level INTEGER NOT NULL DEFAULT 0,
    low_stock_threshold INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'fulfilled')),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    item_id UUID REFERENCES inventory_items(id),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 3. API Endpoints

**Authentication Routes (`/auth`)**
- `POST /auth/login`: User authentication with email/password
- `POST /auth/register`: Complete user registration for invited users

**User Management Routes (`/users`) - Admin Only**
- `POST /users/invite`: Create user invitation
- `GET /users`: List all users (invited and active)
- `DELETE /users/{user_id}`: Delete user

**Inventory Routes (`/inventory`)**
- `GET /inventory`: List all inventory items (all roles)
- `POST /inventory`: Create inventory item (admin, warehouse_manager)
- `PUT /inventory/{item_id}`: Update inventory item (admin, warehouse_manager)

**Order Routes (`/orders`)**
- `POST /orders`: Create new order (salesperson only)
- `GET /orders/{order_id}`: Get order details (all roles)
- `PUT /orders/{order_id}/status`: Update order status (admin, warehouse_manager)

## Data Models

### User Models

```python
class UserRole(str, Enum):
    ADMIN = "admin"
    SALESPERSON = "salesperson"
    WAREHOUSE_MANAGER = "warehouse_manager"

class UserStatus(str, Enum):
    INVITED = "invited"
    ACTIVE = "active"

class UserCreate(BaseModel):
    email: EmailStr
    role: UserRole

class UserRegister(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., regex=r'^\d{10,14}$')
    emergency_contact_number: str = Field(..., regex=r'^\d{10,14}$')
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    emergency_contact_number: Optional[str]
    role: UserRole
    status: UserStatus
    created_at: datetime
```

### Inventory Models

```python
class InventoryItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    stock_level: int = Field(..., ge=0)
    low_stock_threshold: int = Field(..., ge=0)

class InventoryItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    stock_level: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)

class InventoryItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    stock_level: int
    low_stock_threshold: int
    created_at: datetime
    updated_at: datetime
```

### Order Models

```python
class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FULFILLED = "fulfilled"

class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    items: List[OrderItemCreate] = Field(..., min_items=1)

class OrderItemResponse(BaseModel):
    id: str
    item_id: str
    item_name: str
    quantity: int

class OrderResponse(BaseModel):
    id: str
    customer_name: str
    status: OrderStatus
    items: List[OrderItemResponse]
    created_by: str
    created_at: datetime
    updated_at: datetime
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful operations
- `201 Created`: Successful resource creation
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server errors

### Error Response Format
```python
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
```

### Custom Exception Handlers
- `AuthenticationError`: Invalid credentials or tokens
- `AuthorizationError`: Insufficient role permissions
- `ValidationError`: Input validation failures
- `DatabaseError`: Supabase connection or query errors
- `BusinessLogicError`: Domain-specific errors (e.g., insufficient stock)

## Testing Strategy

### Unit Tests
- Authentication utilities (JWT, password hashing)
- Input validation functions
- Database query functions
- Business logic functions

### Integration Tests
- API endpoint functionality
- Database operations with test data
- Authentication and authorization flows
- Error handling scenarios

### Test Database
- Use separate Supabase project for testing
- Automated test data setup and teardown
- Mock external dependencies where appropriate

## Security Considerations

### Authentication Security
- JWT tokens with 24-hour expiration
- Secure password hashing with bcrypt (12 rounds)
- Password complexity validation
- Rate limiting on authentication endpoints

### Authorization Security
- Role-based access control on all protected endpoints
- JWT token validation on every request
- Principle of least privilege for role permissions

### Data Security
- Input validation and sanitization
- Parameterized queries to prevent SQL injection
- HTTPS enforcement in production
- Sensitive data exclusion from logs

### Environment Security
- Environment variables for all secrets
- Supabase service key protection
- CORS configuration for frontend domain only

## Performance Considerations

### Database Performance
- Supabase connection pooling
- Indexed columns for frequent queries (email, order status)
- Efficient query patterns with minimal N+1 queries

### API Performance
- Pydantic model validation caching
- Response compression for large datasets
- Pagination for list endpoints

### Caching Strategy
- JWT token validation caching
- User role information caching
- Inventory data caching for read-heavy operations

## Deployment and Configuration

### Environment Variables
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173,https://your-frontend-domain.com
```

### Production Deployment
- Docker containerization
- Health check endpoints
- Logging configuration
- Error monitoring integration
- Automated database migrations