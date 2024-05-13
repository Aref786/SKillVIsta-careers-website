CREATE TABLE Employers (
    employer_id int identity(1,1) PRIMARY KEY,  -- Unique identifier for employer (e.g., "EMPLER_001")
    username VARCHAR(50) UNIQUE NOT NULL,      -- Username of the employer
    email VARCHAR(100) NOT NULL,               -- Email address of the employer
    password VARCHAR(100) NOT NULL,            -- Password of the employer (hashed and salted)
    company_name VARCHAR(100) NOT NULL,        -- Name of the company
    industry VARCHAR(50),                      -- Industry the company belongs to
    company_size VARCHAR(20),                  -- Size of the company (small, medium, large)
    website VARCHAR(100),                      -- Company website URL
    contact_person VARCHAR(100),               -- Contact person's name
    contact_email VARCHAR(100),                -- Contact email address
    contact_phone VARCHAR(20),                 -- Contact phone number
    company_address VARCHAR(200)               -- Company address
);

CREATE TABLE JobSeekers (
    job_seeker_id INT IDENTITY(1,1) PRIMARY KEY, -- Unique identifier for job seeker
    username VARCHAR(50) UNIQUE NOT NULL,             -- Username of the job seeker
    email VARCHAR(100) NOT NULL,               -- Email address of the job seeker
    password VARCHAR(100) NOT NULL,            -- Password of the job seeker (hashed and salted)
    full_name VARCHAR(100) NOT NULL,           -- Full name of the job seeker
    phone VARCHAR(20),                         -- Phone number of the job seeker
    location VARCHAR(100),                     -- Location of the job seeker
    occupation VARCHAR(100),                   -- Job title or occupation
    industry_expertise VARCHAR(100),           -- Industry expertise of the job seeker
    experience_years INT,                      -- Years of experience
    education VARCHAR(100),                    -- Educational background
    skills VARCHAR(200),                       -- Key skills of the job seeker
    certifications VARCHAR(200),               -- Certifications or licenses
    work_type VARCHAR(100),                    -- Type of work sought
    job_categories VARCHAR(200),               -- Preferred job categories or fields
    salary VARCHAR(50)                         -- Desired hourly rate or salary range
);

---CReating a login table 
CREATE TABLE login (
    id INT IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    email NVARCHAR(100) NOT NULL,
);
-- Create UserJobPostinges table with foreign key reference to usersname table in user table
CREATE TABLE UserJobPostings(
    JobID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(100) NOT NULL,
    Description NVARCHAR(MAX) NOT NULL,
    Budget DECIMAL(10, 2) NOT NULL,
    Deadline DATE NOT NULL,
    Instructions NVARCHAR(MAX) NOT NULL,
    ContactInfo NVARCHAR(MAX) NOT NULL,
    SalaryBenefits NVARCHAR(MAX) NOT NULL,
    UserName NVARCHAR(50) NOT NULL
);
/*
-- Trigger for JobSeekers table
CREATE TRIGGER trg_InsertLoginJobSeekers
ON JobSeekers
AFTER INSERT
AS
BEGIN
    INSERT INTO login (username, password, email)
    SELECT username, password, email
    FROM inserted
    WHERE job_seeker_id NOT IN (SELECT id FROM login);
END;
GO

-- Trigger for Employers table
CREATE TRIGGER trg_InsertLoginEmployers
ON Employers
AFTER INSERT
AS
BEGIN
    INSERT INTO login (username, password, email)
    SELECT username, password, email
    FROM inserted
    WHERE employer_id NOT IN (SELECT id FROM login);
END;
GO


CREATE PROCEDURE RetrieveAllJobPostings
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT E.username AS EmployerUsername, E.email AS EmployerEmail, E.company_name AS CompanyName,
           E.industry AS Industry, E.company_size AS CompanySize, E.website AS CompanyWebsite,
           E.contact_person AS ContactPerson, E.contact_email AS ContactEmail, E.contact_phone AS ContactPhone,
           E.company_address AS CompanyAddress,
           U.Title AS JobTitle, U.Description AS JobDescription, U.Budget AS JobBudget,
           U.Deadline AS JobDeadline, U.Instructions AS JobInstructions, U.ContactInfo AS JobContactInfo,
           U.SalaryBenefits AS JobSalaryBenefits
    FROM Employers E
    JOIN UserJobPostings U ON E.username = U.UserName;
END;

GO 
*/

CREATE TABLE JobApplications (
    ApplicationID INT PRIMARY KEY IDENTITY,
    JobID INT,
    ApplicantName NVARCHAR(100),
    ApplicantEmail NVARCHAR(100),
    ResumeFilePath NVARCHAR(255),
    ApplicationDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (JobID) REFERENCES UserJobPostings(JobID)
);
