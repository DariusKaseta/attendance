import gui_main

headings = main.headings
layout = main.layout
window = main.window

# while True:
#     event, values = window.read()
#     if event == main.sg.WINDOW_CLOSED:
#         break
#     if event == '-ADD-':
#         main.add_employee(window, values)

#     if event == '-VIEWLIST-':
#         main.employee_list(window)

#     if event == '-CHANGELIST-':
#         main.employee_changelist(window, values)

#     if event == '-SAVE-':
#         employee_id = main.get_index(values)
#         if employee_id:
#             main.save_updated_employee(window, employee_id, values)
#             main.sg.popup('Information successfully changed!')
#         else:
#             main.sg.popup('Please select an employee from the list.')

#     if event == '-DELETE-':
#         main.delete_selected_employee(window, values)