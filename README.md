This is a simple python game of Tic-Tac-Toe with OOP principles and added with a minimax algorithm for the computer to be unbeatable
V1: 
-Used pygame to draw and construct the screen and the board and to handle keypresses and clicks
-Used numpy to construct multidimensional arryays that can store the positions of X's and O's 
-Main game logic relies on creating functions that check if a square is available, if the board is full and the winner function 
-The recurisve minimax algorithm is simple. The best result for the computer is 1 and the worst is -1, with 0 being a tie. The minimax function utilizes DFS to visualize 1 move, and then increases the depth to keep going and find the most favourable outcome. It also takes into account what the player itself is doing by setting the is_max parameter to False

V1.1: 
-Added a home screen, and the ability to play against a player or the minimax AI
-better visuals 

