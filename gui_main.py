import PySimpleGUI as sg
from datetime import date


# darbuotojai = PersonaloValdymas()
# darbuotojai = PersonaloValdymas.pickle_nuskaitymas(darbuotojai)
td=[]
headings=['Vardas Pavardė', 'Komentaras', 'Alga', 'Priimtas', 'Telefono numeris', 'Asmens kodas', 'Išsilavinimas', 'Skyrius']

layout=[
        [sg.Text(headings[0], size=(15,1)),sg.Input(size=20,key=headings[0])],
        [sg.Text(headings[1], size=(15,1)),sg.Input(size=20,key=headings[1])],
        [sg.Text(headings[2], size=(15,1)),sg.Input(size=20,key=headings[2])],
        [sg.Text(headings[3], size=(15,1)),sg.Input(size=20,key=headings[3])],
        [sg.Text(headings[4], size=(15,1)),sg.Input(size=20,key=headings[4])],
        [sg.Text(headings[5], size=(15,1)),sg.Input(size=20,key=headings[5])],
        [sg.Text(headings[6], size=(15,1)),sg.Input(size=20,key=headings[6])],
        [sg.Text(headings[7], size=(18,1)),sg.Combo(['IT skyrius','Finansai','Administracija'],key=headings[7])],
        [sg.Button('Pridėti'), sg.Button('Redaguoti'), sg.Button('Išsaugoti',disabled=True), sg.Button('Ištrinti'), sg.Push(), sg.Exit()],
        [sg.Table(td,headings,key='myTable')]]

window=sg.Window('Personalo valdymo programa',layout)
# 
while True:
    event,values= window.read()
    print (values)
    if event == 'Pridėti':
        values = [values[h] for h in headings]
        td.append(values)
        darbuotojai.prideti_darbuotoja(*values)
        darbuotojai.darbuotoju_sarasas()
        window['myTable'].update(values=td)
        for i in range(len(headings)):    
            window[headings[i]].update(value='')
    if event == 'Redaguoti':
        if values['myTable']==[]:
            sg.popup('Pasirinkite eilutę, kurią norite redaguoti')
        else:
            editRow=values['myTable'][0]
            for i in range(len(headings)):  
                window[headings[i]].update(value=td[editRow][i])
            window['Išsaugoti'].update(disabled=False)
    if event == 'Išsaugoti':
        td[editRow]=([values[h] for h in headings])
        window['myTable'].update(values=td)
        for i in range(len(headings)):
            window[headings[i]].update(value='')
        window['Išsaugoti'].update(disabled=True)
    if event == 'Ištrinti':
        if values['myTable']==[]:
            sg.popup('Pasirinkite eilutę')
        else:
            if sg.popup_ok_cancel('Ar tikrai norite tęsti?') == 'OK':
                pasirinkta_eilute = values['myTable'][0]
                pasirinktas_vardas = td[pasirinkta_eilute][0]
                print(pasirinktas_vardas)
                del td[pasirinkta_eilute]
                data = date.today()
                data_str = data.strftime('%Y-%m-%d')
                darbuotojai.atleisti_darbuotoja(pasirinktas_vardas, data_str)
                darbuotojai.atleistu_darbuotoju_sarasas()
                darbuotojai.darbuotoju_sarasas()
                window['myTable'].update(values=td)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()


# from attendance import *
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# import PySimpleGUI as sg

# Session = sessionmaker(bind=engine)
# session = Session()
# headings=['Lecture', 'Student', 'Attendance']
# layout = [
#     [sg.Text(headings[0], size=(15,1)), sg.Input(size=20,key='-NAME-')],
#     [sg.Text(headings[1], size=(15,1)), sg.Input(size=20,key='-SURNAME-')],
#     [sg.Text(headings[2], size=(15,1)), sg.Input(size=20,key='-BIRTHDATE-')],
#     [sg.Button('Add', key='-ADD-'), sg.Button('View', key='-VIEWLIST-'), sg.Button('Edit', key='-CHANGELIST-'), sg.Button('Save', key='-SAVE-', disabled=True), sg.Button('Delete', key='-DELETE-')],
#     [sg.Table(values=[], headings=['ID', 'Lecture', 'Student', 'Attendance'], key='-EMPLOYEES-', justification='left', auto_size_columns=False, col_widths=[3, 10, 10, 12, 17, 10, 15])]
# ]

# window = sg.Window('Students attendance in a lecture', layout)
# while True:
#    event, values = window.read()
#    print(event, values)
#    if event in (None, 'Exit'):
#       break
# window.close()
