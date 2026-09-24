CREATE DATABASE IF NOT EXISTS interntrack;

USE interntrack;


-- =========================
-- STUDENT TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    college VARCHAR(150),
    graduation_year YEAR
);


-- =========================
-- COMPANY TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    website VARCHAR(255)
);


-- =========================
-- INTERNSHIP TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Internship (
    internship_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    stipend DECIMAL(10,2),
    deadline DATE NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);


-- =========================
-- APPLICATION TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Application (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    internship_id INT NOT NULL,
    application_date DATE NOT NULL,
    status ENUM(
        'Applied',
        'Shortlisted',
        'Interview',
        'Selected',
        'Rejected'
    ) DEFAULT 'Applied',
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (internship_id) REFERENCES Internship(internship_id),
    UNIQUE (student_id, internship_id)
);


-- =========================
-- INTERVIEW TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Interview (
    interview_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    round_number INT NOT NULL,
    interview_date DATE,
    result ENUM(
        'Pending',
        'Passed',
        'Failed'
    ) DEFAULT 'Pending',
    feedback TEXT,
    FOREIGN KEY (application_id) REFERENCES Application(application_id)
);


-- =========================
-- SKILL TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Skill (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);


-- =========================
-- INTERNSHIP_SKILL TABLE
-- =========================

CREATE TABLE IF NOT EXISTS Internship_Skill (
    internship_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (internship_id, skill_id),
    FOREIGN KEY (internship_id) REFERENCES Internship(internship_id),
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);


-- =========================
-- SAMPLE COMPANIES
-- =========================

INSERT IGNORE INTO Company
(company_name, location, website)
VALUES
('Microsoft', 'Hyderabad', 'https://www.microsoft.com'),
('Amazon', 'Hyderabad', 'https://www.amazon.jobs'),
('Google', 'Bangalore', 'https://careers.google.com'),
('TCS', 'Hyderabad', 'https://www.tcs.com'),
('Infosys', 'Bangalore', 'https://www.infosys.com'),
('Deloitte', 'Hyderabad', 'https://www.deloitte.com');


-- =========================
-- SAMPLE STUDENTS
-- =========================

INSERT IGNORE INTO Student
(name, email, phone, college, graduation_year)
VALUES
('Rahul Sharma', 'rahul@example.com', '9876543210', 'VNR VJIET', 2027),
('Ananya Reddy', 'ananya@example.com', '9876543211', 'VNR VJIET', 2028),
('Arjun Kumar', 'arjun@example.com', '9876543212', 'VNR VJIET', 2027),
('Sneha Patel', 'sneha@example.com', '9876543213', 'CBIT', 2028),
('Kiran Rao', 'kiran@example.com', '9876543214', 'JNTUH', 2027);


-- =========================
-- SAMPLE INTERNSHIPS
-- =========================

INSERT IGNORE INTO Internship
(company_id, title, description, stipend, deadline)
VALUES
(1,
 'Software Engineering Intern',
 'Work on software development and real-world engineering projects.',
 30000,
 '2026-10-30'),

(2,
 'Amazon SDE Intern',
 'Develop scalable applications and solve real-world engineering problems.',
 40000,
 '2026-11-15'),

(3,
 'Data Science Intern',
 'Work with data analysis, machine learning and visualization.',
 35000,
 '2026-11-10'),

(4,
 'Full Stack Development Intern',
 'Build web applications using modern development technologies.',
 20000,
 '2026-10-25'),

(5,
 'Python Developer Intern',
 'Develop Python-based applications and automation solutions.',
 18000,
 '2026-11-05'),

(6,
 'Technology Analyst Intern',
 'Work on technology solutions, analytics and software projects.',
 25000,
 '2026-11-20');


-- =========================
-- SAMPLE SKILLS
-- =========================

INSERT IGNORE INTO Skill
(skill_name)
VALUES
('Java'),
('Python'),
('SQL'),
('Data Structures'),
('Machine Learning'),
('HTML/CSS'),
('JavaScript'),
('Spring Boot'),
('Flask'),
('Git/GitHub');


-- =========================
-- INTERNSHIP-SKILL MAPPING
-- =========================

INSERT IGNORE INTO Internship_Skill
(internship_id, skill_id)
VALUES
(1, 1),
(1, 3),
(1, 4),

(2, 1),
(2, 3),
(2, 4),

(3, 2),
(3, 3),
(3, 5),

(4, 6),
(4, 7),
(4, 9),

(5, 2),
(5, 3),
(5, 10),

(6, 1),
(6, 3),
(6, 10);


-- =========================
-- SAMPLE APPLICATIONS
-- =========================

INSERT IGNORE INTO Application
(student_id, internship_id, application_date, status)
VALUES
(1, 1, '2026-09-15', 'Applied'),
(1, 2, '2026-09-16', 'Interview'),
(2, 3, '2026-09-14', 'Interview'),
(3, 4, '2026-09-17', 'Selected'),
(4, 5, '2026-09-18', 'Rejected'),
(5, 6, '2026-09-19', 'Applied');


-- =========================
-- SAMPLE INTERVIEWS
-- =========================

INSERT IGNORE INTO Interview
(application_id, round_number, interview_date, result, feedback)
VALUES
(2, 1, '2026-09-20', 'Passed',
 'Good technical performance'),

(3, 1, '2026-09-21', 'Passed',
 'Strong problem-solving skills'),

(3, 2, '2026-09-25', 'Pending',
 NULL),

(4, 1, '2026-09-19', 'Passed',
 'Excellent interview performance'),

(2, 2, '2026-09-28', 'Pending',
 'Technical interview scheduled');


-- =========================
-- APPLICATION DETAILS VIEW
-- =========================

CREATE OR REPLACE VIEW ApplicationDetails AS
SELECT
    a.application_id,
    s.name AS student_name,
    c.company_name,
    i.title AS internship_title,
    a.application_date,
    a.status
FROM Application a
JOIN Student s
    ON a.student_id = s.student_id
JOIN Internship i
    ON a.internship_id = i.internship_id
JOIN Company c
    ON i.company_id = c.company_id;


-- =========================
-- INTERNSHIP SKILLS VIEW
-- =========================

CREATE OR REPLACE VIEW InternshipSkills AS
SELECT
    i.internship_id,
    i.title AS internship_title,
    c.company_name,
    s.skill_name
FROM Internship i
JOIN Company c
    ON i.company_id = c.company_id
JOIN Internship_Skill isk
    ON i.internship_id = isk.internship_id
JOIN Skill s
    ON isk.skill_id = s.skill_id;


-- =========================
-- DEADLINE TRIGGER
-- =========================

DROP TRIGGER IF EXISTS prevent_late_application;

DELIMITER //

CREATE TRIGGER prevent_late_application
BEFORE INSERT ON Application
FOR EACH ROW
BEGIN

    DECLARE internship_deadline DATE;

    SELECT deadline
    INTO internship_deadline
    FROM Internship
    WHERE internship_id = NEW.internship_id;

    IF NEW.application_date > internship_deadline THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Application deadline has passed';

    END IF;

END //

DELIMITER ;


-- =========================
-- STORED PROCEDURE
-- =========================

DROP PROCEDURE IF EXISTS ApplyForInternship;

DELIMITER //

CREATE PROCEDURE ApplyForInternship(
    IN p_student_id INT,
    IN p_internship_id INT,
    IN p_application_date DATE
)
BEGIN

    INSERT INTO Application
    (student_id, internship_id, application_date, status)
    VALUES
    (p_student_id, p_internship_id, p_application_date, 'Applied');

END //

DELIMITER ;