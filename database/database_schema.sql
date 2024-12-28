-- Author: Tariq Ahmed
-- Email: t.ahmed@stride.ae
-- Organization: Stride Information Technology

-- This SQL script creates the necessary database tables and indexes for the project.

-- Enable the ltree extension for hierarchical queries
CREATE EXTENSION IF NOT EXISTS ltree;

-- Create the DOCUMENT table
CREATE TABLE DOCUMENT (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the SECTION table
CREATE TABLE SECTION (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES DOCUMENT(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES SECTION(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    level INTEGER NOT NULL,
    position INTEGER NOT NULL,
    path LTREE,  -- Stores the hierarchical path (e.g., '1.2.3' for 3rd subsection of 2nd section of 1st heading)
    CONSTRAINT valid_level CHECK (level BETWEEN 1 AND 6)
);

-- Create the JSON_OUTPUT table
CREATE TABLE JSON_OUTPUT (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES DOCUMENT(id) ON DELETE CASCADE,
    json_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the VALIDATION_RESULT table
CREATE TABLE VALIDATION_RESULT (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES DOCUMENT(id) ON DELETE CASCADE,
    is_valid BOOLEAN NOT NULL,
    errors TEXT,
    validated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster hierarchical queries
CREATE INDEX sections_path_idx ON SECTION USING GIST (path);
CREATE INDEX sections_document_id_idx ON SECTION(document_id);
CREATE INDEX sections_parent_id_idx ON SECTION(parent_id);
