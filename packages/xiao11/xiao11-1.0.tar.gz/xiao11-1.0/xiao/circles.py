import turtle
t = turtle.Pen()
my_clors = ("red","green","yellow","black")
t.width(5)
t.speed(1)
for i in range(10):
    t.penup()
    t.goto(0,-i * 10)
    t.pendown()
    t.color(my_clors[i%len(my_clors)])
    t.circle(15+i*10)
turtle.done()