Advanced 4x4 Tic-Tac-Toe with AI
An enhanced version of Tic-Tac-Toe built with Python and Pygame featuring a 4x4 grid, strategic power moves ("Swap" and "Block"), and a smart AI opponent using the Minimax algorithm with Alpha-Beta Pruning.

🧠 Project Overview
This project introduces a 4x4 variant of the classic Tic-Tac-Toe game with added strategic complexity through power moves. The AI opponent is designed to make optimal decisions using advanced search algorithms and heuristic evaluation.

🎮 Game Features
4x4 Grid: Requires four aligned marks to win.

Power Moves:

Swap (2 per game): Swap any two marks on the board.

Block (1 per game): Temporarily block a cell for one turn.

Game Modes: Play against the AI or another human.

Interactive GUI: Built using Pygame for smooth user experience.

🧩 Game Rules
Players alternate turns placing X or O.

Power moves are optional and can be used strategically:

Swap and Block moves have limited usage.

Swaps cannot be used immediately after an opponent's move.

A player wins by aligning four marks in a row, column, or diagonal.

Game ends with a win or a draw when the board is full.

🧠 AI Implementation
Minimax Algorithm: Explores all possible moves to find the best one.

Alpha-Beta Pruning: Cuts off unneeded branches to improve efficiency.

Heuristic Evaluation:

+1000 for a win, -1000 for a loss.

+50 for three aligned marks.

+10 for two marks with potential to extend.

Extra weighting for power move effects.

Depth-Limited Search: Ensures fast decision-making (adjustable difficulty).

💻 Tech Stack
Python 3.x

Pygame – For GUI and user interaction.

NumPy – For efficient board state management.

📁 Code Structure
GameBoard: Manages grid, power moves, and win logic.

AI: Implements Minimax, Alpha-Beta, and heuristic scoring.

GUI: Renders the board, handles user input.

🧪 Results
AI responds within 1–3 seconds.

Effectively uses power moves and adapts strategies.

User-friendly gameplay with clean visual feedback.

🚧 Challenges
Handling expanded state space from 4x4 grid and power moves.

Designing nuanced heuristics for varied game states.

Balancing computation time with intelligent play.

🚀 Future Enhancements
Machine Learning AI using reinforcement learning.

Online Multiplayer Support.

Advanced Heuristics and difficulty levels.

Mobile App Version for Android/iOS.
