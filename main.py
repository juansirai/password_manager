from tkinter import *
import string
import random
from tkinter import messagebox
import json

FONT_NAME = 'Arial'
FONT_COLOR = "#F0F0F0"
BACKGROUND = "#000033"
SEP_COLOR = "#e28743"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    entry_password.delete(0, END)
    # default values
    num_upper = 0
    num_special = 0
    num_dig = 0
    # checking if the user set rules
    if entry_upper.get():
        num_upper = int(entry_upper.get())
    if entry_special.get():
        num_special = int(entry_special.get())
    if entry_numbers.get():
        num_dig = int(entry_numbers.get())
    if not(entry_lenght.get()):
        messagebox.showerror(title="Error", message="Select a length")
    elif int(entry_lenght.get()) < (num_dig+num_special+num_upper):
        messagebox.showerror(title="Error", message="Rules greater than total length")
    else:
        long = int(entry_lenght.get()) - num_upper - num_dig - num_special
        upper = string.ascii_uppercase
        dig = string.digits
        special = string.punctuation
        lower = string.ascii_lowercase
        result = ''.join(random.choice(upper) for i in range(num_upper)) + \
                 ''.join(random.choice(dig) for i in range(num_dig)) + \
                 ''.join(random.choice(lower) for i in range(long)) + \
                 ''.join(random.choice(special) for i in range(num_special))
        result = ''.join(random.sample(result, len(result)))
        entry_password.insert(index=0, string=result)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pass():
    website = entry_website.get()
    email = entry_userName.get()
    password = entry_password.get()
    check = True
    if not website:
        messagebox.showerror(title="Error", message="Enter Website")
    elif not email:
        messagebox.showerror(title="Error", message="Enter Email")
    elif not password:
        messagebox.showerror(title="Error", message="Enter Password")
    else:
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }
        try:
            with open("claves.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("claves.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            try:
                data[website]
            except KeyError:
                data.update(new_data)
                with open("claves.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            else:
                check = messagebox.askyesno(message="Website already saved, do you want to update? ")
                if check:
                    data.update(new_data)
                    with open("claves.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            if check:
                messagebox.showinfo(message=f"Saved correctly:\nWebsite: {website} \nPass: {password}")

# -------------------------------HIDE/SHOW PASS--------------------------#


hide = True


def hide_show():
    global hide
    if hide:
        entry_password.config(show='*')
    else:
        entry_password.config(show='')
    hide = not hide

# ----------------------------SEARCH----------------------------------- #


def search():
    web = entry_website.get()
    if not web:
        messagebox.showerror(message="Please enter a website")
    else:
        try:
            with open("claves.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(message="Not file created")
        else:
            try:
                password = data[web]["password"]
                email = data[web]["email"]
            except KeyError:
                messagebox.showerror(message="Website not found")
            else:
                messagebox.showinfo(title=web, message=f"Website: {web}\n"
                                                       f"User: {email}\n"
                                                       f"Pass: {password}")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, height=800, width=600, bg=BACKGROUND)

canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
logo = PhotoImage(file='logo1.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

label_settings = Label(text="<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>SETTINGS<<>><<>><<>><<>><<>>\
                            <<>><<>><<>><<>><<>><<>><<>><<>>",
                       width=60, font=(FONT_NAME, 10, "bold"),
                       fg=SEP_COLOR, bg=BACKGROUND)
label_settings.grid(column=0, row=1, columnspan=5)

label_div = Label(text="<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>\
                        <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>",
                  width=60, font=(FONT_NAME, 10, "bold"),
                  fg=SEP_COLOR, bg=BACKGROUND)
label_div.grid(column=0, row=4, columnspan=5)

label_lenght = Label(text="Password lenght", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_lenght.grid(column=0, row=2)

entry_lenght = Entry(width=25)
entry_lenght.insert(index=0, string='8')
entry_lenght.grid(column=1, row=2, columnspan=1)

label_upper = Label(text="# UpperCase", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_upper.grid(column=0, row=3)

entry_upper = Entry(width=25)
entry_upper.insert(index=0, string='1')
entry_upper.grid(column=1, row=3)

label_special = Label(text="# SpecialChar", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_special.grid(column=2, row=2)

entry_special = Entry(width=5)
entry_special.insert(index=0, string='1')
entry_special.grid(column=3, row=2)

label_numbers = Label(text='# Numbers', font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_numbers.grid(column=2, row=3)

entry_numbers = Entry(width=5)
entry_numbers.insert(index=0, string='1')
entry_numbers.grid(column=3, row=3)

label_website = Label(text="Website:", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_website.grid(column=0, row=5)

entry_website = Entry(width=25)
entry_website.focus()
entry_website.grid(column=1, row=5)


label_email = Label(text="Email / UserName:", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_email.grid(column=0, row=6)

default_email = "your_user_name@some_domain.com"
entry_userName = Entry(width=25)
entry_userName.insert(index=0, string=default_email)
entry_userName.grid(column=1, row=6)


label_password = Label(text="Password:", font=(FONT_NAME, 10), justify='left', bg=BACKGROUND, fg=FONT_COLOR)
label_password.grid(column=0, row=7)

entry_password = Entry(width=25)
entry_password.grid(column=1, row=7)

generate_button = Button(text="Generate", command=generate_password)
generate_button.grid(column=3, row=7)

add_button = Button(width=20, text="Add", command=save_pass, bg=SEP_COLOR)
add_button.grid(column=1, row=8)

hidde_button = Button(text="Show/Hide", command=hide_show)
hidde_button.grid(column=2, row=7)

search_button = Button(text="Search", width=18, command=search)
search_button.grid(column=2, row=5, columnspan=2)

window.mainloop()
