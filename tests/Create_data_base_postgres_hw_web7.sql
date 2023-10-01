-- Спочатку видаляємо таблиці, якщо вони існують
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS grades;

-- Створюємо таблиці
CREATE TABLE groups (
 id SERIAL PRIMARY KEY,
 name VARCHAR(255) UNIQUE
);

CREATE TABLE teachers (
 id SERIAL PRIMARY KEY,
 fullname VARCHAR(255)
);

CREATE TABLE students (
 id SERIAL PRIMARY KEY,
 fullname VARCHAR(255),
 group_id INTEGER REFERENCES groups (id)
);

CREATE TABLE subjects (
 id SERIAL PRIMARY KEY,
 name VARCHAR(255),
 teacher_id INTEGER REFERENCES teachers (id)
);

CREATE TABLE grades (
 id SERIAL PRIMARY KEY,
 subject_id INTEGER REFERENCES subjects (id),
 student_id INTEGER REFERENCES students (id),
 grade INTEGER,
 day_of DATE
);