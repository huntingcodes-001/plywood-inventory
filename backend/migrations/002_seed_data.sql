-- Migration 002: Seed initial data
-- Creates default admin user with bcrypt hashed password
-- Includes validation for existing data to prevent duplicate seeding

-- Insert default admin user if not exists
-- Password: 'admin123!' (meets complexity requirements)
-- Bcrypt hash with 12 rounds for security
INSERT INTO users (
    first_name,
    last_name,
    email,
    password_hash,
    phone_number,
    emergency_contact_number,
    role,
    status
)
SELECT 
    'System',
    'Administrator',
    'admin@admin.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.F5e', -- admin123!
    '1234567890',
    '1234567890',
    'admin',
    'active'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@admin.com'
);

-- Verify the admin user was created
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE email = 'admin@admin.com' AND role = 'admin') THEN
        RAISE NOTICE 'Default admin user created successfully';
    ELSE
        RAISE NOTICE 'Default admin user already exists or creation failed';
    END IF;
END $$;