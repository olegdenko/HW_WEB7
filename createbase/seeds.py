from datetime import datetime, date, timedelta
from faker import Faker
from random import randint
from pprint import pprint
from database.db import session

subjects = ["Вища математика",
            "Дискретна математика",
            "Лінійна Алгебра",
            "Програмування",
            "Теорія імовірності",
            "Історія України",
            "Англійська",
            "Креслення"]

groups = ["Є-331", "ТП-05-1", "КН-51", "ПЦБ-13з"]
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
fake = Faker('uk-UA')
connect = session
cur = connect.cursor()


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers,))


def seed_subjects():
    sql = "INSERT INTO subjects(name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(subjects, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(subjects)))))


def seed_groups():
    sql = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(sql, zip(groups))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students(fullname, group_id) VALUES(?, ?);"
    cur.executemany(sql, zip(students, iter(randint(1, len(groups))
                    for _ in range(len(students)))))
    

def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")
    sql = "INSERT INTO grades(subject_id, student_id, grade, day_of) VALUES(?, ?, ?, ?)"

    def get_list_date(start: date, end: date):
        result = []
        current_data = start
        while current_data <= end:
            if current_data.isoweekday() < 6:
                result.append(current_data)
            current_data += timedelta(1)
        return result
    list_dates = get_list_date(start_date, end_date)
    grades = []
    for day in list_dates:
        random_subjects = randint(1, len(subjects))
        random_students = [randint(1, NUMBER_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((random_subjects, student, randint(1, 12), day.date()))
    cur.executemany(sql, grades)


if __name__ == "__main__":
    try:
        seed_teachers()
        seed_subjects()
        seed_groups()
        seed_students()
        seed_grades()
        connect.commit()
    except sqlite3.Error as  error:
        pprint(error)
    finally:
        connect.close()
