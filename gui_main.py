from attendance import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import PySimpleGUI as sg

Session = sessionmaker(bind=engine)
session = Session()
headings=['Lecture', 'Student', 'Attendance']
layout = [
    [sg.Text(headings[0], size=(15,1)), sg.Input(size=20,key='-NAME-')],
    [sg.Text(headings[1], size=(15,1)), sg.Input(size=20,key='-SURNAME-')],
    [sg.Text(headings[2], size=(15,1)), sg.Input(size=20,key='-BIRTHDATE-')],
    [sg.Button('Add', key='-ADD-'), sg.Button('View', key='-VIEWLIST-'), sg.Button('Edit', key='-CHANGELIST-'), sg.Button('Save', key='-SAVE-', disabled=True), sg.Button('Delete', key='-DELETE-')],
    [sg.Table(values=[], headings=['ID', 'Lecture', 'Student', 'Attendance'], key='-EMPLOYEES-', justification='left', auto_size_columns=False, col_widths=[3, 10, 10, 12, 17, 10, 15])]
]

window = sg.Window('Students attendance in a lecture', layout)
while True:
   event, values = window.read()
   print(event, values)
   if event in (None, 'Exit'):
      break
window.close()

# 
# 
def create_employee(name, surname, birthdate, position, salary):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    employee = Employee(name=name, surname=surname, birthdate=birthdate, position=position, salary=salary)
    session.add(employee)
    session.commit()

def get_employees():
    employees = session.query(Employee).all()
    return employees

def change_employee(employee_id, **kwargs):
    employee = session.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        session.commit()

def delete_employee(employee_id):
    employee = session.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()

def employee_list(window):
    employees = get_employees()
    window['-EMPLOYEES-'].update([f'{e.id} {e.name} {e.surname} {e.birthdate} {e.position} {e.salary} {e.working_since}' for e in employees])

def delete_selected_employee(window, values):
    selected_rows = values['-EMPLOYEES-']
    if selected_rows:
        selected_row_index = selected_rows[0]
        employees = get_employees()
        if selected_row_index < len(employees):
            employee = employees[selected_row_index]
            employee_id = employee.id
            delete_employee(employee_id)
            sg.popup('Employee deleted succesfully')
    employee_list(window)

def save_updated_employee(window, employee_id, values):
    if employee_id is not None:
        name = values['-NAME-']
        surname = values['-SURNAME-']
        birthdate = values['-BIRTHDATE-']
        position = values['-POSITION-']
        salary = values['-SALARY-']
        if name or surname or birthdate or position or salary:
            try:
                birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
                change_employee(employee_id, name=name, surname=surname, birthdate=birthdate, position=position, salary=salary)
                employee_list(window)
            except ValueError:
                sg.popup('Incorrect date format, please use this format: YYYY-MM-DD.')

def employee_changelist(window, values):
    sg.popup('Enter new values you wish to change')
    selected_rows = values['-EMPLOYEES-']
    if selected_rows:
        selected_row_index = selected_rows[0]
        employees = get_employees()
        if selected_row_index < len(employees):
            employee = employees[selected_row_index]
            for attribute, value in zip(['-NAME-', '-SURNAME-', '-BIRTHDATE-', '-POSITION-', '-SALARY-'], [employee.name, employee.surname, employee.birthdate, employee.position, employee.salary]):
                window[attribute].update(value=value)
            window['-SAVE-'].update(disabled=False)
        else:
            sg.popup('Invalid selected row index.')
    else:
        sg.popup('Please select an employee from the list.') 

def get_index(values):
    selected_rows = values['-EMPLOYEES-']
    if selected_rows:
        selected_row_index = selected_rows[0]
        employees = get_employees()
        if selected_row_index < len(employees):
            employee = employees[selected_row_index]
            employee_id = employee.id   
    return employee_id

def add_employee(window, values):
    keys=['-NAME-', '-SURNAME-', '-BIRTHDATE-', '-POSITION-', '-SALARY-']
    input_values = [values[key] for key in keys]
    if all(input_values):
        try:
            create_employee(input_values[0], input_values[1], input_values[2], input_values[3], input_values[4])
            sg.popup('Employee succesfully added!')
        except ValueError:
            sg.popup('Incorrect date format, please use this format: YYYY-MM-DD.')
    else:
        sg.popup('Please fill all the fields.')
    employee_list(window)