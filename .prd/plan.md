Act as an expert backend developer. I need to build the complete backend for an inventory management system using Python (FastAPI or Flask) and a MySQL database.

The system has three user roles: "Admin," "Salesperson," and "Warehouse Manager."
The login system is a simple email/password check. **No Multi-Factor Authentication is needed.**

Here are the specific requirements:

**1. Database Schema:**
Generate the SQL schema for the following tables:
* `users`: Must include `id`, `first_name` (nullable), `last_name` (nullable), `email` (unique), `password_hash` (nullable), `phone_number` (nullable), `emergency_contact_number` (nullable), `role` (enum: 'admin', 'salesperson', 'warehouse_manager'), and `status` (enum: 'invited', 'active').
* `inventory_items`: `id`, `name`, `description`, `stock_level` (integer), `low_stock_threshold` (integer).
* `orders`: `id`, `customer_name`, `status` (enum: 'pending', 'processing', 'fulfilled'), `created_at`.
* `order_items`: `id`, `order_id` (foreign key), `item_id` (foreign key), `quantity` (integer).

**2. Database Seeding (Default Admin):**
* Provide a SQL script or a function to run once (`seed.py`) that pre-populates the database.
* This script MUST create the default Admin user.
* The admin's details should be:
    * `email`: 'admin@admin.com'
    * `password_hash`: (the bcrypt hash of '12qwaszx')
    * `first_name`: 'Admin'
    * `last_name`: 'User'
    * `role`: 'admin'
    * `status`: 'active'

**3. API Endpoints & Logic:**

* **Auth:**
    * `POST /auth/register`: (Public) This is for Salespersons/Warehouse Managers to complete their signup.
        1.  It receives: `first_name`, `last_name`, `email`, `phone_number`, `emergency_contact_number`, and `password`.
        2.  **Crucial Logic:** Check the `users` table. Find a user where `email` matches AND `status` is 'invited'.
        3.  If no such user exists, return a 403 Forbidden error: "This email is not authorized to register."
        4.  If the user exists:
            * Validate the password (min 8 chars, upper, lower, num, special) and phone numbers (10-14 digits).
            * Hash the new password using `bcrypt`.
            * Update the *existing* user row with all the new details (`first_name`, `last_name`, `password_hash`, `phone_number`, `emergency_contact_number`).
            * Change the user's `status` from 'invited' to 'active'.
            * Return a success message or a login token.
    * `POST /auth/login`: (Public)
        1.  Receives `email` and `password`.
        2.  Checks for a user with matching `email` and `status` = 'active'.
        3.  Verify the password using `bcrypt.checkpw`.
        4.  If valid, return a JWT token containing `user_id` and `role`.

* **User Management (Admin Only - Requires Admin JWT):**
    * `POST /users/invite`:
        1.  Receives: `email` and `role` (must be 'salesperson' or 'warehouse_manager').
        2.  Logic: Creates a *new* row in the `users` table with the given `email` and `role`, and sets `status` to 'invited'. All other fields (`password_hash`, `first_name`, etc.) should be `NULL`.
    * `GET /users`: Lists all users (both 'invited' and 'active').
    * `DELETE /users/{user_id}`: Deletes a user.

* **Inventory (Role-Protected):**
    * `GET /inventory`: (All authenticated roles) Lists all inventory items.
    * `POST /inventory`: (Admin, Warehouse Manager only) Adds a new inventory item.
    * `PUT /inventory/{item_id}`: (Admin, Warehouse Manager only) Updates an item's details or stock level.

* **Orders (Role-Protected):**
    * `POST /orders`: (Salesperson only) Creates a new customer order.
        1.  **Validation:** Check if `quantity` requested is available in `inventory_items.stock_level`. If not, reject the order.
        2.  **Transaction:** If stock is available, *atomically* (in a single database transaction) create the `orders` record AND decrease the `stock_level` in the `inventory_items` table.
    * `GET /orders/{order_id}`: (All authenticated roles) Gets details for a single order.
    * `PUT /orders/{order_id}/status`: (Warehouse Manager, Admin only) Updates an order's status.

**4. Validation & Security:**
* **RBAC:** All endpoints (except auth) must be protected by JWT and strictly enforce role permissions.
* **Input Validation:**
    * **Password:** On registration, enforce: min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char.
    * **Email:** Validate format (e.g., `user@domain.com` or `user@domain.org`).
    * **Phone Numbers:** Validate as 10-14 digits only.
* **Password Hashing:** Use `bcrypt` for all password hashing and verification.
* **Data Safety:** Provide a simple bash script (e.g., `backup.sh`) that uses `mysqldump` to create an automated daily backup of the database.