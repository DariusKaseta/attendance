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


def add_student_gui(student_fname, student_lname):
    try:
        student = Student(student_fname=student_fname, student_lname=student_lname)
        session.add(student)
        session.commit()
        sg.popup(f"Student {student_fname} {student_lname} was created")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add student:", (e))


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


def teacher_window():
    layout = [
        [sg.Text("Name", size=(15, 1)), sg.Input(key="-T-name-")],
        [sg.Text("Last name", size=(15, 1)), sg.Input(key="-T-lname-")],
        [sg.Text("Subject", size=(15, 1)), sg.Input(key="-T-sub-")],
        [sg.Button("Add teacher", key="-ADD-T-"), sg.Button("Back", key="Exit")],
    ]
    window = sg.Window("Please add teacher", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == "-ADD-T-":
            add_teacher_gui(values["-T-name-"], values["-T-lname-"], values["-T-sub-"])
            break
        if event in (None, "Exit"):
            break
    window.close()


def get_lesson_gui():
    lessons = session.query(Lesson).all()
    data = [
        [
            lesson.id,
            lesson.teacher.f_name + " " + lesson.teacher.l_name,
            lesson.date_,
            str(lesson.topic),
        ]
        for lesson in lessons
    ]
    layout = [
        [sg.Combo(values=data, key="combo", size=(80, 0), readonly=True)],
        [sg.Button("Choose", key="Chosen")],
    ]
    window = sg.Window("Choose lecture", layout)
    while True:
        event, values = window.read()
        if event == "Chosen" or event == sg.WINDOW_CLOSED:
            try:
                window.close()
                return list(values["combo"])[0]
            except:
                window.close()
                return 0


def lessons_window(lesson):
    if lesson != 0:
        all_students = session.query(StudentAttendance).filter_by(lesson_id=lesson)
    else:
        all_students = session.query(StudentAttendance).all()
    status_data = [
        [
            item.status.id,
        ]
        for item in all_students
    ]
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
        for item in all_students
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
    table = sg.Table(
        data,
        headings,
        selected_row_colors="red on yellow",
        key="-TABLE-",
        enable_events=True,
    )
    layout = [
        [table],
        [sg.Button("Back", key="Exit", pad=((200, 0), 3))],
        [
            sg.Button(
                "Edit marked student",
                key="-EDIT-",
                pad=((200, 0), 3),
            )
        ],
        [
            sg.Radio("Present", group_id=1, key="-Present-"),
            sg.Radio("Absent", group_id=1, key="-Absent-"),
            sg.Radio("Late", group_id=1, key="-Late-"),
        ],
    ]
    window = sg.Window("Students attendance in a lecture", layout)
    while True:
        event, values = window.read()
        if "-TABLE-" in event:
            indexas = values[event][0]
            sg.popup(data[indexas][5])

        if event == "-EDIT-":
            pass

        if event == "add":
            print(values["add"])
        if event in (None, "Exit"):
            break
    window.close()


def student_window():
    layout = [
        [sg.Text("Name", size=(15, 1)), sg.Input(key="-S-name-")],
        [sg.Text("Last name", size=(15, 1)), sg.Input(key="-S-lname-")],
        [sg.Button("Add student", key="-ADD-S-"), sg.Button("Back", key="Exit")],
    ]
    window = sg.Window("Adding new student", layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == "-ADD-S-":
            add_student_gui(values["-S-name-"], values["-S-lname-"])
            break
        if event in (None, "Exit"):
            break
    window.close()
