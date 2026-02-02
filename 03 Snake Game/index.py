from turtle import Screen
from snake import Snake
from scoreboard import *
import time
from food import Food

screen = Screen()
screen.setup(width=900, height=550)
screen.bgcolor("black")
screen.title("SnaPy")
screen.tracer(0)  # Disable automatic updates

"""
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
segments = []
"""
# 1 create a snake body !

# segment_1 = Turtle("square")
# segment_1.color("white")
#
# segment_2 = Turtle("square")
# segment_2.color("white")
# segment_2.goto(-20, 0)
#
# segment_3 = Turtle("square")
# segment_3.color("white")
# segment_3.goto(-40, 0)


"""
for position in starting_positions:
    new_segment = Turtle("square")
    new_segment.color("white")
    new_segment.penup()  # removes horizontal line
    new_segment.goto(position)
    segments.append(new_segment)
"""

snake = Snake()  # calling Snake class from snake module
food = Food()
scoreboard = Scoreboard()

# 3 control the snake
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.15)
    snake.move()  # 2 move the snake !

    #  """
    #  for seg_num in range(len(segments)-1, 0, -1):
    #         new_x = segments[seg_num-1].xcor()
    #         new_y = segments[seg_num-1].ycor()
    #         segments[seg_num].goto(new_x, new_y)
    #     segments[0].forward(20)
    # """

    # create a snake class and move to OOP

    # Detect collision with food.
    if snake.segments[0].distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # Detect collision with wall
    if snake.segments[0].xcor() > 445 or snake.segments[0].xcor() < -445 or snake.segments[0].ycor() > 275 or \
            snake.segments[0].ycor() < -275:
        game_is_on = False
        scoreboard.game_over()

    # Detect the collision with tail
    for segment in snake.segments:
        if segment == snake.segments[0]:
            pass
        elif snake.segments[0].distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

    # or (By Slicing)
    """for segment in snake.segments[1:]:
        if snake.segments[0].distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()"""
    # if head collides with any segments in the tail:
    # trigger game_over

# keep the window open

screen.exitonclick()
