from attendance import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import PySimpleGUI as sg

Session = sessionmaker(bind=engine)
session = Session()
headings=['Vardas', 'Pavardė', 'Gimimo data', 'Pareigos', 'Atlyginimas']
layout = [
    [sg.Text(headings[0], size=(15,1)), sg.Input(size=20,key='-NAME-')],
    [sg.Text(headings[1], size=(15,1)), sg.Input(size=20,key='-SURNAME-')],
    [sg.Text(headings[2], size=(15,1)), sg.Input(size=20,key='-BIRTHDATE-')],
    [sg.Text(headings[3], size=(15,1)), sg.Input(size=20,key='-POSITION-')],
    [sg.Text(headings[4], size=(15,1)), sg.Input(size=20,key='-SALARY-')],
    [sg.Button('Pridėti', key='-ADD-'), sg.Button('Peržiūrėti', key='-VIEWLIST-'), sg.Button('Redaguoti', key='-CHANGELIST-'), sg.Button('Išsaugoti', key='-SAVE-', disabled=True), sg.Button('Ištrinti', key='-DELETE-')],
    [sg.Table(values=[], headings=['ID', 'Vardas', 'Pavardė', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Isidarbinimo data'], key='-EMPLOYEES-', justification='left', auto_size_columns=False, col_widths=[3, 10, 10, 12, 17, 10, 15])]
]

window = sg.Window('Darbuotojų valdymas', layout)

# 
# create_employee("Petras", "Petraitis", datetime(1998, 7, 14), "Programuotojas", "1500")