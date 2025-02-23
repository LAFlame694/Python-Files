from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Data Entry Form")
options = ["Mr.", "Ms.", "Dr."]
continents = ["Africa", "Antarctica", "Asia", "Europe", "S.America", "N.America", "Oceania"]
v1 = StringVar(value="Not Registered")
terms_and_conditions = StringVar(value="Not Accepted")

#===Functions===========================================================================================================
def enter_data():
    terms = terms_and_conditions.get()
    if terms == "Accepted":

        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        title = combobox.get()
        nationality = nationality_combobox.get()
        age = age_spinbox.get()
        numbercoursesspinbox = nummber_courses_spinbox.get()
        numberofsemesters = semester_spinbox.get()
        registration = v1.get()


        print("First Name: ", first_name,
              "\nLast Name: ", last_name,
              "\nTitle: ", title,
              "\nNationality: ", nationality,
              "\nAge: ", age,
              "\nNumber of Courses: ", numbercoursesspinbox,
              "\nNumber of Semesters: ", numberofsemesters,
              "\nRegistration Status:", registration)
    else:
        print("Error")

#===Frames==============================================================================================================
frame = Frame(window)
frame.pack()

user_info_frame = LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

courses_frame = LabelFrame(frame)
courses_frame.grid(row = 1, column = 0, sticky = "news", padx = 20, pady = 20)

terms_frame = LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row = 2, column = 0, sticky = "news", padx = 20, pady = 20)

#===Labels==============================================================================================================
first_name_label = Label(user_info_frame, text="First Name")
first_name_label.grid(row = 0, column = 0)

last_name_label = Label(user_info_frame, text="Last Name")
last_name_label.grid(row = 0, column = 1)

title_label = Label(user_info_frame, text="Title")
title_label.grid(row = 0, column = 2)

age_label = Label(user_info_frame, text="Age")
age_label.grid(row = 2, column = 0)

nationality_label = Label(user_info_frame, text="Nationality")
nationality_label.grid(row = 2, column = 1)

registered_label = Label(courses_frame, text="Registration Status")
registered_label.grid(row = 0, column = 0)

nummber_courses = Label(courses_frame, text="Completed Courses")
nummber_courses.grid(row = 0, column = 1)

semester_number = Label(courses_frame, text="Semesters")
semester_number.grid(row = 0, column = 2)

#===SpinBox=============================================================================================================
age_spinbox = Spinbox(user_info_frame, from_=18, to=110)
age_spinbox.grid(row = 3, column = 0)

nummber_courses_spinbox = Spinbox(courses_frame, from_=0, to="infinity")
nummber_courses_spinbox.grid(row = 1, column = 1)

semester_spinbox = Spinbox(courses_frame, from_=0, to="infinity")
semester_spinbox.grid(row = 1, column = 2)

#===ComboBox============================================================================================================
combobox = ttk.Combobox(user_info_frame, values=options)
combobox.grid(row = 1, column = 2)

nationality_combobox = ttk.Combobox(user_info_frame, values=continents)
nationality_combobox.grid(row = 3, column = 1)

#===CheckButton=========================================================================================================
registered_checkbutton = Checkbutton(courses_frame, text="Currently Registered", variable=v1, onvalue="Registered", offvalue="Not Registered")
registered_checkbutton.grid(row = 1, column = 0)

terms_checkbutton = Checkbutton(terms_frame, text="I accept the terms and conditions", variable=terms_and_conditions, onvalue="Accepted", offvalue="Not Accepted")
terms_checkbutton.grid(row = 0, column = 0)

#===Entry===============================================================================================================
first_name_entry = Entry(user_info_frame)
first_name_entry.grid(row = 1, column = 0)

last_name_entry = Entry(user_info_frame)
last_name_entry.grid(row = 1, column = 1)

#===Buttons=============================================================================================================
button = Button(frame, text="Enter Data", command=enter_data)
button.grid(row = 3, column = 0, sticky = "news", pady = 20, padx = 20)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(pady=5, padx=5)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()