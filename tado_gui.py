import attendance_be as be
import PySimpleGUI as sg

layout = [
    [sg.Button("Create Lesson", key="-CREATE-L-", size=(50, 3))],
    [sg.Button("Mark Lessons", key="-MARK-L-", size=(50, 3))],
    [sg.Button("Add teacher", key="-ADD-T-", size=(50, 3))],
    [sg.Button("Add student", key="-ADD-S-", size=(50, 3))],
    [sg.Button("Exit", key="-EXIT-", size=(50, 3))],
]
window = sg.Window("Attendance", layout)
while True:
    event, values = window.read()
    if event == "-ADD-T-":
        be.teacher_window()
    if event == "-MARK-L-":
        be.lessons_window(be.get_lesson_gui())
    if event == "-MARK-L-":
        pass
    if event in (None, "-EXIT-"):
        break
