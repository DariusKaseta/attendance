from sqlalchemy.exc import SQLAlchemyError
from attendance import *


def add_teacher():
    try:
        f_name = input("Insert teachers name: ")
        l_name = input("Insert teachers last name: ")
        subject = input("Insert teacher's subject: ")
        teacher = Teacher(f_name=f_name, l_name=l_name, subject=subject)
        session.add(teacher)
        session.commit()
        print(f"Teacher {f_name} {l_name} was created")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add teacher:", (e))



def add_student():
    try:
        student_fname = input("Insert students name: ")
        student_lname = input("Insert students last name: ")
        student = Student(student_fname=student_fname, student_lname=student_lname)
        session.add(student)
        session.commit()
        print(f"Student {student_fname} {student_lname} was created")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add student:", str(e))



def add_status():
    try:
        status_name = input("Insert status name:")
        status = AttStatus(name=status_name)
        session.add(status)
        session.commit()
        print(f"{status_name} was added")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add status:", str(e))


def get_teachers():
    try:
        teahcers = session.query(Teacher).all()
        for teacher in teahcers:
            print(teacher.id, teacher.f_name, teacher.l_name, teacher.subject)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve teacher:", str(e))


def get_students():
    try:
        students = session.query(Student).all()
        for student in students:
            print(student.id, student.student_fname, student.student_lname)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve student:", str(e))


def get_lessons():
    try:
        lessons = session.query(Lesson).all()
        for lesson in lessons:
            teacher_name = f"{lesson.teacher.f_name} {lesson.teacher.l_name}" if lesson.teacher is not None else "N/A"
            print(lesson.id, teacher_name, lesson.date_)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve lesson:", str(e))



def get_status():
    try:
        stasuses = session.query(AttStatus).all()
        for status in stasuses:
            print(status.id, status.name)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve status:", str(e))


def create_lesson():
    try:
        get_teachers()
        choosen_teacher = input("Choose a teacher: ")
        today_date = datetime.strptime(
            input("Insert lesson's day (YYYY-MM-DD): "), "%Y-%m-%d"
        )
        t_date = Lesson(date_=today_date, teacher_id=choosen_teacher)
        session.add(t_date)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to create lesson:", str(e))


def check_attendance():
    try:
        get_lessons()
        chosen_lesson = input("Choose a lesson:")
        get_students()
        while True:
            chosen_student = input("Choose student or insert 0 to finish: ")
            if chosen_student == "0":
                break
            else:
                get_status()
                chosen_status = input("Insert attendance status: ")
                student_atendance = StudentAttendance(
                    lesson_id=chosen_lesson,
                    student_id=chosen_student,
                    attstatus_id=chosen_status,
                )
                session.add(student_atendance)
                session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to check attendances:", str(e))


check_attendance()
