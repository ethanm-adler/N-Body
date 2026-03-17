from turtle import Turtle
class body(Turtle):
    def __init__(self, size, x, y, mass, vx, vy):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.size = float(size)
        self.shapesize(stretch_wid=float(size), stretch_len=float(size))
        self.fillcolor("blue")
        self.penup()
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.mass = float(mass)
