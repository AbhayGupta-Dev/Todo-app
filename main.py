import customtkinter as ctk
import sqlite3
import tkinter as tk   # Needed for Listbox

# ---------------- Database Setup ----------------
def create_table():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---------------- Functions ----------------
def add_task():
    task = entry.get()
    if task.strip() != "":
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks(task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        entry.delete(0, ctk.END)
        show_tasks()

def delete_task():
    selected_index = task_listbox.curselection()
    if selected_index:
        selected_task = task_listbox.get(selected_index)
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
        conn.commit()
        conn.close()
        show_tasks()

def show_tasks():
    task_listbox.delete(0, tk.END)
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task FROM tasks")
    rows = cursor.fetchall()
    for row in rows:
        task_listbox.insert(tk.END, row[0])
    conn.close()

# ---------------- UI Setup ----------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("To-Do List")
app.geometry("800x500")
app.resizable(False, False)



labeltext=ctk.CTkLabel(app, text= "Task Manager",font = ("bold",35))
labeltext.pack (pady=10)
entry = ctk.CTkEntry(app, placeholder_text="Enter your task", width=600)
entry.pack(pady=10)

# Task Display Frame
listbox_frame = ctk.CTkFrame(app, width=600 , height=250)
listbox_frame.pack(pady=10)

# Use standard tkinter Listbox
task_listbox = tk.Listbox(listbox_frame, height=11, width=50, font=("Arial", 14))
task_listbox.pack()

# Buttons Frame
buttons_frame = ctk.CTkFrame(app, width=500, height=80, corner_radius=20)
buttons_frame.pack(pady=20)
buttons_frame.pack_propagate("False")

add_btn = ctk.CTkButton(buttons_frame, text="Add Task", font=("bold", 20) ,corner_radius=10, width=150, height=40,
                        hover_color="lightblue", text_color="white", command=add_task)
add_btn.pack(side="left", padx=20)

delete_btn = ctk.CTkButton(buttons_frame, text="Delete Task", font=("bold", 20) , corner_radius=10, width=150, height=40,
                           hover_color="lightblue", fg_color="red",
                           text_color="white",command=delete_task)
delete_btn.pack(side="right", padx=20)

# Initialize DB + Load Tasks
create_table()
show_tasks()

app.mainloop()
