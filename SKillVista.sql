--Create database
CREATE database ['SKillVist']
go
-- Create users table
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    resume_path NVARCHAR(255)
);
go
-- Create login table with foreign key reference to users table
CREATE TABLE login (
    id INT PRIMARY KEY,
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id)
);

/*
CREATE TRIGGER UpdateLoginTable
ON users
AFTER INSERT
AS
BEGIN
    -- Insert new records into login table
    INSERT INTO login (id, username, password, email)
    SELECT id, username, password, email
    FROM inserted
    WHERE id NOT IN (SELECT id FROM login);
END;

*/

CREATE TABLE UserJobPostings(
    JobID INT IDENTITY(1,1),
    Title NVARCHAR(100) NOT NULL,
    Description NVARCHAR(MAX) NOT NULL,
    Budget DECIMAL(10, 2) NOT NULL,
    Deadline DATE NOT NULL,
    Instructions NVARCHAR(MAX) NOT NULL,
    ContactInfo NVARCHAR(MAX) NOT NULL,
    SalaryBenefits NVARCHAR(MAX) NOT NULL,
    UserName NVARCHAR(50) NOT NULL
);


