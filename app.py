import tkinter as tk
from tkinter import messagebox
import threading
import time

class NoteTakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Mini Project: Threaded Task Manager")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # --- UI Header ---
        self.title_label = tk.Label(root, text="Task List", font=("Arial", 18, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # --- Input Section ---
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=20)
        self.task_entry.pack(side="left", padx=5)

        self.add_btn = tk.Button(self.input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_btn.pack(side="left")

        # --- Scrollable Task Area ---
        self.tasks_container = tk.Frame(root, bg="white", bd=1, relief="sunken")
        self.tasks_container.pack(pady=20, padx=20, fill="both", expand=True)

    def add_task(self):
        content = self.task_entry.get()
        if content.strip() == "":
            messagebox.showwarning("Input Error", "Please enter a task name.")
            return

        # Create a container for the individual task row
        task_row = tk.Frame(self.tasks_container, bg="white")
        task_row.pack(fill="x", anchor="w", padx=10, pady=5)

        # Checkbox variable
        status_var = tk.BooleanVar()
        
        # Checkbutton (The Note/Task)
        cb = tk.Checkbutton(task_row, text=content, variable=status_var, font=("Arial", 11),
                            bg="white", command=lambda: self.log_activity(content, status_var.get()))
        cb.pack(side="left")

        # Delete Button (To show resource deallocation)
        del_btn = tk.Button(task_row, text="Delete", fg="red", font=("Arial", 8),
                            command=lambda: self.delete_task(task_row, content))
        del_btn.pack(side="right")

        self.task_entry.delete(0, tk.END)
        self.log_activity(content, "CREATED")

    def delete_task(self, row, name):
        row.destroy()
        self.log_activity(name, "DELETED")

    def log_activity(self, task_name, status):
        """
        OS Concept: Multithreading. 
        We start a background thread to handle File I/O so the UI stays responsive.
        """
        # Mapping boolean to string if it's from the checkbox
        if isinstance(status, bool):
            status = "COMPLETED" if status else "PENDING"
            
        # Create and start a new thread
        save_thread = threading.Thread(target=self.file_worker, args=(task_name, status))
        save_thread.daemon = True # Thread closes when main app closes
        save_thread.start()

    def file_worker(self, name, status):
        """This function simulates a heavy OS Disk I/O operation."""
        try:
            # Simulated delay to show how threads work independently
            time.sleep(0.5) 
            with open("os_logs.txt", "a") as f:
                timestamp = time.strftime("%H:%M:%S")
                f.write(f"[{timestamp}] Task: {name} | Status: {status}\n")
            print(f"Background Thread: Successfully logged '{name}' as {status}")
        except Exception as e:
            print(f"File Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteTakerApp(root)
    root.mainloop()