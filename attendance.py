# Main page
from sqlalchemy import Integer, Float, String, ForeignKey, Date, create_engine
from sqlalchemy.orm import (
    Session,
    relationship,
    sessionmaker,
    DeclarativeBase,
    mapped_column,
)
from datetime import datetime
from typing import Any

engine = create_engine("sqlite:///attendance.db")
session = sessionmaker(bind=engine)()


class Base(DeclarativeBase):
    pass


class Teacher(Base):
    __tablename__ = "teacher"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    f_name = mapped_column("f_name", String(50))
    l_name = mapped_column("l_name", String(50))
    subject = mapped_column("subject", String(100))
    lessons = relationship("Lesson", back_populates="teacher")

    def __repr__(self):
        return f"{self.id}. {self.f_name} {self.l_name}, {self.subject}"


class AttStatus(Base):
    __tablename__ = "attstatus"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column("name", String(50))
    student_attendance = relationship("StudentAttendance", back_populates="status")

    def __repr__(self):
        return f"{self.id}. {self.name}"


class Lesson(Base):
    __tablename__ = "lesson"
    id = mapped_column(Integer, primary_key=True)
    topic = mapped_column(String(50))
    date_ = mapped_column("Lesson's Date", Date, default=datetime.utcnow)
    teacher_id = mapped_column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="lessons")
    attendance = relationship("StudentAttendance", back_populates="lesson")

    def __repr__(self):
        return f"{self.id}. {self.date_}, {self.topic}, {self.teacher_id}"


class Student(Base):
    __tablename__ = "student"
    id = mapped_column(Integer, primary_key=True)
    student_fname = mapped_column("student_fname", String(50))
    student_lname = mapped_column("student_lname", String(50))
    lesson_attend = relationship("StudentAttendance", back_populates="student")

    def __repr__(self):
        return f"{self.id}. {self.student_fname} {self.student_lname}"


class StudentAttendance(Base):
    __tablename__ = "student_attendance"
    id = mapped_column(Integer, primary_key=True)
    lesson_id = mapped_column(Integer, ForeignKey("lesson.id"))
    student_id = mapped_column(Integer, ForeignKey("student.id"))
    attstatus_id = mapped_column(Integer, ForeignKey("attstatus.id"))
    status = relationship("AttStatus", back_populates="student_attendance")
    student = relationship("Student", back_populates="lesson_attend")
    lesson = relationship("Lesson", back_populates="attendance")

    def __repr__(self):
        return f"{self.id}. {self.lesson_id}, {self.student_id}, {self.attstatus_id}"


Base.metadata.create_all(engine)
