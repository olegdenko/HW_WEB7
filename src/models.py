import logging
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, func, event, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from src.db import engine

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(25), unique=True, nullable=False)
    password = Column(String(25), nullable=False)


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(String(150), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    user_in = Column('user_id', Integer, ForeignKey('users.id'))
    user = relationship(User)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    start_work = Column(Date, nullable=False)
    students = relationship(
        'Student', secondary='teachers_to_students', back_populates='teachers')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(Group)
    teachers = relationship('Teacher', secondary='teachers_to_students', back_populates='students')
    contacts = relationship('ContactPerson', back_populates='student')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class ContactPerson(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    student_id = Column(Integer, ForeignKey(
        'students.id', ondelete='CASCADE'))
    student = relationship(
        'Student', back_populates='contacts')

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class TeacherStudent(Base):
    __tablename__ = 'teachers_to_students'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey(
        'students.id', ondelete='CASCADE'))


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship(Teacher)


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    grade = Column(Integer)
    day_of = Column(DateTime)


@event.listens_for(Todo, 'before_update')
def update_updated_at(mapper, conn, target):
    target.updated_at = func.now()


Base.metadata.create_all(engine)
