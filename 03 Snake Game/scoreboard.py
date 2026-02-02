from turtle import Turtle


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color("white")
        self.penup()
        self.goto(0, 244)
        self.write(f"score: {self.score}  High Score: {self.high_score}", align="center", font=("Arial", 22, "normal"))
        self.hideturtle()

    def update_scoreboard(self):
        self.clear()
        self.write(f"score: {self.score}  High Score: {self.high_score}", align="center", font=("Arial", 22, "normal"))

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    def check_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def game_over(self):
        self.goto(0, 0)
        self.write("Game Over", align="center", font=("Arial", 28, "normal"))
