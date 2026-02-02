import turtle
from turtle import Screen

import pandas

screen = turtle.Screen()

screen.title("U.S. states Game")
image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)

# def get_mouse_click_coor(x,y):
#     print(x, y)
#
# turtle.onscreenclick(get_mouse_click_coor)
#
# turtle.mainloop()
#
# screen.exitonclick()


data = pandas.read_csv("50_states.csv")

all_states = data.state.to_list()

guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 correct", prompt="Enter state name?").title()
    print(answer_state)

    if answer_state == "Exit":

        missing_states = [i for i in all_states if i not in guessed_states]

        # list_comprehension_syntax
        # new_list = [new_item for item in list if test]

        """
        missing_states = []
        for i in all_states:
            if i not in guessed_states:
                missing_states.append(i)
        """
        print(missing_states)

        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break # quit the screen

    if answer_state in all_states:
        guessed_states.append(answer_state)
        # Create a turtle to write the name of the state at the state's X and Y co-ordinate
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()  # so it can't drag and draw
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())

        t.write(answer_state)
        # t.write(state_data.state.item())

# screen.exitonclick()


# states_to_learn.csv

