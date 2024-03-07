-- Create the main and test databases
CREATE DATABASE geo_stac_db;
CREATE DATABASE test_geo_stac_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE geo_stac_db TO "postgres";
GRANT ALL PRIVILEGES ON DATABASE test_geo_stac_db TO "postgres";

-- Connect to the main database and create the PostGIS extension
\c geo_stac_db;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Connect to the test database and create the PostGIS extension
\c test_geo_stac_db;
CREATE EXTENSION IF NOT EXISTS postgis;
