# 🐍 SnaPy - Classic Snake Game

A fun, Python-based implementation of the classic arcade Snake game. Built using Python's built-in `turtle` graphics library, this project demonstrates core Object-Oriented Programming (OOP) concepts, real-time game loops, and event-driven keyboard bindings.

---

## ✨ Features

* **Classic Gameplay:** Navigate the snake to eat the blue food and grow your tail.
* **Collision Detection:** The game automatically ends if the snake collides with the screen boundaries or its own tail.
* **Live Scoreboard:** Tracks and updates your score in real-time as you eat food.
* **Modular Architecture:** Clean code structure divided into separate class files for easy maintenance and scalability.

---

## 🗂 Project Structure

The project logic is split into four main files to adhere to OOP best practices:

* `index.py`: The main game loop that initializes the screen, objects, and handles collision logic.
* `snake.py`: Contains the `Snake` class. Manages the snake's segments, movement logic, and direction changes.
* `food.py`: Contains the `Food` class. Handles the random generation and placement of food items on the screen.
* `scoreboard.py`: Contains the `Scoreboard` class. Manages score tracking and the "Game Over" display.

---

## 🚀 How to Run

### Prerequisites
This game uses the `turtle` module, which comes pre-installed with standard Python. You do not need to install any external libraries from the `requirements.txt` to run this specific game.

1. Ensure you have **Python 3.x** installed on your machine.
2. Clone this repository to your local machine.
3. Open your terminal or command prompt and navigate to the project directory:
   ```bash
   cd path/to/03-Snake-Game