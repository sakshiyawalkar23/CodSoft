from tkinter import *
import math

root = Tk()
root.title('Neo Calculator')
root.geometry('360x540')
root.config(bg='#0f172a')
root.resizable(False, False)

expr = ''
history = []

# ---------- functions ----------
def set_text(value):
    display_var.set(value)


def tap(v):
    global expr
    expr += str(v)
    set_text(expr)


def clear_all():
    global expr
    expr = ''
    set_text('0')


def erase():
    global expr
    expr = expr[:-1]
    set_text(expr if expr else '0')


def solve():
    global expr
    try:
        value = eval(expr)
        if isinstance(value, float):
            value = round(value, 10)
        history.append(f'{expr} = {value}')
        expr = str(value)
        set_text(expr)
    except:
        expr = ''
        set_text('Error')


def square():
    global expr
    try:
        value = eval(expr) ** 2
        expr = str(round(value,10))
        set_text(expr)
    except:
        set_text('Error')
        expr = ''


def root_val():
    global expr
    try:
        value = math.sqrt(eval(expr))
        expr = str(round(value,10))
        set_text(expr)
    except:
        set_text('Error')
        expr = ''


def percent():
    global expr
    try:
        value = eval(expr) / 100
        expr = str(round(value,10))
        set_text(expr)
    except:
        set_text('Error')
        expr = ''


def show_history():
    top = Toplevel(root)
    top.title('Recent Calculations')
    top.geometry('300x350')
    top.config(bg='#111827')

    Label(top, text='History', font=('Arial', 18, 'bold'), bg='#111827', fg='white').pack(pady=10)
    box = Listbox(top, font=('Consolas', 12), bg='#1f2937', fg='white', bd=0)
    box.pack(fill=BOTH, expand=True, padx=12, pady=12)

    for item in reversed(history):
        box.insert(END, item)

# ---------- display ----------
Label(root, text='Calculator', font=('Arial', 14, 'bold'), bg='#0f172a', fg='#94a3b8').pack(anchor='w', padx=18, pady=(14,0))

frame = Frame(root, bg='#0f172a')
frame.pack(fill='both', expand=True, padx=14, pady=10)

display_var = StringVar(value='0')
Entry(frame, textvariable=display_var, font=('Consolas', 28, 'bold'), justify='right', bd=0,
      bg='#111827', fg='white').grid(row=0, column=0, columnspan=4, sticky='nsew', pady=(0,12), ipady=18)

# ---------- buttons ----------
btns = [
    ('AC',1,0,clear_all), ('⌫',1,1,erase), ('%',1,2,percent), ('🕘',1,3,show_history),
    ('7',2,0,lambda: tap('7')), ('8',2,1,lambda: tap('8')), ('9',2,2,lambda: tap('9')), ('÷',2,3,lambda: tap('/')),
    ('4',3,0,lambda: tap('4')), ('5',3,1,lambda: tap('5')), ('6',3,2,lambda: tap('6')), ('×',3,3,lambda: tap('*')),
    ('1',4,0,lambda: tap('1')), ('2',4,1,lambda: tap('2')), ('3',4,2,lambda: tap('3')), ('-',4,3,lambda: tap('-')),
    ('0',5,0,lambda: tap('0')), ('.',5,1,lambda: tap('.')), ('√',5,2,root_val), ('+',5,3,lambda: tap('+')),
    ('x²',6,0,square)
]

for text,r,c,cmd in btns:
    span = 1
    bg = '#1e293b'
    fg = 'white'
    if text in ['÷','×','-','+']:
        bg = '#334155'
    if text in ['AC','⌫','%','🕘']:
        bg = '#475569'
    Button(frame, text=text, command=cmd, font=('Arial', 16, 'bold'), bd=0,
           bg=bg, fg=fg, activebackground='#64748b', activeforeground='white')\
        .grid(row=r, column=c, sticky='nsew', padx=5, pady=5, ipady=14)

Button(frame, text='=', command=solve, font=('Arial', 18, 'bold'), bd=0,
       bg='#22c55e', fg='white', activebackground='#16a34a').grid(row=6, column=1, columnspan=3, sticky='nsew', padx=5, pady=5, ipady=14)

for i in range(7):
    frame.rowconfigure(i, weight=1)
for j in range(4):
    frame.columnconfigure(j, weight=1)

root.mainloop()