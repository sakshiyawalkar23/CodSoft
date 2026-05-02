from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('To-Do List Manager')
root.geometry('420x560')
root.config(bg='#0f172a')
root.resizable(False, False)

tasks = []

# ---------- functions ----------
def refresh_list():
    listbox.delete(0, END)
    for i, task in enumerate(tasks, start=1):
        listbox.insert(END, f"{i}. {task}")


def add_task():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        entry.delete(0, END)
        refresh_list()
    else:
        messagebox.showwarning('Warning', 'Enter a task first.')


def delete_task():
    try:
        idx = listbox.curselection()[0]
        tasks.pop(idx)
        refresh_list()
    except:
        messagebox.showwarning('Warning', 'Select a task to delete.')


def complete_task():
    try:
        idx = listbox.curselection()[0]
        if not tasks[idx].startswith('✔ '):
            tasks[idx] = '✔ ' + tasks[idx]
        refresh_list()
    except:
        messagebox.showwarning('Warning', 'Select a task to mark complete.')


def update_task():
    try:
        idx = listbox.curselection()[0]
        popup = Toplevel(root)
        popup.title('Update Task')
        popup.geometry('320x160')
        popup.config(bg='#0f172a')
        popup.resizable(False, False)

        Label(popup, text='Enter updated task', font=('Arial', 13, 'bold'), bg='#0f172a', fg='white').pack(pady=15)

        new_entry = Entry(popup, font=('Arial', 12), bd=0, bg='#e2e8f0', fg='black')
        new_entry.pack(fill='x', padx=20, ipady=8)
        new_entry.insert(0, tasks[idx].replace('✔ ', ''))
        new_entry.focus()

        def save_update():
            text = new_entry.get().strip()
            if text:
                tasks[idx] = text
                refresh_list()
                popup.destroy()
            else:
                messagebox.showwarning('Warning', 'Task cannot be empty.')

        Button(popup, text='OK', command=save_update, font=('Arial', 11, 'bold'), width=10,
               bg='#22c55e', fg='white', bd=0).pack(pady=18)
    except:
        messagebox.showwarning('Warning', 'Select a task to update.')

# ---------- UI ----------
Label(root, text='To-Do List', font=('Arial', 22, 'bold'), bg='#0f172a', fg='white').pack(pady=15)

entry = Entry(root, font=('Arial', 14), bd=0, bg='#e2e8f0', fg='black')
entry.pack(fill='x', padx=20, ipady=10)

btn_frame = Frame(root, bg='#0f172a')
btn_frame.pack(pady=15)

buttons = [
    ('Add', add_task),
    ('Update', update_task),
    ('Complete', complete_task),
    ('Delete', delete_task)
]

for i, (txt, cmd) in enumerate(buttons):
    Button(btn_frame, text=txt, command=cmd, font=('Arial', 11, 'bold'), width=9,
           bg='#2563eb', fg='white', bd=0, activebackground='#1d4ed8').grid(row=0, column=i, padx=5)

list_frame = Frame(root, bg='#0f172a')
list_frame.pack(fill='both', expand=True, padx=20, pady=10)

scroll = Scrollbar(list_frame)
scroll.pack(side=RIGHT, fill=Y)

listbox = Listbox(list_frame, font=('Arial', 13), bg='#111827', fg='white', bd=0,
                  selectbackground='#22c55e', yscrollcommand=scroll.set)
listbox.pack(fill='both', expand=True)
scroll.config(command=listbox.yview)

Label(root, text='Tip: Select a task before Update / Complete / Delete',
      font=('Arial', 10), bg='#0f172a', fg='#94a3b8').pack(pady=8)

root.mainloop()
