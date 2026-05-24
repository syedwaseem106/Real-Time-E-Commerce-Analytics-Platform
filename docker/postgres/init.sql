-- ==============================================================================
-- POSTGRES WAREHOUSE INITIALIZATION SCHEMA
-- ==============================================================================

-- Create additional schemas to implement staging, warehousing, and analytics division
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Enable UUID extension just in case
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Log completion
SELECT 'Database initialized successfully' as message;
