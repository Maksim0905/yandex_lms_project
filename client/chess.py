import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMessageBox
)
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt, QPointF, pyqtSignal
from config import default_server
import api
import threading
import time

# Размер клетки
CELL_SIZE = 80
# TOKEN = api.create_game()

class ChessBoard(QWidget):
    game_over_signal = pyqtSignal(str, str)
    def __init__(self, token, player_1, player_2, turn, title_name):
        super().__init__()
        self.setWindowTitle(title_name)
        self.setFixedSize(CELL_SIZE * 8, CELL_SIZE * 8)
        # self.board = self.create_initial_board()
        self.selected_piece = None
        self.selected_pos = None
        self.current_player = 'w' if turn == player_1 else 'b'
        self.possible_moves = []  # Список возможных ходов
        self.token = token
        self.player_1 = player_1
        self.player_2 = player_2
        self.turn = turn
        self.game_over_signal.connect(self.handle_game_over)
        # self.setWindowTitle(title_name)

        # Отслеживание перемещения короля и ладей для рокировки
        self.kings_moved = {'w': False, 'b': False}
        self.rooks_moved = {
            'w': {'a': False, 'h': False},
            'b': {'a': False, 'h': False}
        }
        self.board = self.create_initial_board()
        self.gstatus = api.get_status(token)
        # print(self.gstatus)

    def create_initial_board(self):
        # Создаем начальную расстановку фигур
        board = api.get_board_by_token(self.token)
        # print(board, type(board))

        # board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP"] * 8,
        #     [""] * 8,
        #     [""] * 8,
        #     [""] * 8,
        #     [""] * 8,
        #     ["wP"] * 8,
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        # ]
        return board
    
    def update_board(self):
        """Функция для обновления доски каждые 2 секунды."""
        while True:
            # Получаем актуальную доску
            self.board = api.get_board_by_token(self.token)
            self.player_2 = api.get_player_2_by_token(self.token)
            self.turn = api.get_turn_by_token(self.token)
            self.current_player = 'w' if self.turn == self.player_1 else 'b'
            # print(self.current_player)
            
            opponent = 'b' if self.current_player == 'w' else 'w'
            self.update()
            if self.is_in_checkmate(opponent):
                self.update()
                self.game_over_signal.emit("Мат!", f"Игрок {'Белые' if opponent == 'w' else 'Чёрные'} выиграл!")
                break
            self.update()
            # print(self.board)
            time.sleep(1)  # Задержка 2 секунды перед следующим обновлением

    def handle_game_over(self, title, message):
        """Обработчик для завершения игры, обновление UI."""
        QMessageBox.information(self, title, message)
        self.close()  # Закрытие окна ChessBoard
        self.parent().resize(1036, 797)
        self.parent().show()
        self.parent().setWindowTitle("Игровые Комнаты")

    def start_background_update(self):
        """Метод для старта фонового обновления доски."""
        # Запуск фонового обновления доски в отдельном потоке
        threading.Thread(target=self.update_board, daemon=True).start()

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(8):
            for col in range(8):
                # Рисуем клетки
                color = QColor(240, 217, 181) if (row + col) % 2 == 0 else QColor(181, 136, 99)
                painter.fillRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE, color)
                
                # Если клетка - возможный ход, выделяем её
                if (row, col) in self.possible_moves:
                    painter.setBrush(QColor(0, 255, 0, 100))  # Полупрозрачный зелёный
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Если клетка выделена, рисуем обводку
                if self.selected_pos == (row, col):
                    pen = QPen(QColor(255, 0, 0), 3)
                    painter.setPen(pen)
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.drawRect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                else:
                    painter.setPen(Qt.PenStyle.NoPen)

                # Рисуем фигуры

                # print(type(self.board))
                # print(self.board)

                piece = self.board[row][col]
                if piece:
                    self.draw_piece(painter, piece, col, row)
        
        # Проверяем наличие шаха
        if self.is_in_check(self.current_player):
            king_pos = self.find_king(self.current_player)
            if king_pos:
                # Используем QPointF и float радиусы
                center_x = king_pos[1] * CELL_SIZE + CELL_SIZE * 0.5
                center_y = king_pos[0] * CELL_SIZE + CELL_SIZE * 0.5
                rx = CELL_SIZE * 0.4
                ry = CELL_SIZE * 0.4
                painter.setBrush(QColor(255, 0, 0, 100))  # Полупрозрачный красный
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPointF(center_x, center_y), rx, ry)
                opponent = 'b' if self.current_player == 'w' else 'w'
                if self.is_in_checkmate(opponent):
                    QMessageBox.information(self, "Мат!", f"Игрок {'Белые' if opponent == 'w' else 'Чёрные'} выиграл!")
                    # self.reset_board()
                    self.close()  # Закрытие окна ChessBoard
                    self.parent().resize(1036, 797)
                    self.parent().show()
                    self.parent().setWindowTitle("Игровые Комнаты")
                    
                elif self.is_in_check(opponent):
                    QMessageBox.information(self, "Шах!", f"Игрок {'Чёрные' if opponent == 'w' else 'Белые'} находится в шахе!")

    def draw_piece(self, painter, piece, col, row):
        # В этом примере будем рисовать символы вместо изображений
        piece_symbols = {
            "wP": "♙",  # Белая пешка (White Pawn)
            "wR": "♖",  # Белая ладья (White Rook)
            "wN": "♘",  # Белый конь (White Knight)
            "wB": "♗",  # Белый слон (White Bishop)
            "wQ": "♕",  # Белая ферзь (White Queen)
            "wK": "♔",  # Белый король (White King)
            "bP": "♟︎",  # Чёрная пешка (Black Pawn)
            "bR": "♜",  # Чёрная ладья (Black Rook)
            "bN": "♞",  # Чёрный конь (Black Knight)
            "bB": "♝",  # Чёрный слон (Black Bishop)
            "bQ": "♛",  # Чёрная ферзь (Black Queen)
            "bK": "♚",  # Чёрный король (Black King)
        }

        piece_symbols = {
            "wP": "♟︎",  # Белая пешка (White Pawn)
            "wR": "♜",  # Белая ладья (White Rook)
            "wN": "♞",  # Белый конь (White Knight)
            "wB": "♝",  # Белый слон (White Bishop)
            "wQ": "♛",  # Белая ферзь (White Queen)
            "wK": "♚",  # Белый король (White King)
            "bP": "♟︎",  # Чёрная пешка (Black Pawn)
            "bR": "♜",  # Чёрная ладья (Black Rook)
            "bN": "♞",  # Чёрный конь (Black Knight)
            "bB": "♝",  # Чёрный слон (Black Bishop)
            "bQ": "♛",  # Чёрная ферзь (Black Queen)
            "bK": "♚",  # Чёрный король (Black King)
        }

        symbol = piece_symbols.get(piece, "")
        if symbol:
            font = QFont("Arial", 36)
            painter.setFont(font)
            if piece.startswith("b"):
                painter.setPen(QColor(0, 0, 0))  # Чёрный цвет для белых фигур
            else:
                painter.setPen(QColor(255, 255, 255))  # Белый цвет для чёрных фигур
            
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(symbol)
            text_height = fm.ascent()

            x = int(col * CELL_SIZE + (CELL_SIZE - text_width) / 2)
            y = int(row * CELL_SIZE + (CELL_SIZE + text_height) / 2)

            painter.drawText(x, y, symbol)

    def mousePressEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)

        if self.selected_piece:
            # Если клик на возможном ходу, делаем ход
            if (row, col) in self.possible_moves:
                if self.is_valid_move(self.selected_pos, (row, col)):
                    self.move_piece(self.selected_pos, (row, col))
                    api.edit_board_by_token(self.token, self.board)
                    # Обновляем флаги перемещения для рокировки
                    self.update_moved_flags(self.selected_pos, (row, col))
                    
                    self.selected_piece = None
                    self.selected_pos = None
                    self.possible_moves = []
                    
                    # Проверяем на мат или шах противника
                    opponent = 'b' if self.current_player == 'w' else 'w'
                    if self.is_in_checkmate(opponent):
                        QMessageBox.information(self, "Мат!", f"Игрок {'Белые' if opponent == 'w' else 'Чёрные'} выиграл!")
                        # self.reset_board()
                        self.close()  # Закрытие окна ChessBoard
                        self.parent().resize(1036, 797)
                        self.parent().show()
                        self.parent().setWindowTitle("Игровые Комнаты")
                        
                    elif self.is_in_check(opponent):
                        QMessageBox.information(self, "Шах!", f"Игрок {'Чёрные' if opponent == 'w' else 'Белые'} находится в шахе!")
                    
                    self.switch_player()
                    api.edit_board_by_token(self.token, self.board)
                    self.board = api.get_board_by_token(self.token)
                    self.update()
                else:
                    # Неверный ход, отменяем выбор
                    self.selected_piece = None
                    self.selected_pos = None
                    self.possible_moves = []
                    self.update()
            else:
                # Клик не на возможном ходу
                piece = self.board[row][col]
                if piece and piece.startswith(self.current_player):
                    self.selected_piece = piece
                    self.selected_pos = (row, col)
                    self.possible_moves = self.get_possible_moves((row, col))
                    self.update()
                else:
                    # Отмена выбора
                    self.selected_piece = None
                    self.selected_pos = None
                    self.possible_moves = []
                    self.update()
        else:
            # Нет выбранной фигуры, пытаемся выбрать
            piece = self.board[row][col]
            if piece and piece.startswith(self.current_player):
                self.selected_piece = piece
                self.selected_pos = (row, col)
                self.possible_moves = self.get_possible_moves((row, col))
                self.update()

    def get_possible_moves(self, pos):
        from_pos = pos
        possible = []
        for row in range(8):
            for col in range(8):
                to_pos = (row, col)
                if self.is_valid_move(from_pos, to_pos):
                    possible.append(to_pos)
        return possible

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]

        # Проверяем, что не пытаемся сходить на ту же клетку
        if from_pos == to_pos:
            return False

        # Проверяем, что целевая клетка либо пустая, либо содержит фигуру противника
        if target and target[0] == piece[0]:
            return False

        # Определяем тип фигуры
        piece_type = piece[1]

        # Логика для каждой фигуры
        if piece_type == 'P':  # Пешка
            valid = self.is_valid_pawn_move(piece, from_pos, to_pos)
        elif piece_type == 'R':  # Ладья
            valid = self.is_valid_rook_move(from_pos, to_pos)
        elif piece_type == 'N':  # Конь
            valid = self.is_valid_knight_move(from_pos, to_pos)
        elif piece_type == 'B':  # Слон
            valid = self.is_valid_bishop_move(from_pos, to_pos)
        elif piece_type == 'Q':  # Ферзь
            valid = self.is_valid_queen_move(from_pos, to_pos)
        elif piece_type == 'K':  # Король
            valid = self.is_valid_king_move(from_pos, to_pos)
        else:
            valid = False

        if not valid:
            return False

        # Симулируем ход и проверяем, не окажется ли король под шахом
        original_target = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""
        in_check = self.is_in_check(self.current_player)
        # Отменяем симулированный ход
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = original_target

        if in_check:
            return False

        return True

    def is_valid_pawn_move(self, piece, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if piece.startswith('w') else 1
        start_row = 6 if piece.startswith('w') else 1
        target = self.board[to_row][to_col]

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # Одноклеточное движение вперёд
        if col_diff == 0 and row_diff == direction and not target:
            return True

        # Двуклеточное движение вперёд
        if col_diff == 0 and row_diff == 2 * direction and from_row == start_row:
            intermediate_square = self.board[from_row + direction][from_col]
            if not intermediate_square and not target:
                return True

        # Взятие наискосок
        if abs(col_diff) == 1 and row_diff == direction and target and target[0] != piece[0]:
            return True

        # Взятие на проходе и превращение не реализованы
        return False

    def is_valid_rook_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Ладья движется только по вертикали или горизонтали
        if from_row != to_row and from_col != to_col:
            return False

        # Проверяем, что путь свободен
        if not self.is_path_clear(from_pos, to_pos):
            return False

        return True

    def is_valid_knight_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Конь движется буквой "Г": 2+1
        if (row_diff, col_diff) in [(2, 1), (1, 2)]:
            return True

        return False

    def is_valid_bishop_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Слон движется только по диагонали
        if row_diff != col_diff:
            return False

        # Проверяем, что путь свободен
        if not self.is_path_clear(from_pos, to_pos):
            return False

        return True

    def is_valid_queen_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Ферзь движется по вертикали, горизонтали или диагонали
        if row_diff != col_diff and from_row != to_row and from_col != to_col:
            return False

        # Проверяем, что путь свободен
        if not self.is_path_clear(from_pos, to_pos):
            return False

        return True

    def is_valid_king_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Король движется на одну клетку в любом направлении
        if max(row_diff, col_diff) == 1:
            return True

        # Рокировка
        if row_diff == 0 and col_diff == 2:
            return self.is_valid_castling(from_pos, to_pos)

        return False

    def is_valid_castling(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        player = 'w' if self.current_player == 'w' else 'b'

        # Проверяем, что король не сделал ход
        if self.kings_moved[player]:
            return False

        # Определяем направление рокировки
        if to_col == 6:  # Малый рокировка (король перемещается на правую сторону)
            rook_col = 7
            new_rook_col = 5
            rook_side = 'h'
        elif to_col == 2:  # Большая рокировка (король перемещается на левую сторону)
            rook_col = 0
            new_rook_col = 3
            rook_side = 'a'
        else:
            return False  # Неверный столбец для рокировки

        # Проверяем, что соответствующая ладья не сделала ход
        if self.rooks_moved[player].get(rook_side, True):
            return False

        # Проверяем, что путь между королём и ладьёй свободен
        step = 1 if rook_col > from_col else -1
        for col in range(from_col + step, rook_col, step):
            if self.board[from_row][col] != "":
                return False

        # Проверяем, что клетки, через которые проходит король, не находятся под атакой
        king_path = [ (from_row, from_col + step), (from_row, from_col + 2*step) ]
        for pos in king_path:
            if self.is_square_attacked(pos, 'b' if self.current_player == 'w' else 'w'):
                return False

        # Проверяем, что целевая клетка не находится под атакой
        if self.is_square_attacked(to_pos, 'b' if self.current_player == 'w' else 'w'):
            return False

        # Проверяем, что король не находится под шахом
        if self.is_in_check(self.current_player):
            return False

        return True

    def is_path_clear(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        row_diff = to_row - from_row
        col_diff = to_col - from_col

        step_row = 0
        step_col = 0

        if row_diff != 0:
            step_row = row_diff // abs(row_diff)
        if col_diff != 0:
            step_col = col_diff // abs(col_diff)

        current_row = from_row + step_row
        current_col = from_col + step_col

        while (current_row, current_col) != to_pos:
            if self.board[current_row][current_col] != "":
                return False
            current_row += step_row
            current_col += step_col

        return True

    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        
        # Обработка рокировки
        if piece[1] == 'K' and abs(to_col - from_col) == 2:
            self.perform_castling(from_pos, to_pos)

        # Перемещаем фигуру
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""

        # Обработка превращения пешки (не реализовано)
        # Обработка взятия на проходе (не реализовано)

    def perform_castling(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        player = 'w' if self.current_player == 'w' else 'b'

        if to_col == 6:  # Малый рокировка
            rook_from = (from_row, 7)
            rook_to = (from_row, 5)
        elif to_col == 2:  # Большая рокировка
            rook_from = (from_row, 0)
            rook_to = (from_row, 3)
        else:
            return  # Неверный столбец для рокировки

        rook_piece = self.board[rook_from[0]][rook_from[1]]
        self.board[rook_to[0]][rook_to[1]] = rook_piece
        self.board[rook_from[0]][rook_from[1]] = ""

        # Обновляем флаги перемещения
        self.rooks_moved[player][ 'h' if to_col == 6 else 'a' ] = True

    def switch_player(self):


        self.turn = api.get_turn_by_token(self.token)
        if self.turn == self.player_1:
            self.current_player = 'b' if self.current_player == 'w' else 'w'
            api.edit_turn_by_token(self.token, self.player_2)
            self.update()
            # print(self.turn, self.current_player, 'player_1:', self.player_1, 'player_2:', self.player_2)
        elif self.turn == self.player_2:
            self.current_player = 'b' if self.current_player == 'w' else 'w'
            api.edit_turn_by_token(self.token, self.player_1)
            self.update()
            # print(self.turn, self.current_player, 'player_1:', self.player_1, 'player_2:', self.player_2)

        # self.current_player = 'b' if self.current_player == 'w' else 'w'

    def find_king(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == f"{player}K":
                    return (row, col)
        return None

    def is_square_attacked(self, pos, by_player):
        attacker = by_player
        target_row, target_col = pos

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith(attacker):
                    from_pos = (row, col)
                    to_pos = pos
                    if self.is_valid_move_attacking(from_pos, to_pos):
                        return True
        return False

    def is_valid_move_attacking(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]

        if piece == "":
            return False

        # Определяем тип фигуры
        piece_type = piece[1]

        # Логика для каждой фигуры (без проверки шаха)
        if piece_type == 'P':  # Пешка
            return self.is_valid_pawn_attack(piece, from_pos, to_pos)
        elif piece_type == 'R':  # Ладья
            return self.is_valid_rook_move(from_pos, to_pos)
        elif piece_type == 'N':  # Конь
            return self.is_valid_knight_move(from_pos, to_pos)
        elif piece_type == 'B':  # Слон
            return self.is_valid_bishop_move(from_pos, to_pos)
        elif piece_type == 'Q':  # Ферзь
            return self.is_valid_queen_move(from_pos, to_pos)
        elif piece_type == 'K':  # Король
            return self.is_valid_king_move_attacking(from_pos, to_pos)
        
        return False

    def is_valid_pawn_attack(self, piece, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if piece.startswith('w') else 1

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # Пешка может атаковать только наискосок
        if abs(col_diff) == 1 and row_diff == direction:
            return True

        return False

    def is_valid_king_move_attacking(self, from_pos, to_pos):
        # Король атакует как обычный ход
        return self.is_valid_king_move(from_pos, to_pos)

    def is_in_check(self, player):
        king_pos = self.find_king(player)
        if king_pos:
            opponent = 'b' if player == 'w' else 'w'
            return self.is_square_attacked(king_pos, opponent)
        return False

    def is_in_checkmate(self, player):
        if not self.is_in_check(player):
            return False

        # Проверяем, есть ли хоть один легальный ход, который спасёт короля от шаха
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith(player):
                    from_pos = (row, col)
                    possible_moves = self.get_possible_moves(from_pos)
                    for to_pos in possible_moves:
                        # Симулируем ход
                        piece_moved = self.board[to_pos[0]][to_pos[1]]
                        self.board[to_pos[0]][to_pos[1]] = piece
                        self.board[from_pos[0]][from_pos[1]] = ""
                        in_check = self.is_in_check(player)
                        # Отменяем ход
                        self.board[from_pos[0]][from_pos[1]] = piece
                        self.board[to_pos[0]][to_pos[1]] = piece_moved

                        if not in_check:
                            return False
        return True

    def reset_board(self):
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.selected_pos = None
        self.current_player = 'w'
        self.possible_moves = []
        self.kings_moved = {'w': False, 'b': False}
        self.rooks_moved = {
            'w': {'a': False, 'h': False},
            'b': {'a': False, 'h': False}
        }
        self.update()

    def update_moved_flags(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[to_row][to_col]

        # Если перемещается король
        if piece == 'wK' or piece == 'bK':
            player = 'w' if piece.startswith('w') else 'b'
            self.kings_moved[player] = True

        # Если перемещается ладья
        if piece == 'wR' or piece == 'bR':
            player = 'w' if piece.startswith('w') else 'b'
            if from_col == 0:
                self.rooks_moved[player]['a'] = True
            elif from_col == 7:
                self.rooks_moved[player]['h'] = True

        # Если взята ладья, обновляем флаги
        target_piece = self.board[to_row][to_col]
        if target_piece.startswith('wR'):
            player = 'w'
            if to_col == 0:
                self.rooks_moved[player]['a'] = True
            elif to_col == 7:
                self.rooks_moved[player]['h'] = True
        elif target_piece.startswith('bR'):
            player = 'b'
            if to_col == 0:
                self.rooks_moved[player]['a'] = True
            elif to_col == 7:
                self.rooks_moved[player]['h'] = True

    def perform_castling(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        player = 'w' if self.current_player == 'w' else 'b'

        if to_col == 6:  # Малый рокировка
            rook_from = (from_row, 7)
            rook_to = (from_row, 5)
        elif to_col == 2:  # Большая рокировка
            rook_from = (from_row, 0)
            rook_to = (from_row, 3)
        else:
            return  # Неверный столбец для рокировки

        rook_piece = self.board[rook_from[0]][rook_from[1]]
        self.board[rook_to[0]][rook_to[1]] = rook_piece
        self.board[rook_from[0]][rook_from[1]] = ""

        # Обновляем флаги перемещения
        self.rooks_moved[player][ 'h' if to_col == 6 else 'a' ] = True

    def get_possible_moves(self, pos):
        from_pos = pos
        possible = []
        for row in range(8):
            for col in range(8):
                to_pos = (row, col)
                if self.is_valid_move(from_pos, to_pos):
                    possible.append(to_pos)
        return possible

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шахматы на PyQt6")
        self.setFixedSize(CELL_SIZE * 8, CELL_SIZE * 8)
        self.chessboard = ChessBoard()
        self.setCentralWidget(self.chessboard)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
