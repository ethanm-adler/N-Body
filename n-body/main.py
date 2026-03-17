from body_class import body
from turtle import Screen
import json
import math
from tkinter import *

s = 1.989 * (10 ** 30)
e = 5.92 * (10 ** 24)
es = 30000
m = 7.3 * (10 ** 22)
ms = 1000
dm = 3.84 * (10 ** 8)
ds = 1.47 * (10 ** 11)

bodies = {}
current_body_index = [1]


def insert_values(case):
    with open("data.json", "r") as file:
        data = json.load(file)

    case_data = data[case]
    num_bodies = len([k for k in case_data.keys() if k != "constants"])

    if current_body_index[0] > num_bodies:
        current_body_index[0] = 1
        return

    i = current_body_index[0]
    key = f"body{i}" if f"body{i}" in case_data else f"bd{i}"

    bodsize.delete(0, END)
    bodsize.insert(0, case_data[key]["size"])
    bodx.delete(0, END)
    bodx.insert(0, case_data[key]["x"])
    bodyy.delete(0, END)
    bodyy.insert(0, case_data[key]["y"])
    bodm.delete(0, END)
    bodm.insert(0, case_data[key]["mass"])
    bodvx.delete(0, END)
    bodvx.insert(0, case_data[key]["vx"])
    bodvy.delete(0, END)
    bodvy.insert(0, case_data[key]["vy"])

    if i == 1:
        cc.delete(0, END)
        cc.insert(0, case_data["constants"]["cc"])
        dtt.delete(0, END)
        dtt.insert(0, case_data["constants"]["dtt"])

    current_body_index[0] += 1


def search_case():
    window1 = Tk()
    window1.title("Load Case")
    window1.minsize(width=200, height=80)
    window1.config(padx=10, pady=10)
    l = Label(window1, text="Case name:")
    l.grid(column=0, row=0)
    name = Entry(window1, width=10)
    name.grid(column=1, row=0)
    name.focus()

    def load_next():
        current_body_index[0] = 1
        insert_values(name.get())

    def load_body():
        insert_values(name.get())

    bl = Button(window1, text="Load First Body", command=load_next)
    bl.grid(column=0, row=1, columnspan=2, pady=5)
    bb = Button(window1, text="Load Next Body", command=load_body)
    bb.grid(column=0, row=2, columnspan=2)
def save(case="memory"):
    with open("data.json", "r") as file:
        data = json.load(file)

    entries = {
        "size": [bodsize1, bodsize2, bodsize3],
        "x": [bodx1, bodx2, bodx3],
        "y": [body1, body2, body3],
        "mass": [bodm1, bodm2, bodm3],
        "vx": [bodvx1, bodvx2, bodvx3],
        "vy": [bodvy1, bodvy2, bodvy3],
    }

    for i in range(1, 4):
        for key, values in entries.items():
            data[case][f"body{i}"][key] = values[i - 1].get()
    data[case]["constants"]["cc"] = cc.get()
    data[case]["constants"]["dtt"] = dtt.get()

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



def save_values(name):

    list = ["size", "x", "y", "mass", "vx", "vy"]
    d = {}
    for key, value in bodies.items():
        d[key] = {}
        for item in list:
            d[key][item] = getattr(value, item)
    d["constants"] = {}
    d["constants"]["cc"] = cc.get()
    d["constants"]["dtt"] = dtt.get()

    with open("data.json", "r") as file:
        data = json.load(file)

    data[name] = d
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def save_case():
    window2 = Tk()
    window2.title("Save Case")
    window2.minsize(width=75, height=50)
    window2.config(padx=10, pady=10)
    l = Label(window2, text="Title:")
    l.grid(column=0, row=0)
    name = Entry(window2, width=6)
    name.grid(column=1, row=0)
    name.focus()
    bb = Button(window2, text="Save", command=lambda: save_values(name.get()))
    bb.grid(column=0, row=1, columnspan=2)

def add_body():
    c = 100 / int(eval(cc.get()))
    n = f"bd{len(bodies)+1}"
    bodies[n] = body(bodsize.get(), eval(bodx.get()), eval(bodyy.get()), eval(bodm.get()), eval(bodvx.get()), eval(bodvy.get()))
    bodies[n].goto(bodies[n].x*c, bodies[n].y*c)
    bodies[n].pendown()
    screen.update()

def calculate_force(m1, m2, dx, dy):
    g = 6.673 * (10 ** (-11))
    r = math.sqrt(dx ** 2 + dy ** 2)
    f = -(g * m1 * m2) / r ** 2
    fx = f * (dx / r)
    fy = f * (dy / r)
    return fx, fy
def compute():
    print(bodies["bd1"].mass)
    c = 100 / eval(cc.get())
    dt = eval(dtt.get())
    save_values("memory")

    while True:
        for i, bd in bodies.items():
            fx = 0
            fy = 0
            for j, other_bd in bodies.items():
                if i != j:
                    fx1, fy1 = calculate_force(bd.mass, other_bd.mass, bd.x - other_bd.x, bd.y - other_bd.y)
                    fx += fx1
                    fy += fy1

            ax = fx / bd.mass
            ay = fy / bd.mass
            bd.vx += ax * dt
            bd.vy += ay * dt
            bd.x += bd.vx * dt
            bd.y += bd.vy * dt
            bd.goto(bd.x * c, bd.y * c)
            screen.update()



window = Tk()
window.title("Body information")
window.geometry("490x230+75+0")
window.config(padx=20, pady=20)



l1 = Label(text="Size(0.5-10)")
l1.grid(column=1, row=0)
l1 = Label(text="X-cord")
l1.grid(column=2, row=0)
l1 = Label(text="Y-cord")
l1.grid(column=3, row=0)
l1 = Label(text="Mass")
l1.grid(column=4, row=0)
l1 = Label(text="Velocity X")
l1.grid(column=5, row=0)
l1 = Label(text="Velocity Y")
l1.grid(column=6, row=0)
bod = Label(text="Body:")
bod.grid(column=0, row=1)

bodsize = Entry(width=6)
bodsize.grid(column=1, row=1)
bodsize.focus()
bodx = Entry(width=6)
bodx.grid(column=2, row=1)
bodyy = Entry(width=6)
bodyy.grid(column=3, row=1)
bodm = Entry(width=6)
bodm.grid(column=4, row=1)
bodvx = Entry(width=6)
bodvx.grid(column=5, row=1)
bodvy = Entry(width=6)
bodvy.grid(column=6, row=1)



# insert_values("memory")
ab = Button(text="Add Body", command=add_body)
ab.grid(column=2, row=2, columnspan=3, pady=10)
b = Button(text="Compute", command=compute, width=10)
b.grid(column=2, row=3, columnspan=3)

window1 = Tk()
window1.title("Constants")

window1.config(padx=10, pady=10)
window1.geometry("230x80+75+230")
lc = Label(window1, text="Meters per 100 Pixels:")
lc.grid(column=0, row=0, columnspan=1)
cc = Entry(window1, width=6)
cc.grid(column=1, row=0)




dtl = Label(window1, text="Time in Seconds:")
dtl.grid(column=0, row=1, columnspan=1)
dtt = Entry(window1, width=6)
dtt.grid(column=1, row=1)
screen = Screen()

screen.bgcolor("white")
screen.tracer(0)
screen._root.geometry("800x800-740+400")
sc = Button(text="Save Case", command=save_case)
sc.grid(column=5, row=5, columnspan=2)
sec = Button(text="Search Case", command=search_case)
sec.grid(column=0, row=5, columnspan=2)
window.mainloop()

