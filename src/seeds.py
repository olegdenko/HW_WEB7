import random
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date, timedelta
from faker import Faker
from random import randint, choice
from pprint import pprint
from db import session

from models import User, Todo, Teacher, TeacherStudent, Subject, Group, Student, Grade

SUBJECTSES = ["Вища математика",
              "Дискретна математика",
              "Лінійна Алгебра",
              "Програмування",
              "Теорія імовірності",
              "Історія України",
              "Англійська",
              "Креслення"]

GROUPSES = ["Є-331", "ТП-05-1", "КН-51", "ПЦБ-13з"]
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
fake = Faker('uk-UA')


def seed_teachers():
    teachers = [Teacher(first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        phone=fake.phone_number(),
                        address=fake.address(),
                        start_work=fake.date_between(start_date='-5y')
                        ) for _ in range(NUMBER_TEACHERS)]
    session.add_all(teachers)
    session.commit()


def seed_subjects():
    teachers = session.query(Teacher).all()
    subjects = [Subject(name=subject, teacher_id=randint(
        1, NUMBER_TEACHERS)) for subject in SUBJECTSES]
    for subject in subjects:
        subject.teacher_id = choice(teachers).id

    session.add_all(subjects)
    session.commit()


def seed_groups():
    groups = [Group(name=group) for group in GROUPSES]
    session.add_all(groups)
    session.commit()


def seed_students():
    groups = session.query(Group).all()
    students = [Student(first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        phone=fake.phone_number(),
                        address=fake.address(),
                        group_id=randint(
        1, len(GROUPSES))) for _ in range(NUMBER_STUDENTS)]
    for student in students:
        student.group_id = choice(groups).id

    session.add_all(students)
    session.commit()


def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")

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

    subjects = session.query(Subject).all()
    students = session.query(Student).all()

    for day in list_dates:
        random_subject = choice(subjects)
        random_student = choice(students)

        grades.append(Grade(subject_id=random_subject.id,
                            student_id=random_student.id, grade=randint(1, 12), day_of=day.date()))

    session.add_all(grades)
    session.commit()


def seed_relationship():
    students = session.query(Student).all()
    teachers = session.query(Teacher).all()

    for student in students:
        teacher = random.choice(teachers)
        rel = TeacherStudent(teacher_id=teacher.id, student_id=student.id)
        session.add(rel)
    session.commit()


if __name__ == "__main__":
    try:
        session.query(TeacherStudent).delete()
        session.query(Grade).delete()
        # session.query(ContactPerson).delete()
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(User).delete()
        session.query(Todo).delete()

        session.commit()

        seed_teachers()
        seed_subjects()
        seed_groups()
        seed_students()
        seed_grades()
        seed_relationship()
    except SQLAlchemyError as error:
        pprint(error)
