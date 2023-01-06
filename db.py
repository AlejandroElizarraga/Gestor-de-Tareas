from tkinter import *
import sqlite3

app = Tk()
app.title('To-do List')
app.geometry('400x500')
app.configure(background='#333333')
cnet = sqlite3.connect('todo.db')

c = cnet.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")
cnet.commit()

def removeTodo(id):
    def _remove():
        c.execute(
                "DELETE FROM todo WHERE id = ?",(id, ))
        cnet.commit()
        render_Todos()
    return _remove
# Currying!
def complete(id):
    def _completed():
        todo = c.execute("SELECT * FROM todo Where id = ?",(id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id  =?", (not todo[3], id))
        cnet.commit
        render_Todos()
        
    return _completed
    # Esta funcion _completed es como alternativa
    # al Lambda ya que este toma el ultimo del valor del id del
    # ciclo for de los renders

def render_Todos():
    rows = c.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0,len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else '#ffffff'
        cb = Checkbutton(frame, text=description,background='#333333',fg=color, width=42, anchor='w', command=complete(id))
        cb.grid(row=i,column=0,sticky='w')
        btn = Button(frame, text = 'Eliminar',command=removeTodo(id))
        btn.grid(row=i,column=1,pady=5)
        cb.select() if completed else cb.deselect

def addTodo():
    todo = e.get()
    if todo:
        c.execute("""
                INSERT INTO todo (description, completed) VALUES (?, ?)
                """,(todo, False))
        cnet.commit()
        e.delete(0,END)
        render_Todos()
    else:
        pass


l = Label(app,text='Tarea')
l.grid(row=0,column=0, padx=5)

e=Entry(app,widt=40)
e.grid(row=0, column=1, padx=5)

btn = Button(app, text = 'Agregar',command=addTodo)
btn.grid(row=0,column=2,pady=3)

frame = LabelFrame(app,text='My To-does', padx=5,pady=5, background='#333333')
frame.grid(row=1, column=0,columnspan=3,sticky='nswe',padx=5)

e.focus()
app.bind('<Return>',lambda x:addTodo())
render_Todos()
app.mainloop()