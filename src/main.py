import sys
import numpy as np
import pygame

pygame.init()

class TicTacToe:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.rows = 3
        self.cols = 3
        self.cell_size = self.width // self.cols

        self.line_width = 10
        self.circle_width = 15
        self.cross_width = 25
        self.circle_radius = self.cell_size // 3

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe AI")

        self.board = np.zeros((self.rows, self.cols))
        self.player = 1
        self.game_over = False
        self.win_line = None

        self.screen.fill(self.BLACK)
        self.draw_lines()

    # Drawing the board
    def draw_lines(self, color=None):
        color = color or self.WHITE
        for i in range(1, self.rows):
            pygame.draw.line(self.screen, color,
                             (0, i*self.cell_size),
                             (self.width, i*self.cell_size),
                             self.line_width)
            pygame.draw.line(self.screen, color,
                             (i*self.cell_size, 0),
                             (i*self.cell_size, self.height),
                             self.line_width)

    def draw_figures(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 1:
                    pygame.draw.circle(
                        self.screen, self.WHITE,
                        (col*self.cell_size + self.cell_size//2,
                         row*self.cell_size + self.cell_size//2),
                        self.circle_radius, self.circle_width
                    )
                elif self.board[row][col] == 2:
                    pygame.draw.line(
                        self.screen, self.WHITE,
                        (col*self.cell_size + self.cell_size//4,
                         row*self.cell_size + self.cell_size//4),
                        (col*self.cell_size + 3*self.cell_size//4,
                         row*self.cell_size + 3*self.cell_size//4),
                        self.cross_width
                    )
                    pygame.draw.line(
                        self.screen, self.WHITE,
                        (col*self.cell_size + self.cell_size//4,
                         row*self.cell_size + 3*self.cell_size//4),
                        (col*self.cell_size + 3*self.cell_size//4,
                         row*self.cell_size + self.cell_size//4),
                        self.cross_width
                    )

    def draw_win_line(self):
        if not self.win_line:
            return

        color = self.GREEN if self.player == 2 else self.RED

        if self.win_line[0] == "row":
            y = self.win_line[1]*self.cell_size + self.cell_size//2
            pygame.draw.line(self.screen, color, (20, y), (self.width-20, y), 15)

        elif self.win_line[0] == "col":
            x = self.win_line[1]*self.cell_size + self.cell_size//2
            pygame.draw.line(self.screen, color, (x, 20), (x, self.height-20), 15)

        elif self.win_line[1] == "main":
            pygame.draw.line(self.screen, color, (20, 20), (self.width-20, self.height-20), 15)

        elif self.win_line[1] == "anti":
            pygame.draw.line(self.screen, color, (20, self.height-20), (self.width-20, 20), 15)

    # Game logic
    def available(self, row, col):
        return self.board[row][col] == 0

    def board_full(self):
        return not np.any(self.board == 0)

    def check_winner(self, player, board=None):
        b = board if board is not None else self.board

        for i in range(3):
            if np.all(b[i, :] == player):
                return ("row", i)
            if np.all(b[:, i] == player):
                return ("col", i)

        if np.all(np.diag(b) == player):
            return ("diag", "main")
        if np.all(np.diag(np.fliplr(b)) == player):
            return ("diag", "anti")

        return None

    # MINIMAX ALGORITHM
    def minimax(self, board, is_max):
        if self.check_winner(2, board):
            return 1
        if self.check_winner(1, board):
            return -1
        if not np.any(board == 0):
            return 0

        if is_max:
            best = -100
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 2
                        best = max(best, self.minimax(board, False))
                        board[r][c] = 0
            return best
        else:
            best = 100
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = 1
                        best = min(best, self.minimax(board, True))
                        board[r][c] = 0
            return best

    def best_move(self):
        best_score = -100
        move = None

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    self.board[r][c] = 2
                    score = self.minimax(self.board, False)
                    self.board[r][c] = 0
                    if score > best_score:
                        best_score = score
                        move = (r, c)

        if move:
            self.board[move] = 2
            return True
        return False

    # MAIN LOOP
    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.__init__()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mx, my = event.pos
                    row, col = my//self.cell_size, mx//self.cell_size

                    if self.available(row, col):
                        self.board[row][col] = 1
                        win = self.check_winner(1)
                        if win:
                            self.win_line = win
                            self.game_over = True

                        if not self.game_over:
                            self.best_move()
                            win = self.check_winner(2)
                            if win:
                                self.win_line = win
                                self.game_over = True

            self.screen.fill(self.BLACK)
            self.draw_lines()
            self.draw_figures()
            self.draw_win_line()
            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    TicTacToe().run()
