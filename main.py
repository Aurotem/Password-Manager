from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    generated_password = password_symbols + password_numbers + password_letters
    shuffle(generated_password)

    password = "".join(generated_password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = url_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showerror(title="Oops!", message="Some fields are empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f" Website: {website}\n"
                                                              f" Email: {email}\n"
                                                              f" Password: {password}\n"
                                                              f" Are you sure that given information is true?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading the old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating the old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                url_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = url_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops!", message="There is no data file.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f" Email: {email}\n"
                                                       f" Password: {password}\n")
        else:
            messagebox.showerror(title="Oops!", message="Entry Not Found!")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
url_label = Label(text="Website:")
url_label.grid(row=1, column=0)
email_label = Label(text="E-mail:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
url_entry = Entry(width=25)
url_entry.grid(row=1, column=1)
url_entry.focus()
email_entry = Entry(width=45)
email_entry.insert(0, "melihcan@email.com")
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password, width=15)
generate_button.grid(row=3, column=2, sticky="nsew")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=0, columnspan=3)
find_button = Button(text="Find", command=find_password, width=15)
find_button.grid(column=2, row=1)

window.mainloop()
