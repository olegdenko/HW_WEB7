from src.db import session
from src.models import Teacher, Subject, Group, Student, Grade
from sqlalchemy import func, desc, select, and_
from sqlalchemy.orm import aliased

# Функція для знаходження 5 студентів із найбільшим середнім балом з усіх предметів


def select_1():
    q = session.query(Student.full_name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5)
    result = q.all()
    return result

# Функція для знаходження студента із найвищим середнім балом з певного предмета


def select_2(subject_id):
    q = session.query(Subject.name,
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
    result = q.all()
    return result

# Функція для знаходження середнього балу у групах з певного предмета.


def select_3(subject_id):
    q = session.query(
        Subject.name.label('subject_name'),
        Group.name.label('group_name'),
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ) \
        .join(Grade, Grade.subject_id == Subject.id) \
        .join(Student, Student.id == Grade.student_id) \
        .join(Group, Group.id == Student.group_id) \
        .filter(Subject.id == subject_id) \
        .group_by(Group.name, Subject.name) \
        .order_by(desc('average_grade'))

    result = q.all()
    return result

# Функція яка знаходить середній бал на потоці(по всій таблиці оцінок).


def select_4():
    q = session.query(func.round(
        func.avg(Grade.grade), 2).label('average_grade'))
    result = q.one()
    return result[0]

# Функція яка знаходить які курси читає певний викладач.


def select_5(teacher_id):
    q = session.query(Subject.name.label('course_name')) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Subject.name, Teacher.full_name) \
        .order_by(Subject.name.desc())

    result = q.all()
    return [row.course_name for row in result]

# Функція яка знаходить список студентів у певній групі.


def select_6(group_id):
    q = session.query(Student.full_name.label('student_name')) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .order_by(Student.full_name.desc())

    result = q.all()
    return [row.student_name for row in result]

# Функція яка знаходить оцінки студентів у окремій групі з певного предмета.


def select_7(subject_id, group_id):
    q = session.query(Student.full_name.label('student_name'), Grade.grade) \
        .join(Grade) \
        .join(Subject) \
        .join(Group) \
        .filter(Subject.id == subject_id, Group.id == group_id)

    result = q.all()
    return result

# Функція яка знаходить середній бал, який ставить певний викладач зі своїх предметів.


def select_8(teacher_id):
    q = session.query(
        Teacher.full_name.label('teacher_name'),
        Subject.name.label('subject_name'),
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Student).join(Subject).join(Group).join(Teacher)\
     .filter(Teacher.id == teacher_id)\
     .group_by(Teacher.full_name, Subject.name)\
     .order_by(func.avg(Grade.grade).desc())

    result = q.all()
    return result


# Функція яка знаходить список курсів, які відвідує певний студент.


def select_9(student_id):
    q = session.query(Subject.name.label('course_name'))\
        .join(Student, Student.id == student_id)\
        .group_by(Subject.name)\
        .order_by(Subject.name)

    result = q.all()
    return result

# Функція яка знаходить cписок курсів, які певному студенту читає певний викладач.


def select_10(student_id, teacher_id):
    student_alias = aliased(Student)
    subject_alias = aliased(Subject)

    q = session.query(subject_alias.name.label('course_name')) \
        .join(Grade, (student_alias.id == Grade.student_id) & (subject_alias.id == Grade.subject_id)) \
        .join(Teacher, subject_alias.teacher_id == Teacher.id) \
        .filter(student_alias.id == student_id) \
        .filter(Teacher.id == teacher_id) \
        .group_by(subject_alias.name) \
        .order_by(subject_alias.name)

    result = q.all()
    return result

# Функція яка знаходить cередній бал, який певний викладач ставить певному студентові.


def select_11(teacher_id, student_id):
    q = session.query(Teacher.full_name.label('teacher_name'),
                      Student.full_name.label('student_name'),
                      func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .join(Subject, Subject.teacher_id == Teacher.id)\
        .join(Grade, and_(Grade.student_id == student_id, Grade.subject_id == Subject.id))\
        .join(Student, Student.id == student_id)\
        .filter(Teacher.id == teacher_id)\
        .group_by(Teacher.full_name, Student.full_name)\
        .order_by(Teacher.full_name, Student.full_name)

    result = q.all()
    return result

# Функція яка виводить оцінки студентів у певній групі з певного предмета на останньому занятті.


def select_12(subject_id, group_id):
    subquery = (select(Grade.day_of).join(Student)
                .join(Group)
                .where(and_(Grade.subject_id == subject_id, Group.id == group_id))
                .order_by(desc(Grade.day_of)).limit(1).scalar_subquery())

    q = session.query(Subject.name,
                      Student.full_name,
                      Group.name,
                      Grade.day_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Subject) \
        .join(Group) \
        .filter(and_(Subject.id == subject_id, Group.id == group_id, Grade.day_of == subquery)) \
        .order_by(desc(Grade.day_of)) \
        .all()

    return q

if __name__ == "__main__":
    result1 = select_1()
    result2 = select_2(3)
    result3 = select_3(3)
    result4 = select_4()
    result5 = select_5(3)
    result6 = select_6(2)
    result7 = select_7(2, 2)
    result8 = select_8(4)
    result9 = select_9(45)
    result10 = select_10(22, 3)
    result11 = 0  # select_11(3, 15)
    result12 = 0  # select_12(3, 2)
    
    print(
        f'\n{result1}\n{result2}\n{result3}\n{result4}\n \
            {result5}\n{result6}\n{result7}\n{result8}\n \
            {result9}\n{result10}\n{result11}\n{result12}')

    session.close()
