import tkinter as tk
from tkinter import filedialog, messagebox

def add_task():
    task = task_entry.get()
    if task:
        listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    try:
        selected_task = listbox.curselection()[0]
        listbox.delete(selected_task)
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def save_tasks(file_type):
    file_extension = "txt" if file_type == "txt" else "md"
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}",
                                             filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            for task in listbox.get(0, tk.END):
                file.write(f"- {task}\n")
        messagebox.showinfo("Success", "Tasks saved successfully!")

# GUI 설정
if __name__=="__main__":
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x400")

    task_entry = tk.Entry(root, width=40)
    task_entry.pack(pady=10)

    add_button = tk.Button(root, text="Add Task", command=add_task)
    add_button.pack()

    listbox = tk.Listbox(root, width=50, height=15)
    listbox.pack(pady=10)

    remove_button = tk.Button(root, text="Remove Task", command=remove_task)
    remove_button.pack()

    save_txt_button = tk.Button(root, text="Save as .txt", command=lambda: save_tasks("txt"))
    save_txt_button.pack()

    save_md_button = tk.Button(root, text="Save as .md", command=lambda: save_tasks("md"))
    save_md_button.pack()

    root.mainloop()
