from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import joinedload, subqueryload
from src.db import session
from src.models import User, Todo, Teacher, Subject, Group, Student, Grade
from pprint import pprint


def get_user(login):
    user = session.query(User).filter(User.login == login).first()
    return user


def get_all_todos(user):
    todos = session.query(Todo).join(User).filter(Todo.user == user).all()  # filter == WHERE
    return todos


def create_todo(title, description, user):
    todo = Todo(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()


def update_todo(_id, title, description, user):
    todo = session.query(Todo).filter(and_(Todo.user == user, Todo.id == _id))
    todo.update({'title': title, 'description': description})
    session.commit()
    session.close()
    return todo.first()


def remove_todo(_id, user):
    r = session.query(Todo).filter(
        and_(Todo.user == user, Todo.id == _id)).delete()
    session.commit()
    session.close()
    return r


def create_model(title, description, user):
    user = User(name='Boris Johnson')
    session.add(user)
    session.commit()

    article = Article(title='Our country’s saddest day',
                    content='Lorem ipsum...', user_id=user.id)
    session.add(article)
    session.commit()


def read_model():
    students = session.query(Student).options(
        joinedload(Student.teachers)).all()
    for st in students:
        print(
            f"id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}")
        print(f"{[t.full_name for t in st.teachers]}")


def update_model(title, description, user):
    todo = Teacher(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()


def delete_model(title, description, user):
    todo = Teacher(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()


def list_model(title, description, user):
    todo = Teacher(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()


def get_student_load():
    students = session.query(Student).options(
        joinedload(Student.teachers)).all()
    for st in students:
        pprint(
            f"id: {st.id}, name: {st.first_name} {st.last_name}, email: {st.email}")
        pprint(f"{[t.full_name for t in st.teachers]}")


def get_teachers():
    teachers = session.query(Teacher).options(
        joinedload(Teacher.students)).filter(and_(Teacher.start_work > datetime(year=2021, month=6, day=15),
                                             Teacher.start_work < datetime(year=2022, month=6, day=15))).all()
    for t in teachers:
        pprint(
            f"Teacher - id: {t.id}, name: {t.first_name} {t.last_name}, email: {t.email}")
        pprint(f"Students - {[st.full_name for st in t.students]}")
