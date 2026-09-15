import turtle
t = turtle.Turtle()
t.speed(1)
t.color("red", "black")
t.shape("turtle")
t.fillcolor("blue")
t.begin_fill()

for i in range(4):
    t.forward(100)
    t.left(90)

t.end_fill()






turtle.done()