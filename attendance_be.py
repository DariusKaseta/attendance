from sqlalchemy.exc import SQLAlchemyError
from attendance import *
import PySimpleGUI as sg


def add_teacher_gui(f_name, l_name, subject):
    try:
        teacher = Teacher(f_name=f_name, l_name=l_name, subject=subject)
        session.add(teacher)
        session.commit()
        sg.popup(f"Teacher {f_name} {l_name} was created")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add teacher:", (e))


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


def get_choice(a_class):
    try:
        choices = session.query(a_class).all()
        for choice in choices:
            print(choice)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve Data:", str(e))


def get_lessons():
    try:
        lessons = session.query(Lesson).all()
        for lesson in lessons:
            teacher_name = (
                f"{lesson.teacher.f_name} {lesson.teacher.l_name}"
                if lesson.teacher is not None
                else "N/A"
            )
            print(lesson.id, teacher_name, lesson.date_)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve lesson:", str(e))


def create_lesson():
    try:
        get_choice(Teacher)
        choosen_teacher = input("Choose a teacher: ")
        today_date = datetime.strptime(
            input("Insert lesson's day (YYYY-MM-DD): "), "%Y-%m-%d"
        )
        topic = input("Insert lessons topic: ")
        t_date = Lesson(date_=today_date, teacher_id=choosen_teacher, topic=topic)
        session.add(t_date)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to create lesson:", str(e))


def check_attendance():
    try:
        get_lessons()
        chosen_lesson = input("Choose a lesson:")
        get_choice(Student)
        while True:
            chosen_student = input("Choose student or insert 0 to finish: ")
            if chosen_student == "0":
                break
            else:
                get_choice(AttStatus)
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


def teacher_window():
    layout = [
        [sg.Text("Name", size=(15, 1)), sg.Input(key="-T-name-")],
        [sg.Text("Last name", size=(15, 1)), sg.Input(key="-T-lname-")],
        [sg.Text("Subject", size=(15, 1)), sg.Input(key="-T-sub-")],
        [sg.Button("Add teacher", key="-ADD-T-"), sg.Button("Back", key="Exit")],
    ]
    window = sg.Window("Students attendance in a lecture", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == "-ADD-T-":
            inputs = [values["-T-name-"], values["-T-lname-"], values["-T-sub-"]]
            add_teacher_gui(inputs[0], inputs[1], inputs[2])
            break
        if event in (None, "Exit"):
            break
    window.close()


def lessons_window():
    all_workers = session.query(StudentAttendance).all()
    data = [
        [
            item.id,
            item.student.student_fname,
            item.student.student_lname,
            item.lesson.date_,
            item.lesson.topic,
            item.status.name,
            item.lesson.teacher.f_name,
            item.lesson.teacher.l_name,
        ]
        for item in all_workers
    ]
    headings = [
        "Id",
        "S name",
        "S last name",
        "Lessons date",
        "lessons topic",
        "Lankomumas",
        "Teachers name",
        "Teachers surname",
    ]
    table = sg.Table(data, headings)
    layout = [[table], [sg.Button("Back", key="Exit", pad=((200, 0), 3))]]
    window = sg.Window("Students attendance in a lecture", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == "-ADD-T-":
            inputs = [values["-T-name-"], values["-T-lname-"], values["-T-sub-"]]
            add_teacher_gui(inputs[0], inputs[1], inputs[2])
            break
        if event in (None, "Exit"):
            break
    window.close()
