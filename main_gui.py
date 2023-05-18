import attendance_be as be
import PySimpleGUI as sg

layout = [
    [sg.Button("Add new teacher", key="-ADD-T-", size=(50, 3))],
    [sg.Button("Add Topic", key="-CREATE-L-", size=(50, 3))],
    [sg.Button("Add student", key="-ADD-S-", size=(50, 3))],
    [sg.Button("Mark Attendance", key="-MARK-A-", size=(50, 3))],
    [sg.Button("Exit", key="-EXIT-", size=(50, 3))],
]
window = sg.Window("Attendance", layout)
while True:
    event, values = window.read()
    if event == "-ADD-T-":
        be.teacher_window()
    if event == "-CREATE-L-":
        be.create_lesson_gui()
    if event == "-ADD-S-":
        be.student_window()
    if event == "-MARK-A-":
        be.lessons_window(be.get_lesson_gui())

    if event in (None, "-EXIT-"):
        break
