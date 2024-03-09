from tkinter import *
from tkinter import ttk, messagebox
import paperclip
import random
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to generate the password
def generate_password():
    characters = get_character_set()
    password = ''.join(random.choice(characters) for _ in range(passlen.get()))
    passstr.set(password)
    update_strength_indicator()
    save_to_history(password)

# Function to copy the password to the clipboard
def copy_to_clipboard():
    random_password = passstr.get()
    pyperclip.copy(random_password)

# Function to get the character set based on complexity options
def get_character_set():
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    special_characters = '!@#$%^&*()`.'

    character_set = lowercase
    if include_uppercase.get():
        character_set += uppercase
    if include_digits.get():
        character_set += digits
    if include_special_chars.get():
        character_set += special_characters

    return character_set

# Function to update the password strength indicator
def update_strength_indicator():
    password = passstr.get()
    strength = calculate_password_strength(password)
    strength_label.config(text=f"Strength: {strength}")

# Function to calculate password strength (a simple example, can be improved)
def calculate_password_strength(password):
    if len(password) < 8:
        return "Weak"
    elif len(password) < 12:
        return "Medium"
    else:
        return "Strong"

# Function to save the generated password to history
def save_to_history(password):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_listbox.insert(0, f"{timestamp}: {password}")

# Function to save the password history to a file
def save_history_to_file():
    with open("password_history.txt", "a") as file:
        file.write("\n".join(history_listbox.get(0, END)) + "\n")
    messagebox.showinfo("Saved", "Password history saved to 'password_history.txt'")

# Function to toggle show/hide password
def toggle_show_password():
    if show_password_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

# Function to toggle show/hide password history
def toggle_show_history():
    if show_history_var.get():
        history_listbox.grid(row=9, column=0, columnspan=4, pady=(0, 10), sticky=W+E)
    else:
        history_listbox.grid_forget()

# Function to send the generated password to an email address
def send_password_to_email():
    try:
        # Update these variables with your email credentials and recipient's email address
        sender_email = "sagardhapate16@gmail.com"
        sender_password = "BOLOJAISHREERAM"
        recipient_email = "sagardhapate16@gmail.com"

        subject = "Generated Password"
        body = f"Here is your generated password: {passstr.get()}"

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        messagebox.showinfo("Email Sent", "Password sent successfully to the specified email address.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Initializing the tkinter
root = Tk()
root.title("Password Generator")
root.geometry("600x400")

# Canvas for gradient background
canvas = Canvas(root, width=600, height=400, highlightthickness=0)
canvas.create_rectangle(0, 0, 600, 400, fill="#b3e0ff", outline="#b3e0ff")  # Light blue gradient background
canvas.grid(row=0, column=0, sticky=N+S+E+W)

# Creating a card-like frame
frame = ttk.Frame(root, padding="10", style="TFrame")
frame.grid(row=0, column=0, padx=20, pady=20, sticky=(N, S, E, W))

# Declaring variables
passstr = StringVar()
passlen = IntVar()
passlen.set(8)  # Setting default password length to 8
include_uppercase = BooleanVar()
include_digits = BooleanVar()
include_special_chars = BooleanVar()
show_password_var = BooleanVar()
show_history_var = BooleanVar()

# Styling using ttk styles
style = ttk.Style()
style.configure("TFrame", background="#b3e0ff")
style.configure("TLabel", font=("calibri", 14), background="#b3e0ff", foreground="#333")
style.configure("TButton", font=("calibri", 12, "bold"), background="#4CAF50", foreground="white")

# Widgets
label_title = ttk.Label(frame, text="Password Generator", style="TLabel")
label_title.grid(row=0, column=0, columnspan=5, pady=(0, 10))

label_length = ttk.Label(frame, text="Enter password length:", style="TLabel")
label_length.grid(row=1, column=0, pady=(0, 5), sticky=W)

entry_length = ttk.Entry(frame, textvariable=passlen, justify=CENTER)
entry_length.grid(row=1, column=1, pady=(0, 10), sticky=W+E)

label_options = ttk.Label(frame, text="Password Complexity Options:", style="TLabel")
label_options.grid(row=2, column=0, columnspan=4, pady=(0, 5), sticky=W)

check_uppercase = ttk.Checkbutton(frame, text="Uppercase", variable=include_uppercase)
check_uppercase.grid(row=3, column=0, pady=(0, 5), sticky=W)

check_digits = ttk.Checkbutton(frame, text="Digits", variable=include_digits)
check_digits.grid(row=3, column=1, pady=(0, 5), sticky=W)

check_special_chars = ttk.Checkbutton(frame, text="Special Characters", variable=include_special_chars)
check_special_chars.grid(row=3, column=2, pady=(0, 5), sticky=W)

show_password_checkbox = ttk.Checkbutton(frame, text="Show Password", variable=show_password_var, command=toggle_show_password)
show_password_checkbox.grid(row=3, column=3, pady=(0, 5), sticky=W)

show_history_checkbox = ttk.Checkbutton(frame, text="Show Password History", variable=show_history_var, command=toggle_show_history)
show_history_checkbox.grid(row=3, column=4, pady=(0, 5), sticky=W)

button_generate = ttk.Button(frame, text="Generate Password", command=generate_password, style="TButton")
button_generate.grid(row=4, column=0, columnspan=4, pady=(0, 10))

entry_password = ttk.Entry(frame, textvariable=passstr, state="readonly", justify=CENTER, show="*")
entry_password.grid(row=5, column=0, columnspan=4, pady=(0, 10), sticky=W+E)

button_copy = ttk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard, style="TButton")
button_copy.grid(row=6, column=0, columnspan=4)

# Password strength indicator
strength_label = ttk.Label(frame, text="Strength: None", style="TLabel")
strength_label.grid(row=7, column=0, columnspan=4, pady=(10, 0), sticky=W)

# Password history
history_label = ttk.Label(frame, text="Password History:", style="TLabel")
history_label.grid(row=8, column=0, columnspan=4, pady=(10, 5), sticky=W)

history_listbox = Listbox(frame, selectmode=SINGLE, height=5)
history_listbox.grid(row=9, column=0, columnspan=4, pady=(0, 10), sticky=W+E)

# Save history to file button
save_button = ttk.Button(frame, text="Save History to File", command=save_history_to_file, style="TButton")
save_button.grid(row=10, column=0, columnspan=4, pady=(0, 10))

# Email password button
email_button = ttk.Button(frame, text="Email Password", command=send_password_to_email, style="TButton")
email_button.grid(row=11, column=0, columnspan=4, pady=(0, 10))

# Configure row and column weights to make the frame expandable
frame.grid_rowconfigure(5, weight=1)
frame.grid_columnconfigure((0,1,2,3,4), weight=1)

root.mainloop()
