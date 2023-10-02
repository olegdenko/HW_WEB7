from src.db import session
from src.models import Teacher, Subject, Group, Student, Grade
from sqlalchemy import func, desc, select

# Функція для знаходження 5 студентів із найбільшим середнім балом з усіх предметів


def select_1():
    query = session.query(Student.full_name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5)
    result = query.all()
    return result

# Функція для знаходження студента із найвищим середнім балом з певного предмета


def select_2(subject_id):
    query = session.query(Subject.name,
                          Student.full_name,
                          func.round(func.avg(Grade.grade), 2).label('avg_grade')
                          ) \
                   .select_from(Grade) \
                   .join(Student) \
                   .join(Subject) \
                   .filter(Subject.id == subject_id) \
                   .group_by(Student.id, Subject.name) \
                   .order_by(desc('avg_grade')) \
                   .limit(1)
    result = query.all()
    return result


# def select_3(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_4(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_5(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_6(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_7(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_8(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_9(subject_id):
#     query = session.query(Subject.name, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.fullname) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_10(subject_id):
#     query = session.query(Subject.name, Student.full_name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.full_name) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


# def select_11(subject_id):
#     query = session.query(Subject.name, Student.full_name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
#                    .join(Grade, Student.id == Grade.student_id) \
#                    .join(Subject, Subject.id == Grade.subject_id) \
#                    .filter(Subject.id == subject_id) \
#                    .group_by(Student.full_name) \
#                    .order_by(desc('average_grade')) \
#                    .limit(1)
#     result = query.first()
#     return result


def select_12(subject_id):
    subquery = session.query(select(func.max(Grade.day_of)).join(Student).join(Group).where(and_))
    result = subquery.first()
    return result

if __name__ == "__main__":
    result1 = select_1()
    result2 = select_2(3)
    print(result1, result2)

    session.close()
