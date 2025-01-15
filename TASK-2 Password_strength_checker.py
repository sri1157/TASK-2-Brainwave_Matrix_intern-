import tkinter as tk
from tkinter import ttk, filedialog
import re
import random
import string

# Function to assess password strength
def assess_password_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Uppercase, lowercase, numbers, special characters
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g., !, @, #).")

    # Repetitive/sequential patterns
    if not re.search(r'(.)\1{2,}', password):  # Checks for repeated characters
        score += 1
    else:
        feedback.append("Avoid repeated characters.")

    if not re.search(r'123|abc|password|qwerty|letmein|iloveyou|welcome', password.lower()):  # Expanded blacklist
        score += 2
    else:
        feedback.append("Avoid common patterns like '123', 'abc', or 'password'.")

    # Password strength evaluation
    if score <= 3:
        strength = "Weak"
        color = "red"
    elif score <= 5:
        strength = "Moderate"
        color = "orange"
    elif score <= 7:
        strength = "Strong"
        color = "blue"
    else:
        strength = "Very Strong"
        color = "green"

    return strength, feedback, score, color

# Function to generate a random password
def generate_password():
    """Generate a strong random password."""
    length = 12  # Default length for generated passwords
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

# Function to update feedback in real-time
def update_feedback(event=None):
    """Update the feedback and progress bar in real-time."""
    password = password_entry.get()
    strength, feedback, score, color = assess_password_strength(password)

    # Update progress bar and label
    progress_bar['value'] = score * 10  # Max score is 10
    strength_label.config(text=f"Strength: {strength}", fg=color)

    # Update feedback tips
    feedback_list.delete(0, tk.END)  # Clear previous feedback
    for tip in feedback:
        feedback_list.insert(tk.END, tip)

# Function to insert generated password
def insert_generated_password():
    """Insert a generated password into the entry field."""
    generated_password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated_password)
    update_feedback()

# Function to toggle password visibility
def toggle_password_visibility():
    """Toggle the visibility of the password."""
    if show_password_var.get():
        password_entry.config(show="")  # Show password
    else:
        password_entry.config(show="*")  # Mask password

# Function to export feedback to a file
def export_feedback():
    """Export feedback and password to a file."""
    password = password_entry.get()
    feedback = feedback_list.get(0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(f"Password: {password}\n\n")
            file.write("Feedback:\n")
            for tip in feedback:
                file.write(f"- {tip}\n")

# GUI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x500")

# Password Entry
tk.Label(root, text="Enter Password:").pack(pady=10)
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)
password_entry.bind("<KeyRelease>", update_feedback)

# View Password Checkbox
show_password_var = tk.BooleanVar()
show_password_checkbox = tk.Checkbutton(
    root, text="Show Password", variable=show_password_var, command=toggle_password_visibility
)
show_password_checkbox.pack()

# Progress Bar
progress_bar = ttk.Progressbar(root, length=300, maximum=100)
progress_bar.pack(pady=10)

# Strength Label
strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12))
strength_label.pack(pady=5)

# Feedback List
tk.Label(root, text="Suggestions:").pack(pady=10)
feedback_list = tk.Listbox(root, width=60, height=6)
feedback_list.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

generate_button = tk.Button(button_frame, text="Generate Strong Password", command=insert_generated_password)
generate_button.grid(row=0, column=0, padx=10)

export_button = tk.Button(button_frame, text="Export Feedback", command=export_feedback)
export_button.grid(row=0, column=1, padx=10)

# Run the application
root.mainloop()
