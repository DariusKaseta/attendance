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

def add_student_gui(student_fname, student_lname):
    try:
        student = Student(student_fname=student_fname, student_lname=student_lname)
        session.add(student)
        session.commit()
        sg.popup(f"Student {student_fname} {student_lname} was created")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to add student:", (e))  


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
        return choices
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve Data:", str(e))
        return None


def get_lessons():
    try:
        lessons = session.query(Lesson).all()
        for lesson in lessons:
            teacher_name = (
                f"{lesson.teacher.f_name} {lesson.teacher.l_name}"
                if lesson.teacher is not None
                else "N/A"
            )
            print(lesson.id, teacher_name, lesson.date_, lesson.topic)
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to retrieve lesson:", str(e))


def create_lesson(teacher_id, date_, topic):
    try:
        today_date = datetime.strptime(date_,"%Y-%m-%d")
        t_date = Lesson(date_=today_date, teacher_id=teacher_id, topic=topic)
        # t_date = Lesson(date_=today_date, teacher_id=choosen_teacher, topic=topic)
        session.add(t_date)
        session.commit()
        sg.popup("Lesson created successfully!")
    except SQLAlchemyError as e:
        session.rollback()
        print("Failed to create lesson:", str(e))


def create_lesson_gui():
    teachers = get_choice(Teacher)
    print(teachers)
    if teachers is not None:
        teacher_names = [f"{teacher.id}. {teacher.f_name} {teacher.l_name}" for teacher in teachers]
        teacher_choice = sg.Combo(teacher_names, key="-TEACHER-", size=(50, 1))

        layout = [
            [sg.Text("Choose a teacher:")],
            [teacher_choice],
            [sg.Button("Create Lesson", key="-CREATE-L-", size=(50, 3))],
        ]

        window = sg.Window("Create Lesson", layout)

        while True:
                    event, values = window.read()
                    
                    if event == sg.WINDOW_CLOSED:
                        break
                    elif event == "-CREATE-L-":
                        selected_teacher = values["-TEACHER-"]
                        if selected_teacher:
                            topic = sg.popup_get_text("Enter lesson's topic:")
                            if topic:
                                try:
                                    teacher_id = int(selected_teacher.split('.')[0])
                                    current_date = datetime.now().strftime("%Y-%m-%d")
                                    create_lesson(teacher_id, current_date, topic)
                                    sg.popup("Topic created successfully!")
                                except SQLAlchemyError as e:
                                    sg.popup("Invalid teacher's choice.", str(e))
                            else:
                                sg.popup("Topic cannot be empty.")
                        else:
                            sg.popup("No teacher selected.")
        window.close()
    else:
        sg.popup("No teachers available")


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
        enable_click_events=True,
        key="-TABLE-",
    )
    layout = [
        [table],
        [sg.Button("Back", key="Exit", pad=((200, 0), 3))],
        [sg.Button("add", key="add", pad=((200, 0), 3))],
    ]
    window = sg.Window("Students attendance in a lecture", layout)
    while True:
        event, values = window.read()
        # if "+CLICKED+" in event:
        #     sg.popup("You clicked row:{} Column: {}".format(event[2][0], event[2][1]))
        if event == "add":
            print(values["-TABLE-"])
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